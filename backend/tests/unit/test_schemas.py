"""
Pruebas unitarias para los modelos Pydantic (schemas).
"""
import pytest
from datetime import date
from decimal import Decimal
from pydantic import ValidationError

from app.schemas import (
    EmpleadoCreate,
    EmpleadoUpdate,
    EmpleadoResponse,
    TipoServicioCreate,
    TipoServicioUpdate,
    TipoServicioResponse,
    ServicioCreate,
    ServicioResponse,
    IngresosResponse,
    BeneficiosResponse,
    ServicioDetalle,
    DesglosePagoResponse,
)


# ============================================================================
# TESTS PARA EMPLEADOS
# ============================================================================

def test_empleado_create_valido():
    """Prueba crear un empleado con datos válidos."""
    empleado = EmpleadoCreate(id="E001", nombre="Juan Pérez")
    assert empleado.id == "E001"
    assert empleado.nombre == "Juan Pérez"


def test_empleado_create_elimina_espacios():
    """Prueba que se eliminan espacios en blanco al inicio y final."""
    empleado = EmpleadoCreate(id="  E001  ", nombre="  Juan Pérez  ")
    assert empleado.id == "E001"
    assert empleado.nombre == "Juan Pérez"


def test_empleado_create_id_vacio_falla():
    """Prueba que un ID vacío falla la validación."""
    with pytest.raises(ValidationError) as exc_info:
        EmpleadoCreate(id="", nombre="Juan")
    assert "string_too_short" in str(exc_info.value) or "at least 1 character" in str(exc_info.value)


def test_empleado_create_id_solo_espacios_falla():
    """Prueba que un ID con solo espacios falla la validación."""
    with pytest.raises(ValidationError) as exc_info:
        EmpleadoCreate(id="   ", nombre="Juan")
    assert "no puede estar vacío" in str(exc_info.value)


def test_empleado_create_nombre_vacio_falla():
    """Prueba que un nombre vacío falla la validación."""
    with pytest.raises(ValidationError) as exc_info:
        EmpleadoCreate(id="E001", nombre="")
    assert "string_too_short" in str(exc_info.value) or "at least 1 character" in str(exc_info.value)


def test_empleado_create_nombre_solo_espacios_falla():
    """Prueba que un nombre con solo espacios falla la validación."""
    with pytest.raises(ValidationError) as exc_info:
        EmpleadoCreate(id="E001", nombre="   ")
    assert "no puede estar vacío" in str(exc_info.value)


def test_empleado_create_id_muy_largo_falla():
    """Prueba que un ID mayor a 50 caracteres falla."""
    with pytest.raises(ValidationError) as exc_info:
        EmpleadoCreate(id="E" * 51, nombre="Juan")
    assert "string_too_long" in str(exc_info.value) or "at most 50 characters" in str(exc_info.value)


def test_empleado_create_nombre_muy_largo_falla():
    """Prueba que un nombre mayor a 100 caracteres falla."""
    with pytest.raises(ValidationError) as exc_info:
        EmpleadoCreate(id="E001", nombre="J" * 101)
    assert "string_too_long" in str(exc_info.value) or "at most 100 characters" in str(exc_info.value)


def test_empleado_update_valido():
    """Prueba actualizar un empleado con datos válidos."""
    update = EmpleadoUpdate(nombre="María García")
    assert update.nombre == "María García"


def test_empleado_update_elimina_espacios():
    """Prueba que se eliminan espacios en blanco."""
    update = EmpleadoUpdate(nombre="  María García  ")
    assert update.nombre == "María García"


def test_empleado_response_valido():
    """Prueba crear una respuesta de empleado."""
    response = EmpleadoResponse(id="E001", nombre="Juan Pérez")
    assert response.id == "E001"
    assert response.nombre == "Juan Pérez"


# ============================================================================
# TESTS PARA TIPOS DE SERVICIOS
# ============================================================================

