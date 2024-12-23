import asyncio
from pickle import dumps
from datetime import datetime, timedelta

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramRetryAfter
from arq.connections import ArqRedis

from core.data.postgre import PgSql
from core.data.redis_storage import redis

from core.menu.menu_1lvl import menu
from core.subcore import bot
from core.utils.keyboards import Cold_Hot, user_by_id
from core.config_main.config import ADMIN_ID
from core.utils.relevant_kb import relevant_extradition


async def arq_run(chat_id: int, arq: ArqRedis):
    data = dumps([])
    now = datetime.now()
    day = 86400

    hour, minute, second = now.hour - 2, now.minute, now.second
    now_in_seconds = 3600 * hour + 60 * minute + second

    ttl = day - now_in_seconds
    await redis.set(f'_{chat_id}', data)
    await arq.enqueue_job('redis_save_n_flush', _defer_by=timedelta(seconds=ttl - 300),  #
                          chat_id=chat_id)



async def show_dishes(message: Message, state: FSMContext, arq: ArqRedis, db: PgSql):
    chat_id = message.chat.id
    root = (await state.get_data()).get('root')
    info = await db.root_dishes(root)

    for i in range(len(info)):
        dish_id = info[i][0]
        text = (f'{info[i][1]}\n'
                f'{info[i][2]}\n')
        link = info[i][3]

        try:
            await message.answer_photo(photo=link, caption=text, reply_markup=await relevant_extradition(chat_id, dish_id))

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await message.answer_photo(photo=link, caption=text, reply_markup=await relevant_extradition(chat_id, dish_id))
        except Exception as e:
            await bot.send_message(ADMIN_ID, f'{e}\n\nВызвана пользователем {message.from_user.id}\n\n{datetime.now().strftime("%d/%m/%y | %H:%M")}')

        await asyncio.sleep(.05)


    """Заказ в Редис и запуск Арк`а"""
    if not await redis.get(f'_{message.chat.id}'):
        await arq_run(message.chat.id, arq)


    await message.answer('Продолжить? - /menu\n'
                         'Перейти к заказу - /my_order', reply_markup=ReplyKeyboardRemove())
    await state.clear()



async def flag_dishes(message: Message, state: FSMContext, arq: ArqRedis, db: PgSql):
    if message.text[:-2] == 'Назад':
        await menu(message, state)
    else:

        mes = message.text[:-1].lower()
        root = (await state.get_data()).get('root')

        if mes == 'горячие' or mes == 'холодные':
            await state.update_data(root=root + '_' + mes)
            await show_dishes(message, state, arq, db)
        else:
            await message.answer('Нажимайте только на кнопки в меню!\n/menu', reply_markup=Cold_Hot())
            await state.clear()



async def show_dishes_ALL(message: Message, db: PgSql):
    info = await db.boom_search()

    for i in range(len(info) - 55):
        name = info[i][0]
        description = info[i][1]
        text = f'{name}\n{description}'
        link = info[i][2]

        try:
            await message.answer_photo(photo=link, caption=text)

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await message.answer_photo(photo=link, caption=text)
        except Exception as e:
            await bot.send_message(ADMIN_ID,
                                   f'{e}\n\nВызвана пользователем {message.from_user.id} в {datetime.now()}', reply_markup=user_by_id(message.from_user.id))

        await asyncio.sleep(.05)
