from uuid import UUID

from bridge.domain.users.models.user import User
from bridge.domain.users.storages.interface import UserStorage


class InMemoryUserStorage(UserStorage):
    """In-memory implementation of the UserStorage interface."""

    _users: dict[UUID, User]

    @property
    def items(self) -> list[User]:
        """All users stored in memory."""
        return list(self._users.values())

    def __init__(self, *args: User):
        self._users = {user.id: user for user in args}

    async def insert(self, user: User):
        self._users[user.id] = user

    async def update(self, user: User):
        self._users[user.id] = user

    async def fetch_by(self, email: str) -> User | None:
        return next((user for user in self.items if user.email == email), None)

    async def fetch_all(self, limit: int, offset: int) -> list[User]:
        start, end = offset, offset + limit
        return self.items[start:end]

    async def delete(self, user: User):
        self._users.pop(user.id, None)
