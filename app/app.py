import os
import time
import random
import redis
from db import seed_data, get_from_db
from redis.sentinel import Sentinel

CACHE_TTL = int(os.getenv("CACHE_TTL") or 10)

def get_redis_client():
    if "REDIS_SENTINEL_HOST" in os.environ:
        sentinel = Sentinel(
            [(os.getenv("REDIS_SENTINEL_HOST"),
              int(os.getenv("REDIS_SENTINEL_PORT")))],
            socket_timeout=0.5
        )
        return sentinel.master_for(
            os.getenv("REDIS_MASTER_NAME"),
            decode_responses=True
        )
    return redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        decode_responses=True
    )

redis_client = get_redis_client()
seed_data()

stats = {"hits": 0, "misses": 0, "db": 0}

def get_item(key):
    cached = redis_client.get(key)
    if cached:
        stats["hits"] += 1
        return cached

    stats["misses"] += 1
    stats["db"] += 1
    doc = get_from_db(int(key))
    time.sleep(0.02)
    if doc:
        if CACHE_TTL <= 0:
            return doc["value"]  # cache disabled
        redis_client.setex(key, CACHE_TTL, doc["value"])
        return doc["value"]

while True:
    key = str(random.randint(0, 9999))
    start = time.time()
    get_item(key)
    latency = (time.time() - start) * 1000

    total = stats["hits"] + stats["misses"]
    if total % 100 == 0:
        hit_rate = stats["hits"] / total
        print(
            f"requests={total} "
            f"hit_rate={hit_rate:.2f} "
            f"db_queries={stats['db']} "
            f"latency_ms={latency:.2f}"
        )

    time.sleep(0.01)
