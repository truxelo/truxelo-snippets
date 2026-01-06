from unittest.mock import patch

import pytest
import pytest_asyncio
from sqlalchemy import Engine
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncEngine

from bridge.config import DatabaseConfig
from bridge.database.core import get_async_engine
from bridge.database.core import get_connection
from bridge.database.core import get_sync_engine


class TestGetAsyncEngine:
    """Tests for get_async_engine function."""

    @pytest_asyncio.fixture
    async def memory_config(self):
        """Provides a memory database configuration."""
        return DatabaseConfig(path=":memory:")

    @pytest_asyncio.fixture
    async def file_config(self):
        """Provides a file database configuration."""
        return DatabaseConfig(path="/tmp/test.db")

    @pytest.mark.asyncio
    async def test_creates_async_engine(self, memory_config):
        """Test that function creates an AsyncEngine."""
        engine = await get_async_engine(memory_config)

        assert isinstance(engine, AsyncEngine)
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_memory_database_creates_tables(self, memory_config):
        """Test that memory database creates tables automatically."""
        with patch("bridge.database.core._create_tables_async") as mock_create:
            engine = await get_async_engine(memory_config)
            mock_create.assert_called_once_with(engine)
            await engine.dispose()

    @pytest.mark.asyncio
    async def test_file_database_skips_table_creation(self, file_config):
        """Test that file database skips automatic table creation."""
        with patch("bridge.database.core._create_tables_async") as mock_create:
            engine = await get_async_engine(file_config)
            mock_create.assert_not_called()
            await engine.dispose()

    @pytest.mark.asyncio
    async def test_engine_url_matches_config(self, memory_config):
        """Test that engine URL matches config async URL."""
        engine = await get_async_engine(memory_config)
        assert str(engine.url) == memory_config.async_url
        await engine.dispose()


class TestGetSyncEngine:
    """Tests for get_sync_engine function."""

    @pytest.fixture
    def memory_config(self):
        """Provides a memory database configuration."""
        return DatabaseConfig(path=":memory:")

    @pytest.fixture
    def file_config(self):
        """Provides a file database configuration."""
        return DatabaseConfig(path="/tmp/test.db")

    def test_creates_sync_engine(self, memory_config):
        """Test that function creates a sync Engine."""
        engine = get_sync_engine(memory_config)
        assert isinstance(engine, Engine)
        engine.dispose()

    def test_memory_database_creates_tables(self, memory_config):
        """Test that memory database creates tables automatically."""
        with patch("bridge.database.core._create_tables_sync") as mock_create:
            engine = get_sync_engine(memory_config)
            mock_create.assert_called_once_with(engine)
            engine.dispose()

    def test_file_database_skips_table_creation(self, file_config):
        """Test that file database skips automatic table creation."""
        with patch("bridge.database.core._create_tables_sync") as mock_create:
            engine = get_sync_engine(file_config)
            mock_create.assert_not_called()
            engine.dispose()

    def test_engine_url_matches_config(self, memory_config):
        """Test that engine URL matches config sync URL."""
        engine = get_sync_engine(memory_config)

        assert str(engine.url) == memory_config.sync_url
        engine.dispose()


class TestGetConnection:
    """Tests for get_connection context manager."""

    @pytest_asyncio.fixture
    async def async_engine(self):
        """Provides an async engine for testing."""
        config = DatabaseConfig(path=":memory:")
        engine = await get_async_engine(config)
        yield engine
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_yields_connection(self, async_engine):
        """Test that context manager yields an AsyncConnection."""
        async with get_connection(async_engine) as conn:
            assert isinstance(conn, AsyncConnection)

    @pytest.mark.asyncio
    async def test_connection_is_active(self, async_engine):
        """Test that yielded connection is active and usable."""
        async with get_connection(async_engine) as conn:
            # Try to execute a simple query to verify connection works
            result = await conn.execute(text("SELECT 1"))
            row = result.one()
            assert row[0] == 1

    @pytest.mark.asyncio
    async def test_connection_closes_after_context(self, async_engine):
        """Test that connection is closed after exiting context."""
        conn_ref = None

        async with get_connection(async_engine) as conn:
            conn_ref = conn
            assert not conn.closed

        assert conn_ref.closed

    @pytest.mark.asyncio
    async def test_multiple_connections_are_independent(self, async_engine):
        """Test that multiple connections from same engine are independent."""
        async with get_connection(async_engine) as conn1:
            async with get_connection(async_engine) as conn2:
                assert conn1 is not conn2
                assert not conn1.closed
                assert not conn2.closed

    @pytest.mark.asyncio
    async def test_exception_in_context_closes_connection(self, async_engine):
        """Test that connection is closed even if exception occurs in context."""
        conn_ref = None

        with pytest.raises(ValueError):
            async with get_connection(async_engine) as conn:
                conn_ref = conn
                raise ValueError("Test exception")

        assert conn_ref.closed  # type: ignore

    @pytest.mark.asyncio
    async def test_can_create_multiple_sequential_connections(self, async_engine):
        """Test creating multiple connections sequentially."""
        connections = []

        for _ in range(3):
            async with get_connection(async_engine) as conn:
                connections.append(conn)
                result = await conn.execute(text("SELECT 1"))
                row = result.one()
                assert row[0] == 1

        for conn in connections:
            assert conn.closed
