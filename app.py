from typing import List

from apistar import Route, Include, Component
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls

from components import DB, initialize_db
from controllers.locations import get_location
from controllers.users import get_user, get_visits, new_user, update_user

components: List[Component] = [
    Component(DB, init=initialize_db)
]

routes: List[Route] = [
    Route('/users/{user_id}', 'GET', get_user),
    Route('/users/{user_id}/visits', 'GET', get_visits),
    Route('/users/new', 'POST', new_user),
    Route('/users/{user_id}/edit', 'POST', update_user),
    Route('/locations/{location_id}', 'GET', get_location),
    Include('/docs', docs_urls),
]

app: App = App(routes=routes, components=components)

if __name__ == '__main__':
    app.main()
