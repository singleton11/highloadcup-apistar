from apistar.frameworks.asyncio import ASyncIOApp as App

from routes import routes

app = App(routes=routes)

if __name__ == '__main__':
    app.main()
