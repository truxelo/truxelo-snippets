import pytest
import pytest_asyncio
from faker import Faker

from bridge.config import DatabaseConfig
from bridge.database.core import get_async_engine
from bridge.database.core import get_connection
from bridge.database.storages.user import PostgresUserStorage
from bridge.domain.users.models.user import User
from bridge.domain.users.storages.in_memory import InMemoryUserStorage

fake = Faker()


@pytest.fixture(scope="session")
def database_config():
    """Provides an in-memory database configuration for testing."""
    return DatabaseConfig(path=":memory:")


@pytest_asyncio.fixture(scope="session")
async def async_engine(database_config):
    """Provides an async SQLAlchemy engine for testing."""
    engine = await get_async_engine(database_config)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def async_connection(async_engine):
    """Provides an async database connection for testing."""
    async with get_connection(async_engine) as conn:
        yield conn


@pytest.fixture
def sample_user():
    """Provides a sample user for testing."""
    return User(
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )


@pytest.fixture
def sample_users():
    """Provides a list of sample users for testing."""
    return [
        User(
            email=fake.unique.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        for _ in range(5)
    ]


@pytest.fixture
def in_memory_user_storage():
    """Provides an in-memory user storage for testing."""
    return InMemoryUserStorage()


@pytest_asyncio.fixture
async def postgres_user_storage(async_connection):
    """Provides a PostgreSQL user storage for testing."""
    return PostgresUserStorage(async_connection)


@pytest.fixture
def user_data():
    """Provides sample user data for testing."""
    return {"email": fake.email(), "first_name": fake.first_name(), "last_name": fake.last_name()}


@pytest.fixture
def multiple_user_data():
    """Provides multiple sample user data sets for testing."""
    return [
        {
            "email": fake.unique.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }
        for _ in range(3)
    ]
