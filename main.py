import os

from aiohttp import web
from dotenv import load_dotenv
from app.db import DatabaseConnector, db_handler_middleware
from app.middlewares import jwt_auth_middleware, rate_limiter
from app.routes import setup_routes


load_dotenv()


async def init_db(app):
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', 5432),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
    }
    db_connector = DatabaseConnector(db_config)
    await db_connector.connect()
    app['db'] = db_connector


async def close_db(app):
    await app['db'].disconnect()


async def main():
    app = web.Application(
        middlewares=[
            jwt_auth_middleware,
            db_handler_middleware,
            rate_limiter
        ]
    )

    app.on_startup.append(init_db)
    app.on_shutdown.append(close_db)

    setup_routes(app)

    return app


web.run_app(main())
