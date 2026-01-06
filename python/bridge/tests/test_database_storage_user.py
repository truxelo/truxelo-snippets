import pytest
from faker import Faker

from bridge.database.storages.user import PostgresUserStorage
from bridge.domain.users.models.user import User

fake = Faker()


class TestPostgresUserStorage:
    """Tests for PostgresUserStorage class."""

    @pytest.mark.asyncio
    async def test_insert_user(self, postgres_user_storage, sample_user):
        """Test inserting a user."""
        await postgres_user_storage.insert(sample_user)

        stored_user = await postgres_user_storage.fetch_by(sample_user.email)

        assert stored_user is not None
        assert stored_user.email == sample_user.email
        assert stored_user.first_name == sample_user.first_name
        assert stored_user.last_name == sample_user.last_name
        assert stored_user.id == sample_user.id

    @pytest.mark.asyncio
    async def test_insert_multiple_users(self, postgres_user_storage, sample_users):
        """Test inserting multiple users."""
        for user in sample_users:
            await postgres_user_storage.insert(user)

        for user in sample_users:
            stored_user = await postgres_user_storage.fetch_by(user.email)
            assert stored_user is not None
            assert stored_user == user

    @pytest.mark.asyncio
    async def test_fetch_by_existing_email(self, postgres_user_storage, sample_user):
        """Test fetching user by existing email."""
        await postgres_user_storage.insert(sample_user)

        found_user = await postgres_user_storage.fetch_by(sample_user.email)

        assert found_user is not None
        assert found_user.email == sample_user.email
        assert found_user.first_name == sample_user.first_name
        assert found_user.last_name == sample_user.last_name
        assert found_user.id == sample_user.id

    @pytest.mark.asyncio
    async def test_fetch_by_nonexistent_email(self, postgres_user_storage):
        """Test fetching user by nonexistent email returns None."""
        found_user = await postgres_user_storage.fetch_by("nonexistent@example.com")
        assert found_user is None

    @pytest.mark.asyncio
    async def test_fetch_by_case_sensitive_email(self, postgres_user_storage):
        """Test that email matching is case sensitive."""
        user = User(email="Test@Example.com", first_name="Test", last_name="User")
        await postgres_user_storage.insert(user)

        # exact match should work
        found_user = await postgres_user_storage.fetch_by("Test@Example.com")
        assert found_user is not None

        # different case should not match
        not_found = await postgres_user_storage.fetch_by("test@example.com")
        assert not_found is None

    @pytest.mark.asyncio
    async def test_update_existing_user(self, postgres_user_storage, sample_user):
        """Test updating an existing user."""
        await postgres_user_storage.insert(sample_user)

        # modify user data
        sample_user.first_name = "UpdatedFirst"
        sample_user.last_name = "UpdatedLast"

        await postgres_user_storage.update(sample_user)

        # verify update persisted
        updated_user = await postgres_user_storage.fetch_by(sample_user.email)
        assert updated_user.first_name == "UpdatedFirst"
        assert updated_user.last_name == "UpdatedLast"
        assert updated_user.id == sample_user.id
        assert updated_user.email == sample_user.email

    @pytest.mark.asyncio
    async def test_update_nonexistent_user(self, postgres_user_storage, sample_user):
        """Test updating a nonexistent user (should not raise error)."""
        # this should not raise an error, just not update anything
        await postgres_user_storage.update(sample_user)

        # verify user was not created
        found_user = await postgres_user_storage.fetch_by(sample_user.email)
        assert found_user is None

    @pytest.mark.asyncio
    async def test_fetch_all_empty_storage(self, postgres_user_storage):
        """Test fetching from empty storage."""
        users = await postgres_user_storage.fetch_all(limit=10, offset=0)
        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_fetch_all_with_users(self, postgres_user_storage, sample_users):
        """Test fetching all users."""
        for user in sample_users:
            await postgres_user_storage.insert(user)

        users = await postgres_user_storage.fetch_all(limit=10, offset=0)

        assert len(users) == len(sample_users)
        for user in sample_users:
            assert any(u.email == user.email for u in users)

    @pytest.mark.asyncio
    async def test_fetch_all_with_limit(self, postgres_user_storage, sample_users):
        """Test fetching users with limit."""
        for user in sample_users:
            await postgres_user_storage.insert(user)

        users = await postgres_user_storage.fetch_all(limit=2, offset=0)

        assert len(users) == 2

    @pytest.mark.asyncio
    async def test_fetch_all_with_offset(self, postgres_user_storage, sample_users):
        """Test fetching users with offset."""
        for user in sample_users:
            await postgres_user_storage.insert(user)

        users = await postgres_user_storage.fetch_all(limit=10, offset=2)

        expected_count = max(0, len(sample_users) - 2)
        assert len(users) == expected_count

    @pytest.mark.asyncio
    async def test_fetch_all_with_limit_and_offset(self, postgres_user_storage, sample_users):
        """Test fetching users with both limit and offset."""
        for user in sample_users:
            await postgres_user_storage.insert(user)

        users = await postgres_user_storage.fetch_all(limit=2, offset=1)

        assert len(users) <= 2

    @pytest.mark.asyncio
    async def test_fetch_all_ordered_by_created_at(self, postgres_user_storage):
        """Test that fetch_all returns users ordered by creation time."""
        user1 = User(email="first@example.com", first_name="First", last_name="User")
        user2 = User(email="second@example.com", first_name="Second", last_name="User")

        await postgres_user_storage.insert(user2)
        await postgres_user_storage.insert(user1)

        users = await postgres_user_storage.fetch_all(limit=10, offset=0)

        assert len(users) == 2
        assert users[0].email == user2.email
        assert users[1].email == user1.email

    @pytest.mark.asyncio
    async def test_delete_existing_user(self, postgres_user_storage, sample_user):
        """Test deleting an existing user."""
        await postgres_user_storage.insert(sample_user)

        found_user = await postgres_user_storage.fetch_by(sample_user.email)
        assert found_user is not None

        await postgres_user_storage.delete(sample_user)

        deleted_user = await postgres_user_storage.fetch_by(sample_user.email)
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_user(self, postgres_user_storage, sample_user):
        """Test deleting a nonexistent user (should not raise error)."""
        await postgres_user_storage.delete(sample_user)

        found_user = await postgres_user_storage.fetch_by(sample_user.email)
        assert found_user is None

    @pytest.mark.asyncio
    async def test_delete_preserves_other_users(self, postgres_user_storage, sample_users):
        """Test that deleting one user preserves others."""
        for user in sample_users:
            await postgres_user_storage.insert(user)

        user_to_delete = sample_users[0]
        await postgres_user_storage.delete(user_to_delete)

        deleted_user = await postgres_user_storage.fetch_by(user_to_delete.email)
        assert deleted_user is None

        for user in sample_users[1:]:
            found_user = await postgres_user_storage.fetch_by(user.email)
            assert found_user is not None
            assert found_user.email == user.email

    @pytest.mark.asyncio
    async def test_insert_duplicate_email_raises_error(self, postgres_user_storage):
        """Test that inserting duplicate email raises error."""
        user1 = User(email="duplicate@example.com", first_name="First", last_name="User")
        user2 = User(email="duplicate@example.com", first_name="Second", last_name="User")

        await postgres_user_storage.insert(user1)

        with pytest.raises(Exception):
            await postgres_user_storage.insert(user2)

    @pytest.mark.asyncio
    async def test_storage_isolation_with_connection(self, async_connection):
        """Test that storage instances with same connection share data."""
        storage1 = PostgresUserStorage(async_connection)
        storage2 = PostgresUserStorage(async_connection)
        user = User(email="shared@example.com", first_name="Shared", last_name="User")

        await storage1.insert(user)

        found_user = await storage2.fetch_by(user.email)
        assert found_user is not None
        assert found_user.email == user.email

    @pytest.mark.asyncio
    async def test_fetch_all_returns_user_objects(self, postgres_user_storage, sample_users):
        """Test that fetch_all returns proper User objects."""
        for user in sample_users:
            await postgres_user_storage.insert(user)

        users = await postgres_user_storage.fetch_all(limit=10, offset=0)

        for user in users:
            assert isinstance(user, User)
            assert hasattr(user, "id")
            assert hasattr(user, "email")
            assert hasattr(user, "first_name")
            assert hasattr(user, "last_name")

    @pytest.mark.asyncio
    async def test_user_data_integrity_after_operations(self, postgres_user_storage, sample_user):
        """Test that user data maintains integrity through all operations."""
        original_id = sample_user.id
        original_email = sample_user.email
        original_first_name = sample_user.first_name
        original_last_name = sample_user.last_name

        await postgres_user_storage.insert(sample_user)

        fetched_user = await postgres_user_storage.fetch_by(sample_user.email)
        assert fetched_user.id == original_id
        assert fetched_user.email == original_email
        assert fetched_user.first_name == original_first_name
        assert fetched_user.last_name == original_last_name

        fetched_user.first_name = "Updated"
        await postgres_user_storage.update(fetched_user)

        updated_user = await postgres_user_storage.fetch_by(sample_user.email)
        assert updated_user.id == original_id
        assert updated_user.email == original_email
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == original_last_name