def test_tipo_servicio_create_valido():
    """Prueba crear un tipo de servicio con datos válidos."""
    tipo = TipoServicioCreate(
        nombre="Corte Básico",
        descripcion="Corte de cabello básico",
        porcentaje_comision=40.0
    )
    assert tipo.nombre == "Corte Básico"
    assert tipo.descripcion == "Corte de cabello básico"
    assert tipo.porcentaje_comision == 40.0


def test_tipo_servicio_create_elimina_espacios_nombre():
    """Prueba que se eliminan espacios en blanco del nombre."""
    tipo = TipoServicioCreate(
        nombre="  Corte Básico  ",
        descripcion="Descripción",
        porcentaje_comision=40.0
    )
    assert tipo.nombre == "Corte Básico"


def test_tipo_servicio_create_porcentaje_cero_valido():
    """Prueba que porcentaje 0 es válido."""
    tipo = TipoServicioCreate(
        nombre="Servicio",
        descripcion="Desc",
        porcentaje_comision=0.0
    )
    assert tipo.porcentaje_comision == 0.0


def test_tipo_servicio_create_porcentaje_cien_valido():
    """Prueba que porcentaje 100 es válido."""
    tipo = TipoServicioCreate(
        nombre="Servicio",
        descripcion="Desc",
        porcentaje_comision=100.0
    )
    assert tipo.porcentaje_comision == 100.0


def test_tipo_servicio_create_porcentaje_negativo_falla():
    """Prueba que porcentaje negativo falla."""
    with pytest.raises(ValidationError) as exc_info:
        TipoServicioCreate(
            nombre="Servicio",
            descripcion="Desc",
            porcentaje_comision=-1.0
        )
    error_str = str(exc_info.value)
    assert ("porcentaje de comisión debe estar entre 0 y 100" in error_str or 
            "greater_than_equal" in error_str or
            "greater than or equal to 0" in error_str)


def test_tipo_servicio_create_porcentaje_mayor_cien_falla():
    """Prueba que porcentaje mayor a 100 falla."""
    with pytest.raises(ValidationError) as exc_info:
        TipoServicioCreate(
            nombre="Servicio",
            descripcion="Desc",
            porcentaje_comision=101.0
        )
    error_str = str(exc_info.value)
    assert ("porcentaje de comisión debe estar entre 0 y 100" in error_str or 
            "less_than_equal" in error_str or
            "less than or equal to 100" in error_str)


def test_tipo_servicio_create_nombre_vacio_falla():
    """Prueba que nombre vacío falla."""
    with pytest.raises(ValidationError) as exc_info:
        TipoServicioCreate(
            nombre="",
            descripcion="Desc",
            porcentaje_comision=40.0
        )
    assert "string_too_short" in str(exc_info.value) or "at least 1 character" in str(exc_info.value)


def test_tipo_servicio_create_nombre_solo_espacios_falla():
    """Prueba que nombre con solo espacios falla."""
    with pytest.raises(ValidationError) as exc_info:
        TipoServicioCreate(
            nombre="   ",
            descripcion="Desc",
            porcentaje_comision=40.0
        )
    assert "no puede estar vacío" in str(exc_info.value)


def test_tipo_servicio_update_valido():
    """Prueba actualizar tipo de servicio con datos válidos."""
    update = TipoServicioUpdate(
        descripcion="Nueva descripción",
        porcentaje_comision=45.0
    )
    assert update.descripcion == "Nueva descripción"
    assert update.porcentaje_comision == 45.0


def test_tipo_servicio_update_solo_descripcion():
    """Prueba actualizar solo la descripción."""
    update = TipoServicioUpdate(descripcion="Nueva descripción")
    assert update.descripcion == "Nueva descripción"
    assert update.porcentaje_comision is None


def test_tipo_servicio_update_solo_porcentaje():
    """Prueba actualizar solo el porcentaje."""
    update = TipoServicioUpdate(porcentaje_comision=50.0)
    assert update.descripcion is None
    assert update.porcentaje_comision == 50.0


