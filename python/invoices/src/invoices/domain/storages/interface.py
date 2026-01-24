from abc import ABC
from abc import abstractmethod

from invoices.domain.models.invoice import Invoice


class InvoiceStorage(ABC):
    """Abstract base class for managing invoice persistence."""

    @abstractmethod
    async def insert(self, invoice: Invoice) -> None:
        """Stores a new invoice."""

    @abstractmethod
    async def fetch_all(self, limit: int = 100, offset: int = 0) -> list[Invoice]:
        """Fetches a paginated list of invoices."""

    @abstractmethod
    async def delete(self, invoice: Invoice) -> None:
        """Deletes an invoice by its ID."""
