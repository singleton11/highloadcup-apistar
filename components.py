import asyncio

import aioodbc

loop = asyncio.get_event_loop()


class DB(object):
    def __init__(self, db: asyncio.Future):
        self.db = db


async def initialize_db() -> asyncio.Future:
    dsn: str = 'Driver=SQLite;Database=travels?mode=memory&cache=shared'
    return await aioodbc.create_pool(dsn=dsn, loop=loop)
