from starlette.applications import Starlette

from invoices.apps.server.extensions import injections
from invoices.apps.server.resources.errors.handlers import handlers
from invoices.apps.server.resources.routes import routes
from invoices.core.config import DatabaseConfig
from invoices.core.config import database


def create_app(config: DatabaseConfig | None = None) -> Starlette:
    """Create and configure the Starlette application instance."""
    app = Starlette(routes=routes)

    configure_extensions(app, config or database)
    configure_errors(app)

    return app


def configure_extensions(app: Starlette, config: DatabaseConfig):
    """Configure the application's extensions."""
    injections.init_app(app, config)


def configure_errors(app: Starlette):
    """Configure the application's errors."""
    for handler in handlers:
        app.add_exception_handler(handler.exc_class, handler)
