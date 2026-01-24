from functools import wraps
from typing import Awaitable
from typing import Callable

from injector import Injector
from injector import Module
from injector import inject
from injector import singleton
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from invoices.core.config import DatabaseConfig
from invoices.database.core import get_async_engine
from invoices.database.core import get_connection
from invoices.database.storages.invoices import DatabaseInvoiceStorage
from invoices.domain.storages.interface import InvoiceStorage


class ApplicationModule(Module):
    """Module to bind the application to its dependencies."""

    def __init__(self, config: DatabaseConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config = config

    def configure(self, binder):
        """Bind the application's dependencies."""
        binder.bind(InvoiceStorage, to=DatabaseInvoiceStorage)
        binder.bind(DatabaseConfig, to=self._config, scope=singleton)


def injected(func: Callable[..., Awaitable[Response]]) -> Callable[[Request], Awaitable[Response]]:
    """Decorator that injects dependencies into a view function."""

    @wraps(func)
    async def wrapper(request: Request) -> Response:
        injector: Injector = request.app.state.injector
        injector.binder.bind(Request, request)

        # Check if we already have a "pinned" connection (from our test fixture)
        pinned_connection = getattr(request.app.state, "pinned_connection", None)
        if pinned_connection:
            injector.binder.bind(AsyncConnection, to=pinned_connection)
            return await injector.call_with_injection(inject(func))

        # Otherwise create a new connection
        config = injector.get(DatabaseConfig)
        engine = await get_async_engine(config)
        async with get_connection(engine) as connection:
            injector.binder.bind(AsyncConnection, to=connection)
            response = await injector.call_with_injection(inject(func))
            await connection.commit()
            return response

    return wrapper


def init_app(app: Starlette, config: DatabaseConfig):
    """Initialize the Starlette app with dependency injection modules."""
    injector = Injector(ApplicationModule(config))
    app.state.injector = injector
