from asyncpg import create_pool

import os
from dotenv import load_dotenv
load_dotenv()


ADMIN_ID = os.getenv('ADMIN_ID')
TOKEN = os.getenv('TOKEN')

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_HOST = os.getenv('PG_HOST')

REDIS_HOST = os.getenv('REDIS_HOST')

ELASTIC_HOST = os.getenv('ELASTIC_HOST')
ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
ELASTIC_PATH = os.getenv('ELASTIC_PATH')
ALIAS = os.getenv('ALIAS')

async def pool_settings():
    return await create_pool(user=PG_USER,
                             password=PG_PASSWORD,
                             host=PG_HOST,
                             port=PG_PORT,
                             database='shab_data',
                             command_timeout=60)