from logzero import logger

from components import DB


def welcome(db: DB):
    logger.info(db.connection.execute('SELECT * FROM users').fetchone())
    return {'message': 'Welcome to API Star!'}
