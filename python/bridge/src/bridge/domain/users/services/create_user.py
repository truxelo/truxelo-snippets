from dataclasses import dataclass

from bridge.domain.users.models.user import User
from bridge.domain.users.storages.interface import UserStorage


@dataclass(frozen=True)
class CreateUser:
    """The create user command payload."""

    email: str
    first_name: str
    last_name: str


class CreateUserHandler:
    """The create user command handler."""

    users: UserStorage

    def __init__(self, users: UserStorage):
        self.users = users

    async def handle(self, command: CreateUser) -> User:
        """Handles the create user command."""

        # create new user
        user = User(
            email=command.email,
            first_name=command.first_name,
            last_name=command.last_name,
        )

        # persist created user
        await self.users.insert(user)

        # return created user
        return user
