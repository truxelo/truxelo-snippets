import asyncio
from functools import wraps

import click
from sqlalchemy.ext.asyncio import AsyncConnection
from tabulate import tabulate

from bridge.config import database
from bridge.database.core import get_async_engine
from bridge.database.core import get_connection
from bridge.database.storages.user import PostgresUserStorage
from bridge.domain.users.services.create_user import CreateUser
from bridge.domain.users.services.create_user import CreateUserHandler
from bridge.domain.users.services.delete_user import DeleteUser
from bridge.domain.users.services.delete_user import DeleteUserHandler
from bridge.domain.users.services.fetch_all_users import FetchAllUsers
from bridge.domain.users.services.fetch_all_users import FetchAllUsersHandler
from bridge.domain.users.services.update_user import UpdateUser
from bridge.domain.users.services.update_user import UpdateUserHandler


def with_async_database_connection(function):
    """Decorator that provides an async database connection to CLI commands."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        async def _run():
            engine = await get_async_engine(database)
            try:
                async with get_connection(engine) as conn:
                    return await function(conn, *args, **kwargs)
            finally:
                await engine.dispose()

        return asyncio.run(_run())

    return wrapper


@click.group()
def users():
    """Manage bridge users."""


@users.command()
@click.option("--email", required=True, help="User email address")
@click.option("--first-name", required=True, help="User first name")
@click.option("--last-name", required=True, help="User last name")
@with_async_database_connection
async def create(conn: AsyncConnection, email: str, first_name: str, last_name: str):
    """Create a new user in the system."""

    storage = PostgresUserStorage(conn)
    handler = CreateUserHandler(storage)

    command = CreateUser(email=email, first_name=first_name, last_name=last_name)
    user = await handler.handle(command)
    await conn.commit()

    click.echo(f"User {user.email} created with ID: {user.id}")


@users.command(name="list")
@click.option("--limit", default=10, help="Number of users to fetch.")
@click.option("--offset", default=0, help="Number of users to skip.")
@with_async_database_connection
async def list_(conn: AsyncConnection, limit: int, offset: int):
    """List all users from the system."""

    storage = PostgresUserStorage(conn)
    handler = FetchAllUsersHandler(storage)

    query = FetchAllUsers(limit=limit, offset=offset)
    users = await handler.handle(query)
    if not users:
        click.echo("No users found.")
        return

    table_data = [[str(u.id), u.email, u.first_name, u.last_name] for u in users]
    headers = ["User ID", "Email", "First Name", "Last Name"]
    click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))


@users.command()
@click.argument("email", type=str)
@click.option("--first-name", help="New first name.")
@click.option("--last-name", help="New last name.")
@with_async_database_connection
async def update(conn: AsyncConnection, email: str, first_name: str | None, last_name: str | None):
    """Update an existing user from the system."""
    storage = PostgresUserStorage(conn)
    handler = UpdateUserHandler(storage)

    command = UpdateUser(email=email, first_name=first_name, last_name=last_name)
    user = await handler.handle(command)
    await conn.commit()

    click.echo(f"User {user.email} updated successfully.")


@users.command()
@click.argument("email", type=str)
@with_async_database_connection
async def delete(conn: AsyncConnection, email: str):
    """Delete a user from the system."""
    storage = PostgresUserStorage(conn)
    handler = DeleteUserHandler(storage)

    command = DeleteUser(email=email)
    await handler.handle(command)
    await conn.commit()

    click.echo(f"User {email} deleted.")
