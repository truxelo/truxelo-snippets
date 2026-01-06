from abc import ABC
from abc import abstractmethod

from bridge.domain.users.models.user import User


class UserStorage(ABC):
    """Abstract base class for managing users persistence."""

    @abstractmethod
    async def insert(self, user: User):
        """Stores the given user."""

    @abstractmethod
    async def update(self, user: User):
        """Stores the given user."""

    @abstractmethod
    async def fetch_by(self, email: str) -> User | None:
        """Fetches one user."""

    @abstractmethod
    async def fetch_all(self, limit: int, offset: int) -> list[User]:
        """Fetches all users."""

    @abstractmethod
    async def delete(self, user: User):
        """Deletes the given user."""
