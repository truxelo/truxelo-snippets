import pytest
from faker import Faker

from bridge.domain.users.models.user import User
from bridge.domain.users.services.delete_user import DeleteUser
from bridge.domain.users.services.delete_user import DeleteUserHandler
from bridge.domain.users.storages.in_memory import InMemoryUserStorage

fake = Faker()


class TestDeleteUser:
    """Tests for DeleteUser command."""

    def test_create_command_with_email(self):
        """Test creating DeleteUser command with email."""
        email = fake.email()

        command = DeleteUser(email=email)

        assert command.email == email

    def test_create_command_with_empty_email(self):
        """Test creating DeleteUser command with empty email."""
        command = DeleteUser(email="")

        assert command.email == ""

    def test_create_command_dataclass_equality(self):
        """Test that commands with same data are equal."""
        email = fake.email()

        command1 = DeleteUser(email=email)
        command2 = DeleteUser(email=email)

        assert command1 == command2

    def test_create_command_dataclass_inequality(self):
        """Test that commands with different data are not equal."""
        command1 = DeleteUser(email="user1@example.com")
        command2 = DeleteUser(email="user2@example.com")

        assert command1 != command2


class TestDeleteUserHandler:
    """Tests for DeleteUserHandler."""

    @pytest.fixture
    def handler_with_users(self, sample_users):
        """Provides a DeleteUserHandler with sample users in storage."""
        storage = InMemoryUserStorage(*sample_users)
        return DeleteUserHandler(storage)

    @pytest.fixture
    def handler(self):
        """Provides a DeleteUserHandler with empty storage."""
        storage = InMemoryUserStorage()
        return DeleteUserHandler(storage)

    def test_handler_initialization(self):
        """Test creating handler with storage."""
        storage = InMemoryUserStorage()
        handler = DeleteUserHandler(storage)

        assert handler.users == storage

    @pytest.mark.asyncio
    async def test_handle_delete_existing_user(self, handler_with_users, sample_users):
        """Test deleting an existing user."""
        target_user = sample_users[0]
        initial_count = len(handler_with_users.users.items)

        command = DeleteUser(email=target_user.email)
        deleted_user = await handler_with_users.handle(command)

        assert deleted_user == target_user
        assert len(handler_with_users.users.items) == initial_count - 1
        assert target_user not in handler_with_users.users.items

    @pytest.mark.asyncio
    async def test_handle_delete_user_not_found(self, handler):
        """Test deleting nonexistent user raises RuntimeError."""
        command = DeleteUser(email="nonexistent@example.com")

        with pytest.raises(RuntimeError, match="User not found"):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_handle_delete_user_not_found_with_users(self, handler_with_users):
        """Test deleting nonexistent user with existing users raises RuntimeError."""
        command = DeleteUser(email="notfound@example.com")

        with pytest.raises(RuntimeError, match="User not found"):
            await handler_with_users.handle(command)

    @pytest.mark.asyncio
    async def test_handle_returns_deleted_user(self, handler_with_users, sample_users):
        """Test that handler returns the deleted user instance."""
        target_user = sample_users[0]
        command = DeleteUser(email=target_user.email)

        returned_user = await handler_with_users.handle(command)

        assert returned_user == target_user

    @pytest.mark.asyncio
    async def test_handle_removes_from_storage(self, handler_with_users, sample_users):
        """Test that delete removes user from storage."""
        target_user = sample_users[0]
        command = DeleteUser(email=target_user.email)

        await handler_with_users.handle(command)

        remaining_user = await handler_with_users.users.fetch_by(target_user.email)
        assert remaining_user is None

    @pytest.mark.asyncio
    async def test_handle_delete_preserves_other_users(self, handler_with_users, sample_users):
        """Test that deleting one user preserves others."""
        target_user = sample_users[0]
        other_users = sample_users[1:]
        command = DeleteUser(email=target_user.email)

        await handler_with_users.handle(command)

        for user in other_users:
            stored_user = await handler_with_users.users.fetch_by(user.email)
            assert stored_user == user

    @pytest.mark.asyncio
    async def test_handle_delete_only_matching_user(self, handler_with_users, sample_users):
        """Test that only the user with matching email is deleted."""
        target_user = sample_users[0]
        initial_count = len(handler_with_users.users.items)
        command = DeleteUser(email=target_user.email)

        await handler_with_users.handle(command)

        assert len(handler_with_users.users.items) == initial_count - 1
        for user in handler_with_users.users.items:
            assert user.email != target_user.email

    @pytest.mark.asyncio
    async def test_handle_delete_with_special_email_characters(self, handler_with_users):
        """Test deleting user with special characters in email."""
        special_user = User(
            email="user+tag@sub-domain.co.uk",
            first_name="Special",
            last_name="User",
        )

        await handler_with_users.users.insert(special_user)

        command = DeleteUser(email=special_user.email)
        deleted_user = await handler_with_users.handle(command)

        assert deleted_user == special_user
        assert special_user not in handler_with_users.users.items

    @pytest.mark.asyncio
    async def test_handle_delete_case_sensitive_email(self, handler_with_users):
        """Test that email matching is case sensitive."""
        test_user = User(email="Test@Example.com", first_name="Test", last_name="User")
        await handler_with_users.users.insert(test_user)

        command = DeleteUser(email="test@example.com")
        with pytest.raises(RuntimeError, match="User not found"):
            await handler_with_users.handle(command)

        stored_user = await handler_with_users.users.fetch_by("Test@Example.com")
        assert stored_user == test_user

    @pytest.mark.asyncio
    async def test_handle_multiple_deletes_same_email(self, handler_with_users, sample_users):
        """Test that deleting same user twice raises error on second attempt."""
        target_user = sample_users[0]
        command = DeleteUser(email=target_user.email)

        await handler_with_users.handle(command)
        with pytest.raises(RuntimeError, match="User not found"):
            await handler_with_users.handle(command)

    @pytest.mark.asyncio
    async def test_handle_delete_single_user_empties_storage(self):
        """Test deleting the only user empties the storage."""
        single_user = User(email="only@example.com", first_name="Only", last_name="User")
        storage = InMemoryUserStorage(single_user)
        handler = DeleteUserHandler(storage)

        command = DeleteUser(email=single_user.email)
        await handler.handle(command)

        assert len(storage.items) == 0

    @pytest.mark.asyncio
    async def test_handle_preserves_user_data_in_return(self, handler_with_users, sample_users):
        """Test that returned deleted user preserves all original data."""
        target_user = sample_users[0]
        original_id = target_user.id
        original_email = target_user.email
        original_first_name = target_user.first_name
        original_last_name = target_user.last_name

        command = DeleteUser(email=target_user.email)
        deleted_user = await handler_with_users.handle(command)

        assert deleted_user.id == original_id
        assert deleted_user.email == original_email
        assert deleted_user.first_name == original_first_name
        assert deleted_user.last_name == original_last_name
