import os
from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class DatabaseConfig:
    """Configuration for the database connection."""

    path: str = field(default_factory=lambda: os.getenv("SQLITE_DATABASE", ":memory:"))

    @property
    def async_url(self) -> str:
        """Construct the SQLAlchemy async URL (default for the app)."""
        return f"sqlite+aiosqlite:///{self.path}"

    @property
    def sync_url(self) -> str:
        """Construct the SQLAlchemy sync URL (required for Alembic)."""
        # On utilise le driver standard sqlite3
        return f"sqlite:///{self.path}"

    @property
    def is_memory(self) -> bool:
        """Check if the database is in-memory."""
        return self.path == ":memory:"


database = DatabaseConfig()
