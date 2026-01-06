import pytest
from faker import Faker

from bridge.domain.users.services.update_user import UpdateUser
from bridge.domain.users.services.update_user import UpdateUserHandler
from bridge.domain.users.storages.in_memory import InMemoryUserStorage

fake = Faker()


class TestUpdateUser:
    """Tests for UpdateUser command."""

    def test_create_command_with_all_fields(self):
        """Test creating UpdateUser command with all fields."""
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()

        command = UpdateUser(email=email, first_name=first_name, last_name=last_name)

        assert command.email == email
        assert command.first_name == first_name
        assert command.last_name == last_name

    def test_create_command_with_none_values(self):
        """Test creating UpdateUser command with None values."""
        email = fake.email()

        command = UpdateUser(email=email, first_name=None, last_name=None)

        assert command.email == email
        assert command.first_name is None
        assert command.last_name is None

    def test_create_command_partial_update(self):
        """Test creating command for partial update."""
        email = fake.email()
        first_name = fake.first_name()

        command = UpdateUser(email=email, first_name=first_name, last_name=None)

        assert command.email == email
        assert command.first_name == first_name
        assert command.last_name is None

    def test_create_command_dataclass_equality(self):
        """Test that commands with same data are equal."""
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()

        command1 = UpdateUser(email=email, first_name=first_name, last_name=last_name)
        command2 = UpdateUser(email=email, first_name=first_name, last_name=last_name)

        assert command1 == command2


class TestUpdateUserHandler:
    """Tests for UpdateUserHandler."""

    @pytest.fixture
    def handler_with_users(self, sample_users):
        """Provides an UpdateUserHandler with sample users in storage."""
        storage = InMemoryUserStorage(*sample_users)
        return UpdateUserHandler(storage)

    @pytest.fixture
    def handler(self):
        """Provides an UpdateUserHandler with empty storage."""
        storage = InMemoryUserStorage()
        return UpdateUserHandler(storage)

    def test_handler_initialization(self):
        """Test creating handler with storage."""
        storage = InMemoryUserStorage()
        handler = UpdateUserHandler(storage)

        assert handler.users == storage

    @pytest.mark.asyncio
    async def test_handle_update_both_names(self, handler_with_users, sample_users):
        """Test updating both first and last name."""
        target_user = sample_users[0]
        new_first_name = "UpdatedFirst"
        new_last_name = "UpdatedLast"

        command = UpdateUser(
            email=target_user.email, first_name=new_first_name, last_name=new_last_name
        )
        updated_user = await handler_with_users.handle(command)

        assert updated_user.first_name == new_first_name
        assert updated_user.last_name == new_last_name
        assert updated_user.email == target_user.email
        assert updated_user.id == target_user.id

    @pytest.mark.asyncio
    async def test_handle_update_first_name_only(self, handler_with_users, sample_users):
        """Test updating only first name."""
        target_user = sample_users[0]
        original_last_name = target_user.last_name
        new_first_name = "UpdatedFirst"

        command = UpdateUser(email=target_user.email, first_name=new_first_name, last_name=None)
        updated_user = await handler_with_users.handle(command)

        assert updated_user.first_name == new_first_name
        assert updated_user.last_name == original_last_name
        assert updated_user.email == target_user.email

    @pytest.mark.asyncio
    async def test_handle_update_last_name_only(self, handler_with_users, sample_users):
        """Test updating only last name."""
        target_user = sample_users[0]
        original_first_name = target_user.first_name
        new_last_name = "UpdatedLast"

        command = UpdateUser(email=target_user.email, first_name=None, last_name=new_last_name)
        updated_user = await handler_with_users.handle(command)

        assert updated_user.first_name == original_first_name
        assert updated_user.last_name == new_last_name
        assert updated_user.email == target_user.email

    @pytest.mark.asyncio
    async def test_handle_update_no_changes(self, handler_with_users, sample_users):
        """Test updating with no actual changes."""
        target_user = sample_users[0]

        command = UpdateUser(email=target_user.email, first_name=None, last_name=None)
        updated_user = await handler_with_users.handle(command)

        assert updated_user.first_name == target_user.first_name
        assert updated_user.last_name == target_user.last_name
        assert updated_user.email == target_user.email

    @pytest.mark.asyncio
    async def test_handle_user_not_found(self, handler):
        """Test updating nonexistent user raises RuntimeError."""
        command = UpdateUser(email="nonexistent@example.com", first_name="New", last_name="Name")

        with pytest.raises(RuntimeError, match="User not found"):
            await handler.handle(command)

    @pytest.mark.asyncio
    async def test_handle_user_not_found_with_users(self, handler_with_users):
        """Test updating nonexistent user with existing users raises RuntimeError."""
        command = UpdateUser(email="notfound@example.com", first_name="New", last_name="Name")

        with pytest.raises(RuntimeError, match="User not found"):
            await handler_with_users.handle(command)

    @pytest.mark.asyncio
    async def test_handle_updates_storage(self, handler_with_users, sample_users):
        """Test that update persists to storage."""
        target_user = sample_users[0]
        new_first_name = "PersistTest"

        command = UpdateUser(email=target_user.email, first_name=new_first_name, last_name=None)
        await handler_with_users.handle(command)

        stored_user = await handler_with_users.users.fetch_by(target_user.email)
        assert stored_user.first_name == new_first_name

    @pytest.mark.asyncio
    async def test_handle_returns_updated_user(self, handler_with_users, sample_users):
        """Test that handler returns the updated user instance."""
        target_user = sample_users[0]
        new_last_name = "ReturnTest"

        command = UpdateUser(email=target_user.email, first_name=None, last_name=new_last_name)
        returned_user = await handler_with_users.handle(command)

        assert returned_user.last_name == new_last_name
        assert returned_user.id == target_user.id

    @pytest.mark.asyncio
    async def test_handle_with_special_characters(self, handler_with_users, sample_users):
        """Test updating with special characters in names."""
        target_user = sample_users[0]

        command = UpdateUser(
            email=target_user.email,
            first_name="José-François",
            last_name="O'Connor-Smith",
        )
        updated_user = await handler_with_users.handle(command)

        assert updated_user.first_name == "José-François"
        assert updated_user.last_name == "O'Connor-Smith"

    @pytest.mark.asyncio
    async def test_handle_with_empty_strings(self, handler_with_users, sample_users):
        """Test updating with empty string values."""
        target_user = sample_users[0]

        command = UpdateUser(email=target_user.email, first_name="", last_name="")
        updated_user = await handler_with_users.handle(command)

        assert updated_user.first_name == ""
        assert updated_user.last_name == ""

    @pytest.mark.asyncio
    async def test_handle_preserves_user_id_and_email(self, handler_with_users, sample_users):
        """Test that update preserves user ID and email."""
        target_user = sample_users[0]
        original_id = target_user.id
        original_email = target_user.email

        command = UpdateUser(email=target_user.email, first_name="NewFirst", last_name="NewLast")
        updated_user = await handler_with_users.handle(command)

        assert updated_user.id == original_id
        assert updated_user.email == original_email

    @pytest.mark.asyncio
    async def test_handle_multiple_updates_same_user(self, handler_with_users, sample_users):
        """Test multiple sequential updates to same user."""
        target_user = sample_users[0]

        command1 = UpdateUser(email=target_user.email, first_name="First", last_name=None)
        await handler_with_users.handle(command1)

        command2 = UpdateUser(email=target_user.email, first_name=None, last_name="Second")
        updated_user2 = await handler_with_users.handle(command2)

        assert updated_user2.first_name == "First"
        assert updated_user2.last_name == "Second"
        assert updated_user2.id == target_user.id
