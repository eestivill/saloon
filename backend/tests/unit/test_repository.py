"""
Pruebas unitarias para SQLAlchemyRepository.

Validates: Requirements 8.4, 8.5, 8.6
"""
import pytest
from datetime import date
from decimal import Decimal
from sqlalchemy import create_engine, inspect

from app.repository import SQLAlchemyRepository
from app.models import Empleado, TipoServicio, ServicioRegistrado
from app.errors import PersistenceError
from app.orm_models import Base


@pytest.fixture
def repository():
    """Crea un repositorio con base de datos en memoria."""
    return SQLAlchemyRepository("sqlite:///:memory:")


def test_crear_tablas_si_no_existen(repository):
    """Verifica que las tablas se crean automáticamente al inicializar el repositorio."""
    # Verificar que el engine existe
    assert repository.engine is not None
    
    # Verificar que las tablas fueron creadas
    inspector = inspect(repository.engine)
    table_names = inspector.get_table_names()
    
    assert 'empleados' in table_names
    assert 'tipos_servicios' in table_names
    assert 'servicios' in table_names


def test_indices_estan_creados_correctamente(repository):
    """Verifica que los índices están creados correctamente."""
    inspector = inspect(repository.engine)
    
    # Verificar índices en la tabla servicios
    indices = inspector.get_indexes('servicios')
    index_names = [idx['name'] for idx in indices]
    
    # SQLite crea índices automáticos para columnas con index=True
    # y para los índices explícitos definidos en __table_args__
    assert 'idx_servicios_empleado_fecha' in index_names
    assert 'idx_servicios_fecha' in index_names


def test_guardar_y_obtener_empleado(repository):
    """Verifica que se puede guardar y recuperar un empleado."""
    # Crear empleado
    empleado = Empleado(id="E001", nombre="Juan Pérez")
    
    # Guardar
    repository.guardar_empleado(empleado)
    
    # Recuperar
    recuperado = repository.obtener_empleado("E001")
    
    # Verificar
    assert recuperado is not None
    assert recuperado.id == "E001"
    assert recuperado.nombre == "Juan Pérez"


def test_obtener_empleado_inexistente_retorna_none(repository):
    """Verifica que obtener un empleado inexistente retorna None."""
    resultado = repository.obtener_empleado("NOEXISTE")
    assert resultado is None


def test_listar_empleados_vacio(repository):
    """Verifica que listar empleados sin datos retorna lista vacía."""
    empleados = repository.listar_empleados()
    assert empleados == []


def test_listar_empleados_con_datos(repository):
    """Verifica que listar empleados retorna todos los empleados guardados."""
    # Guardar varios empleados
    repository.guardar_empleado(Empleado(id="E001", nombre="Juan"))
    repository.guardar_empleado(Empleado(id="E002", nombre="María"))
    repository.guardar_empleado(Empleado(id="E003", nombre="Pedro"))
    
    # Listar
    empleados = repository.listar_empleados()
    
    # Verificar
    assert len(empleados) == 3
    ids = [emp.id for emp in empleados]
    assert "E001" in ids
    assert "E002" in ids
    assert "E003" in ids


def test_actualizar_empleado_existente(repository):
    """Verifica que guardar un empleado existente actualiza sus datos."""
    # Guardar empleado inicial
    repository.guardar_empleado(Empleado(id="E001", nombre="Juan"))
    
    # Actualizar
    repository.guardar_empleado(Empleado(id="E001", nombre="Juan Pérez"))
    
    # Verificar
    recuperado = repository.obtener_empleado("E001")
    assert recuperado.nombre == "Juan Pérez"
    
    # Verificar que no se duplicó
    empleados = repository.listar_empleados()
    assert len(empleados) == 1


def test_guardar_y_obtener_tipo_servicio(repository):
    """Verifica que se puede guardar y recuperar un tipo de servicio."""
    # Crear tipo de servicio
    tipo = TipoServicio(
        nombre="Corte",
        descripcion="Corte de cabello",
        porcentaje_comision=40.0
    )
    
    # Guardar
    repository.guardar_tipo_servicio(tipo)
    
    # Recuperar
    recuperado = repository.obtener_tipo_servicio("Corte")
    
    # Verificar
    assert recuperado is not None
    assert recuperado.nombre == "Corte"
    assert recuperado.descripcion == "Corte de cabello"
    assert recuperado.porcentaje_comision == 40.0


def test_obtener_tipo_servicio_inexistente_retorna_none(repository):
    """Verifica que obtener un tipo de servicio inexistente retorna None."""
    resultado = repository.obtener_tipo_servicio("NOEXISTE")
    assert resultado is None


def test_listar_tipos_servicios_vacio(repository):
    """Verifica que listar tipos de servicios sin datos retorna lista vacía."""
    tipos = repository.listar_tipos_servicios()
    assert tipos == []


