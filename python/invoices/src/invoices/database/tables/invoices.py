from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy.types import UUID

from invoices.database.core import metadata

invoices = Table(
    "invoices",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
)
