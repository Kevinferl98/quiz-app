from fastapi import WebSocket
import asyncio
from typing import Dict, List
from app.models.multiplayer import Room
import logging

logger = logging.getLogger(__name__)

QUESTION_DURATION = 15
LEADERBOARD_DURATION = 3

class RoomManager:
    def __init__(self):
        self.active_rooms: Dict[str, Room] = {}
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
                    self.active_rooms.pop(room_id, None)

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

    async def start_quiz(self, room: Room):
        if room.room_id in self.quiz_tasks:
            return

        task = asyncio.create_task(self._run_quiz(room))
        self.quiz_tasks[room.room_id] = task

    async def _run_quiz(self, room: Room):
        room.started = True
        leaderboard = []

        try:
            for idx, question in enumerate(room.questions):
                room.current_question_index = idx
                await self.broadcast(room.room_id, {
                    "type": "question",
                    "question": question.dict(),
                    "index": idx
                })

                for t in range(QUESTION_DURATION, 0, -1):
                    await self.broadcast(room.room_id, {
                        "type": "timer",
                        "seconds": t
                    })
                    await asyncio.sleep(1)

                for player in room.players:
                    if player.current_answer == question.correct_option:
                        player.score += 1
                    player.current_answer = None

                leaderboard = [
                    {"name": p.name, "score": p.score}
                    for p in room.players
                ]

                await self.broadcast(room.room_id, {
                    "type": "leaderboard",
                    "leaderboard": leaderboard,
                    "show_for": LEADERBOARD_DURATION
                })

                await asyncio.sleep(LEADERBOARD_DURATION)

            await self.broadcast(room.room_id, {
                    "type": "end",
                    "leaderboard": leaderboard
                })
        except asyncio.CancelledError:
            logger.info(f"Quiz cancelled for room {room.room_id}")

        finally:
            room.started = False
            self.quiz_tasks.pop(room.room_id, None)

room_manager = RoomManager()