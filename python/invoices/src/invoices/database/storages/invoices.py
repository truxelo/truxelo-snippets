from injector import inject
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from invoices.database.tables.invoices import invoices
from invoices.domain.models.invoice import Invoice
from invoices.domain.storages.interface import InvoiceStorage


class DatabaseInvoiceStorage(InvoiceStorage):
    """Postgres implementation of the InvoiceStorage interface."""

    @inject
    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def insert(self, invoice: Invoice) -> None:
        """Inserts a new invoice into the database."""
        stmt = insert(invoices).values(id=invoice.id)
        await self._connection.execute(stmt)

    async def fetch_all(self, limit: int = 100, offset: int = 0) -> list[Invoice]:
        """Fetches a paginated list of invoices, ordered by ID (chronological via uuid7)."""
        stmt = select(invoices).limit(limit).offset(offset).order_by(invoices.c.id)
        result = await self._connection.execute(stmt)
        rows = result.fetchall()
        return [Invoice(id_=row.id) for row in rows]

    async def delete(self, invoice: Invoice) -> None:
        """Deletes an invoice by its ID."""
        stmt = delete(invoices).where(invoices.c.id == invoice.id)
        await self._connection.execute(stmt)
