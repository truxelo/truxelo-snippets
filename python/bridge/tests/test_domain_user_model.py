from uuid import UUID
from uuid import uuid4

from faker import Faker

from bridge.domain.users.models.user import User

fake = Faker()


class TestUser:
    """Tests for User domain model."""

    def test_create_user_with_all_fields(self):
        """Test creating a user with all required fields."""
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()
        user_id = uuid4()

        user = User(email=email, first_name=first_name, last_name=last_name, id_=user_id)

        assert user.id == user_id
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name

    def test_create_user_without_id_generates_uuid(self):
        """Test creating a user without ID generates a UUID automatically."""
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()

        user = User(email=email, first_name=first_name, last_name=last_name)

        assert isinstance(user.id, UUID)
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name

    def test_create_multiple_users_have_different_ids(self):
        """Test that multiple users created without explicit IDs have different IDs."""
        user1 = User(email="user1@example.com", first_name="John", last_name="Doe")
        user2 = User(email="user2@example.com", first_name="Jane", last_name="Smith")

        assert user1.id != user2.id

    def test_user_with_empty_strings(self):
        """Test creating a user with empty string values."""
        user = User(email="", first_name="", last_name="")

        assert isinstance(user.id, UUID)
        assert user.email == ""
        assert user.first_name == ""
        assert user.last_name == ""

    def test_user_dataclass_equality(self):
        """Test that users with same data are equal."""
        user_id = uuid4()
        email = fake.email()
        first_name = fake.first_name()
        last_name = fake.last_name()

        user1 = User(email=email, first_name=first_name, last_name=last_name, id_=user_id)
        user2 = User(email=email, first_name=first_name, last_name=last_name, id_=user_id)

        assert user1 == user2

    def test_user_dataclass_inequality(self):
        """Test that users with different data are not equal."""
        user1 = User(email="user1@example.com", first_name="John", last_name="Doe")
        user2 = User(email="user2@example.com", first_name="Jane", last_name="Smith")

        assert user1 != user2

    def test_user_repr(self):
        """Test string representation of user."""
        user_id = uuid4()
        user = User(email="test@example.com", first_name="Test", last_name="User", id_=user_id)

        repr_str = repr(user)
        assert "User(" in repr_str
        assert "test@example.com" in repr_str
        assert "Test" in repr_str
        assert "User" in repr_str
        assert str(user_id) in repr_str
