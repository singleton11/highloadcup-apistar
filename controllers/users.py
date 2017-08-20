from components import DB


async def welcome(db: DB):
    return {'message': 'Welcome to API Star!'}
