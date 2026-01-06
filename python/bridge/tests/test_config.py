import os
from unittest.mock import patch

from bridge.config import DatabaseConfig


class TestDatabaseConfig:
    """Tests for DatabaseConfig class."""

    def test_default_path_from_env(self):
        """Test that default path comes from environment variable."""
        with patch.dict(os.environ, {"SQLITE_DATABASE": "/tmp/test.db"}):
            config = DatabaseConfig()
            assert config.path == "/tmp/test.db"

    def test_default_path_fallback(self):
        """Test that default path falls back to memory when env var not set."""
        with patch.dict(os.environ, {}, clear=True):
            config = DatabaseConfig()
            assert config.path == ":memory:"

    def test_explicit_path(self):
        """Test that explicit path overrides environment variable."""
        with patch.dict(os.environ, {"SQLITE_DATABASE": "/tmp/env.db"}):
            config = DatabaseConfig(path="/tmp/explicit.db")
            assert config.path == "/tmp/explicit.db"

    def test_async_url_with_file_path(self):
        """Test async URL generation with file path."""
        config = DatabaseConfig(path="/tmp/test.db")
        assert config.async_url == "sqlite+aiosqlite:////tmp/test.db"

    def test_async_url_with_memory(self):
        """Test async URL generation with memory database."""
        config = DatabaseConfig(path=":memory:")
        assert config.async_url == "sqlite+aiosqlite:///:memory:"

    def test_sync_url_with_file_path(self):
        """Test sync URL generation with file path."""
        config = DatabaseConfig(path="/tmp/test.db")
        assert config.sync_url == "sqlite:////tmp/test.db"

    def test_sync_url_with_memory(self):
        """Test sync URL generation with memory database."""
        config = DatabaseConfig(path=":memory:")
        assert config.sync_url == "sqlite:///:memory:"

    def test_is_memory_true(self):
        """Test is_memory returns True for memory database."""
        config = DatabaseConfig(path=":memory:")
        assert config.is_memory is True

    def test_is_memory_false(self):
        """Test is_memory returns False for file database."""
        config = DatabaseConfig(path="/tmp/test.db")
        assert config.is_memory is False

    def test_is_memory_false_with_similar_path(self):
        """Test is_memory returns False for paths containing 'memory'."""
        config = DatabaseConfig(path="/tmp/memory.db")
        assert config.is_memory is False
