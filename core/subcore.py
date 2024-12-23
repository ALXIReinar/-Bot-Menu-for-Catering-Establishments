from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from core.menu.menu_1lvl import menu
from core.data.postgre import PgSql
from core.commands import set_commands
from core.config_main.config import TOKEN, ADMIN_ID

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


async def on_startup():
    await bot.send_message(ADMIN_ID, 'Бот запущен!', reply_markup=ReplyKeyboardRemove())

async def start(message: Message, state: FSMContext, db: PgSql):
    tg_id = message.from_user.id
    name = message.from_user.first_name

    await db.add_user(tg_id, name)
    await set_commands(bot)

    await message.answer(f'Привет, {message.from_user.first_name}!',reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await menu(message, state)
