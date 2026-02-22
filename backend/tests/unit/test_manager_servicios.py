"""
Pruebas unitarias para la gestión de servicios en SalonManager.
"""
import pytest
from datetime import date
from decimal import Decimal

from app.manager import SalonManager
from app.repository import SQLAlchemyRepository
from app.result import Ok, Err
from app.errors import ValidationError, NotFoundError


@pytest.fixture
def manager():
    """Fixture que proporciona un SalonManager con repositorio en memoria."""
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    return SalonManager(repository)


def test_registrar_servicio_exitoso_con_datos_validos(manager):
    """Probar registro exitoso con datos válidos."""
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Registrar servicio
    resultado = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00")
    )
    
    # Verificar resultado
    assert isinstance(resultado, Ok)
    servicio = resultado.value
    assert servicio.fecha == date(2024, 1, 15)
    assert servicio.empleado_id == "E001"
    assert servicio.tipo_servicio == "Corte"
    assert servicio.precio == Decimal("25.00")
    assert servicio.comision_calculada == Decimal("10.00")  # 40% de 25.00
    assert servicio.id is not None  # ID generado automáticamente


def test_registrar_servicio_con_precio_invalido_retorna_error(manager):
    """Probar error con precio inválido."""
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Intentar registrar con precio cero
    resultado = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("0")
    )
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, ValidationError)
    
    # Intentar registrar con precio negativo
    resultado = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("-10.00")
    )
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, ValidationError)


def test_registrar_servicio_con_empleado_inexistente_retorna_error(manager):
    """Probar error con empleado inexistente."""
    # Setup: crear solo tipo de servicio
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Intentar registrar con empleado inexistente
    resultado = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="NOEXISTE",
        tipo_servicio="Corte",
        precio=Decimal("25.00")
    )
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, NotFoundError)
    assert resultado.error.entity == "Empleado"
    assert resultado.error.identifier == "NOEXISTE"


def test_registrar_servicio_con_tipo_servicio_inexistente_retorna_error(manager):
    """Probar error con tipo de servicio inexistente."""
    # Setup: crear solo empleado
    manager.crear_empleado("E001", "Juan Pérez")
    
    # Intentar registrar con tipo de servicio inexistente
    resultado = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="NOEXISTE",
        precio=Decimal("25.00")
    )
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, NotFoundError)
    assert resultado.error.entity == "TipoServicio"
    assert resultado.error.identifier == "NOEXISTE"


def test_registrar_servicio_calcula_comision_correctamente(manager):
    """Probar que la comisión se calcula correctamente."""
    # Setup: crear empleado y varios tipos de servicios con diferentes porcentajes
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    manager.crear_tipo_servicio("Tinte", "Tinte completo", 35.0)
    manager.crear_tipo_servicio("Peinado", "Peinado especial", 50.0)
    
    # Registrar servicios con diferentes precios y porcentajes
    resultado1 = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00")
    )
    assert isinstance(resultado1, Ok)
    assert resultado1.value.comision_calculada == Decimal("10.00")  # 40% de 25.00
    
    resultado2 = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Tinte",
        precio=Decimal("100.00")
    )
    assert isinstance(resultado2, Ok)
    assert resultado2.value.comision_calculada == Decimal("35.00")  # 35% de 100.00
    
    resultado3 = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Peinado",
        precio=Decimal("50.00")
    )
    assert isinstance(resultado3, Ok)
    assert resultado3.value.comision_calculada == Decimal("25.00")  # 50% de 50.00


def test_registrar_servicio_genera_id_unico(manager):
    """Probar que cada servicio registrado tiene un ID único."""
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Registrar múltiples servicios
    ids = set()
    for _ in range(10):
        resultado = manager.registrar_servicio(
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio="Corte",
            precio=Decimal("25.00")
        )
        assert isinstance(resultado, Ok)
        ids.add(resultado.value.id)
    
    # Verificar que todos los IDs son únicos
    assert len(ids) == 10


def test_registrar_servicio_persiste_en_repositorio(manager):
    """Probar que el servicio se persiste correctamente."""
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Registrar servicio
    resultado = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00")
    )
    
    assert isinstance(resultado, Ok)
    servicio_id = resultado.value.id
    
    # Verificar que está en el repositorio
    servicios = manager.repository.listar_servicios()
    assert len(servicios) == 1
    assert servicios[0].id == servicio_id
    assert servicios[0].precio == Decimal("25.00")
    assert servicios[0].comision_calculada == Decimal("10.00")


# Pruebas para consultas de servicios

