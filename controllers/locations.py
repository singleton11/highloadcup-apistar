from typing import Tuple, Union, Dict

import arrow

from components import DB


def get_location(db: DB, location_id: int) -> Dict[str, Union[int, str]]:
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


def get_average(db: DB,
                location_id: int,
                fromDate: int,
                toDate: int,
                fromAge: int,
                toAge: int,
                gender: str) -> Dict[str, float]:
    query = '''
SELECT round(avg(mark), 5) AS avg
FROM visits
LEFT JOIN users ON visits.user = users.id
WHERE location = ?
    '''
    params = (location_id,)

    if fromDate:
        query += ' AND visited_at > ?'
        params += (fromDate,)
    if toDate:
        query += ' AND visited_at < ?'
        params += (toDate,)
    if fromAge:
        timestamp: int = arrow.now().shift(years=-fromAge).timestamp
        query += ' AND birth_date < ?'
        params += (timestamp,)
    if toAge:
        timestamp: int = arrow.now().shift(years=-toAge).timestamp
        query += ' AND birth_date > ?'
        params += (timestamp,)
    if gender:
        query += ' AND gender = ?'
        params += (gender,)
    row: Tuple[float] = db.connection.execute(query, params).fetchone()

    return {
        'avg': row[0] if row[0] else 0,
    }
