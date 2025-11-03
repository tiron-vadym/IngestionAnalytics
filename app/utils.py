import time
from collections import defaultdict


class TokenBucket:
    def __init__(self, rate_per_min: int):
        self.rate = rate_per_min
        self.tokens = defaultdict(lambda: self.rate)
        self.updated = defaultdict(lambda: time.time())

    def allow(self, key: str) -> bool:
        now = time.time()
        elapsed = now - self.updated[key]
        refill = elapsed * (self.rate / 60.0)
        self.tokens[key] = min(self.rate, self.tokens[key] + refill)
        self.updated[key] = now
        if self.tokens[key] >= 1:
            self.tokens[key] -= 1
            return True
        return False


rate_limiter = TokenBucket(rate_per_min=6000)
