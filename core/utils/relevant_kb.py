from pickle import loads

from core.data.redis_storage import redis

from core.utils.keyboards import add_basket
from core.utils.keyboards import rm_basket


async def relevant_extradition(chat_id: int, dish_id: int):
    kb = add_basket(dish_id)
    order_list = await redis.get(f'_{chat_id}')

    if order_list:
        order_list = loads(order_list)
        for dish in order_list:
            info = dish.split('_')
            id = info[0]
            qty = info[1]
            if int(id) == dish_id:
                return rm_basket(id, qty)
    return kb
