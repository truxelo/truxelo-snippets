from starlette.routing import Route

from .endpoints import get_invoices

routes = [
    Route("/invoices", get_invoices, methods=["GET"]),
]
