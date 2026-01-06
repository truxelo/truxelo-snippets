from click import Group

from bridge.cli.commands.database import database
from bridge.cli.commands.users import users


def create_app() -> Group:
    """Create a cli entrypoint."""
    app = Group("bridge")
    configure_commands(app)
    return app


def configure_commands(app: Group):
    """Configure the application's commands."""
    app.add_command(database)
    app.add_command(users)
