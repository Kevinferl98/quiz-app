from app.services.redis_client import RedisClient

ROOM_COUNTER_KEY = "global_room_counter"

async def create_room(redis: RedisClient, quiz_id: str, user_id: str, quiz_data: dict) -> dict:
    room_number = await redis.incr_counter(ROOM_COUNTER_KEY)
    room_id = f"{room_number:05d}"

    await redis.save_room_meta(
        room_id=room_id,
        owner_id=user_id,
        quiz_id=quiz_id,
        started=False,
        current_question_index=0,
        ttl_seconds=3600
    )

    await redis.save_questions(
        room_id=room_id,
        questions=quiz_data.get("questions", []),
        ttl_seconds=3600
    )

    return {"room_id": room_id}