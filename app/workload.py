import redis
import random
import time
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

while True:
    key = str(random.randint(0, 9999))
    r.get(key)
    time.sleep(0.005)
