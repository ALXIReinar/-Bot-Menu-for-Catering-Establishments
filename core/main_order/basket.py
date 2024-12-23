from aiogram.types import CallbackQuery, InputMediaPhoto
from arq import ArqRedis

from core.menu.menu_3lvl import arq_run
from core.subcore import bot
from core.utils.keyboards import add_basket, rm_basket

from core.data.postgre import PgSql
from core.data.redis_storage import redis
from pickle import dumps, loads


def check_id(data: str) -> int:
    res = 0
    split_data = data.split('_')
    if len(split_data) == 3:
        res = int(split_data[1])
    return res


class Basket:
    def __init__(self, call: CallbackQuery):
        self.chat_id = call.message.chat.id
        self.mes_id = call.message.message_id
        self.dish_id = check_id(call.data)
        self.lname = f'_{self.chat_id}'


    async def get_pic_N_text(self, db: PgSql) -> tuple[str,str]:
        info = await db.id_search(self.dish_id)

        name = info[0][0]
        description = info[0][1]
        pic = info[0][2]
        text = f'{name}\n{description}'
        return pic, text



    async def switch_on(self, call: CallbackQuery, arq: ArqRedis, db: PgSql):
        """Добавление к Заказу"""
        info = await self.get_pic_N_text(db)

        "Фронтенд"
        await bot.edit_message_media(chat_id=self.chat_id, message_id=self.mes_id,
                                     media=InputMediaPhoto(media=info[0], caption=info[1]),
                                     reply_markup=rm_basket(self.dish_id))
        await call.answer()

        "Redis Path"
        get_list = await redis.get(self.lname)
        if not get_list:
            dish_list = []
            await arq_run(call.message.chat.id, arq)
        else:
            dish_list: list = loads(get_list)

        for i in range(len(dish_list)):
            new_dish = call.data[2:]
            if dish_list[i][:-2] == new_dish[:-2]:
                dish_list[i] = new_dish
                break
        else:
            dish_list.append(call.data[2:])

        await redis.set(f'_{self.chat_id}', dumps(dish_list), ex=43200) #12 часов



    async def switch_off(self, call: CallbackQuery, db: PgSql):
        """Удаление из Заказа"""
        info = await self.get_pic_N_text(db)

        "Фронтенд"
        await bot.edit_message_media(chat_id=self.chat_id, message_id=self.mes_id,
                                     media=InputMediaPhoto(media=info[0], caption=info[1]),
                                     reply_markup=add_basket(self.dish_id))
        await call.answer()

        "Redis Path"
        dish_list: list = loads(await redis.get(self.lname))
        for i in range(len(dish_list)):
            if str(self.dish_id) in dish_list[i]:
                dish_list.pop(i)
                break
        await redis.set(self.lname, dumps(dish_list))



    async def increase_one(self, call: CallbackQuery, db: PgSql):
        """Увеличение на 1"""
        info = await self.get_pic_N_text(db)
        n = int(call.data.split('_')[2]) + 1

        "Фронтенд"
        await bot.edit_message_media(chat_id=self.chat_id, message_id=self.mes_id,
                                     media=InputMediaPhoto(media=info[0], caption=info[1]),
                                     reply_markup=rm_basket(self.dish_id, n))
        await call.answer()

        "Redis Path"
        dish_list = []
        check_list = await redis.get(self.lname)
        if check_list:
            dish_list: list = loads(check_list)
        for i in range(len(dish_list)):
            if str(self.dish_id) in dish_list[i]:
                dish = dish_list[i]
                dish_list[i] = f'{dish[:-1]}{n}'
                break

        await redis.set(self.lname, dumps(dish_list))



    async def reduce(self, call: CallbackQuery, db: PgSql):
        """Уменьшение на 1/ Удаление"""
        info = await self.get_pic_N_text(db)
        dish_list: list = loads(await redis.get(self.lname))
        dish = ''
        index = 0
        n = int(call.data.split('_')[2])

        "Поиск эл-та в Заказе"
        for i in range(len(dish_list)):
            if str(self.dish_id) in dish_list[i]:
                dish = dish_list[i]
                index = i
                break

        "Уменьшение на 1/ Удаление"
        n -= 1
        reply_kb = rm_basket(self.dish_id, n)
        if n <= 0:
            dish_list.pop(index)
            reply_kb = add_basket(self.dish_id)
        else:
            dish_list[index] = f'{dish[:-1]}{n}'
        await redis.set(self.lname, dumps(dish_list))

        "Фронтенд"
        await bot.edit_message_media(chat_id=self.chat_id, message_id=self.mes_id,
                                     media=InputMediaPhoto(media=info[0], caption=info[1]),
                                     reply_markup=reply_kb)
        await call.answer()
