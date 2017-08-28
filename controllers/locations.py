from typing import Tuple, Union, Dict

import arrow
from apistar import typesystem, Response

from components import DB


class NewLocation(typesystem.Object):
    properties = {
        'id': typesystem.Integer,
        'place': typesystem.String,
        'country': typesystem.String,
        'city': typesystem.String,
        'distance': typesystem.Integer,
    }


class EditLocation(typesystem.Object):
    properties = {
        'place': typesystem.String,
        'country': typesystem.String,
        'city': typesystem.String,
        'distance': typesystem.Integer,
    }


def get_location(db: DB, location_id: int) -> Dict[str, Union[int, str]]:
    row: Tuple[Union[str, int], ...] = db.connection.execute('''
SELECT id, place, country, city, distance FROM locations WHERE id = ?
    ''', (location_id,)).fetchone()
    return Response({
        'id': row[0],
        'place': row[1],
        'country': row[2],
        'city': row[3],
        'distance': row[4],
    })


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

    return Response({
        'avg': row[0] if row[0] else 0,
    })


def new_location(db: DB, location: NewLocation) -> Dict:
    data: NewLocation = NewLocation(location)
    db.connection.execute('INSERT INTO locations VALUES (?, ?, ?, ?, ?)',
                          (data['id'],
                           data['place'],
                           data['country'],
                           data['city'],
                           data['distance']))
    return Response({})


def update_location(db: DB, location_id: int, location: EditLocation) -> Dict:
    data: EditLocation = EditLocation(location)
    db.connection.execute('''
UPDATE locations
SET    place = ?,
       country = ?,
       city = ?,
       distance = ?
WHERE  id = ?
    ''', (data['place'],
          data['country'],
          data['city'],
          data['distance'],
          location_id))
    return Response({})
