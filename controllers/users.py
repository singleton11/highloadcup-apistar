from typing import Dict, Union, List, Tuple

from apistar import Response, typesystem

from components import DB


class NewUser(typesystem.Object):
    properties = {
        'id': typesystem.Integer,
        'email': typesystem.String,
        'first_name': typesystem.String,
        'last_name': typesystem.String,
        'gender': typesystem.String,
        'birth_date': typesystem.Integer,
    }


class EditUser(typesystem.Object):
    properties = {
        'email': typesystem.String,
        'first_name': typesystem.String,
        'last_name': typesystem.String,
        'gender': typesystem.String,
        'birth_date': typesystem.Integer,
    }


def get_user(db: DB, user_id: int) -> Response:
    data: Dict[str, Union[str, int]] = db.connection.execute(
        '''
SELECT id,
       email,
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
    )


def new_user(db: DB, user: NewUser) -> Dict:
    data: NewUser = NewUser(user)
    db.connection.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
                          (data['id'],
                           data['email'],
                           data['first_name'],
                           data['last_name'],
                           data['gender'],
                           data['birth_date']))
    return {}


def update_user(db: DB, user_id: int, user: EditUser) -> Dict:
    data: EditUser = EditUser(user)
    db.connection.execute('''
UPDATE users 
SET    email = ?, 
       first_name = ?, 
       last_name = ?, 
       gender = ?, 
       birth_date = ? 
WHERE  id = ? 
''', (data['email'],
      data['first_name'],
      data['last_name'],
      data['gender'],
      data['birth_date']))
    return {}
