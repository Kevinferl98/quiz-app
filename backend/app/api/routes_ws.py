from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.multiplayer import Room, Player
import logging
from app.websockets import room_manager

router_ws = APIRouter()
logger = logging.getLogger(__name__)

@router_ws.websocket("/ws/rooms/{room_id}/{player_id}")
async def weboscket_room(websocket: WebSocket, room_id: str, player_id: str):
    await room_manager.connect(room_id, websocket)

    if room_id not in room_manager.active_rooms:
        room_manager.active_rooms[room_id] = Room(
            room_id=room_id,
            quiz_id="",
            owner_id=player_id
        )

    room = room_manager.active_rooms[room_id]
    role = "host" if player_id == room.owner_id else "player"

    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("type")

            if action == "join":
                if role == "host":
                    continue
                name = data.get("name", "Guest")

                if not any(p.player_id == player_id for p in room.players):
                    room.players.append(
                        Player(player_id=player_id, name=name)
                    )
                
                await room_manager.broadcast(room_id, {
                    "type": "player_joined",
                    "players": [p.name for p in room.players]
                })

            elif action == "start":
                if role != "host":
                    await websocket.send_json({
                        "type": "error",
                        "message": "Only host can start the quiz"
                    })
                    continue
                await room_manager.start_quiz(room)

            elif action == "answer":
                if role != "player":
                    await websocket.send_json({
                        "type": "error",
                        "message": "Host cannot answer"
                    })
                    continue

                answer = data.get("answe")
                for p in room.players:
                    if p.player_id == player_id:
                        p.current_answer = answer
                        break
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": "Unknown action"
                })
    
    except WebSocketDisconnect:
        logger.info(f"{player_id} disconnected from {room_id}")

        if role == "player":
            room.players = [
                p for p in room.players if p.player_id != player_id
            ]

            await room_manager.broadcast(room_id, {
                "type": "player_left",
                "players": [p.name for p in room.players]
            })

        await room_manager.disconnect(room_id, websocket)