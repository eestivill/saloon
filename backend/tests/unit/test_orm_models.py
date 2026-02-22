"""
Pruebas unitarias para los modelos ORM de SQLAlchemy.
"""
import pytest
from datetime import date
from decimal import Decimal
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.orm_models import Base, EmpleadoORM, TipoServicioORM, ServicioORM


@pytest.fixture
def engine():
    """Crea un engine de SQLAlchemy en memoria para pruebas."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Crea una sesión de base de datos para pruebas."""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_crear_tablas(engine):
    """Verifica que las tablas se crean correctamente."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    assert 'empleados' in tables
    assert 'tipos_servicios' in tables
    assert 'servicios' in tables


def test_empleado_orm_crear_y_recuperar(session):
    """Verifica que se puede crear y recuperar un empleado."""
    empleado = EmpleadoORM(id="E001", nombre="Juan Pérez")
    session.add(empleado)
    session.commit()
    
    recuperado = session.query(EmpleadoORM).filter_by(id="E001").first()
    assert recuperado is not None
    assert recuperado.id == "E001"
    assert recuperado.nombre == "Juan Pérez"


def test_tipo_servicio_orm_crear_y_recuperar(session):
    """Verifica que se puede crear y recuperar un tipo de servicio."""
    tipo = TipoServicioORM(
        nombre="Corte",
        descripcion="Corte de cabello",
        porcentaje_comision=40.0
    )
    session.add(tipo)
    session.commit()
    
    recuperado = session.query(TipoServicioORM).filter_by(nombre="Corte").first()
    assert recuperado is not None
    assert recuperado.nombre == "Corte"
    assert recuperado.descripcion == "Corte de cabello"
    assert recuperado.porcentaje_comision == 40.0


def test_servicio_orm_crear_y_recuperar(session):
    """Verifica que se puede crear y recuperar un servicio."""
    # Primero crear empleado y tipo de servicio
    empleado = EmpleadoORM(id="E001", nombre="Juan")
    tipo = TipoServicioORM(nombre="Corte", descripcion="Corte", porcentaje_comision=40.0)
    session.add(empleado)
    session.add(tipo)
    session.commit()
    
    # Crear servicio
    servicio = ServicioORM(
        id="S001",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00"),
        comision_calculada=Decimal("10.00")
    )
    session.add(servicio)
    session.commit()
    
    recuperado = session.query(ServicioORM).filter_by(id="S001").first()
    assert recuperado is not None
    assert recuperado.id == "S001"
    assert recuperado.fecha == date(2024, 1, 15)
    assert recuperado.empleado_id == "E001"
    assert recuperado.tipo_servicio == "Corte"
    assert recuperado.precio == Decimal("25.00")
    assert recuperado.comision_calculada == Decimal("10.00")


def test_indices_servicios_existen(engine):
    """Verifica que los índices están creados correctamente."""
    inspector = inspect(engine)
    indices = inspector.get_indexes('servicios')
    
    # Obtener nombres de índices
    index_names = [idx['name'] for idx in indices]
    
    # Verificar que existen los índices esperados
    assert 'idx_servicios_empleado_fecha' in index_names
    assert 'idx_servicios_fecha' in index_names


def test_empleado_orm_repr(session):
    """Verifica la representación string del empleado."""
    empleado = EmpleadoORM(id="E001", nombre="Juan")
    assert repr(empleado) == "<Empleado(id='E001', nombre='Juan')>"


def test_tipo_servicio_orm_repr(session):
    """Verifica la representación string del tipo de servicio."""
    tipo = TipoServicioORM(nombre="Corte", descripcion="Desc", porcentaje_comision=40.0)
    assert repr(tipo) == "<TipoServicio(nombre='Corte', comision=40.0%)>"


def test_servicio_orm_repr(session):
    """Verifica la representación string del servicio."""
    servicio = ServicioORM(
        id="S001",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00"),
        comision_calculada=Decimal("10.00")
    )
    assert repr(servicio) == "<Servicio(id='S001', empleado='E001', fecha=2024-01-15)>"



def test_tipo_servicio_constraint_porcentaje_invalido(session):
    """Verifica que el constraint de porcentaje rechaza valores fuera de rango."""
    from sqlalchemy.exc import IntegrityError
    
    # Intentar crear con porcentaje > 100
    tipo = TipoServicioORM(
        nombre="Invalido",
        descripcion="Test",
        porcentaje_comision=150.0
    )
    session.add(tipo)
    
    with pytest.raises(IntegrityError):
        session.commit()
    
    session.rollback()
    
    # Intentar crear con porcentaje < 0
    tipo2 = TipoServicioORM(
        nombre="Invalido2",
        descripcion="Test",
        porcentaje_comision=-10.0
    )
    session.add(tipo2)
    
    with pytest.raises(IntegrityError):
        session.commit()


def test_servicio_constraint_precio_invalido(session):
    """Verifica que el constraint de precio rechaza valores <= 0."""
    from sqlalchemy.exc import IntegrityError
    
    # Primero crear empleado y tipo de servicio
    empleado = EmpleadoORM(id="E001", nombre="Juan")
    tipo = TipoServicioORM(nombre="Corte", descripcion="Corte", porcentaje_comision=40.0)
    session.add(empleado)
    session.add(tipo)
    session.commit()
    
    # Intentar crear servicio con precio 0
    servicio = ServicioORM(
        id="S001",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("0.00"),
        comision_calculada=Decimal("0.00")
    )
    session.add(servicio)
    
    with pytest.raises(IntegrityError):
        session.commit()
    
    session.rollback()
    
    # Intentar crear servicio con precio negativo
    servicio2 = ServicioORM(
        id="S002",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("-10.00"),
        comision_calculada=Decimal("0.00")
    )
    session.add(servicio2)
    
    with pytest.raises(IntegrityError):
        session.commit()



def test_empleado_from_orm_conversion(session):
    """Verifica que se puede convertir EmpleadoORM a Empleado."""
    from app.models import Empleado
    
    empleado_orm = EmpleadoORM(id="E001", nombre="Juan Pérez")
    session.add(empleado_orm)
    session.commit()
    
    empleado = Empleado.from_orm(empleado_orm)
    assert empleado.id == "E001"
    assert empleado.nombre == "Juan Pérez"


def test_tipo_servicio_from_orm_conversion(session):
    """Verifica que se puede convertir TipoServicioORM a TipoServicio."""
    from app.models import TipoServicio
    
    tipo_orm = TipoServicioORM(
        nombre="Corte",
        descripcion="Corte de cabello",
        porcentaje_comision=40.0
    )
    session.add(tipo_orm)
    session.commit()
    
    tipo = TipoServicio.from_orm(tipo_orm)
    assert tipo.nombre == "Corte"
    assert tipo.descripcion == "Corte de cabello"
    assert tipo.porcentaje_comision == 40.0


def test_servicio_from_orm_conversion(session):
    """Verifica que se puede convertir ServicioORM a ServicioRegistrado."""
    from app.models import ServicioRegistrado
    
    # Crear dependencias
    empleado = EmpleadoORM(id="E001", nombre="Juan")
    tipo = TipoServicioORM(nombre="Corte", descripcion="Corte", porcentaje_comision=40.0)
    session.add(empleado)
    session.add(tipo)
    session.commit()
    
    servicio_orm = ServicioORM(
        id="S001",
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=Decimal("25.00"),
        comision_calculada=Decimal("10.00")
    )
    session.add(servicio_orm)
    session.commit()
    
    servicio = ServicioRegistrado.from_orm(servicio_orm)
    assert servicio.id == "S001"
    assert servicio.fecha == date(2024, 1, 15)
    assert servicio.empleado_id == "E001"
    assert servicio.tipo_servicio == "Corte"
    assert servicio.precio == Decimal("25.00")
    assert servicio.comision_calculada == Decimal("10.00")
