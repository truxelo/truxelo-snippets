from uuid import UUID

from invoices.domain.models.invoice import Invoice
from invoices.domain.storages.interface import InvoiceStorage


class InMemoryInvoiceStorage(InvoiceStorage):
    """In-memory implementation of the InvoiceStorage interface."""

    _invoices: dict[UUID, Invoice]

    def __init__(self, *args: Invoice):
        self._invoices = {invoice.id: invoice for invoice in args}

    @property
    def items(self) -> list[Invoice]:
        """All invoices stored in memory."""
        return list(self._invoices.values())

    async def insert(self, invoice: Invoice) -> None:
        """Insert a new invoice."""
        self._invoices[invoice.id] = invoice

    async def fetch_all(self, limit: int = 100, offset: int = 0) -> list[Invoice]:
        """Fetch a paginated list of invoices."""
        start, end = offset, offset + limit
        return self.items[start:end]

    async def delete(self, invoice: Invoice) -> None:
        """Delete an invoice."""
        self._invoices.pop(invoice.id, None)
