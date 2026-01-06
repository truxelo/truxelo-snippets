import pytest
from faker import Faker

from bridge.domain.users.models.user import User
from bridge.domain.users.services.fetch_all_users import FetchAllUsers
from bridge.domain.users.services.fetch_all_users import FetchAllUsersHandler
from bridge.domain.users.storages.in_memory import InMemoryUserStorage

fake = Faker()


class TestFetchAllUsers:
    """Tests for FetchAllUsers query."""

    def test_create_query_with_limit_and_offset(self):
        """Test creating FetchAllUsers query with limit and offset."""
        limit = 10
        offset = 5

        query = FetchAllUsers(limit=limit, offset=offset)

        assert query.limit == limit
        assert query.offset == offset

    def test_create_query_with_zero_values(self):
        """Test creating query with zero limit and offset."""
        query = FetchAllUsers(limit=0, offset=0)

        assert query.limit == 0
        assert query.offset == 0

    def test_create_query_with_large_values(self):
        """Test creating query with large values."""
        query = FetchAllUsers(limit=1000, offset=5000)

        assert query.limit == 1000
        assert query.offset == 5000

    def test_query_dataclass_equality(self):
        """Test that queries with same data are equal."""
        query1 = FetchAllUsers(limit=10, offset=5)
        query2 = FetchAllUsers(limit=10, offset=5)

        assert query1 == query2

    def test_query_dataclass_inequality(self):
        """Test that queries with different data are not equal."""
        query1 = FetchAllUsers(limit=10, offset=5)
        query2 = FetchAllUsers(limit=20, offset=5)

        assert query1 != query2


class TestFetchAllUsersHandler:
    """Tests for FetchAllUsersHandler."""

    @pytest.fixture
    def handler(self):
        """Provides a FetchAllUsersHandler with empty storage."""
        storage = InMemoryUserStorage()
        return FetchAllUsersHandler(storage)

    @pytest.fixture
    def handler_with_users(self, sample_users):
        """Provides a FetchAllUsersHandler with sample users."""
        storage = InMemoryUserStorage(*sample_users)
        return FetchAllUsersHandler(storage)

    def test_handler_initialization(self):
        """Test creating handler with storage."""
        storage = InMemoryUserStorage()
        handler = FetchAllUsersHandler(storage)

        assert handler.users == storage

    @pytest.mark.asyncio
    async def test_handle_empty_storage(self, handler):
        """Test fetching from empty storage."""
        query = FetchAllUsers(limit=10, offset=0)

        users = await handler.handle(query)

        assert isinstance(users, list)
        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_handle_fetch_all_users_no_pagination(self, handler_with_users, sample_users):
        """Test fetching all users without pagination."""
        query = FetchAllUsers(limit=100, offset=0)

        users = await handler_with_users.handle(query)

        assert len(users) == len(sample_users)
        for user in sample_users:
            assert user in users

    @pytest.mark.asyncio
    async def test_handle_with_limit(self, handler_with_users):
        """Test fetching users with limit."""
        query = FetchAllUsers(limit=2, offset=0)

        users = await handler_with_users.handle(query)

        assert len(users) == 2

    @pytest.mark.asyncio
    async def test_handle_with_offset(self, handler_with_users, sample_users):
        """Test fetching users with offset."""
        query = FetchAllUsers(limit=100, offset=2)

        users = await handler_with_users.handle(query)

        expected_count = len(sample_users) - 2
        assert len(users) == expected_count

    @pytest.mark.asyncio
    async def test_handle_with_limit_and_offset(self, handler_with_users):
        """Test fetching users with both limit and offset."""
        query = FetchAllUsers(limit=2, offset=1)

        users = await handler_with_users.handle(query)

        assert len(users) == 2

    @pytest.mark.asyncio
    async def test_handle_limit_larger_than_available(self, handler_with_users, sample_users):
        """Test fetching with limit larger than available users."""
        query = FetchAllUsers(limit=100, offset=0)

        users = await handler_with_users.handle(query)

        assert len(users) == len(sample_users)

    @pytest.mark.asyncio
    async def test_handle_offset_larger_than_available(self, handler_with_users):
        """Test fetching with offset larger than available users."""
        query = FetchAllUsers(limit=10, offset=100)

        users = await handler_with_users.handle(query)

        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_handle_zero_limit(self, handler_with_users):
        """Test fetching with zero limit."""
        query = FetchAllUsers(limit=0, offset=0)

        users = await handler_with_users.handle(query)

        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_handle_returns_user_objects(self, handler_with_users):
        """Test that handler returns actual User objects."""
        query = FetchAllUsers(limit=10, offset=0)

        users = await handler_with_users.handle(query)

        for user in users:
            assert isinstance(user, User)
            assert hasattr(user, "id")
            assert hasattr(user, "email")
            assert hasattr(user, "first_name")
            assert hasattr(user, "last_name")

    @pytest.mark.asyncio
    async def test_handle_pagination_sequence(self, handler_with_users, sample_users):
        """Test paginating through all users in sequence."""
        page_size = 2
        all_fetched_users = []

        offset = 0
        while True:
            query = FetchAllUsers(limit=page_size, offset=offset)
            users = await handler_with_users.handle(query)

            if not users:
                break

            all_fetched_users.extend(users)
            offset += page_size

        assert len(all_fetched_users) == len(sample_users)
        for user in sample_users:
            assert user in all_fetched_users

    @pytest.mark.asyncio
    async def test_handle_with_single_user(self):
        """Test fetching from storage with single user."""
        user = User(email="single@example.com", first_name="Single", last_name="User")
        storage = InMemoryUserStorage(user)
        handler = FetchAllUsersHandler(storage)
        query = FetchAllUsers(limit=10, offset=0)

        users = await handler.handle(query)

        assert len(users) == 1
        assert users[0] == user

    @pytest.mark.asyncio
    async def test_handle_preserves_user_data_integrity(self, handler_with_users, sample_users):
        """Test that fetched users maintain their data integrity."""
        query = FetchAllUsers(limit=10, offset=0)

        users = await handler_with_users.handle(query)

        for user in users:
            original = next(u for u in sample_users if u.id == user.id)
            assert user.email == original.email
            assert user.first_name == original.first_name
            assert user.last_name == original.last_name
