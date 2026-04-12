import os
import redis
from dotenv import load_dotenv

load_dotenv()


def get_redis_client():
    redis_url = os.getenv("REDIS_URL")

    if redis_url:
        return redis.Redis.from_url(
            redis_url,
            decode_responses=True
        )

    return redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )
