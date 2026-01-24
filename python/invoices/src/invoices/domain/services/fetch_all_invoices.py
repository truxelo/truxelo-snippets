from dataclasses import dataclass

from injector import inject

from invoices.domain.models.invoice import Invoice
from invoices.domain.storages.interface import InvoiceStorage


@dataclass(frozen=True)
class FetchAllInvoices:
    """The fetch all invoices query payload."""

    limit: int
    offset: int


class FetchAllInvoicesHandler:
    """The fetch all invoices query handler."""

    invoices: InvoiceStorage

    @inject
    def __init__(self, invoices: InvoiceStorage):
        self.invoices = invoices

    async def handle(self, query: FetchAllInvoices) -> list[Invoice]:
        """Handles the fetch all invoices query."""
        invoices = await self.invoices.fetch_all(limit=query.limit, offset=query.offset)
        return invoices
