from invoices.apps.server.resources.invoices import routes as invoices

routes = [
    *invoices.routes,
]
