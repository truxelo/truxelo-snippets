from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from bridge.database.tables.users import users
from bridge.domain.users.models.user import User
from bridge.domain.users.storages.interface import UserStorage


class PostgresUserStorage(UserStorage):
    """Postgres implementation of the UserStorage interface."""

    def __init__(self, connection: AsyncConnection):
        self._connection = connection

    async def insert(self, user: User):
        stmt = insert(users).values(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        await self._connection.execute(stmt)

    async def update(self, user: User):
        stmt = (
            update(users)
            .where(users.c.id == user.id)
            .values(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )
        )
        await self._connection.execute(stmt)

    async def fetch_by(self, email: str) -> User | None:
        stmt = select(users).where(users.c.email == email)
        result = await self._connection.execute(stmt)
        row = result.fetchone()

        if row is None:
            return None

        return User(
            id_=row.id,
            email=row.email,
            first_name=row.first_name,
            last_name=row.last_name,
        )

    async def fetch_all(self, limit: int, offset: int) -> list[User]:
        stmt = select(users).limit(limit).offset(offset).order_by(users.c.created_at)
        result = await self._connection.execute(stmt)
        rows = result.fetchall()

        return [
            User(
                id_=row.id,
                email=row.email,
                first_name=row.first_name,
                last_name=row.last_name,
            )
            for row in rows
        ]

    async def delete(self, user: User):
        stmt = delete(users).where(users.c.id == user.id)
        await self._connection.execute(stmt)
