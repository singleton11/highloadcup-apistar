import asyncio

import aioodbc

loop = asyncio.get_event_loop()


class DB(object):
    def __init__(self, db: asyncio.Future):
        self.db = db


async def initialize_db() -> DB:
    dsn: str = 'Driver=SQLite;Database=travels?mode=memory&cache=shared'
    pool: asyncio.Future = await aioodbc.create_pool(dsn=dsn, loop=loop)
    return DB(pool)
