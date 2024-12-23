from asyncpg import pool, Record
from typing import List


class PgSql:
    '''
    users(id, tg_id, name)
    dishes(id, name, description, pic, root)
    order_history(id, prsn_id, order, qtys, date)
    tech_appeals(id_appeal, tg_id, problem, media, status, date)
    '''
    def __init__(self, connection: pool.Pool):
        self.cursor = connection

    async def add_user(self, tg_id, name):
        async with self.cursor.acquire():
            query = "INSERT INTO users (tg_id, name) VALUES($1,$2) ON CONFLICT (tg_id) DO UPDATE SET name = $2"
            await self.cursor.execute(query, tg_id, name)

    async def get_dish_data(self):
        async with self.cursor.acquire():
            query = 'SELECT id, name, description FROM dishes'
            res: List[Record] = await self.cursor.fetch(query)
            return res

    async def add_dish(self, name, descr, picture, root):
        async with self.cursor.acquire():
            query = "INSERT INTO dishes (name, description, pic, root) VALUES($1,$2,$3,$4)"
            await self.cursor.execute(query, name, descr, picture, root)

    async def root_dishes(self, root):
        async with self.cursor.acquire():
            query = "SELECT id, name, description, pic FROM dishes WHERE root = $1"
            res: List[Record] = await self.cursor.fetch(query, root)
            return res

    async def boom_search(self):
        async with self.cursor.acquire():
            query = "SELECT name, description, pic FROM dishes"
            res: List[Record] = await self.cursor.fetch(query)
            return res

    async def id_search(self, _id):
        async with self.cursor.acquire():
            query = "SELECT name, description, pic FROM dishes WHERE id = $1"
            res: List[Record] = await self.cursor.fetch(query, _id)
            return res

    async def add_order(self, prsn_id, order, qtys):
        async with self.cursor.acquire():
            query = 'INSERT INTO orders_history (prsn_id, "order", qtys) VALUES($1, $2, $3)'
            await self.cursor.execute(query, prsn_id, order, qtys)

    async def add_appeal(self, id_appeal,tg_id, problem):
        async with self.cursor.acquire():
            query = "INSERT INTO tech_appeals (id_appeal ,tg_id, problem) VALUES ($1, $2, $3)"
            await self.cursor.execute(query, id_appeal, tg_id, problem)

    async def update_tech_status(self, status, id_appeal):
        async with self.cursor.acquire():
            query = "UPDATE tech_appeals SET status = $1 WHERE id_appeal = $2"
            await self.cursor.execute(query, status, id_appeal)

    async def user_id_by_appeal(self, id_appeal):
        async with self.cursor.acquire():
            query = ""
            res: List[Record] = await self.cursor.fetch(query, id_appeal)
            return res

    async def free_request(self, query, *args):
        async with self.cursor.acquire():
            if 'SELECT' in query:
                list_res: List[Record] = await self.cursor.fetch(query, *args)
                return list_res
            else:
                await self.cursor.execute(query, args)

    async def close(self):
        await self.cursor.close()
