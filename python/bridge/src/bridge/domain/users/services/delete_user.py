from dataclasses import dataclass

from bridge.domain.users.models.user import User
from bridge.domain.users.storages.interface import UserStorage


@dataclass(frozen=True)
class DeleteUser:
    """The delete user command payload."""

    email: str


class DeleteUserHandler:
    """The delete user command handler."""

    users: UserStorage

    def __init__(self, users: UserStorage):
        self.users = users

    async def handle(self, command: DeleteUser) -> User:
        """Handles the delete user command."""

        # fetch user matching email
        user = await self.users.fetch_by(command.email)
        if not user:
            raise RuntimeError("User not found")

        # persist user deletion
        await self.users.delete(user)

        # return deleted user
        return user
