import secrets
from app.core.redis_client import get_redis_client

redis = get_redis_client()


def generate_api_key(company_name: str) -> str:
    api_key = f"tf_live_{secrets.token_hex(16)}"

    redis.hset(
        "taskforge:api_keys",
        api_key,
        company_name
    )

    return api_key


def is_valid_api_key(api_key: str) -> bool:
    return redis.hexists("taskforge:api_keys", api_key)


def revoke_api_key(api_key: str):
    redis.hdel("taskforge:api_keys", api_key)
