from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from faker import Faker

from bridge.cli.commands.users import create
from bridge.cli.commands.users import delete
from bridge.cli.commands.users import list_
from bridge.cli.commands.users import update
from bridge.cli.commands.users import users
from bridge.domain.users.models.user import User

fake = Faker()


class TestUsersGroup:
    """Tests for the users command group."""

    def test_users_group_exists(self):
        """Test that users command group exists."""
        runner = CliRunner()
        result = runner.invoke(users, ["--help"])

        assert result.exit_code == 0
        assert "Manage bridge users" in result.output


class TestCreateUserCommand:
    """Tests for create user command."""

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    @patch("bridge.cli.commands.users.PostgresUserStorage")
    @patch("bridge.cli.commands.users.CreateUserHandler")
    def test_create_user_success(
        self, mock_handler_class, mock_storage_class, mock_get_connection, mock_get_engine
    ):
        """Test successful user creation."""
        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_storage = Mock()
        mock_handler = AsyncMock()
        mock_user = User(email="test@example.com", first_name="Test", last_name="User")

        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None
        mock_storage_class.return_value = mock_storage
        mock_handler_class.return_value = mock_handler
        mock_handler.handle.return_value = mock_user

        runner = CliRunner()
        result = runner.invoke(
            create, ["--email", "test@example.com", "--first-name", "Test", "--last-name", "User"]
        )

        assert result.exit_code == 0
        assert "User test@example.com created with ID:" in result.output
        mock_handler.handle.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_engine.dispose.assert_called_once()

    def test_create_user_missing_email(self):
        """Test create user command with missing email."""
        runner = CliRunner()
        result = runner.invoke(create, ["--first-name", "Test", "--last-name", "User"])

        assert result.exit_code != 0
        assert "Missing option" in result.output

    def test_create_user_missing_first_name(self):
        """Test create user command with missing first name."""
        runner = CliRunner()
        result = runner.invoke(create, ["--email", "test@example.com", "--last-name", "User"])

        assert result.exit_code != 0
        assert "Missing option" in result.output

    def test_create_user_missing_last_name(self):
        """Test create user command with missing last name."""
        runner = CliRunner()
        result = runner.invoke(create, ["--email", "test@example.com", "--first-name", "Test"])

        assert result.exit_code != 0
        assert "Missing option" in result.output


class TestListUsersCommand:
    """Tests for list users command."""

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    @patch("bridge.cli.commands.users.PostgresUserStorage")
    @patch("bridge.cli.commands.users.FetchAllUsersHandler")
    def test_list_users_success(
        self, mock_handler_class, mock_storage_class, mock_get_connection, mock_get_engine
    ):
        """Test successful user listing."""
        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_storage = Mock()
        mock_handler = AsyncMock()
        mock_users = [
            User(email="user1@example.com", first_name="User", last_name="One"),
            User(email="user2@example.com", first_name="User", last_name="Two"),
        ]

        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None
        mock_storage_class.return_value = mock_storage
        mock_handler_class.return_value = mock_handler
        mock_handler.handle.return_value = mock_users

        runner = CliRunner()
        result = runner.invoke(list_, [])

        assert result.exit_code == 0
        assert "user1@example.com" in result.output
        assert "user2@example.com" in result.output
        assert "User" in result.output
        assert "One" in result.output
        assert "User" in result.output
        assert "Two" in result.output
        mock_handler.handle.assert_called_once()
        mock_engine.dispose.assert_called_once()

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    @patch("bridge.cli.commands.users.PostgresUserStorage")
    @patch("bridge.cli.commands.users.FetchAllUsersHandler")
    def test_list_users_empty(
        self, mock_handler_class, mock_storage_class, mock_get_connection, mock_get_engine
    ):
        """Test listing when no users exist."""
        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_storage = Mock()
        mock_handler = AsyncMock()

        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None
        mock_storage_class.return_value = mock_storage
        mock_handler_class.return_value = mock_handler
        mock_handler.handle.return_value = []

        runner = CliRunner()
        result = runner.invoke(list_, [])

        assert result.exit_code == 0
        assert "No users found." in result.output
        mock_engine.dispose.assert_called_once()

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    @patch("bridge.cli.commands.users.PostgresUserStorage")
    @patch("bridge.cli.commands.users.FetchAllUsersHandler")
    def test_list_users_with_pagination(
        self, mock_handler_class, mock_storage_class, mock_get_connection, mock_get_engine
    ):
        """Test listing users with custom pagination."""
        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_storage = Mock()
        mock_handler = AsyncMock()
        mock_users = [User(email="user@example.com", first_name="User", last_name="Test")]

        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None
        mock_storage_class.return_value = mock_storage
        mock_handler_class.return_value = mock_handler
        mock_handler.handle.return_value = mock_users

        runner = CliRunner()
        result = runner.invoke(list_, ["--limit", "5", "--offset", "10"])

        assert result.exit_code == 0
        call_args = mock_handler.handle.call_args[0][0]
        assert call_args.limit == 5
        assert call_args.offset == 10


