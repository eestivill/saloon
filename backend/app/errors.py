"""
Tipos de error para el sistema de gestión de salón de peluquería.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationError:
    """Error de validación de datos."""
    message: str
    field: Optional[str] = None


@dataclass
class NotFoundError:
    """Error cuando una entidad no se encuentra."""
    entity: str
    identifier: str


@dataclass
class DuplicateError:
    """Error cuando se intenta crear una entidad con identificador duplicado."""
    entity: str
    identifier: str


@dataclass
class PersistenceError:
    """Error durante operaciones de persistencia."""
    message: str
    context: Optional[str] = None
