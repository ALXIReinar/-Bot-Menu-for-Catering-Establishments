from aioredis import Redis
from core.config_main.config import REDIS_HOST

redis = Redis(host=REDIS_HOST)
