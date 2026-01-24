from __future__ import annotations

from functools import partial
from typing import Callable
from typing import Iterable
from typing import Type
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic.root_model import RootModel

from invoices.core.utils import Case
from invoices.core.utils import force_case

L = TypeVar("L", bound="ListComponent")
C = TypeVar("C", bound="Component")
M = TypeVar("M")
N = TypeVar("N")


def _shared_defaults(**kwargs):
    """Set default kwargs for `model_dump` and `model_dump_json`."""
    kwargs.setdefault("exclude_unset", True)
    kwargs.setdefault("by_alias", True)
    kwargs.setdefault("mode", "json")
    return kwargs


class Component(BaseModel):
    """Base component class with camelCase field naming and strict validation."""

    model_config = ConfigDict(
        alias_generator=partial(force_case, case=Case.CAMEL),
        validate_default=True,
        populate_by_name=True,
        use_enum_values=False,
        extra="forbid",
        frozen=True,
    )

    def model_dump(self, *args, **kwargs):
        """Override to always set exclude_unset=True by default."""
        kwargs = _shared_defaults(**kwargs)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        """Override to always set exclude_unset=True by default."""
        kwargs = _shared_defaults(**kwargs)
        return super().model_dump_json(*args, **kwargs)


class ListComponent(RootModel[list[C]]):
    """List of components of type T."""

    @classmethod
    def from_iterable(cls: Type[L], iterable: Iterable[C]) -> L:
        """Create a list component from an iterable of components."""
        return cls(root=list(iterable))

    @classmethod
    def mapped(cls: Type[L], mapper: Callable[[M], C], iterable: Iterable[M]) -> L:
        """Create a list component by mapping items through a mapper function."""
        return cls(root=[mapper(item) for item in iterable])

    def model_dump(self, *args, **kwargs):
        """Override to always set exclude_unset=True by default."""
        kwargs = _shared_defaults(**kwargs)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        """Override to always set exclude_unset=True by default."""
        kwargs = _shared_defaults(**kwargs)
        return super().model_dump_json(*args, **kwargs)


class QueryParams(BaseModel):
    """Base query params class with snake_case field naming and lax validation."""

    model_config = ConfigDict(
        alias_generator=partial(force_case, case=Case.SNAKE),
        validate_default=True,
        populate_by_name=True,
        use_enum_values=False,
        extra="ignore",
        frozen=True,
    )