def test_tipo_servicio_update_porcentaje_invalido_falla():
    """Prueba que porcentaje inválido falla en update."""
    with pytest.raises(ValidationError) as exc_info:
        TipoServicioUpdate(porcentaje_comision=150.0)
    error_str = str(exc_info.value)
    assert ("porcentaje de comisión debe estar entre 0 y 100" in error_str or 
            "less_than_equal" in error_str or
            "less than or equal to 100" in error_str)


def test_tipo_servicio_response_valido():
    """Prueba crear una respuesta de tipo de servicio."""
    response = TipoServicioResponse(
        nombre="Corte",
        descripcion="Desc",
        porcentaje_comision=40.0
    )
    assert response.nombre == "Corte"
    assert response.descripcion == "Desc"
    assert response.porcentaje_comision == 40.0


# ============================================================================
# TESTS PARA SERVICIOS
# ============================================================================

def test_servicio_create_valido():
    """Prueba crear un servicio con datos válidos."""
    servicio = ServicioCreate(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00")
    )
    assert servicio.fecha == date(2024, 1, 15)
    assert servicio.empleado_id == "E001"
    assert servicio.tipo_servicio == "Corte"
    assert servicio.precio == Decimal("25.00")


def test_servicio_create_elimina_espacios():
    """Prueba que se eliminan espacios en blanco."""
    servicio = ServicioCreate(
        fecha=date(2024, 1, 15),
        empleado_id="  E001  ",
        tipo_servicio="  Corte  ",
        precio=Decimal("25.00")
    )
    assert servicio.empleado_id == "E001"
    assert servicio.tipo_servicio == "Corte"


def test_servicio_create_precio_cero_falla():
    """Prueba que precio cero falla."""
    with pytest.raises(ValidationError) as exc_info:
        ServicioCreate(
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio="Corte",
            precio=Decimal("0")
        )
    error_str = str(exc_info.value)
    assert ("debe ser mayor que cero" in error_str or 
            "greater_than" in error_str or
            "greater than 0" in error_str)


def test_servicio_create_precio_negativo_falla():
    """Prueba que precio negativo falla."""
    with pytest.raises(ValidationError) as exc_info:
        ServicioCreate(
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio="Corte",
            precio=Decimal("-10.00")
        )
    error_str = str(exc_info.value)
    assert ("debe ser mayor que cero" in error_str or 
            "greater_than" in error_str or
            "greater than 0" in error_str)


def test_servicio_create_empleado_id_vacio_falla():
    """Prueba que empleado_id vacío falla."""
    with pytest.raises(ValidationError) as exc_info:
        ServicioCreate(
            fecha=date(2024, 1, 15),
            empleado_id="",
            tipo_servicio="Corte",
            precio=Decimal("25.00")
        )
    # Puede fallar por min_length o por el validator
    error_str = str(exc_info.value)
    assert "empleado" in error_str.lower() or "field required" in error_str.lower()


def test_servicio_create_empleado_id_solo_espacios_falla():
    """Prueba que empleado_id con solo espacios falla."""
    with pytest.raises(ValidationError) as exc_info:
        ServicioCreate(
            fecha=date(2024, 1, 15),
            empleado_id="   ",
            tipo_servicio="Corte",
            precio=Decimal("25.00")
        )
    assert "no puede estar vacío" in str(exc_info.value)


def test_servicio_create_tipo_servicio_vacio_falla():
    """Prueba que tipo_servicio vacío falla."""
    with pytest.raises(ValidationError) as exc_info:
        ServicioCreate(
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio="",
            precio=Decimal("25.00")
        )
    error_str = str(exc_info.value)
    assert "servicio" in error_str.lower() or "field required" in error_str.lower()


def test_servicio_create_tipo_servicio_solo_espacios_falla():
    """Prueba que tipo_servicio con solo espacios falla."""
    with pytest.raises(ValidationError) as exc_info:
        ServicioCreate(
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio="   ",
            precio=Decimal("25.00")
        )
    assert "no puede estar vacío" in str(exc_info.value)


