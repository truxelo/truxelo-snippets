from __future__ import annotations

from enum import StrEnum
from json.decoder import JSONDecodeError
from typing import Iterable

from pydantic import RootModel
from pydantic import ValidationError as PydanticValidationError
from starlette.exceptions import HTTPException

from invoices.apps.server.resources.shared.components import Component
from invoices.core.utils import Case
from invoices.core.utils import force_case


class ErrorKind(StrEnum):
    """Represents the possible kinds of errors."""

    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    FORBIDDEN = "forbidden"
    INTERNAL = "internal"
    NOT_FOUND = "not-found"
    UNKNOWN = "unknown"
    VALIDATION = "validation"

    @staticmethod
    def from_http_exception(exc: HTTPException) -> ErrorKind:
        """Convert an HTTPException into an ErrorKind."""
        match exc.status_code:
            case 401:
                return ErrorKind.AUTHENTICATION
            case 403:
                return ErrorKind.AUTHORIZATION
            case 404:
                return ErrorKind.NOT_FOUND
            case 409:
                return ErrorKind.FORBIDDEN
            case 422:
                return ErrorKind.VALIDATION
            case 500:
                return ErrorKind.INTERNAL
            case _:
                return ErrorKind.UNKNOWN


class ExceptionDetails(Component):
    """API component representing exception details."""

    class_: str  # class name, e.g., 'ValueError'
    message: str  # stringified exception message

    @staticmethod
    def from_exception(exc: Exception | None) -> ExceptionDetails | None:
        """Convert an Exception into an ExceptionDetails."""
        if not exc:
            return None
        cleaned = exc.__class__.__name__.replace("JSON", "Json")
        exc_class = force_case(cleaned, Case.KEBAB)
        return ExceptionDetails(class_=exc_class, message=str(exc).lower())


class ParsingErrorDetails(Component):
    """API component representing parsing error details."""

    line: int
    column: int
    position: int

    @staticmethod
    def from_json_decode_error(exc: JSONDecodeError) -> ParsingErrorDetails:
        """Convert a JSONDecodeError into a ParsingErrorDetails."""
        return ParsingErrorDetails(
            line=exc.lineno,
            column=exc.colno,
            position=exc.pos,
        )


class ValidationErrorItem(Component):
    """API component representing validation error item."""

    location: str
    message: str
    kind: str


class ValidationErrorDetails(RootModel[list[ValidationErrorItem]]):
    """API component representing validation error details."""

    @staticmethod
    def _stringify(location: Iterable[str | int]) -> str:
        """Stringify a location tuple into a dot-separated string."""

        def _clean(item: str | int) -> str:
            return force_case(str(item), Case.CAMEL)

        return ".".join(map(_clean, location))

    @staticmethod
    def from_pydantic_error(exception: PydanticValidationError) -> ValidationErrorDetails:
        """Convert a pydantic.ValidationError into a ValidationErrorDetails."""
        return ValidationErrorDetails(
            root=[
                ValidationErrorItem(
                    location=ValidationErrorDetails._stringify(error["loc"]),
                    message=error["msg"].lower(),
                    kind=error["type"].lower(),
                )
                for error in exception.errors()
            ]
        )


class Error(Component):
    """API component representing an error."""

    code: str
    message: str
    kind: ErrorKind
    status: int
    exception: ExceptionDetails | None
    details: ValidationErrorDetails | ParsingErrorDetails | None
