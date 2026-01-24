from typing import AsyncGenerator

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette.applications import Starlette
from starlette.testclient import TestClient

from invoices.apps.server.app import create_app
from invoices.core.config import DatabaseConfig
from invoices.database.core import get_async_engine
from invoices.database.core import get_connection
from invoices.database.storages.invoices import DatabaseInvoiceStorage
from invoices.domain.models.invoice import Invoice

fake = Faker()


@pytest.fixture(scope="session")
def database_config() -> DatabaseConfig:
    """Provides an in-memory database configuration for testing."""
    return DatabaseConfig(path=":memory:")


@pytest_asyncio.fixture
async def connection(database_config: DatabaseConfig) -> AsyncGenerator[AsyncConnection, None]:
    """Keep one connection alive so the :memory: database doesn't disappear."""
    engine = await get_async_engine(database_config)
    async with get_connection(engine) as connection:
        yield connection
        await connection.close()
    await engine.dispose()


@pytest.fixture
def app(database_config: DatabaseConfig, connection: AsyncConnection) -> Starlette:
    """Create a Starlette application instance for testing."""
    app_instance = create_app(database_config)
    app_instance.state.pinned_connection = connection
    return app_instance


@pytest.fixture
def client(app: Starlette) -> TestClient:
    """A TestClient instance that can be used by tests to make http requests."""
    return TestClient(app)


@pytest_asyncio.fixture
async def invoice(connection: AsyncConnection) -> Invoice:
    """Now uses the same connection pinned to the app."""
    storage = DatabaseInvoiceStorage(connection)
    invoice = Invoice()
    await storage.insert(invoice)
    await connection.commit()
    return invoice
