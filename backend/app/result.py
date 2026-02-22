"""
Patrón Result para manejo de errores funcional.
"""
from dataclasses import dataclass
from typing import TypeVar, Generic, Union


T = TypeVar('T')
E = TypeVar('E')


@dataclass
class Ok(Generic[T]):
    """Representa un resultado exitoso."""
    value: T


@dataclass
class Err(Generic[E]):
    """Representa un resultado con error."""
    error: E


# Type alias para Result
Result = Union[Ok[T], Err[E]]
