from __future__ import annotations

from http import HTTPStatus

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response

from invoices.apps.server.extensions.injections import injected
from invoices.apps.server.resources.invoices.components import GetInvoicesQueryParams
from invoices.apps.server.resources.invoices.components import InvoiceComponent
from invoices.apps.server.resources.shared.components import ListComponent
from invoices.domain.services.fetch_all_invoices import FetchAllInvoices
from invoices.domain.services.fetch_all_invoices import FetchAllInvoicesHandler


@injected
async def get_invoices(
    request: Request,
    fetch_all_invoices_handler: FetchAllInvoicesHandler,
) -> Response:
    """Handles `GET /invoices` requests."""
    query_params = GetInvoicesQueryParams.model_validate(request.query_params)
    fetch_all_invoices = FetchAllInvoices(
        limit=query_params.limit,
        offset=query_params.offset,
    )
    invoices = await fetch_all_invoices_handler.handle(fetch_all_invoices)
    response = ListComponent.mapped(InvoiceComponent.from_invoice, invoices)
    return JSONResponse(
        response.model_dump(),
        status_code=HTTPStatus.OK,
    )
