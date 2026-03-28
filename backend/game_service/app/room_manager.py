import logging
import asyncio
import time
from fastapi import WebSocket
from typing import Dict, List, Optional
from app.services.redis_client import RedisClient
from contextlib import suppress

logger = logging.getLogger(__name__)

QUESTION_DURATION = 15
LEADERBOARD_DURATION = 8
QUIZ_LOCK_TTL = 60
ANSWER_REVEAL_DURATION = 4
SLEEP_DURATION = 0.3

class RoomManager:
    """
    Manages:
    - WebScocket connections per room
    - Quiz lifecycle
    - Redis pub/sub
    """

    def __init__(self, redis_client: RedisClient):
        self._redis = redis_client
        self._room_connections: Dict[str, List[WebSocket]] = {}
        self._quiz_tasks: Dict[str, asyncio.Task] = {}
        self._ws_to_player: Dict[WebSocket, str] = {}

        self._lock = asyncio.Lock()
        self._subscribe_task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        """Start background subscriptions."""
        if self._running:
            return
        
        self._running = True
        self._subscribe_task = asyncio.create_task(
            self._redis.subscribe_rooms(self._broadcast_local)
        )
        logger.info("RoomManager started")

    async def stop(self) -> None:
        """Stop all tasks"""
        self._running = False

        if self._subscribe_task:
            self._subscribe_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._subscribe_task
        
        async with self._lock:
            for task in self._quiz_tasks.values():
                task.cancel()

            for task in self._quiz_tasks.values():
                with suppress(asyncio.CancelledError):
                    await task

            self._quiz_tasks.clear()

        logger.info("RoomManager stopped")

    async def connect(self, room_id: str, websocket: WebSocket) -> None:
        await websocket.accept()

        async with self._lock:
            self._room_connections.setdefault(room_id, []).append(websocket)

        logger.debug("WebSocket connected", extra={"room_id": room_id})

    async def disconnect(self, room_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            connections = self._room_connections.get(room_id)
            if not connections:
                return
            
            if websocket in connections:
                connections.remove(websocket)

            player_id = self._ws_to_player.pop(websocket, None)

            if not connections:
                self._room_connections.pop(room_id, None)
                await self._cleanup_room(room_id)

            if player_id:
                await self._redis.remove_player(room_id, player_id)

                players = await self._redis.get_players(room_id)

                await self._redis.publish_room_message(
                    room_id, {
                        "type": "player_left",
                        "players": [p["name"] for p in players]
                    }
                )

        logger.debug("WebSocket disconnected", extra={"room_id": room_id})

    async def _cleanup_room(self, room_id: str) -> None:
        """Cleanup room resources when empty"""
        task = self._quiz_tasks.pop(room_id, None)
        if task:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

        logger.info("Room cleaned up", extra={"room_id": room_id})

    async def _broadcast_local(self, room_id: str, message: dict) -> None:
        async with self._lock:
            connections = list(self._room_connections.get(room_id, []))

        if not connections:
            return
        
        dead: List[WebSocket] = []

        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        
        for ws in dead:
            await self.disconnect(room_id, ws)

    async def start_quiz(self, room_id: str):

        lock_key = f"quiz_lock:{room_id}"
        acquired = await self._redis.acquire_lock(lock_key, QUIZ_LOCK_TTL)
        if not acquired:
            logger.warning("Quiz already running in another instance", extra={"room_id": room_id})

        async with self._lock:
            if room_id in self._quiz_tasks:
                await self._redis.release_lock(lock_key)
                logger.warning("Quiz already running", extra={"room_id": room_id})
                return
            
            task = asyncio.create_task(self._run_quiz(room_id, lock_key))
            self._quiz_tasks[room_id] = task

    async def _run_quiz(self, room_id: str, lock_key: str) -> None:
        logger.info("Quiz started", extra={"room_id": room_id})

        try:
            room_meta = await self._redis.get_room_meta(room_id)
            if not room_meta:
                logger.warning("Room not found", extra={"room_id": room_id})
                return
            
            questions = await self._redis.get_all_questions(room_id)
            if not questions:
                logger.warning("No questions found", extra={"room_id": room_id})
                return
            
            await self._redis.save_room_meta(
                room_id,
                owner_id=room_meta["owner_id"],
                quiz_id=room_meta["quiz_id"],
                started=True,
                current_question_index=0
            )

            for idx, question in enumerate(questions):

                is_last = idx == len(questions) - 1

                await self._redis.save_room_meta(
                    room_id,
                    owner_id=room_meta["owner_id"],
                    quiz_id=room_meta["quiz_id"],
                    started=True,
                    current_question_index=idx
                )

                await self._publish_question(room_id, question, idx)

                await self._wait_for_answers_or_timeout(room_id, idx)

                await self._process_answers(room_id, question, idx)

                await asyncio.sleep(ANSWER_REVEAL_DURATION)

                await self._publish_leaderboard(room_id, final=is_last)

                if not is_last:
                    await asyncio.sleep(LEADERBOARD_DURATION)
        except asyncio.CancelledError:
            logger.info("Quiz cancelled", extra={"room_id": room_id})
            raise
        except Exception:
            logger.exception("Quiz crashed", extra={"room_id": room_id})
        finally:
            await self._reset_room_state(room_id)
            async with self._lock:
                self._quiz_tasks.pop(room_id, None)
            await self._redis.release_lock(lock_key)

    async def _publish_question(self, room_id, question, idx):
        await self._redis.publish_room_message(
            room_id,
            {"type": "question", "question": question, "index": idx}
        )

        await self._redis.set_question_start(room_id, QUESTION_DURATION + 5)

    async def _process_answers(self, room_id, question, idx):
        answers = await self._redis.get_answers(room_id, idx)

        start_time = await self._redis.get_question_start(room_id)
        if start_time is None:
            start_time = time.time()

        await self._redis.publish_room_message(
            room_id,
            {"type": "answer_result", "correct_answer": question["correct_option"]}
        )

        for player_id, data in answers.items():
            answer = data["answer"]
            ts = data["ts"]

            if answer == question["correct_option"]:
                response_time = ts - start_time
                time_ratio = min(response_time / QUESTION_DURATION, 1)

                max_points = 1000
                min_points = 200

                points = int(max_points * (1 - time_ratio))
                points = max(points, min_points)

                await self._redis.increment_score(room_id, player_id, points)

        await self._redis.delete_answers(room_id, idx)

    async def _publish_leaderboard(self, room_id, final=False):
        players = await self._redis.get_players(room_id)

        players_sorted = sorted(players, key=lambda p: p["score"], reverse=True)

        leaderboard = [
            {"name": p["name"], "score": p["score"]} 
            for p in players_sorted[:5]
        ]

        await self._redis.publish_room_message(
            room_id,
            {
                "type": "leaderboard",
                "final": final,
                "leaderboard": leaderboard,
                "show_for": LEADERBOARD_DURATION,
            },
        )

        return leaderboard
    
    async def _reset_room_state(self, room_id):
        room_meta = await self._redis.get_room_meta(room_id)
        if not room_meta:
            return

        await self._redis.save_room_meta(
            room_id,
            owner_id=room_meta["owner_id"],
            quiz_id=room_meta["quiz_id"],
            started=False,
            current_question_index=0,
        )

    async def _wait_for_answers_or_timeout(self, room_id, idx):
        start = time.time()

        while True:
            elapsed = time.time() - start

            if elapsed >= QUESTION_DURATION:
                return

            answers_count = await self._redis.count_answers(room_id, idx)
            players = await self._redis.get_players(room_id)

            if players and answers_count >= len(players):
                logger.info("All players answered early", extra={"room_id": room_id})
                return

            await asyncio.sleep(SLEEP_DURATION)

    async def register_player_ws(self, websocket: WebSocket, player_id: str):
        self._ws_to_player[websocket] = player_id