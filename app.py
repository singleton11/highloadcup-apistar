from typing import List

from apistar import Route, Include, Component
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls

from components import DB, initialize_db
from controllers.locations import (get_location,
                                   get_average,
                                   new_location,
                                   update_location)
from controllers.users import get_user, get_visits, new_user, update_user
from controllers.visits import get_visit, new_visit, update_visit

components: List[Component] = [
    Component(DB, init=initialize_db)
]

routes: List[Route] = [
    Route('/users/{user_id}', 'GET', get_user),
    Route('/users/{user_id}/visits', 'GET', get_visits),
    Route('/users/new', 'POST', new_user),
    Route('/users/{user_id}/edit', 'POST', update_user),
    Route('/locations/{location_id}', 'GET', get_location),
    Route('/locations/{location_id}/avg', 'GET', get_average),
    Route('/locations/new', 'POST', new_location),
    Route('/locations/{location_id}/edit', 'POST', update_location),
    Route('/visits/{visit_id}', 'GET', get_visit),
    Route('/visits/new', 'POST', new_visit),
    Route('/visits/{visit_id}/edit', 'POST', update_visit),
    Include('/docs', docs_urls),
]

app: App = App(routes=routes, components=components)

if __name__ == '__main__':
    app.main()
