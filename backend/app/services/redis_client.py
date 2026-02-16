import redis.asyncio as redis
from app.models.quiz import Question
from app.config import config
import json

class RedisClient:
    def __init__(self):
        self.redis = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)

    async def save_room_meta(self, room_id: str, owner_id: str, quiz_id: str, 
                             started: bool = False, current_question_index: int = 0, ttl_seconds: int = 3600):
        await self.redis.hset(f"room:{room_id}", mapping={
            "room_id": room_id,
            "owner_id": owner_id,
            "quiz_id": quiz_id,
            "started": int(started),
            "current_question_index": current_question_index
        })
        await self.redis.expire(f"room:{room_id}", ttl_seconds)

    async def get_room_meta(self, room_id: str):
        data = await self.redis.hgetall(f"room:{room_id}")
        if not data:
            return None
        data["started"] = bool(int(data.get("started", 0)))
        data["current_question_index"] = int(data.get("current_question_index", 0))
        return data
    
    async def delete_room_meta(self, room_id: str):
        await self.redis.delete(f"room:{room_id}")

    async def save_questions(self, room_id: str, questions: list[Question], ttl_seconds: int = 3600):
        qlist = [q.model_dump() for q in questions]
        await self.redis.set(f"room:{room_id}:questions", json.dumps(qlist), ex=ttl_seconds)
    
    async def get_question(self, room_id: str, index: int):
        data = await self.redis.get(f"room:{room_id}:questions")
        if not data:
            return None
        qlist = json.loads(data)
        if index < 0 or index >= len(qlist):
            return None
        return Question.model_validate(qlist[index])
    
    async def get_all_questions(self, room_id: str) -> list[Question] | None:
        data = await self.redis.get(f"room:{room_id}:questions")
        if not data:
            return None
        qlist = json.loads(data)
        return [Question.model_validate(q) for q in qlist]

    async def delete_questions(self, room_id: str):
        await self.redis.delete(f"room:{room_id}:questions")

    async def add_player(self, room_id: str, player: Player, ttl_seconds: int = 3600):
        await self.redis.sadd(f"room:{room_id}:players", player.player_id)
        await self.redis.hset(f"room:{room_id}:player:{player.player_id}", mapping={
            "name": player.name,
            "score": player.score
        })
        await self.redis.expire(f"room:{room_id}:player:{player.player_id}", ttl_seconds)

    async def remove_player(self, room_id: str, player_id: str):
        await self.redis.srem(f"room:{room_id}:players", player_id)
        await self.redis.delete(f"room:{room_id}:player:{player_id}")

    async def get_players(self, room_id: str) -> list[dict]:
        player_ids = await self.redis.smembers(f"room:{room_id}:players")
        players = []
        for pid in player_ids:
            pdata = await self.redis.hgetall(f"room:{room_id}:player:{pid}")
            if pdata:
                players.append({
                    "player_id": pid,
                    "name": pdata.get("name"),
                    "score": int(pdata.get("score", 0))
                })
        return players
    
    async def save_answer(self, room_id: str, question_index: int, player_id: str, answer: str):
        await self.redis.hset(f"room:{room_id}:answers:{question_index}", player_id, answer)

    async def get_answers(self, room_id: str, question_index: int):
        return await self.redis.hgetall(f"room:{room_id}:answers:{question_index}")

    async def delete_answers(self, room_id: str, question_index: int):
        await self.redis.delete(f"room:{room_id}:answers:{question_index}")

    async def increment_score(self, room_id: str, player_id: str, points: int = 1):
        await self.redis.hincrby(f"room:{room_id}:player:{player_id}", "score", points)