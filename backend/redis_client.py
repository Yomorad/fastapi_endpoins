import os
import aioredis
from dotenv import load_dotenv

load_dotenv()
redis = aioredis.from_url(os.getenv("REDIS_URL"))

async def get_redis():
    return redis
