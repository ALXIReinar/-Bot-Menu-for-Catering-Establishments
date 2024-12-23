from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/menu', description='Показывает меню'),
        BotCommand(command='/my_order', description='Перейти к заказу'),
        BotCommand(command='/search', description='Поиск еды'),
        BotCommand(command='/orders_history', description='История заказов за период'),
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/tech_support', description='Техническая поддержка')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
