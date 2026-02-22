"""
Pruebas unitarias para los tipos de error.
"""
import pytest

from app.errors import (
    ValidationError,
    NotFoundError,
    DuplicateError,
    PersistenceError
)


class TestValidationError:
    """Pruebas para ValidationError."""
    
    def test_crear_validation_error_con_campo(self):
        """Verifica que se puede crear un error de validación con campo."""
        error = ValidationError(
            message="El porcentaje debe estar entre 0 y 100",
            field="porcentaje_comision"
        )
        assert error.message == "El porcentaje debe estar entre 0 y 100"
        assert error.field == "porcentaje_comision"
    
    def test_crear_validation_error_sin_campo(self):
        """Verifica que se puede crear un error de validación sin campo."""
        error = ValidationError(message="Datos inválidos")
        assert error.message == "Datos inválidos"
        assert error.field is None


class TestNotFoundError:
    """Pruebas para NotFoundError."""
    
    def test_crear_not_found_error(self):
        """Verifica que se puede crear un error de no encontrado."""
        error = NotFoundError(entity="Empleado", identifier="E001")
        assert error.entity == "Empleado"
        assert error.identifier == "E001"


class TestDuplicateError:
    """Pruebas para DuplicateError."""
    
    def test_crear_duplicate_error(self):
        """Verifica que se puede crear un error de duplicado."""
        error = DuplicateError(entity="Empleado", identifier="E001")
        assert error.entity == "Empleado"
        assert error.identifier == "E001"


class TestPersistenceError:
    """Pruebas para PersistenceError."""
    
    def test_crear_persistence_error_con_contexto(self):
        """Verifica que se puede crear un error de persistencia con contexto."""
        error = PersistenceError(
            message="Error al guardar en la base de datos",
            context="SQLAlchemy"
        )
        assert error.message == "Error al guardar en la base de datos"
        assert error.context == "SQLAlchemy"
    
    def test_crear_persistence_error_sin_contexto(self):
        """Verifica que se puede crear un error de persistencia sin contexto."""
        error = PersistenceError(message="Error de persistencia")
        assert error.message == "Error de persistencia"
        assert error.context is None
