from typing import Dict, Union, List, Tuple

from apistar import typesystem, Response

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


def get_user(db: DB, user_id: int) -> Dict[str, Union[str, int]]:
    row: Tuple[Union[str, int], ...] = db.connection.execute(
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

    return Response({
        'id': row[0],
        'email': row[1],
        'first_name': row[2],
        'last_name': row[3],
        'gender': row[4],
        'birth_date': row[5]
    })


def get_visits(db: DB,
               user_id: int,
               fromDate: int,
               toDate: int,
               country: str,
               toDistance: int) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    params: Tuple[Union[int, str]] = (user_id,)
    query: str = f'''
SELECT   mark, 
         visited_at, 
         locations.place, 
         distance, 
         country 
FROM     visits 
         LEFT JOIN locations 
              ON visits.location = locations.id 
WHERE    USER = ? 
ORDER BY visited_at
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
    data: List[Tuple[Union[str, int]]] = db.connection.execute(
        query,
        params,
    ).fetchall()
    return Response({
        'visits': [
            {
                'mark': el[0],
                'visited_at': el[1],
                'place': el[2]
            } for el in data
        ]
    })


def new_user(db: DB, user: NewUser) -> Dict:
    data: NewUser = NewUser(user)
    db.connection.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
                          (data['id'],
                           data['email'],
                           data['first_name'],
                           data['last_name'],
                           data['gender'],
                           data['birth_date']))
    return Response({})


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
      data['birth_date'],
      user_id))
    return Response({})
