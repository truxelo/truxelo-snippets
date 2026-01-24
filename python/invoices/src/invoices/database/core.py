from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import Engine
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from invoices.core.config import DatabaseConfig

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)


async def _create_tables_async(engine: AsyncEngine):
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


def _create_tables_sync(engine: Engine):
    """Create all tables in the database."""
    metadata.create_all(engine)


async def get_async_engine(config: DatabaseConfig) -> AsyncEngine:
    """Create a new async engine."""
    engine = create_async_engine(config.async_url)
    if config.is_memory:
        await _create_tables_async(engine)
    return engine


def get_sync_engine(config: DatabaseConfig) -> Engine:
    """Create a new engine."""
    engine = create_engine(config.sync_url)
    if config.is_memory:
        _create_tables_sync(engine)
    return engine


@asynccontextmanager
async def get_connection(engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    """Async context manager that yields a database connection."""
    async with engine.connect() as conn:
        yield conn
