from dataclasses import dataclass
from uuid import UUID

from uuid6 import uuid7


@dataclass
class Invoice:
    """Represents an invoice of the system."""

    id: UUID

    def __init__(
        self,
        id_: UUID | None = None,
    ):
        self.id = id_ or uuid7()
