from click import Group

from invoices.apps.cli.commands.database import database


def create_app() -> Group:
    """Create a cli entrypoint."""
    app = Group("invoices")
    configure_commands(app)
    return app


def configure_commands(app: Group):
    """Configure the application's commands."""
    app.add_command(database)
