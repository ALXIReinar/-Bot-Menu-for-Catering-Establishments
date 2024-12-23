from pickle import loads

from aiogram.types import Message

from core.data.postgre import PgSql
from aioredis import Redis
from core.data.redis_storage import redis

from core.utils.keyboards import add_smth



async def data_for_db(order_list: list, db: PgSql) -> tuple[str, str]:
    text = ''
    qtys = ''
    for i in range(len(order_list)):
        dish_id = int(order_list[i].split('_')[0])

        d_name = (await db.free_request("SELECT name FROM dishes WHERE id = $1", dish_id))[0][0]
        qtys += order_list[i].split('_')[1]

        text += f'{i+1}. <code>{d_name}</code> - ' + '<b>{}</b>\n'

    return text, qtys

async def show_order(message: Message, db: PgSql):
    mes_p1 = 'Ваш Заказ:\n\n'
    get_order = await redis.get(f"_{message.chat.id}")
    order = []
    if get_order:
        order: list = loads(get_order)

    redis_order = await data_for_db(order, db)

    qtys =  redis_order[1]
    mes_p2 = redis_order[0]

    await message.answer(mes_p1 + mes_p2.format(*qtys), reply_markup=add_smth())

async def redis_path(_redis: Redis, chat_id: int) -> list:
    get_order = await _redis.get(f'_{chat_id}')
    if get_order:
        order_list: list = loads(get_order)
        return order_list
    return []
