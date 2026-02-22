"""
Sistema de gestión de salón de peluquería.
"""
from app.models import (
    Empleado,
    TipoServicio,
    ServicioRegistrado,
    ServicioDetalle,
    DesglosePago
)
from app.result import Ok, Err, Result
from app.errors import (
    ValidationError,
    NotFoundError,
    DuplicateError,
    PersistenceError
)

__all__ = [
    # Models
    "Empleado",
    "TipoServicio",
    "ServicioRegistrado",
    "ServicioDetalle",
    "DesglosePago",
    # Result types
    "Ok",
    "Err",
    "Result",
    # Error types
    "ValidationError",
    "NotFoundError",
    "DuplicateError",
    "PersistenceError",
]
