import sqlite3


class DB(object):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection


def initialize_db() -> DB:
    connection: sqlite3.Connection = sqlite3.connect(
        database='travels.db',
        check_same_thread=False,
    )
    connection.execute('PRAGMA journal_mode=OFF')
    return DB(connection)
