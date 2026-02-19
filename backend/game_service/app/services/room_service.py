import uuid
from app.services.redis_client import RedisClient

redis_client = RedisClient()

async def create_room(quiz_id: str, user_id: str, quiz_data: dict) -> dict:
    room_id = str(uuid.uuid4())

    await redis_client.save_room_meta(
        room_id=room_id,
        owner_id=user_id,
        quiz_id=quiz_id,
        started=False,
        current_question_index=0,
        ttl_seconds=3600
    )

    await redis_client.save_questions(
        room_id=room_id,
        questions=quiz_data.get("questions", []),
        ttl_seconds=3600
    )

    return {"room_id": room_id}