def test_listar_tipos_servicios_con_datos(repository):
    """Verifica que listar tipos de servicios retorna todos los tipos guardados."""
    # Guardar varios tipos
    repository.guardar_tipo_servicio(TipoServicio("Corte", "Corte básico", 40.0))
    repository.guardar_tipo_servicio(TipoServicio("Tinte", "Tinte completo", 35.0))
    repository.guardar_tipo_servicio(TipoServicio("Peinado", "Peinado especial", 30.0))
    
    # Listar
    tipos = repository.listar_tipos_servicios()
    
    # Verificar
    assert len(tipos) == 3
    nombres = [tipo.nombre for tipo in tipos]
    assert "Corte" in nombres
    assert "Tinte" in nombres
    assert "Peinado" in nombres


def test_actualizar_tipo_servicio_existente(repository):
    """Verifica que guardar un tipo de servicio existente actualiza sus datos."""
    # Guardar tipo inicial
    repository.guardar_tipo_servicio(TipoServicio("Corte", "Corte básico", 40.0))
    
    # Actualizar
    repository.guardar_tipo_servicio(TipoServicio("Corte", "Corte premium", 45.0))
    
    # Verificar
    recuperado = repository.obtener_tipo_servicio("Corte")
    assert recuperado.descripcion == "Corte premium"
    assert recuperado.porcentaje_comision == 45.0
    
    # Verificar que no se duplicó
    tipos = repository.listar_tipos_servicios()
    assert len(tipos) == 1


def test_guardar_y_listar_servicio(repository):
    """Verifica que se puede guardar y listar servicios."""
    # Primero crear las entidades relacionadas
    repository.guardar_empleado(Empleado(id="E001", nombre="Juan"))
    repository.guardar_tipo_servicio(TipoServicio("Corte", "Corte básico", 40.0))
    
    # Crear servicio
    servicio = ServicioRegistrado(
        id="S001",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00"),
        comision_calculada=Decimal("10.00")
    )
    
    # Guardar
    repository.guardar_servicio(servicio)
    
    # Listar
    servicios = repository.listar_servicios()
    
    # Verificar
    assert len(servicios) == 1
    assert servicios[0].id == "S001"
    assert servicios[0].empleado_id == "E001"
    assert servicios[0].tipo_servicio == "Corte"
    assert servicios[0].precio == Decimal("25.00")
    assert servicios[0].comision_calculada == Decimal("10.00")


def test_listar_servicios_vacio(repository):
    """Verifica que listar servicios sin datos retorna lista vacía."""
    servicios = repository.listar_servicios()
    assert servicios == []


def test_listar_servicios_con_multiples_datos(repository):
    """Verifica que listar servicios retorna todos los servicios guardados."""
    # Crear entidades relacionadas
    repository.guardar_empleado(Empleado(id="E001", nombre="Juan"))
    repository.guardar_tipo_servicio(TipoServicio("Corte", "Corte básico", 40.0))
    
    # Guardar varios servicios
    repository.guardar_servicio(ServicioRegistrado(
        id="S001",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00"),
        comision_calculada=Decimal("10.00")
    ))
    repository.guardar_servicio(ServicioRegistrado(
        id="S002",
        fecha=date(2024, 1, 16),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("30.00"),
        comision_calculada=Decimal("12.00")
    ))
    
    # Listar
    servicios = repository.listar_servicios()
    
    # Verificar
    assert len(servicios) == 2
    ids = [serv.id for serv in servicios]
    assert "S001" in ids
    assert "S002" in ids


def test_actualizar_servicio_existente(repository):
    """Verifica que guardar un servicio existente actualiza sus datos."""
    # Crear entidades relacionadas
    repository.guardar_empleado(Empleado(id="E001", nombre="Juan"))
    repository.guardar_tipo_servicio(TipoServicio("Corte", "Corte básico", 40.0))
    
    # Guardar servicio inicial
    repository.guardar_servicio(ServicioRegistrado(
        id="S001",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00"),
        comision_calculada=Decimal("10.00")
    ))
    
    # Actualizar
    repository.guardar_servicio(ServicioRegistrado(
        id="S001",
        fecha=date(2024, 1, 16),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("30.00"),
        comision_calculada=Decimal("12.00")
    ))
    
    # Verificar
    servicios = repository.listar_servicios()
    assert len(servicios) == 1
    assert servicios[0].precio == Decimal("30.00")
    assert servicios[0].comision_calculada == Decimal("12.00")


def test_get_session_retorna_sesion_valida(repository):
    """Verifica que get_session retorna una sesión válida."""
    session = repository.get_session()
    
    # Verificar que es una sesión válida
    assert session is not None
    
    # Verificar que se puede usar para consultas
    result = session.query(Base.metadata.tables['empleados']).all()
    assert isinstance(result, list)
    
    session.close()


def test_persistencia_despues_de_guardar(repository):
    """Verifica que los datos persisten después de guardar."""
    # Guardar empleado
    repository.guardar_empleado(Empleado(id="E001", nombre="Juan"))
    
    # Crear una nueva sesión para verificar persistencia
    session = repository.get_session()
    try:
        from app.orm_models import EmpleadoORM
        orm_empleado = session.query(EmpleadoORM).filter_by(id="E001").first()
        assert orm_empleado is not None
        assert orm_empleado.nombre == "Juan"
    finally:
        session.close()
