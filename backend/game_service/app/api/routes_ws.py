import logging
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.models.multiplayer import Player
from app.dependencies import get_room_manager, get_redis_client
from app.auth import get_current_user

router_ws = APIRouter()
logger = logging.getLogger(__name__)

@router_ws.websocket("/ws/rooms/{room_id}")
async def weboscket_room(websocket: WebSocket, room_id: str, manager=Depends(get_room_manager), redis=Depends(get_redis_client)):
    await manager.connect(room_id, websocket)

    token = websocket.query_params.get("token")

    user_payload = None
    player_id = None
    username = None

    if token:
        try:
            user_payload = get_current_user(f"Bearer {token}")
        except Exception:
            user_payload = None

    if user_payload:
        player_id = user_payload.get("sub")
        username = user_payload.get("preferred_username", "User")
    else:
        player_id = str(uuid.uuid4())
        username = None

    room_meta = await redis.get_room_meta(room_id)
    if not room_meta:
        await websocket.send_json({"type": "error", "message": "Room not found"})
        await websocket.close()
        return

    role = "host" if player_id == room_meta["owner_id"] else "player"

    await websocket.send_json({
        "type": "role",
        "role": role,
        "player_id": player_id
    })

    if role == "host" or user_payload:
        await redis.add_player(
            room_id,
            Player(player_id=player_id, name=username)
        )

    players = await redis.get_players(room_id)
    await redis.publish_room_message(room_id, {
        "type": "player_joined",
        "players": [p["name"] for p in players]
    })

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("type")

            if action == "join":
                if user_payload:
                    continue

                name = data.get("name")
                if not name:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Name required"
                    })
                    continue

                username = name

                await redis.add_player(room_id, Player(player_id=player_id, name=name))

                players = await redis.get_players(room_id)
                await redis.publish_room_message(room_id, {
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

                await manager.start_quiz(room_id)

            elif action == "answer":

                answer = data.get("answer")

                room_meta = await redis.get_room_meta(room_id)
                if not room_meta:
                    continue

                question_index = room_meta.get("current_question_index", 0)
                await redis.save_answer(room_id, question_index, player_id, answer)
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": "Unknown action"
                })
    
    except WebSocketDisconnect:
        logger.info(f"{player_id} disconnected from {room_id}")

        if role == "player":
            await redis.remove_player(room_id, player_id)

            players = await redis.get_players(room_id)
            await redis.publish_room_message(room_id, {
                "type": "player_left",
                "players": [p["name"] for p in players]
            })

        await manager.disconnect(room_id, websocket)