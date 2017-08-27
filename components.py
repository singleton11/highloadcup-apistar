import sqlite3


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


class DB(object):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection


def initialize_db() -> DB:
    connection: sqlite3.Connection = sqlite3.connect(
        database='/dev/shm/travels.db',
        check_same_thread=False,
    )
    connection.row_factory = dict_factory
    return DB(connection)
