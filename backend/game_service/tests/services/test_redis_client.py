import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.redis_client import RedisClient
from app.models.multiplayer import Player

@pytest.fixture
def redis_client():
    client = RedisClient()
    client.redis = MagicMock()
    return client

@pytest.mark.asyncio
async def test_save_room_meta(redis_client):
    redis_client.redis.hset = AsyncMock()
    redis_client.redis.expire = AsyncMock()

    await redis_client.save_room_meta(
        room_id="12345",
        owner_id="user1",
        quiz_id="quiz1",
        started=True,
        current_question_index=2,
        ttl_seconds=100
    )

    redis_client.redis.hset.assert_called_once_with(
        "room:12345",
        mapping={
            "room_id": "12345",
            "owner_id": "user1",
            "quiz_id": "quiz1",
            "started": 1,
            "current_question_index": 2
        }
    )

    redis_client.redis.expire.assert_called_once_with("room:12345", 100)

@pytest.mark.asyncio
async def test_get_room_meta(redis_client):
    redis_client.redis.hgetall = AsyncMock(return_value={
        "room_id": "12345",
        "owner_id": "user1",
        "quiz_id": "quiz1",
        "started": "1",
        "current_question_index": "3"
    })

    result = await redis_client.get_room_meta("12345")

    assert result["started"] is True
    assert result["current_question_index"] == 3

@pytest.mark.asyncio
async def test_get_room_meta_none(redis_client):
    redis_client.redis.hgetall = AsyncMock(return_value={})

    result = await redis_client.get_room_meta("12345")

    assert result is None

@pytest.mark.asyncio
async def test_save_questions(redis_client):
    redis_client.redis.set = AsyncMock()

    questions = [{"q": "test"}]

    await redis_client.save_questions("12345", questions, ttl_seconds=50)

    redis_client.redis.set.assert_called_once()

@pytest.mark.asyncio
async def test_get_question_valid(redis_client):
    redis_client.redis.get = AsyncMock(return_value='[{"q": "A"}, {"q": "B"}]')

    result = await redis_client.get_question("12345", 1)

    assert result == {"q": "B"}

@pytest.mark.asyncio
async def test_get_question_out_of_range(redis_client):
    redis_client.redis.get = AsyncMock(return_value='[{"q": "A"}]')

    result = await redis_client.get_question("12345", 5)

    assert result is None

@pytest.mark.asyncio
async def test_add_player(redis_client):
    redis_client.redis.sadd = AsyncMock()
    redis_client.redis.hset = AsyncMock()
    redis_client.redis.expire = AsyncMock()

    player = Player(player_id="p1", name="John", score=0)

    await redis_client.add_player("12345", player)

    redis_client.redis.sadd.assert_called_once()
    redis_client.redis.hset.assert_called_once()
    redis_client.redis.expire.assert_called_once()

@pytest.mark.asyncio
async def test_get_players(redis_client):
    redis_client.redis.smembers = AsyncMock(return_value={"p1"})
    redis_client.redis.hgetall = AsyncMock(return_value={
        "name": "John",
        "score": "5"
    })

    players = await redis_client.get_players("12345")

    assert players == [{
        "player_id": "p1",
        "name": "John",
        "score": 5
    }]

@pytest.mark.asyncio
async def test_increment_score(redis_client):
    redis_client.redis.hincrby = AsyncMock()

    await redis_client.increment_score("12345", "p1", 3)

    redis_client.redis.hincrby.assert_called_once_with(
        "room:12345:player:p1",
        "score",
        3
    )

@pytest.mark.asyncio
async def test_publish_room_message(redis_client):
    redis_client.redis.publish = AsyncMock()

    await redis_client.publish_room_message("12345", {"type": "test"})

    redis_client.redis.publish.assert_called_once()

@pytest.mark.asyncio
async def test_subscribe_rooms(redis_client):
    pubsub_mock = MagicMock()
    pubsub_mock.psubscribe = AsyncMock()
    
    async def fake_listen():
        yield {
            "type": "pmessage",
            "channel": "room_12345",
            "data": '{"type": "test"}'
        }

    pubsub_mock.listen = fake_listen
    redis_client.redis.pubsub = MagicMock(return_value=pubsub_mock)

    handler = AsyncMock()

    await redis_client.subscribe_rooms(handler)

    handler.assert_called_once_with("12345", {"type": "test"})