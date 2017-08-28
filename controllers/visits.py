from typing import Dict, Union, Tuple

from components import DB


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
