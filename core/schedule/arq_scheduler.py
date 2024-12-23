from arq import run_worker
from arq.typing import WorkerSettingsBase
from arq.connections import RedisSettings

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from aioredis import Redis

from core.main_order.order_output import data_for_db, redis_path
from core.config_main.config import TOKEN, pool_settings, REDIS_HOST
from core.data.postgre import PgSql



async def startup(ctx):
    ctx['bot'] = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    ctx['redis'] = Redis(host=REDIS_HOST)
    ctx['db'] = PgSql(await pool_settings())

async def shutdown(ctx):
    await ctx['db'].close()


async def redis_save_n_flush(ctx, chat_id: int):
    redis = ctx['redis']
    db = ctx['db']

    order_list = await redis_path(redis, chat_id)

    parse_data = await data_for_db(order_list, db)
    order = parse_data[0]
    qtys = parse_data[1]

    if len(order) != 0:
        await db.add_order(chat_id, order, qtys)
    await redis.delete(f'_{chat_id}')


class WorkerSettings(WorkerSettingsBase):
    redis_settings = RedisSettings(REDIS_HOST)
    on_startup = startup
    on_shutdown = shutdown
    functions = [redis_save_n_flush]

run_worker(WorkerSettings)
