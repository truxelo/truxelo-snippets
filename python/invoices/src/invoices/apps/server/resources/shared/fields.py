from typing import Annotated
from typing import Any
from uuid import UUID

from pydantic import AfterValidator
from pydantic import PlainSerializer


def validate_uuid_version(version: int):
    """Generates a validator for a specific UUID version."""

    def validator(value: Any) -> UUID:
        if isinstance(value, str):
            value = UUID(value)
        if not isinstance(value, UUID):
            raise ValueError("Invalid UUID format")
        if value.version != version:
            raise ValueError(f"UUID must be version {version}, found version {value.version}")
        return value

    return validator


serialize_uuid = PlainSerializer(str, return_type=str)


UUID7 = Annotated[  # pylint: disable=invalid-name
    UUID, AfterValidator(validate_uuid_version(7)), serialize_uuid
]
