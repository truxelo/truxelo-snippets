from uuid import UUID

import pytest
from faker import Faker

from bridge.domain.users.models.user import User
from bridge.domain.users.services.create_user import CreateUser
from bridge.domain.users.services.create_user import CreateUserHandler
from bridge.domain.users.storages.in_memory import InMemoryUserStorage

fake = Faker()


class TestCreateUser:
    """Tests for CreateUser command."""

    def test_create_command_with_all_fields(self):
        """Test creating CreateUser command with all fields."""
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()

        command = CreateUser(email=email, first_name=first_name, last_name=last_name)

        assert command.email == email
        assert command.first_name == first_name
        assert command.last_name == last_name

    def test_create_command_dataclass_equality(self):
        """Test that commands with same data are equal."""
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()

        command1 = CreateUser(email=email, first_name=first_name, last_name=last_name)
        command2 = CreateUser(email=email, first_name=first_name, last_name=last_name)

        assert command1 == command2

    def test_create_command_with_empty_strings(self):
        """Test creating command with empty string values."""
        command = CreateUser(email="", first_name="", last_name="")

        assert command.email == ""
        assert command.first_name == ""
        assert command.last_name == ""


class TestCreateUserHandler:
    """Tests for CreateUserHandler."""

    @pytest.fixture
    def handler(self):
        """Provides a CreateUserHandler with in-memory storage."""
        storage = InMemoryUserStorage()
        return CreateUserHandler(storage)

    @pytest.fixture
    def handler_with_users(self, sample_users):
        """Provides a CreateUserHandler with existing users in storage."""
        storage = InMemoryUserStorage(*sample_users)
        return CreateUserHandler(storage)

    def test_handler_initialization(self):
        """Test creating handler with storage."""
        storage = InMemoryUserStorage()
        handler = CreateUserHandler(storage)

        assert handler.users == storage

    @pytest.mark.asyncio
    async def test_handle_creates_user(self, handler):
        """Test that handler creates and stores a user."""
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()
        command = CreateUser(email=email, first_name=first_name, last_name=last_name)

        user = await handler.handle(command)

        assert isinstance(user, User)
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user in handler.users.items

    @pytest.mark.asyncio
    async def test_handle_generates_user_id(self, handler):
        """Test that handler generates a UUID for new user."""
        command = CreateUser(email="test@example.com", first_name="Test", last_name="User")

        user = await handler.handle(command)

        assert user.id is not None
        assert isinstance(user.id, UUID)

    @pytest.mark.asyncio
    async def test_handle_multiple_users_have_different_ids(self, handler):
        """Test that multiple users created have different IDs."""
        command1 = CreateUser(email="user1@example.com", first_name="User", last_name="One")
        command2 = CreateUser(email="user2@example.com", first_name="User", last_name="Two")

        user1 = await handler.handle(command1)
        user2 = await handler.handle(command2)

        assert user1.id != user2.id

    @pytest.mark.asyncio
    async def test_handle_adds_user_to_storage(self, handler):
        """Test that handler adds user to storage."""
        initial_count = len(handler.users.items)
        command = CreateUser(email="new@example.com", first_name="New", last_name="User")

        await handler.handle(command)

        assert len(handler.users.items) == initial_count + 1

    @pytest.mark.asyncio
    async def test_handle_with_existing_users(self, handler_with_users):
        """Test creating user when storage already has users."""
        initial_count = len(handler_with_users.users.items)
        command = CreateUser(email="new@example.com", first_name="New", last_name="User")

        user = await handler_with_users.handle(command)

        assert len(handler_with_users.users.items) == initial_count + 1
        assert user in handler_with_users.users.items

    @pytest.mark.asyncio
    async def test_handle_returns_created_user(self, handler):
        """Test that handler returns the created user instance."""
        command = CreateUser(email="return@example.com", first_name="Return", last_name="Test")

        returned_user = await handler.handle(command)
        stored_users = handler.users.items

        assert returned_user in stored_users
        assert returned_user.email == command.email

    @pytest.mark.asyncio
    async def test_handle_with_special_characters(self, handler):
        """Test creating user with special characters in name."""
        command = CreateUser(
            email="special@example.com",
            first_name="José-François",
            last_name="O'Connor-Smith",
        )

        user = await handler.handle(command)

        assert user.first_name == "José-François"
        assert user.last_name == "O'Connor-Smith"
        assert user in handler.users.items

    @pytest.mark.asyncio
    async def test_handle_preserves_command_data(self, handler):
        """Test that user data exactly matches command data."""
        email = "preserve@example.com"
        first_name = "Preserve"
        last_name = "Data"
        command = CreateUser(email=email, first_name=first_name, last_name=last_name)

        user = await handler.handle(command)

        assert user.email == command.email
        assert user.first_name == command.first_name
        assert user.last_name == command.last_name
