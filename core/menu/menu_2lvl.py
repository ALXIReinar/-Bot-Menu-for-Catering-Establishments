from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from arq.connections import ArqRedis

from core.data.postgre import PgSql
from core.menu.menu_3lvl import show_dishes
from core.utils.word_arrays import one_to_two
from core.utils.keyboards import Cold_Hot, menu_branch_1lvl
from core.utils.state_machine import SaveSteps



async def menu_phase2(message: Message, state: FSMContext, arq: ArqRedis, db: PgSql):
    mes = message.text[:-1]
    text = mes + ' ->'
    root = mes.lower().replace(' ', '-')
    await state.update_data(root=root)

    reply_kb = Cold_Hot()
    if root == 'закуски' or root == 'роллы':
        await state.set_state(SaveSteps.LVL2_TO_3)
        await message.answer(text, reply_markup=reply_kb)
    elif root in one_to_two:
        await message.answer(text)
        await show_dishes(message, state, arq, db)
    else:
        text = 'Нажимайте только на кнопки в меню!\n/menu'
        await message.answer(text, reply_markup=menu_branch_1lvl())
        await state.clear()



