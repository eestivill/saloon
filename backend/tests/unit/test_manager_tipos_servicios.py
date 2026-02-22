"""
Pruebas unitarias para la gestión de tipos de servicios en SalonManager.
"""
import pytest
from app.manager import SalonManager
from app.repository import SQLAlchemyRepository
from app.result import Ok, Err
from app.errors import ValidationError, DuplicateError, NotFoundError


@pytest.fixture
def manager():
    """Fixture que proporciona un SalonManager con base de datos en memoria."""
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    return SalonManager(repository)


def test_crear_tipo_servicio_exitoso_con_porcentaje_valido(manager):
    """Probar creación exitosa con porcentaje válido."""
    resultado = manager.crear_tipo_servicio(
        "Corte Básico",
        "Corte de cabello estándar",
        40.0
    )
    
    assert isinstance(resultado, Ok)
    tipo = resultado.value
    assert tipo.nombre == "Corte Básico"
    assert tipo.descripcion == "Corte de cabello estándar"
    assert tipo.porcentaje_comision == 40.0


def test_crear_tipo_servicio_con_porcentaje_fuera_de_rango_retorna_error(manager):
    """Probar error con porcentaje fuera de rango."""
    # Porcentaje mayor a 100
    resultado = manager.crear_tipo_servicio(
        "Servicio Test",
        "Descripción",
        150.0
    )
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, ValidationError)
    
    # Porcentaje negativo
    resultado = manager.crear_tipo_servicio(
        "Servicio Test",
        "Descripción",
        -10.0
    )
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, ValidationError)


def test_crear_tipo_servicio_con_nombre_duplicado_retorna_error(manager):
    """Probar error con nombre duplicado."""
    # Crear primer tipo de servicio
    manager.crear_tipo_servicio("Corte", "Descripción 1", 40.0)
    
    # Intentar crear segundo tipo con mismo nombre
    resultado = manager.crear_tipo_servicio("Corte", "Descripción 2", 50.0)
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, DuplicateError)
    assert resultado.error.entity == "TipoServicio"
    assert resultado.error.identifier == "Corte"


def test_obtener_tipo_servicio_existente(manager):
    """Probar obtención de tipo de servicio existente."""
    manager.crear_tipo_servicio("Tinte", "Tinte completo", 35.0)
    
    tipo = manager.obtener_tipo_servicio("Tinte")
    
    assert tipo is not None
    assert tipo.nombre == "Tinte"
    assert tipo.descripcion == "Tinte completo"
    assert tipo.porcentaje_comision == 35.0


def test_obtener_tipo_servicio_inexistente_retorna_none(manager):
    """Probar que obtener tipo de servicio inexistente retorna None."""
    tipo = manager.obtener_tipo_servicio("NOEXISTE")
    
    assert tipo is None


def test_listar_tipos_servicios_vacio(manager):
    """Probar lista vacía cuando no hay tipos de servicios."""
    tipos = manager.listar_tipos_servicios()
    
    assert tipos == []
    assert len(tipos) == 0


def test_listar_tipos_servicios_con_multiples(manager):
    """Probar listar múltiples tipos de servicios."""
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    manager.crear_tipo_servicio("Tinte", "Tinte completo", 35.0)
    manager.crear_tipo_servicio("Peinado", "Peinado especial", 30.0)
    
    tipos = manager.listar_tipos_servicios()
    
    assert len(tipos) == 3
    nombres = {tipo.nombre for tipo in tipos}
    assert nombres == {"Corte", "Tinte", "Peinado"}


def test_actualizar_tipo_servicio_porcentaje(manager):
    """Probar actualización de porcentaje."""
    # Crear tipo de servicio
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Actualizar porcentaje
    resultado = manager.actualizar_tipo_servicio("Corte", 45.0)
    
    assert isinstance(resultado, Ok)
    tipo_actualizado = resultado.value
    assert tipo_actualizado.nombre == "Corte"
    assert tipo_actualizado.porcentaje_comision == 45.0
    assert tipo_actualizado.descripcion == "Corte básico"  # Descripción se preserva
    
    # Verificar que se actualizó en el repositorio
    tipo_recuperado = manager.obtener_tipo_servicio("Corte")
    assert tipo_recuperado.porcentaje_comision == 45.0


def test_actualizar_tipo_servicio_con_porcentaje_invalido_retorna_error(manager):
    """Probar error al actualizar con porcentaje inválido."""
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Intentar actualizar con porcentaje mayor a 100
    resultado = manager.actualizar_tipo_servicio("Corte", 150.0)
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, ValidationError)
    
    # Verificar que no se actualizó
    tipo = manager.obtener_tipo_servicio("Corte")
    assert tipo.porcentaje_comision == 40.0


def test_actualizar_tipo_servicio_inexistente_retorna_error(manager):
    """Probar error al actualizar tipo de servicio inexistente."""
    resultado = manager.actualizar_tipo_servicio("NOEXISTE", 50.0)
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, NotFoundError)
    assert resultado.error.entity == "TipoServicio"
    assert resultado.error.identifier == "NOEXISTE"


def test_actualizar_tipo_servicio_preserva_nombre_y_descripcion(manager):
    """Probar que actualizar preserva nombre y descripción."""
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    resultado = manager.actualizar_tipo_servicio("Corte", 50.0)
    
    assert isinstance(resultado, Ok)
    tipo = resultado.value
    assert tipo.nombre == "Corte"
    assert tipo.descripcion == "Corte básico"
    
    # Verificar que solo hay un tipo de servicio
    tipos = manager.listar_tipos_servicios()
    assert len(tipos) == 1


def test_crear_tipo_servicio_con_porcentaje_en_limites(manager):
    """Probar creación con porcentajes en los límites válidos."""
    # Porcentaje 0
    resultado = manager.crear_tipo_servicio("Servicio Gratis", "Sin comisión", 0.0)
    assert isinstance(resultado, Ok)
    assert resultado.value.porcentaje_comision == 0.0
    
    # Porcentaje 100
    resultado = manager.crear_tipo_servicio("Servicio Premium", "Comisión completa", 100.0)
    assert isinstance(resultado, Ok)
    assert resultado.value.porcentaje_comision == 100.0