def test_servicio_response_valido():
    """Prueba crear una respuesta de servicio."""
    response = ServicioResponse(
        id="S001",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00"),
        comision_calculada=Decimal("10.00")
    )
    assert response.id == "S001"
    assert response.fecha == date(2024, 1, 15)
    assert response.empleado_id == "E001"
    assert response.tipo_servicio == "Corte"
    assert response.precio == Decimal("25.00")
    assert response.comision_calculada == Decimal("10.00")


# ============================================================================
# TESTS PARA REPORTES
# ============================================================================

def test_ingresos_response_valido():
    """Prueba crear una respuesta de ingresos."""
    response = IngresosResponse(
        total=Decimal("1000.00"),
        fecha_inicio=date(2024, 1, 1),
        fecha_fin=date(2024, 1, 31)
    )
    assert response.total == Decimal("1000.00")
    assert response.fecha_inicio == date(2024, 1, 1)
    assert response.fecha_fin == date(2024, 1, 31)


def test_ingresos_response_sin_fechas():
    """Prueba crear respuesta de ingresos sin fechas."""
    response = IngresosResponse(total=Decimal("1000.00"))
    assert response.total == Decimal("1000.00")
    assert response.fecha_inicio is None
    assert response.fecha_fin is None


def test_beneficios_response_valido():
    """Prueba crear una respuesta de beneficios."""
    response = BeneficiosResponse(
        ingresos=Decimal("1000.00"),
        comisiones=Decimal("400.00"),
        beneficios=Decimal("600.00"),
        fecha_inicio=date(2024, 1, 1),
        fecha_fin=date(2024, 1, 31)
    )
    assert response.ingresos == Decimal("1000.00")
    assert response.comisiones == Decimal("400.00")
    assert response.beneficios == Decimal("600.00")
    assert response.fecha_inicio == date(2024, 1, 1)
    assert response.fecha_fin == date(2024, 1, 31)


def test_beneficios_response_sin_fechas():
    """Prueba crear respuesta de beneficios sin fechas."""
    response = BeneficiosResponse(
        ingresos=Decimal("1000.00"),
        comisiones=Decimal("400.00"),
        beneficios=Decimal("600.00")
    )
    assert response.ingresos == Decimal("1000.00")
    assert response.comisiones == Decimal("400.00")
    assert response.beneficios == Decimal("600.00")
    assert response.fecha_inicio is None
    assert response.fecha_fin is None


def test_servicio_detalle_valido():
    """Prueba crear un detalle de servicio."""
    detalle = ServicioDetalle(
        fecha=date(2024, 1, 15),
        tipo_servicio="Corte",
        precio=Decimal("25.00"),
        comision=Decimal("10.00")
    )
    assert detalle.fecha == date(2024, 1, 15)
    assert detalle.tipo_servicio == "Corte"
    assert detalle.precio == Decimal("25.00")
    assert detalle.comision == Decimal("10.00")


def test_desglose_pago_response_valido():
    """Prueba crear una respuesta de desglose de pago."""
    servicios = [
        ServicioDetalle(
            fecha=date(2024, 1, 15),
            tipo_servicio="Corte",
            precio=Decimal("25.00"),
            comision=Decimal("10.00")
        ),
        ServicioDetalle(
            fecha=date(2024, 1, 16),
            tipo_servicio="Tinte",
            precio=Decimal("50.00"),
            comision=Decimal("17.50")
        )
    ]
    
    response = DesglosePagoResponse(
        empleado_id="E001",
        empleado_nombre="Juan Pérez",
        servicios=servicios,
        total=Decimal("27.50")
    )
    
    assert response.empleado_id == "E001"
    assert response.empleado_nombre == "Juan Pérez"
    assert len(response.servicios) == 2
    assert response.total == Decimal("27.50")


def test_desglose_pago_response_sin_servicios():
    """Prueba crear desglose de pago sin servicios."""
    response = DesglosePagoResponse(
        empleado_id="E001",
        empleado_nombre="Juan Pérez",
        servicios=[],
        total=Decimal("0")
    )
    
    assert response.empleado_id == "E001"
    assert response.empleado_nombre == "Juan Pérez"
    assert len(response.servicios) == 0
    assert response.total == Decimal("0")
