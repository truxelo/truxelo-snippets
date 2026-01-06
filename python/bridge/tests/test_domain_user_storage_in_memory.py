import pytest

from bridge.domain.users.models.user import User
from bridge.domain.users.storages.in_memory import InMemoryUserStorage


class TestInMemoryUserStorage:
    """Tests for InMemoryUserStorage class."""

    @pytest.fixture
    def empty_storage(self):
        """Provides an empty in-memory storage."""
        return InMemoryUserStorage()

    @pytest.fixture
    def storage_with_users(self, sample_users):
        """Provides an in-memory storage with sample users."""
        return InMemoryUserStorage(*sample_users)

    def test_create_empty_storage(self, empty_storage):
        """Test creating empty storage."""
        assert len(empty_storage.items) == 0

    def test_create_storage_with_users(self, sample_users):
        """Test creating storage with initial users."""
        storage = InMemoryUserStorage(*sample_users)
        assert len(storage.items) == len(sample_users)

    @pytest.mark.asyncio
    async def test_insert_user(self, empty_storage, sample_user):
        """Test inserting a user."""
        await empty_storage.insert(sample_user)
        assert sample_user in empty_storage.items
        assert len(empty_storage.items) == 1

    @pytest.mark.asyncio
    async def test_insert_multiple_users(self, empty_storage, sample_users):
        """Test inserting multiple users."""
        for user in sample_users:
            await empty_storage.insert(user)

        assert len(empty_storage.items) == len(sample_users)
        for user in sample_users:
            assert user in empty_storage.items

    @pytest.mark.asyncio
    async def test_update_existing_user(self, storage_with_users, sample_users):
        """Test updating an existing user."""
        user_to_update = sample_users[0]
        user_to_update.first_name = "Updated"

        await storage_with_users.update(user_to_update)

        updated_user = await storage_with_users.fetch_by(user_to_update.email)
        assert updated_user.first_name == "Updated"

    @pytest.mark.asyncio
    async def test_update_nonexistent_user(self, empty_storage, sample_user):
        """Test updating a user that doesn't exist adds it."""
        await empty_storage.update(sample_user)
        assert sample_user in empty_storage.items

    @pytest.mark.asyncio
    async def test_fetch_by_existing_email(self, storage_with_users, sample_users):
        """Test fetching user by existing email."""
        target_user = sample_users[0]
        found_user = await storage_with_users.fetch_by(target_user.email)

        assert found_user == target_user

    @pytest.mark.asyncio
    async def test_fetch_by_nonexistent_email(self, storage_with_users):
        """Test fetching user by nonexistent email returns None."""
        found_user = await storage_with_users.fetch_by("nonexistent@example.com")
        assert found_user is None

    @pytest.mark.asyncio
    async def test_fetch_all_no_pagination(self, storage_with_users, sample_users):
        """Test fetching all users without pagination."""
        users = await storage_with_users.fetch_all(limit=10, offset=0)

        assert len(users) == len(sample_users)
        for user in sample_users:
            assert user in users

    @pytest.mark.asyncio
    async def test_fetch_all_with_limit(self, storage_with_users):
        """Test fetching users with limit."""
        users = await storage_with_users.fetch_all(limit=2, offset=0)
        assert len(users) == 2

    @pytest.mark.asyncio
    async def test_fetch_all_with_offset(self, storage_with_users, sample_users):
        """Test fetching users with offset."""
        users = await storage_with_users.fetch_all(limit=10, offset=2)
        expected_users = sample_users[2:]

        assert len(users) == len(expected_users)
        for user in expected_users:
            assert user in users

    @pytest.mark.asyncio
    async def test_fetch_all_with_limit_and_offset(self, storage_with_users, sample_users):
        """Test fetching users with both limit and offset."""
        users = await storage_with_users.fetch_all(limit=2, offset=1)
        expected_users = sample_users[1:3]

        assert len(users) == len(expected_users)
        for user in expected_users:
            assert user in users

    @pytest.mark.asyncio
    async def test_fetch_all_empty_storage(self, empty_storage):
        """Test fetching from empty storage."""
        users = await empty_storage.fetch_all(limit=10, offset=0)
        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_delete_existing_user(self, storage_with_users, sample_users):
        """Test deleting an existing user."""
        user_to_delete = sample_users[0]
        initial_count = len(storage_with_users.items)

        await storage_with_users.delete(user_to_delete)

        assert len(storage_with_users.items) == initial_count - 1
        assert user_to_delete not in storage_with_users.items

    @pytest.mark.asyncio
    async def test_delete_nonexistent_user(self, empty_storage, sample_user):
        """Test deleting a nonexistent user doesn't raise error."""
        await empty_storage.delete(sample_user)  # Should not raise
        assert len(empty_storage.items) == 0

    @pytest.mark.asyncio
    async def test_delete_user_not_in_storage(self, storage_with_users):
        """Test deleting a user not in storage."""
        new_user = User(email="new@example.com", first_name="New", last_name="User")
        initial_count = len(storage_with_users.items)

        await storage_with_users.delete(new_user)

        assert len(storage_with_users.items) == initial_count

    def test_items_property_returns_list(self, storage_with_users, sample_users):
        """Test that items property returns a list."""
        items = storage_with_users.items

        assert isinstance(items, list)
        assert len(items) == len(sample_users)

    def test_storage_isolation(self):
        """Test that different storage instances are isolated."""
        user1 = User(email="user1@example.com", first_name="User", last_name="One")
        user2 = User(email="user2@example.com", first_name="User", last_name="Two")

        storage1 = InMemoryUserStorage(user1)
        storage2 = InMemoryUserStorage(user2)

        assert len(storage1.items) == 1
        assert len(storage2.items) == 1
        assert user1 in storage1.items
        assert user1 not in storage2.items
        assert user2 in storage2.items
        assert user2 not in storage1.items
