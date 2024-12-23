import asyncio

from aiogram import Dispatcher, F
from aiogram.filters import Command
from arq.connections import create_pool, RedisSettings

from elasticsearch import AsyncElasticsearch

from core.orders_history import request_history, answer_history, concrete_date
from core.searching.search_main import search_flag, send_search_res
from core.subcore import bot, start, on_startup
from core.middleware.pg_middleware import PgPoolMiddleware
from core.main_order.callbacks import call_hub
from core.main_order.order_output import show_order
from core.menu import menu_1lvl, menu_2lvl, menu_3lvl
from core.tech_support.users_part import support_flag, send_problem
from core.utils.state_machine import SaveSteps

from core.data.postgre import PgSql

from core.config_main.config import pool_settings, ADMIN_ID, ELASTIC_PASSWORD, REDIS_HOST, ELASTIC_PATH, ELASTIC_HOST

dp = Dispatcher()

es = AsyncElasticsearch(
    hosts=[f'https://{ELASTIC_HOST}:9200'],
    basic_auth=('elastic', ELASTIC_PASSWORD),
    ca_certs=ELASTIC_PATH,
    verify_certs=False
)

async def main():
    pool_connect = await pool_settings()
    arq_pool = await create_pool(RedisSettings(REDIS_HOST))

    dp.update.middleware.register(PgPoolMiddleware(pool_connect))

    dp.message.register(start, Command(commands='start'))
    dp.message.register(show_order, Command(commands='my_order'))
    dp.message.register(menu_3lvl.show_dishes_ALL, Command(commands='dish_boom'), F.chat.id == int(ADMIN_ID))

    dp.message.register(menu_1lvl.menu, Command(commands='menu'))
    dp.message.register(menu_2lvl.menu_phase2, SaveSteps.LVL1_TO_2)
    dp.message.register(menu_3lvl.flag_dishes, SaveSteps.LVL2_TO_3)

    dp.message.register(request_history, Command(commands='orders_history'))
    dp.message.register(answer_history, SaveSteps.TIME_INTERVAL)
    dp.message.register(concrete_date, SaveSteps.WAIT_DATE)

    dp.message.register(search_flag, Command(commands='search'))
    dp.message.register(send_search_res, SaveSteps.GET_SEARCH)

    dp.message.register(support_flag, Command(commands='tech_support'))
    dp.message.register(send_problem, SaveSteps.SEND_PROBLEM)

    dp.callback_query.register(call_hub)

    dp.startup.register(on_startup)
    await dp.start_polling(bot,
                           allowed_updates=dp.resolve_used_update_types(),
                           db=PgSql(pool_connect),
                           arq=arq_pool,
                           es=es)

if __name__ == '__main__':
    asyncio.run(main())
