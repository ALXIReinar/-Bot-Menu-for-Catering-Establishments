from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.data.postgre import PgSql
from core.subcore import bot
from core.utils.state_machine import SaveSteps
from core.utils.keyboards import time_intervals
from core.utils.word_arrays import time_interval



async def interval_wrapper(message: Message, state: FSMContext, db: PgSql, query: str, args_tuple: tuple=None):
    reply_mes = False

    "Запрос в БД"
    if args_tuple:
        data_tuple = await db.free_request(query, message.chat.id, *args_tuple)
    else:
        data_tuple = await db.free_request(query, message.chat.id)


    "Кейс при ``Указать дату`` "
    if not data_tuple:
        await message.answer('Ничего не найдено')


    "Реплай на первую запись в БД - ч1"
    if len(data_tuple) >= 3:
        reply_mes = True


    "Раздача из БД"
    for i in range(len(data_tuple)):
        date = data_tuple[i][0] + timedelta(days=1)
        order = data_tuple[i][1]
        qtys = data_tuple[i][2]

        mes = f'<u><b><i>{date.strftime("%d-%m-%Y")}</i></b></u>\n\n' + f'{order.format(*qtys)}'
        await message.answer(mes)

        "Запись mes_id для Реплая"
        mes_id = (await state.get_data()).get('reply_message_id')
        if not mes_id:
            await state.update_data(reply_message_id=message.message_id + 1)


    "Реплай на первую запись в БД - ч2"
    if reply_mes:
        mes_id = (await state.get_data()).get('reply_message_id')
        await bot.send_message(message.chat.id, 'Первое сообщение', reply_to_message_id=mes_id)

    await state.clear()



async def request_history(message: Message, state: FSMContext):
    await message.answer('Выберите промежуток времени:', reply_markup=time_intervals())
    await state.set_state(SaveSteps.TIME_INTERVAL)

async def answer_history(message: Message, state: FSMContext, db: PgSql):
    ans = message.text.lower()

    if ans in time_interval.keys():
        db_arg = time_interval[ans]
        query = db_arg[0]
        dates = db_arg[1]

        await interval_wrapper(message, state, db, query, dates)

    elif ans == 'за всё время':
        query = 'SELECT date, "order", qtys FROM orders_history WHERE prsn_id = $1 ORDER BY date ASC'

        await interval_wrapper(message, state, db, query)

    elif ans == 'указать дату':
        await message.answer('''
        Введите дату в числовом виде
        ```
        Например 09/06/24
        ```
        ''', parse_mode='MarkdownV2')

        await state.set_state(SaveSteps.WAIT_DATE)

    else:
        await message.answer('Неверный Ввод❌\nПопробуйте ещё раз')
        await request_history(message, state)



async def concrete_date(message: Message, state: FSMContext, db: PgSql):
    date_string = message.text

    ch = ''
    for i in range(len(date_string)):
        if not date_string[i].isdigit():
            ch = date_string[i]
            break

    try:
        date_format = f'%d{ch}%m{ch}%y'
        if date_string[-4:].isdigit():
            date_format = f'%d{ch}%m{ch}%Y'

        date = datetime.strptime(date_string, date_format)
        query = 'SELECT date, "order", qtys FROM orders_history WHERE prsn_id = $1 AND date = $2'
        await interval_wrapper(message, state, db, query, (date,))

    except ValueError:
        await message.answer('Некорректный ввод❌\nПопробуйте ещё раз - /orders_history')
        await state.clear()
