from fastapi import Header, HTTPException
from app.core.redis_client import get_redis_client
from app.core.rate_limiter import RateLimiter

VALID_API_KEYS = {
    "taskforge_dev_key_123"
}


redis_client = get_redis_client()

rate_limiter = RateLimiter(
    redis=redis_client,
    limit=10,
    window=60
)

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not rate_limiter.allow(x_api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    return x_api_key
