from typing import Dict, Union, List, Tuple

from apistar import Response, typesystem

from components import DB


class User(typesystem.Object):
    properties = {
        'id': typesystem.Integer,
        'first_name': typesystem.String,
        'last_name': typesystem.String,
        'gender': typesystem.String,
        'birth_date': typesystem.Integer
    }


def get_user(db: DB, user_id: int) -> Response:
    data: Dict[str, Union[str, int]] = db.connection.execute(
        '''
SELECT id,
       first_name,
       last_name,
       gender,
       birth_date
FROM   users
WHERE  id = ?
''',
        (user_id,)
    ).fetchone()
    return Response(
        str(data).encode('utf-8'),
        content_type='application/json;charset=utf-8',
    )


def get_visits(db: DB,
               user_id: int,
               fromDate: int,
               toDate: int,
               country: str,
               toDistance: int) -> Response:
    params: Tuple[Union[int, str]] = (user_id,)
    query: str = f'''
SELECT mark, 
       visited_at, 
       place, 
       distance, 
       country 
FROM   visits 
       LEFT JOIN locations 
              ON visits.location = locations.id 
WHERE  USER = ? 
'''
    if fromDate:
        query += ' AND visited_at > ?'
        params += (fromDate,)
    if toDate:
        query += ' AND visited_at < ?'
        params += (toDate,)
    if country:
        query += ' AND country = ?'
        params += (country,)
    if toDistance:
        query += ' AND distance < ?'
        params += (toDistance,)
    data: List[Dict[str, Union[str, int]]] = db.connection.execute(
        query,
        params,
    ).fetchall()
    return Response(
        str({'visits': [{
            'mark': el['mark'],
            'visited_at': el['visited_at'],
            'place': el['place']
        } for el in data]}).encode('utf-8'),
        content_type='application/json;charset=utf-8',
        status=200 if len(data) else 404,
    )