def test_obtener_servicios_filtra_por_empleado(manager):
    """Probar filtrado por empleado."""
    # Setup: crear empleados, tipo de servicio y servicios
    manager.crear_empleado("E001", "Juan")
    manager.crear_empleado("E002", "María")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("25.00"))
    manager.registrar_servicio(date(2024, 1, 16), "E002", "Corte", Decimal("30.00"))
    manager.registrar_servicio(date(2024, 1, 17), "E001", "Corte", Decimal("25.00"))
    
    # Filtrar por E001
    servicios_e001 = manager.obtener_servicios(empleado_id="E001")
    assert len(servicios_e001) == 2
    assert all(s.empleado_id == "E001" for s in servicios_e001)
    
    # Filtrar por E002
    servicios_e002 = manager.obtener_servicios(empleado_id="E002")
    assert len(servicios_e002) == 1
    assert servicios_e002[0].empleado_id == "E002"


def test_obtener_servicios_filtra_por_rango_fechas(manager):
    """Probar filtrado por rango de fechas."""
    # Setup: crear empleado, tipo de servicio y servicios en diferentes fechas
    manager.crear_empleado("E001", "Juan")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    manager.registrar_servicio(date(2024, 1, 10), "E001", "Corte", Decimal("25.00"))
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("30.00"))
    manager.registrar_servicio(date(2024, 1, 20), "E001", "Corte", Decimal("35.00"))
    manager.registrar_servicio(date(2024, 1, 25), "E001", "Corte", Decimal("40.00"))
    
    # Filtrar por fecha_inicio
    servicios = manager.obtener_servicios(fecha_inicio=date(2024, 1, 15))
    assert len(servicios) == 3
    assert all(s.fecha >= date(2024, 1, 15) for s in servicios)
    
    # Filtrar por fecha_fin
    servicios = manager.obtener_servicios(fecha_fin=date(2024, 1, 20))
    assert len(servicios) == 3
    assert all(s.fecha <= date(2024, 1, 20) for s in servicios)
    
    # Filtrar por rango completo
    servicios = manager.obtener_servicios(
        fecha_inicio=date(2024, 1, 15),
        fecha_fin=date(2024, 1, 20)
    )
    assert len(servicios) == 2
    assert all(date(2024, 1, 15) <= s.fecha <= date(2024, 1, 20) for s in servicios)


def test_obtener_servicios_ordenamiento_descendente(manager):
    """Probar ordenamiento descendente por fecha."""
    # Setup: crear empleado, tipo de servicio y servicios en diferentes fechas
    manager.crear_empleado("E001", "Juan")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    manager.registrar_servicio(date(2024, 1, 10), "E001", "Corte", Decimal("25.00"))
    manager.registrar_servicio(date(2024, 1, 20), "E001", "Corte", Decimal("30.00"))
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("35.00"))
    
    # Obtener servicios
    servicios = manager.obtener_servicios()
    
    # Verificar ordenamiento descendente (más recientes primero)
    assert len(servicios) == 3
    assert servicios[0].fecha == date(2024, 1, 20)
    assert servicios[1].fecha == date(2024, 1, 15)
    assert servicios[2].fecha == date(2024, 1, 10)


def test_obtener_servicios_lista_vacia_cuando_no_hay_servicios(manager):
    """Probar lista vacía cuando no hay servicios."""
    # Sin crear servicios
    servicios = manager.obtener_servicios()
    assert servicios == []
    
    # Con filtros que no coinciden
    manager.crear_empleado("E001", "Juan")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("25.00"))
    
    servicios = manager.obtener_servicios(empleado_id="E999")
    assert servicios == []
    
    servicios = manager.obtener_servicios(fecha_inicio=date(2024, 2, 1))
    assert servicios == []


# Pruebas para cálculos financieros

def test_calcular_ingresos_con_multiples_servicios(manager):
    """Probar cálculo de ingresos con múltiples servicios."""
    # Setup: crear empleado, tipo de servicio y servicios
    manager.crear_empleado("E001", "Juan")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("25.00"))
    manager.registrar_servicio(date(2024, 1, 16), "E001", "Corte", Decimal("30.00"))
    manager.registrar_servicio(date(2024, 1, 17), "E001", "Corte", Decimal("45.00"))
    
    # Calcular ingresos
    ingresos = manager.calcular_ingresos_totales()
    assert ingresos == Decimal("100.00")


def test_calcular_ingresos_con_lista_vacia_retorna_cero(manager):
    """Probar que ingresos con lista vacía retorna cero."""
    ingresos = manager.calcular_ingresos_totales()
    assert ingresos == Decimal("0")


def test_calcular_ingresos_filtrado_por_periodo(manager):
    """Probar filtrado de ingresos por período."""
    # Setup: crear empleado, tipo de servicio y servicios en diferentes fechas
    manager.crear_empleado("E001", "Juan")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    manager.registrar_servicio(date(2024, 1, 10), "E001", "Corte", Decimal("25.00"))
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("30.00"))
    manager.registrar_servicio(date(2024, 1, 20), "E001", "Corte", Decimal("35.00"))
    manager.registrar_servicio(date(2024, 1, 25), "E001", "Corte", Decimal("40.00"))
    
    # Calcular ingresos por período
    ingresos = manager.calcular_ingresos_totales(
        fecha_inicio=date(2024, 1, 15),
        fecha_fin=date(2024, 1, 20)
    )
    assert ingresos == Decimal("65.00")  # 30 + 35


