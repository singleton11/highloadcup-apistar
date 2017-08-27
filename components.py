import sqlite3


class DB(object):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection


def initialize_db() -> DB:
    connection: sqlite3.Connection = sqlite3.connect(
        database='/dev/shm/travels.db',
        check_same_thread=False,
    )
    return DB(connection)
