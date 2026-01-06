from dataclasses import dataclass
from uuid import UUID

from uuid6 import uuid7


@dataclass
class User:
    """Represents a user of the system."""

    id: UUID
    email: str
    first_name: str
    last_name: str

    def __init__(
        self,
        email: str,
        first_name: str,
        last_name: str,
        id_: UUID | None = None,
    ):
        self.id = id_ or uuid7()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
