from apistar import Include, Route
from apistar.handlers import docs_urls, static_urls

from controllers.users import welcome

routes = [
    Route('/', 'GET', welcome),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
