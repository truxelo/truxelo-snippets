from __future__ import annotations

import inspect
from http import HTTPStatus
from json.decoder import JSONDecodeError
from typing import Callable
from typing import Generic
from typing import TypeVar
from typing import get_type_hints

from pydantic import ValidationError as PydanticValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response

from invoices.apps.server.resources.errors.components import Error
from invoices.apps.server.resources.errors.components import ErrorKind
from invoices.apps.server.resources.errors.components import ExceptionDetails
from invoices.apps.server.resources.errors.components import ParsingErrorDetails
from invoices.apps.server.resources.errors.components import ValidationErrorDetails

E = TypeVar("E", bound=Exception)
ErrorHandler = Callable[[E], Error]


class ExceptionHandler(Generic[E]):
    """Handles a specific exception type and returns a serialized error response."""

    _exc_class: type[E]
    _handler: ErrorHandler

    def __init__(self, exc_class: type[E], handler: ErrorHandler):
        self._exc_class = exc_class
        self._handler = handler

    async def __call__(self, request: Request, exc: E) -> Response:
        """Handles the exception and returns a JSON error response."""
        error = self._handler(exc)
        return JSONResponse(
            error.model_dump(by_alias=True, exclude_none=True),
            status_code=error.status,
        )

    @property
    def exc_class(self) -> type[E]:
        """Expose the inner exception class"""
        return self._exc_class


handlers: list[ExceptionHandler] = []


def _register(func: ErrorHandler) -> ErrorHandler:
    """Decorator that registers a typed exception handler based on its argument type."""
    signature = inspect.signature(func)
    exc_type = get_type_hints(func).get(next(iter(signature.parameters)))

    if not exc_type or not issubclass(exc_type, Exception):
        raise TypeError(f"Cannot determine exception type for handler: {func.__name__}")

    handlers.append(ExceptionHandler(exc_type, func))
    return func


@_register
def pydantic_validation_error(exc: PydanticValidationError) -> Error:
    """Returns an error response from a pydantic.ValidationError."""
    return Error(
        code="EV-422",
        message="input validation failure",
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
        exception=None,
        details=ValidationErrorDetails.from_pydantic_error(exc),
        kind=ErrorKind.VALIDATION,
    )


@_register
def json_decode_error(exc: JSONDecodeError) -> Error:
    """Returns an error response from a JSONDecodeError."""
    return Error(
        code="EH-400",
        message="invalid json body",
        status=HTTPStatus.BAD_REQUEST,
        exception=ExceptionDetails.from_exception(exc),
        details=ParsingErrorDetails.from_json_decode_error(exc),
        kind=ErrorKind.VALIDATION,
    )


@_register
def http_exception(exc: HTTPException) -> Error:
    """Returns an error response from a HTTPException."""
    return Error(
        code=f"EH-{exc.status_code}",
        message=exc.detail.lower(),
        status=exc.status_code,
        exception=None,
        details=None,
        kind=ErrorKind.from_http_exception(exc),
    )


@_register
def all_exception(exc: Exception) -> Error:
    """Returns an error response from a Exception."""
    return Error(
        code="EH-500",
        message="internal server error",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
        exception=ExceptionDetails.from_exception(exc),
        details=None,
        kind=ErrorKind.INTERNAL,
    )
