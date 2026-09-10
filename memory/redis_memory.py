import redis
import json
from config.settings import settings

#decode_responses=True means Redis returns strings instead of raw bytes —
# without this, every value you get back would be like b"hello" instead of "hello"
client = redis.Redis(
    host = settings.REDIS_HOST,
    port = settings.REDIS_PORT,
    username= settings.REDIS_USERNAME,
    password= settings.REDIS_PASSWORD,
    decode_responses= True
)

TTL_seconds = 24 * 60 * 60

# def _session_key(session_id: str) -> str : # generate code under which we store every conversation within the chat
#     return f"session:{session_id}:history"
#
# def save_message (session_id: str , role : str , content : str , user_id = None):
#     user_id = user_id or session_id
#     key = _session_key(session_id) # the generate code tells where to add this message
#
#     message = json.dumps({"role" : role , "content" : content , "user_id" : user_id})
#     client.rpush(key , message)
#     client.expire(key , TTL_seconds)
#
# def get_history(session_id : str) -> list :
#     key = _session_key(session_id)
#     raw_message = client.lrange(key , 0 , -1)
#     formated_message = [json.loads(msg) for msg in raw_message]
#     return formated_message
#
# def clear_history(session_id : str ):
#     key = _session_key(session_id)
#     client.delete(key)

def _session_key(session_id : str ) -> str:
    return f"session:{session_id}:history"

def save_message(session_id : str , role: str , content: str , user_id : str = None):
    user_id = user_id or session_id
    key = _session_key(session_id)

    message = json.dumps({"role": role , "content" : content , "user_id": user_id})
    client.rpush(key , message)
    client.expire(key , TTL_seconds)

def get_history(session_id : str) -> list:
    key = _session_key(session_id)
    raw_message = client.lrange(key , 0 , -1)
    formated = [json.loads(msg) for msg in raw_message]
    return formated

def clear_history(session_id : str ):
    key = _session_key(session_id)
    client.delete(key)