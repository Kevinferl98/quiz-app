from fastapi import WebSocket
import asyncio
from typing import Dict, List
from app.services.redis_client import RedisClient
import logging

logger = logging.getLogger(__name__)

QUESTION_DURATION = 15
LEADERBOARD_DURATION = 3

redis_client = RedisClient()

class RoomManager:
    def __init__(self):
        self.room_connections: Dict[str, List[WebSocket]] = {}
        self.lock = asyncio.Lock()
        self.quiz_tasks: Dict[str, asyncio.Task] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.room_connections.setdefault(room_id, []).append(websocket)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        async with self.lock:
            if room_id in self.room_connections:
                if websocket in self.room_connections[room_id]:
                    self.room_connections[room_id].remove(websocket)

                if not self.room_connections[room_id]:
                    self.room_connections.pop(room_id, None)

                    task = self.quiz_tasks.pop(room_id, None)
                    if task:
                        task.cancel()

                    logger.info(f"Room {room_id} cleaned up")

    async def broadcast(self, room_id: str, message: dict):
        connections = self.room_connections.get(room_id, [])
        dead_connections = []

        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:
                logger.warning("Removing dead websocket")
                dead_connections.append(ws)

        for ws in dead_connections:
            await self.disconnect(room_id, ws)

    async def start_quiz(self, room_id: str):
        if room_id in self.quiz_tasks:
            return

        task = asyncio.create_task(self._run_quiz(room_id))
        self.quiz_tasks[room_id] = task

    async def _run_quiz(self, room_id: str):
        room_meta = await redis_client.get_room_meta(room_id)
        if not room_meta:
            logger.warning(f"Room {room_id} not found")
            return
        
        await redis_client.save_room_meta(
            room_id,
            owner_id=room_meta["owner_id"],
            quiz_id=room_meta["quiz_id"],
            started=True,
            current_question_index=0
        )

        leaderboard = []

        questions = await redis_client.get_all_questions(room_id)
        if not questions:
            logger.warning(f"No questions for room {room_id}")
            return

        try:
            for idx, question in enumerate(questions):
                await redis_client.save_room_meta(
                    room_id,
                    owner_id=room_meta["owner_id"],
                    quiz_id=room_meta["quiz_id"],
                    started=True,
                    current_question_index=idx
                )

                await self.broadcast(room_id, {
                    "type": "question",
                    "question": question.model_dump(),
                    "index": idx
                })

                for t in range(QUESTION_DURATION, 0, -1):
                    await self.broadcast(room_id, {
                        "type": "timer",
                        "seconds": t
                    })
                    await asyncio.sleep(1)

                answers = await redis_client.get_answers(room_id, idx)
                for pid, ans in answers.items():
                    if ans == question.correct_option:
                        await redis_client.increment_score(room_id, pid)

                await redis_client.delete_answers(room_id, idx)

                players = await redis_client.get_players(room_id)
                leaderboard = [{"name": p["name"], "score": p["score"]} for p in players]

                await self.broadcast(room_id, {
                    "type": "leaderboard",
                    "leaderboard": leaderboard,
                    "show_for": LEADERBOARD_DURATION
                })

                await asyncio.sleep(LEADERBOARD_DURATION)

            await self.broadcast(room_id, {
                "type": "end",
                "leaderboard": leaderboard
            })
        except asyncio.CancelledError:
            logger.info(f"Quiz cancelled for room {room_id}")

        finally:
            await redis_client.save_room_meta(
                room_id,
                owner_id=room_meta["owner_id"],
                quiz_id=room_meta["quiz_id"],
                started=False,
                current_question_index=len(questions)
            )
            self.quiz_tasks.pop(room_id, None)

room_manager = RoomManager()