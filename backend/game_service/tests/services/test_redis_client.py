import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.redis_client import RedisClient
from app.schemas.multiplayer import Player

@pytest.fixture
def redis_client():
    client = RedisClient()
    client.redis = MagicMock()
    client.redis.hset = AsyncMock()
    client.redis.hgetall = AsyncMock()
    client.redis.expire = AsyncMock()
    client.redis.set = AsyncMock()
    client.redis.get = AsyncMock()
    client.redis.delete = AsyncMock()
    client.redis.sadd = AsyncMock()
    client.redis.srem = AsyncMock()
    client.redis.smembers = AsyncMock()
    client.redis.hincrby = AsyncMock()
    client.redis.incr = AsyncMock()
    client.redis.publish = AsyncMock()
    client.redis.eval = AsyncMock(return_value=1)
    client.redis.pubsub = MagicMock()
    return client

@pytest.mark.asyncio
async def test_save_and_get_room_meta(redis_client):
    redis_client.redis.hgetall.return_value = {
        "room_id": "123",
        "owner_id": "owner",
        "quiz_id": "quiz1",
        "started": "1",
        "current_question_index": "2"
    }

    await redis_client.save_room_meta("123", "owner", "quiz1", True, 2, ttl_seconds=50)
    redis_client.redis.hset.assert_called_once()
    redis_client.redis.expire.assert_called_once()

    result = await redis_client.get_room_meta("123")
    assert result["started"] is True
    assert result["current_question_index"] == 2

@pytest.mark.asyncio
async def test_delete_room_meta(redis_client):
    await redis_client.delete_room_meta("123")
    redis_client.redis.delete.assert_called_once_with("room:123")

@pytest.mark.asyncio
async def test_questions_flow(redis_client):
    questions = [{"q": "A"}, {"q": "B"}]
    await redis_client.save_questions("123", questions, ttl_seconds=100)
    redis_client.redis.set.assert_called_once()

    redis_client.redis.get.return_value = '[{"q":"A"},{"q":"B"}]'
    q = await redis_client.get_question("123", 0)
    assert q == {"q": "A"}

    q_all = await redis_client.get_all_questions("123")
    assert q_all == [{"q":"A"},{"q":"B"}]

    await redis_client.delete_questions("123")
    redis_client.redis.delete.assert_called_with("room:123:questions")

@pytest.mark.asyncio
async def test_player_management(redis_client):
    player = Player(player_id="p1", name="John", score=0)

    await redis_client.add_player("123", player, ttl_seconds=60)
    redis_client.redis.sadd.assert_called_once()
    redis_client.redis.hset.assert_called_once()
    redis_client.redis.expire.assert_called_once()

    redis_client.redis.smembers.return_value = {"p1"}
    redis_client.redis.hgetall.return_value = {"name": "John", "score": "5"}
    players = await redis_client.get_players("123")
    assert players[0]["player_id"] == "p1"
    assert players[0]["score"] == 5

    await redis_client.remove_player("123", "p1")
    redis_client.redis.srem.assert_called_once()
    redis_client.redis.delete.assert_called_with("room:123:player:p1")


@pytest.mark.asyncio
async def test_answers_flow(redis_client):
    await redis_client.save_answer("123", 0, "p1", "ans")
    redis_client.redis.hset.assert_called_with("room:123:answers:0", "p1", "ans")

    redis_client.redis.hgetall.return_value = {"p1": "ans"}
    ans = await redis_client.get_answers("123", 0)
    assert ans == {"p1": "ans"}

    await redis_client.delete_answers("123", 0)
    redis_client.redis.delete.assert_called_with("room:123:answers:0")

@pytest.mark.asyncio
async def test_increment_and_counter(redis_client):
    await redis_client.increment_score("123", "p1", 3)
    redis_client.redis.hincrby.assert_called_once_with("room:123:player:p1", "score", 3)

    redis_client.redis.incr.return_value = 10
    val = await redis_client.incr_counter("key1")
    assert val == 10

@pytest.mark.asyncio
async def test_publish_room_message(redis_client):
    await redis_client.publish_room_message("123", {"type": "msg"})
    redis_client.redis.publish.assert_called_once()

@pytest.mark.asyncio
async def test_subscribe_rooms(redis_client):
    pubsub_mock = MagicMock()
    pubsub_mock.psubscribe = AsyncMock()
    async def fake_listen():
        yield {"type":"pmessage","channel":"room_123","data":'{"type":"msg"}'}
    pubsub_mock.listen = fake_listen
    redis_client.redis.pubsub.return_value = pubsub_mock
    handler = AsyncMock()
    await redis_client.subscribe_rooms(handler)
    handler.assert_called_once_with("123", {"type":"msg"})

@pytest.mark.asyncio
async def test_locks(redis_client):
    redis_client.redis.set.return_value = True
    acquired = await redis_client.acquire_lock("key1")
    assert acquired is True

    redis_client.redis.set.return_value = False
    acquired = await redis_client.acquire_lock("key1")
    assert acquired is False

    redis_client._locks["key1"] = "val"
    redis_client.redis.eval.return_value = 1
    released = await redis_client.release_lock("key1")
    assert released is True

    redis_client._locks.pop("key1")
    released = await redis_client.release_lock("key1")
    assert released is False