def test_calcular_beneficios(manager):
    """Probar cálculo de beneficios."""
    # Setup: crear empleado, tipos de servicio con diferentes comisiones
    manager.crear_empleado("E001", "Juan")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    manager.crear_tipo_servicio("Tinte", "Tinte completo", 35.0)
    
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("25.00"))  # comisión: 10.00
    manager.registrar_servicio(date(2024, 1, 16), "E001", "Tinte", Decimal("100.00"))  # comisión: 35.00
    
    # Calcular beneficios
    beneficios = manager.calcular_beneficios()
    # Ingresos: 125.00, Comisiones: 45.00, Beneficios: 80.00
    assert beneficios == Decimal("80.00")


# Pruebas para pagos a empleados

def test_calcular_pago_empleado_con_multiples_servicios(manager):
    """Probar cálculo de pago con múltiples servicios."""
    # Setup: crear empleado, tipo de servicio y servicios
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("25.00"))  # comisión: 10.00
    manager.registrar_servicio(date(2024, 1, 16), "E001", "Corte", Decimal("30.00"))  # comisión: 12.00
    manager.registrar_servicio(date(2024, 1, 17), "E001", "Corte", Decimal("35.00"))  # comisión: 14.00
    
    # Calcular pago
    desglose = manager.calcular_pago_empleado("E001")
    
    assert desglose.empleado_id == "E001"
    assert desglose.empleado_nombre == "Juan Pérez"
    assert len(desglose.servicios) == 3
    assert desglose.total == Decimal("36.00")  # 10 + 12 + 14


def test_calcular_pago_empleado_sin_servicios_retorna_cero(manager):
    """Probar que empleado sin servicios retorna pago de cero."""
    # Setup: crear empleado sin servicios
    manager.crear_empleado("E001", "Juan Pérez")
    
    # Calcular pago
    desglose = manager.calcular_pago_empleado("E001")
    
    assert desglose.empleado_id == "E001"
    assert desglose.empleado_nombre == "Juan Pérez"
    assert len(desglose.servicios) == 0
    assert desglose.total == Decimal("0")


def test_calcular_pago_empleado_filtrado_por_periodo(manager):
    """Probar filtrado de pago por período."""
    # Setup: crear empleado, tipo de servicio y servicios en diferentes fechas
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    manager.registrar_servicio(date(2024, 1, 10), "E001", "Corte", Decimal("25.00"))  # comisión: 10.00
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("30.00"))  # comisión: 12.00
    manager.registrar_servicio(date(2024, 1, 20), "E001", "Corte", Decimal("35.00"))  # comisión: 14.00
    manager.registrar_servicio(date(2024, 1, 25), "E001", "Corte", Decimal("40.00"))  # comisión: 16.00
    
    # Calcular pago por período
    desglose = manager.calcular_pago_empleado(
        "E001",
        fecha_inicio=date(2024, 1, 15),
        fecha_fin=date(2024, 1, 20)
    )
    
    assert len(desglose.servicios) == 2
    assert desglose.total == Decimal("26.00")  # 12 + 14


def test_calcular_pago_desglose_contiene_todos_servicios(manager):
    """Probar que el desglose contiene todos los servicios."""
    # Setup: crear empleado, tipos de servicio y servicios
    manager.crear_empleado("E001", "Juan Pérez")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    manager.crear_tipo_servicio("Tinte", "Tinte completo", 35.0)
    
    manager.registrar_servicio(date(2024, 1, 15), "E001", "Corte", Decimal("25.00"))
    manager.registrar_servicio(date(2024, 1, 16), "E001", "Tinte", Decimal("100.00"))
    
    # Calcular pago
    desglose = manager.calcular_pago_empleado("E001")
    
    # Verificar desglose
    assert len(desglose.servicios) == 2
    
    # Verificar primer servicio (más reciente primero por ordenamiento descendente)
    assert desglose.servicios[0].fecha == date(2024, 1, 16)
    assert desglose.servicios[0].tipo_servicio == "Tinte"
    assert desglose.servicios[0].precio == Decimal("100.00")
    assert desglose.servicios[0].comision == Decimal("35.00")
    
    # Verificar segundo servicio
    assert desglose.servicios[1].fecha == date(2024, 1, 15)
    assert desglose.servicios[1].tipo_servicio == "Corte"
    assert desglose.servicios[1].precio == Decimal("25.00")
    assert desglose.servicios[1].comision == Decimal("10.00")
    
    # Verificar total
    assert desglose.total == Decimal("45.00")
