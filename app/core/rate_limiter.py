class RateLimiter:
    def __init__(self, redis, limit: int, window: int):
        self.redis = redis
        self.limit = limit
        self.window = window

    def allow(self, api_key: str) -> bool:
        key = f"rate_limit:{api_key}"

        current = self.redis.incr(key)

        if current == 1:
            self.redis.expire(key, self.window)

        return current <= self.limit
