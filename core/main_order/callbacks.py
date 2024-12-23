from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from elasticsearch import AsyncElasticsearch
from core.data.postgre import PgSql
from arq import ArqRedis

from core.main_order.basket import Basket
from core.menu.menu_1lvl import menu
from core.searching.search_main import send_search_res, thats_all
from core.tech_support.support_part import read_it, reply_flag, is_trash


async def call_hub(call: CallbackQuery, state: FSMContext, arq: ArqRedis, db: PgSql, es: AsyncElasticsearch):
    bk = Basket(call)
    if '*' in call.data:
        await bk.switch_on(call, arq, db)
    elif '/' in call.data:
        await bk.switch_off(call, db)

    elif 'add' in call.data:
        await bk.increase_one(call, db)
    elif 'rm' in call.data:
        await bk.reduce(call, db)

    elif call.data == 'more':
        await menu(call.message, state)
        await call.answer()

    elif call.data == 'search_residue':
        await send_search_res(call.message, state, db, es)
        await call.answer()
    elif call.data == 'thats_all!':
        await thats_all(call, state)

    elif call.data == 'read-it':
        await read_it(call)
    elif 'reply-to' in call.data:
        await reply_flag(call, state)
    elif 'trash' in call.data:
        await is_trash(call, db)

    else:
        await call.answer()