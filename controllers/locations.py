from typing import Tuple, Union

from components import DB


def get_location(db: DB, location_id: int):
    row: Tuple[Union[str, int], ...] = db.connection.execute('''
SELECT id, place, country, city, distance FROM locations WHERE id = ?
    ''', (location_id,)).fetchone()
    return {
        'id': row[0],
        'place': row[1],
        'country': row[2],
        'city': row[3],
        'distance': row[4],
    }
