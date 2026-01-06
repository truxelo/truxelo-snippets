# pylint: disable=not-callable

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import func
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import UUID
from sqlalchemy.types import VARCHAR

from bridge.database.core import metadata

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("email", VARCHAR(255), unique=True, nullable=False),
    Column("first_name", VARCHAR(255), nullable=False),
    Column("last_name", VARCHAR(255), nullable=False),
    Column("created_at", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False),
)
