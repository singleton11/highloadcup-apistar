from apistar import Route, Include, Component
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls

from components import DB, initialize_db
from controllers.users import get_user, get_visits

components = [
    Component(DB, init=initialize_db)
]

routes = [
    Route('/users/{user_id}', 'GET', get_user),
    Route('/users/{user_id}/visits', 'GET', get_visits),
    Include('/docs', docs_urls),
]

app = App(routes=routes, components=components)

if __name__ == '__main__':
    app.main()
