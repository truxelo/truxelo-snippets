import click
from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError

config = Config()
config.set_main_option("script_location", "invoices:database:migrations")
config.set_main_option("file_template", "%%(year)d%%(month).2d%%(day).2d_%%(rev)s")


@click.group()
def database():
    """Wrapper around alembic database migrations"""


@database.command()
@click.argument("revision", required=True)
@click.option(
    "--sql",
    is_flag=True,
    help="Don't emit SQL to postgres, dump to standard output.",
)
def downgrade(revision, sql):  # pylint: disable=redefined-outer-name
    """Revert to a previous version"""
    try:
        command.downgrade(config, revision, sql)
    except CommandError as error:
        click.echo(str(error))


@database.command()
@click.option(
    "-m",
    "--message",
    help="Message string to use with revision.",
)
@click.option(
    "--autogenerate",
    is_flag=True,
    help=(
        "Populate revision script with candidate migration operations, "
        "based on comparison of postgres to model."
    ),
)
def revision(message, autogenerate):
    """Create a new revision"""
    try:
        command.revision(config, message=message, autogenerate=autogenerate)
    except CommandError as error:
        click.echo(str(error))


@database.command()
@click.argument("revision")
@click.option(
    "--sql",
    is_flag=True,
    help="Don't emit SQL to postgres, dump to standard output.",
)
def upgrade(revision, sql):  # pylint: disable=redefined-outer-name
    """Upgrade to a later version"""
    try:
        command.upgrade(config, revision, sql)
    except CommandError as error:
        click.echo(str(error))


@database.command()
def current():
    """Show the current revision."""
    try:
        command.current(config)
    except CommandError as error:
        click.echo(str(error))


@database.command()
@click.option("-r", "--rev-range", help="Specify revision range.")
@click.option("-i", "--indicate-current", is_flag=True, help="Indicate the current revision.")
def history(rev_range, indicate_current):
    """List changeset scripts in chronological order."""
    try:
        command.history(config, rev_range=rev_range, indicate_current=indicate_current)
    except CommandError as error:
        click.echo(str(error))
