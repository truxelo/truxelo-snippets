from dataclasses import dataclass

from bridge.domain.users.models.user import User
from bridge.domain.users.storages.interface import UserStorage


@dataclass(frozen=True)
class UpdateUser:
    """The update user command payload."""

    email: str
    first_name: str | None
    last_name: str | None


class UpdateUserHandler:
    """The update user command handler."""

    users: UserStorage

    def __init__(self, users: UserStorage):
        self.users = users

    async def handle(self, command: UpdateUser) -> User:
        """Handles the update user command."""

        # fetch user matching email
        user = await self.users.fetch_by(command.email)
        if not user:
            raise RuntimeError("User not found")

        # update user according to command payload
        if command.first_name is not None:
            user.first_name = command.first_name
        if command.last_name is not None:
            user.last_name = command.last_name

        # persist updated user
        await self.users.update(user)

        # return updated user
        return user
