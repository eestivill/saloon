"""
Pruebas unitarias para la gestión de empleados en SalonManager.
"""
import pytest
from app.manager import SalonManager
from app.repository import SQLAlchemyRepository
from app.result import Ok, Err
from app.errors import DuplicateError, NotFoundError


@pytest.fixture
def manager():
    """Fixture que proporciona un SalonManager con base de datos en memoria."""
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    return SalonManager(repository)


def test_crear_empleado_exitoso(manager):
    """Probar creación exitosa de empleado."""
    resultado = manager.crear_empleado("E001", "Juan Pérez")
    
    assert isinstance(resultado, Ok)
    empleado = resultado.value
    assert empleado.id == "E001"
    assert empleado.nombre == "Juan Pérez"


def test_crear_empleado_con_id_duplicado_retorna_error(manager):
    """Probar error al crear empleado con ID duplicado."""
    # Crear primer empleado
    manager.crear_empleado("E001", "Juan Pérez")
    
    # Intentar crear segundo empleado con mismo ID
    resultado = manager.crear_empleado("E001", "María García")
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, DuplicateError)
    assert resultado.error.entity == "Empleado"
    assert resultado.error.identifier == "E001"


def test_obtener_empleado_existente(manager):
    """Probar obtención de empleado existente."""
    manager.crear_empleado("E001", "Juan Pérez")
    
    empleado = manager.obtener_empleado("E001")
    
    assert empleado is not None
    assert empleado.id == "E001"
    assert empleado.nombre == "Juan Pérez"


def test_obtener_empleado_inexistente_retorna_none(manager):
    """Probar que obtener empleado inexistente retorna None."""
    empleado = manager.obtener_empleado("NOEXISTE")
    
    assert empleado is None


def test_listar_empleados_vacio(manager):
    """Probar lista vacía cuando no hay empleados."""
    empleados = manager.listar_empleados()
    
    assert empleados == []
    assert len(empleados) == 0


def test_listar_empleados_con_multiples(manager):
    """Probar listar múltiples empleados."""
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_empleado("E002", "María García")
    manager.crear_empleado("E003", "Pedro López")
    
    empleados = manager.listar_empleados()
    
    assert len(empleados) == 3
    ids = {emp.id for emp in empleados}
    assert ids == {"E001", "E002", "E003"}


def test_actualizar_empleado_existente(manager):
    """Probar actualización de empleado existente."""
    # Crear empleado
    manager.crear_empleado("E001", "Juan Pérez")
    
    # Actualizar nombre
    resultado = manager.actualizar_empleado("E001", "Juan Carlos Pérez")
    
    assert isinstance(resultado, Ok)
    empleado_actualizado = resultado.value
    assert empleado_actualizado.id == "E001"
    assert empleado_actualizado.nombre == "Juan Carlos Pérez"
    
    # Verificar que se actualizó en el repositorio
    empleado_recuperado = manager.obtener_empleado("E001")
    assert empleado_recuperado.nombre == "Juan Carlos Pérez"


def test_actualizar_empleado_preserva_id(manager):
    """Probar que actualizar empleado preserva su ID."""
    manager.crear_empleado("E001", "Juan Pérez")
    
    resultado = manager.actualizar_empleado("E001", "Nuevo Nombre")
    
    assert isinstance(resultado, Ok)
    assert resultado.value.id == "E001"
    
    # Verificar que solo hay un empleado
    empleados = manager.listar_empleados()
    assert len(empleados) == 1


def test_actualizar_empleado_inexistente_retorna_error(manager):
    """Probar error al actualizar empleado inexistente."""
    resultado = manager.actualizar_empleado("NOEXISTE", "Nombre")
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, NotFoundError)
    assert resultado.error.entity == "Empleado"
    assert resultado.error.identifier == "NOEXISTE"
