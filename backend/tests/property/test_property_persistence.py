"""
Pruebas de propiedad para persistencia de modelos ORM.

Feature: salon-peluqueria-gestion
Property 26: Persistencia Round-Trip para Todas las Entidades
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from hypothesis import given, strategies as st, settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.orm_models import Base, EmpleadoORM, TipoServicioORM, ServicioORM
from app.models import Empleado, TipoServicio, ServicioRegistrado


# Estrategias de generación de datos
empleado_ids = st.text(
    min_size=1, 
    max_size=50,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'),
        blacklist_characters=' \t\n\r'
    )
)

nombres = st.text(
    min_size=1,
    max_size=100,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Zs'),
        blacklist_characters='\t\n\r'
    )
)

descripciones = st.text(
    min_size=1,
    max_size=200,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Zs', 'Nd', 'Po'),
        blacklist_characters='\t\n\r'
    )
)

porcentajes = st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)

precios = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("99999.99"),
    places=2,
    allow_nan=False,
    allow_infinity=False
)

fechas = st.dates(
    min_value=date(2020, 1, 1),
    max_value=date(2030, 12, 31)
)

servicio_ids = st.text(
    min_size=1,
    max_size=50,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'),
        blacklist_characters=' \t\n\r'
    )
)


def create_db_session():
    """Crea una sesión de base de datos en memoria."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


@given(
    empleado_id=empleado_ids,
    nombre=nombres
)
@settings(max_examples=100)
def test_property_26_empleado_round_trip(empleado_id, nombre):
    """
    Feature: salon-peluqueria-gestion, Property 26:
    Para cualquier entidad Empleado creada y guardada,
    cargar los datos desde persistencia debe recuperar una entidad equivalente
    con todos sus atributos intactos.
    
    Validates: Requirements 3.6, 8.1, 8.2, 8.3, 8.4
    """
    # Crear sesión de base de datos
    db_session = create_db_session()
    
    try:
        # Crear y guardar empleado ORM
        empleado_orm = EmpleadoORM(id=empleado_id, nombre=nombre)
        db_session.add(empleado_orm)
        db_session.commit()
        
        # Recuperar desde la base de datos
        recuperado_orm = db_session.query(EmpleadoORM).filter_by(id=empleado_id).first()
        
        # Verificar que se recuperó correctamente
        assert recuperado_orm is not None
        assert recuperado_orm.id == empleado_id
        assert recuperado_orm.nombre == nombre
        
        # Convertir a modelo de dominio
        empleado_dominio = Empleado.from_orm(recuperado_orm)
        
        # Verificar que la conversión preserva todos los atributos
        assert empleado_dominio.id == empleado_id
        assert empleado_dominio.nombre == nombre
        
        # Verificar que to_dict funciona correctamente
        empleado_dict = empleado_dominio.to_dict()
        assert empleado_dict["id"] == empleado_id
        assert empleado_dict["nombre"] == nombre
    finally:
        db_session.close()


@given(
    nombre=empleado_ids,  # Reutilizamos la estrategia de IDs para nombres de servicios
    descripcion=descripciones,
    porcentaje=porcentajes
)
@settings(max_examples=100)
def test_property_26_tipo_servicio_round_trip(nombre, descripcion, porcentaje):
    """
    Feature: salon-peluqueria-gestion, Property 26:
    Para cualquier entidad TipoServicio creada y guardada,
    cargar los datos desde persistencia debe recuperar una entidad equivalente
    con todos sus atributos intactos.
    
    Validates: Requirements 3.6, 8.1, 8.2, 8.3, 8.4
    """
    # Crear sesión de base de datos
    db_session = create_db_session()
    
    try:
        # Crear y guardar tipo de servicio ORM
        tipo_orm = TipoServicioORM(
            nombre=nombre,
            descripcion=descripcion,
            porcentaje_comision=porcentaje
        )
        db_session.add(tipo_orm)
        db_session.commit()
        
        # Recuperar desde la base de datos
        recuperado_orm = db_session.query(TipoServicioORM).filter_by(nombre=nombre).first()
        
        # Verificar que se recuperó correctamente
        assert recuperado_orm is not None
        assert recuperado_orm.nombre == nombre
        assert recuperado_orm.descripcion == descripcion
        assert recuperado_orm.porcentaje_comision == porcentaje
        
        # Convertir a modelo de dominio
        tipo_dominio = TipoServicio.from_orm(recuperado_orm)
        
        # Verificar que la conversión preserva todos los atributos
        assert tipo_dominio.nombre == nombre
        assert tipo_dominio.descripcion == descripcion
        assert tipo_dominio.porcentaje_comision == porcentaje
        
        # Verificar que to_dict funciona correctamente
        tipo_dict = tipo_dominio.to_dict()
        assert tipo_dict["nombre"] == nombre
        assert tipo_dict["descripcion"] == descripcion
        assert tipo_dict["porcentaje_comision"] == porcentaje
    finally:
        db_session.close()


