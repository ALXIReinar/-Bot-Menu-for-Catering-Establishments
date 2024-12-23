from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from asyncpg import pool
from core.data.postgre import PgSql

from typing import Dict, Any, Awaitable, Callable


class PgPoolMiddleware(BaseMiddleware):
    def __init__(self, connection: pool.Pool):
        super().__init__()
        self.connection = connection

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> None:
        async with self.connection.acquire() as conn:
            data['psql_pool'] = PgSql(conn)
            return await handler(event, data)
