from apistar import Route, Include, Component
from apistar.frameworks.asyncio import ASyncIOApp as App
from apistar.handlers import docs_urls

from components import DB, initialize_db
from controllers.users import welcome

components = [
    Component(DB, init=initialize_db)
]

routes = [
    Route('/', 'GET', welcome),
    Include('/docs', docs_urls),
]

app = App(routes=routes, components=components)

if __name__ == '__main__':
    app.main()
