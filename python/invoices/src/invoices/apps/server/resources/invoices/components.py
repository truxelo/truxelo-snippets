from invoices.apps.server.resources.shared.components import Component
from invoices.apps.server.resources.shared.components import QueryParams
from invoices.apps.server.resources.shared.fields import UUID7
from invoices.domain.models.invoice import Invoice

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 100


class InvoiceComponent(Component):
    """Component for invoice-related data."""

    id: UUID7

    @staticmethod
    def from_invoice(invoice: Invoice):
        """Create an `InvoiceComponent` from an `Invoice`."""
        return InvoiceComponent(
            id=invoice.id,
        )


class GetInvoicesQueryParams(QueryParams):
    """Query parameters for fetching invoices."""

    offset: int = DEFAULT_OFFSET
    limit: int = DEFAULT_LIMIT
