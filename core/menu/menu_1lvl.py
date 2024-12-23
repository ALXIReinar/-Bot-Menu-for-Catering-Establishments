from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.keyboards import menu_branch_1lvl
from core.utils.state_machine import SaveSteps


async def menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выбери блюдо:', reply_markup=menu_branch_1lvl())
    await state.set_state(SaveSteps.LVL1_TO_2)