class TestUpdateUserCommand:
    """Tests for update user command."""

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    @patch("bridge.cli.commands.users.PostgresUserStorage")
    @patch("bridge.cli.commands.users.UpdateUserHandler")
    def test_update_user_success(
        self, mock_handler_class, mock_storage_class, mock_get_connection, mock_get_engine
    ):
        """Test successful user update."""
        # Setup mocks
        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_storage = Mock()
        mock_handler = AsyncMock()
        mock_user = User(email="test@example.com", first_name="Updated", last_name="User")

        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None
        mock_storage_class.return_value = mock_storage
        mock_handler_class.return_value = mock_handler
        mock_handler.handle.return_value = mock_user

        runner = CliRunner()
        result = runner.invoke(update, ["test@example.com", "--first-name", "Updated"])

        assert result.exit_code == 0
        assert "User test@example.com updated successfully." in result.output
        mock_handler.handle.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_engine.dispose.assert_called_once()

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    @patch("bridge.cli.commands.users.PostgresUserStorage")
    @patch("bridge.cli.commands.users.UpdateUserHandler")
    def test_update_user_both_names(
        self, mock_handler_class, mock_storage_class, mock_get_connection, mock_get_engine
    ):
        """Test updating both first and last name."""
        # Setup mocks
        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_storage = Mock()
        mock_handler = AsyncMock()
        mock_user = User(email="test@example.com", first_name="New", last_name="Name")

        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None
        mock_storage_class.return_value = mock_storage
        mock_handler_class.return_value = mock_handler
        mock_handler.handle.return_value = mock_user

        runner = CliRunner()
        result = runner.invoke(
            update, ["test@example.com", "--first-name", "New", "--last-name", "Name"]
        )

        assert result.exit_code == 0
        # Verify the command was called with correct parameters
        call_args = mock_handler.handle.call_args[0][0]
        assert call_args.email == "test@example.com"
        assert call_args.first_name == "New"
        assert call_args.last_name == "Name"

    def test_update_user_missing_email(self):
        """Test update user command with missing email argument."""
        runner = CliRunner()
        result = runner.invoke(update, ["--first-name", "Test"])

        assert result.exit_code != 0
        assert "Missing argument" in result.output


class TestDeleteUserCommand:
    """Tests for delete user command."""

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    @patch("bridge.cli.commands.users.PostgresUserStorage")
    @patch("bridge.cli.commands.users.DeleteUserHandler")
    def test_delete_user_success(
        self, mock_handler_class, mock_storage_class, mock_get_connection, mock_get_engine
    ):
        """Test successful user deletion."""
        # Setup mocks
        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_storage = Mock()
        mock_handler = AsyncMock()

        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None
        mock_storage_class.return_value = mock_storage
        mock_handler_class.return_value = mock_handler

        runner = CliRunner()
        result = runner.invoke(delete, ["test@example.com"])

        assert result.exit_code == 0
        assert "User test@example.com deleted." in result.output
        mock_handler.handle.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_engine.dispose.assert_called_once()

        # Verify the command was called with correct email
        call_args = mock_handler.handle.call_args[0][0]
        assert call_args.email == "test@example.com"

    def test_delete_user_missing_email(self):
        """Test delete user command with missing email argument."""
        runner = CliRunner()
        result = runner.invoke(delete, [])

        assert result.exit_code != 0
        assert "Missing argument" in result.output


class TestWithAsyncDatabaseConnectionDecorator:
    """Tests for the with_async_database_connection decorator."""

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    def test_decorator_provides_connection(self, mock_get_connection, mock_get_engine):
        """Test that decorator provides connection to decorated function."""
        from bridge.cli.commands.users import with_async_database_connection

        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None

        # Create a test function
        test_func = AsyncMock()
        decorated_func = with_async_database_connection(test_func)

        # Call the decorated function
        decorated_func("arg1", "arg2", kwarg1="value1")

        # Verify the async function was called with connection as first arg
        test_func.assert_called_once_with(mock_conn, "arg1", "arg2", kwarg1="value1")
        mock_engine.dispose.assert_called_once()

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    def test_decorator_disposes_engine(self, mock_get_connection, mock_get_engine):
        """Test that decorator disposes engine after function execution."""
        from bridge.cli.commands.users import with_async_database_connection

        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None

        test_func = AsyncMock()
        decorated_func = with_async_database_connection(test_func)

        decorated_func()

        mock_engine.dispose.assert_called_once()

    @patch("bridge.cli.commands.users.get_async_engine")
    @patch("bridge.cli.commands.users.get_connection")
    def test_decorator_disposes_engine_on_exception(self, mock_get_connection, mock_get_engine):
        """Test that decorator disposes engine even when function raises exception."""
        from bridge.cli.commands.users import with_async_database_connection

        mock_engine = AsyncMock()
        mock_conn = AsyncMock()
        mock_get_engine.return_value = mock_engine
        mock_get_connection.return_value.__aenter__.return_value = mock_conn
        mock_get_connection.return_value.__aexit__.return_value = None

        # Create a function that raises an exception
        async def failing_func(conn):
            raise ValueError("Test exception")

        decorated_func = with_async_database_connection(failing_func)

        with pytest.raises(ValueError, match="Test exception"):
            decorated_func()

        # Engine should still be disposed
        mock_engine.dispose.assert_called_once()
