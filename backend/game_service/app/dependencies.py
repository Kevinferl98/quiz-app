from app.services.redis_client import RedisClient
from app.room_manager import RoomManager

_redis_instance = RedisClient()
_manager_instance = RoomManager(_redis_instance)

def get_redis_client() -> RedisClient:
    return _redis_instance

def get_room_manager() -> RoomManager:
    return _manager_instance