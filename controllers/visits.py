from typing import Dict, Union, Tuple

from apistar import typesystem

from components import DB


class NewVisit(typesystem.Object):
    properties = {
        'id': typesystem.Integer,
        'location': typesystem.Integer,
        'user': typesystem.Integer,
        'visited_at': typesystem.Integer,
        'mark': typesystem.Integer,
    }


class EditVisit(typesystem.Object):
    properties = {
        'location': typesystem.Integer,
        'user': typesystem.Integer,
        'visited_at': typesystem.Integer,
        'mark': typesystem.Integer,
    }


def get_visit(db: DB, visit_id: int) -> Dict[str, Union[int, str]]:
    row: Tuple[Union[str, int], ...] = db.connection.execute('''
SELECT id, location, user, visited_at, mark FROM visits WHERE id = ?
    ''', (visit_id,)).fetchone()
    return {
        'id': row[0],
        'location': row[1],
        'user': row[2],
        'visited_at': row[3],
        'mark': row[4],
    }


def new_visit(db: DB, visit: NewVisit) -> Dict:
    data: NewVisit = NewVisit(visit)
    db.connection.execute('INSERT INTO visits VALUES (?, ?, ?, ?, ?)',
                          (data['id'],
                           data['location'],
                           data['user'],
                           data['visited_at'],
                           data['mark']))
    return {}


def update_visit(db: DB, visit_id: int, visit: EditVisit) -> Dict:
    data: EditVisit = EditVisit(visit)
    db.connection.execute('''
UPDATE visits
SET    location = ?,
       user = ?,
       visited_at = ?,
       mark = ?
WHERE id = ?
    ''', (data['location'],
          data['user'],
          data['visited_at'],
          data['mark'],
          visit_id))
    return {}
