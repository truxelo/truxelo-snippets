from dataclasses import dataclass

from bridge.domain.users.models.user import User
from bridge.domain.users.storages.interface import UserStorage


@dataclass(frozen=True)
class FetchAllUsers:
    """The fetch all users query payload."""

    limit: int
    offset: int


class FetchAllUsersHandler:
    """The fetch all users query handler."""

    users: UserStorage

    def __init__(self, users: UserStorage):
        self.users = users

    async def handle(self, query: FetchAllUsers) -> list[User]:
        """Handles The fetch all users query."""

        # fetch all users with pagination
        users = await self.users.fetch_all(
            offset=query.offset,
            limit=query.limit,
        )

        # return fetched users
        return users