@given(
    servicio_id=servicio_ids,
    fecha=fechas,
    empleado_id=empleado_ids,
    tipo_servicio=empleado_ids,
    precio=precios
)
@settings(max_examples=100)
def test_property_26_servicio_round_trip(
    servicio_id, fecha, empleado_id, tipo_servicio, precio
):
    """
    Feature: salon-peluqueria-gestion, Property 26:
    Para cualquier entidad ServicioRegistrado creada y guardada,
    cargar los datos desde persistencia debe recuperar una entidad equivalente
    con todos sus atributos intactos.
    
    Validates: Requirements 3.6, 8.1, 8.2, 8.3, 8.4
    """
    # Crear sesión de base de datos
    db_session = create_db_session()
    
    try:
        # Primero crear las entidades relacionadas
        empleado_orm = EmpleadoORM(id=empleado_id, nombre="Test Empleado")
        tipo_orm = TipoServicioORM(
            nombre=tipo_servicio,
            descripcion="Test Servicio",
            porcentaje_comision=40.0
        )
        db_session.add(empleado_orm)
        db_session.add(tipo_orm)
        db_session.commit()
        
        # Calcular comisión (redondeada a 2 decimales para coincidir con la BD)
        comision = ((precio * Decimal("40.0")) / Decimal("100.0")).quantize(Decimal("0.01"))
        
        # Crear y guardar servicio ORM
        servicio_orm = ServicioORM(
            id=servicio_id,
            fecha=fecha,
            empleado_id=empleado_id,
            tipo_servicio=tipo_servicio,
            precio=precio,
            comision_calculada=comision
        )
        db_session.add(servicio_orm)
        db_session.commit()
        
        # Recuperar desde la base de datos
        recuperado_orm = db_session.query(ServicioORM).filter_by(id=servicio_id).first()
        
        # Verificar que se recuperó correctamente
        assert recuperado_orm is not None
        assert recuperado_orm.id == servicio_id
        assert recuperado_orm.fecha == fecha
        assert recuperado_orm.empleado_id == empleado_id
        assert recuperado_orm.tipo_servicio == tipo_servicio
        assert recuperado_orm.precio == precio
        assert recuperado_orm.comision_calculada == comision
        
        # Convertir a modelo de dominio
        servicio_dominio = ServicioRegistrado.from_orm(recuperado_orm)
        
        # Verificar que la conversión preserva todos los atributos
        assert servicio_dominio.id == servicio_id
        assert servicio_dominio.fecha == fecha
        assert servicio_dominio.empleado_id == empleado_id
        assert servicio_dominio.tipo_servicio == tipo_servicio
        assert servicio_dominio.precio == precio
        assert servicio_dominio.comision_calculada == comision
        
        # Verificar que to_dict funciona correctamente
        servicio_dict = servicio_dominio.to_dict()
        assert servicio_dict["id"] == servicio_id
        assert servicio_dict["fecha"] == fecha.isoformat()
        assert servicio_dict["empleado_id"] == empleado_id
        assert servicio_dict["tipo_servicio"] == tipo_servicio
        assert servicio_dict["precio"] == str(precio)
        assert servicio_dict["comision_calculada"] == str(comision)
    finally:
        db_session.close()
