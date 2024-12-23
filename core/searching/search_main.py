from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from elasticsearch import AsyncElasticsearch

from core.data.postgre import PgSql
from core.searching.search_pattern import looking
from core.utils.keyboards import get_more
from core.utils.relevant_kb import relevant_extradition
from core.utils.state_machine import SaveSteps

from core.config_main.logger_settings import logger, sh
from core.config_main.config import ALIAS
logger.setLevel('INFO')
logger.addHandler(sh)


async def search_flag(message: Message, state: FSMContext):
    await message.answer("Введите поисковой запрос🔍", reply_markup=ReplyKeyboardRemove())
    await state.set_data({})
    await state.set_state(SaveSteps.GET_SEARCH)

async def send_search_res(message: Message, state: FSMContext, db: PgSql, es: AsyncElasticsearch):
    chat_id = message.chat.id
    mes_id = message.message_id + 1
    searched = (await state.get_data()).get('count')

    if not searched:
        query = looking(message.text)
        async with es:
            search_res = await es.search(index=ALIAS, query=query, size=50, source=False, filter_path='hits.hits')

        hits = search_res['hits']['hits']
        dishes_es = []
        for hit in hits:
            dishes_es.append(int(hit['_id']))
        count = 0
    else:
        count = searched[0]
        dishes_es = searched[1]

    edge_dishes_es = len(dishes_es)

    if edge_dishes_es:
        next_count = (count + 7) if (count + 7) <= edge_dishes_es else edge_dishes_es
        for i in range(count, next_count):
            _id = dishes_es[i]
            dish_db = await db.id_search(_id)

            name = dish_db[0][0]
            description = dish_db[0][1]
            pic = dish_db[0][2]
            await message.answer_photo(photo=pic, caption=name+description, reply_markup=await relevant_extradition(chat_id, _id))

        last_search_records = edge_dishes_es - next_count
        await message.answer(reply_to_message_id=mes_id,
                             text='Результаты поиска✨🔍',
                             reply_markup=get_more(last_search_records))

        await state.update_data(count=(next_count, dishes_es))
    else:
        await message.answer("Ничего не найдено, возможно, вы имели в виду: ") # ПОЛЕ ДЛЯ САДЖЕШЕНА

    await state.set_state(None)


async def thats_all(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Все результаты поиска были представлены!🤓")
    await state.clear()
    await call.answer()
