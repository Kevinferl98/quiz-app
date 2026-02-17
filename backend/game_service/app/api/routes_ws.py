from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.multiplayer import Player
import logging
from app.room_manager import room_manager
from app.services.redis_client import RedisClient

router_ws = APIRouter()
logger = logging.getLogger(__name__)
redis_client = RedisClient()

@router_ws.websocket("/ws/rooms/{room_id}/{player_id}")
async def weboscket_room(websocket: WebSocket, room_id: str, player_id: str):
    await room_manager.connect(room_id, websocket)

    room_meta = await redis_client.get_room_meta(room_id)
    if not room_meta:
        await websocket.send_json({"type": "error", "message": "Room not found"})
        await websocket.close()
        return

    role = "host" if player_id == room_meta["owner_id"] else "player"

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("type")

            if action == "join":
                if role == "host":
                    continue

                name = data.get("name", "Guest")

                await redis_client.add_player(room_id, Player(player_id=player_id, name=name))

                players = await redis_client.get_players(room_id)
                await room_manager.broadcast(room_id, {
                    "type": "player_joined",
                    "players": [p["name"] for p in players]
                })

            elif action == "start":
                if role != "host":
                    await websocket.send_json({
                        "type": "error",
                        "message": "Only host can start the quiz"
                    })
                    continue

                await room_manager.start_quiz(room_id)

            elif action == "answer":
                if role != "player":
                    continue

                answer = data.get("answer")

                room_meta = await redis_client.get_room_meta(room_id)
                if not room_meta:
                    continue

                question_index = room_meta.get("current_question_index", 0)
                await redis_client.save_answer(room_id, question_index, player_id, answer)
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": "Unknown action"
                })
    
    except WebSocketDisconnect:
        logger.info(f"{player_id} disconnected from {room_id}")

        if role == "player":
            await redis_client.remove_player(room_id, player_id)

            players = await redis_client.get_players(room_id)
            await room_manager.broadcast(room_id, {
                "type": "player_left",
                "players": [p["name"] for p in players]
            })

        await room_manager.disconnect(room_id, websocket)