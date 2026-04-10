from fastapi import Header, HTTPException
from app.core.redis_client import get_redis_client
from app.core.rate_limiter import RateLimiter
from app.core.api_key_manager import is_valid_api_key


redis_client = get_redis_client()

rate_limiter = RateLimiter(
    redis=redis_client,
    limit=10,
    window=60
)

def verify_api_key(x_api_key: str = Header(...)):
    if not is_valid_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    if not rate_limiter.allow(x_api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    return x_api_key
