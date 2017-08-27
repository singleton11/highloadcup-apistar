#!/usr/bin/env python
import json
import sqlite3
from typing import Any, Dict, List, Generator, NamedTuple
from zipfile import ZipFile

from logzero import logger


class Location(NamedTuple):
    id: int
    place: str
    country: str
    city: str
    distance: int


class User(NamedTuple):
    id: int
    email: str
    first_name: str
    last_name: str
    gender: str
    birth_date: int


class Visit(NamedTuple):
    id: int
    location: int
    user: int
    visited_at: int
    mark: int


connection: sqlite3.Connection = sqlite3.connect(
    database='/dev/shm/travels.db',
    check_same_thread=False,
)

# Create schema
with open('migrations/initial.sql') as f:
    content = f.read()
    cursor = connection.cursor()
    [cursor.execute(statement) for statement in content.split(';')]
    connection.commit()

with ZipFile('/tmp/data/data.zip') as zf:
    for info in zf.infolist():
        if info.filename != 'options.txt':
            logger.info(f'Reading {info.filename}...')
            piece: Dict[str, List[Dict[str, Any]]] = json.loads(
                zf.read(info.filename)
            )
            if 'locations' in piece:
                data: Generator[Location, Any, None] = (
                    Location(**location)
                    for location in piece['locations']
                )
                query: str = '''
    INSERT INTO locations VALUES (?, ?, ?, ?, ?)
                                '''
                cursor.executemany(query, data)
            if 'users' in piece:
                data: Generator[User, Any, None] = (
                    User(**user)
                    for user in piece['users']
                )
                query: str = '''
    INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)
                            '''
                cursor.executemany(query, data)
            if 'visits' in piece:
                data: Generator[Visit, Any, None] = (
                    Visit(**visit)
                    for visit in piece['visits']
                )
                query: str = '''
    INSERT INTO visits VALUES (?, ?, ?, ?, ?)
                            '''
                cursor.executemany(query, data)
            connection.commit()
cursor.close()
connection.close()
