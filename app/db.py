import asyncpg
from typing import Optional, Dict, Any
from aiohttp import web


class DatabaseConnector:
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.pool: Optional[asyncpg.pool.Pool] = None

    async def connect(self):
        """Create a connection pool to the database."""
        self.pool = await asyncpg.create_pool(
            host=self.db_config['host'],
            port=self.db_config['port'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database'],
            min_size=5,  # Minimum number of connections in the pool
            max_size=10,  # Maximum number of connections in the pool
        )

    async def disconnect(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()

    async def fetch(self, query: str, *args) -> list:
        """Fetch rows from the database."""
        if not self.pool:
            raise RuntimeError("Database connection pool is not initialized.")
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute(self, query: str, *args):
        """Execute a query (e.g., INSERT, UPDATE, DELETE)."""
        if not self.pool:
            raise RuntimeError("Database connection pool is not initialized.")
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)


@web.middleware
async def db_handler_middleware(request, handler):
    db_connector = request.app['db']

    async with db_connector.pool.acquire() as connection:
        request['connection'] = connection  # Attach connection to the request
        response = await handler(request)  # Pass control to the handler
        return response
