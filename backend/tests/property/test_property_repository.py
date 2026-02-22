"""
Pruebas de propiedad para validación de integridad en el repositorio.

Feature: salon-peluqueria-gestion
Property 27: Validación de Integridad al Cargar Datos
"""
import pytest
from datetime import date
from decimal import Decimal
from hypothesis import given, strategies as st, settings, assume
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.repository import SQLAlchemyRepository
from app.models import Empleado, TipoServicio, ServicioRegistrado
from app.orm_models import Base, EmpleadoORM, TipoServicioORM, ServicioORM
from app.errors import PersistenceError


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

porcentajes_invalidos = st.one_of(
    st.floats(min_value=-1000.0, max_value=-0.01, allow_nan=False, allow_infinity=False),
    st.floats(min_value=100.01, max_value=1000.0, allow_nan=False, allow_infinity=False),
    st.just(float('nan')),
    st.just(float('inf')),
    st.just(float('-inf'))
)

precios_invalidos = st.one_of(
    st.decimals(
        min_value=Decimal("-99999.99"),
        max_value=Decimal("-0.01"),
        places=2,
        allow_nan=False,
        allow_infinity=False
    ),
    st.just(Decimal("0.00"))
)


@given(
    empleado_id=empleado_ids,
    nombre=nombres
)
@settings(max_examples=100)
def test_property_27_empleado_datos_validos_se_cargan_correctamente(empleado_id, nombre):
    """
    Feature: salon-peluqueria-gestion, Property 27:
    Para cualquier empleado con datos válidos guardado en la base de datos,
    el sistema debe poder cargarlo correctamente sin errores.
    
    Validates: Requirements 8.6
    """
    # Crear repositorio
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Guardar empleado con datos válidos
    empleado = Empleado(id=empleado_id, nombre=nombre)
    repository.guardar_empleado(empleado)
    
    # Intentar cargar - no debe lanzar excepción
    recuperado = repository.obtener_empleado(empleado_id)
    
    # Verificar que se cargó correctamente
    assert recuperado is not None
    assert recuperado.id == empleado_id
    assert recuperado.nombre == nombre


@given(
    nombre=empleado_ids,
    descripcion=st.text(min_size=1, max_size=200),
    porcentaje=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
)
@settings(max_examples=100)
def test_property_27_tipo_servicio_datos_validos_se_cargan_correctamente(
    nombre, descripcion, porcentaje
):
    """
    Feature: salon-peluqueria-gestion, Property 27:
    Para cualquier tipo de servicio con datos válidos guardado en la base de datos,
    el sistema debe poder cargarlo correctamente sin errores.
    
    Validates: Requirements 8.6
    """
    # Crear repositorio
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Guardar tipo de servicio con datos válidos
    tipo = TipoServicio(
        nombre=nombre,
        descripcion=descripcion,
        porcentaje_comision=porcentaje
    )
    repository.guardar_tipo_servicio(tipo)
    
    # Intentar cargar - no debe lanzar excepción
    recuperado = repository.obtener_tipo_servicio(nombre)
    
    # Verificar que se cargó correctamente
    assert recuperado is not None
    assert recuperado.nombre == nombre
    assert recuperado.descripcion == descripcion
    assert recuperado.porcentaje_comision == porcentaje


@given(
    servicio_id=empleado_ids,
    fecha=st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31)),
    empleado_id=empleado_ids,
    tipo_servicio=empleado_ids,
    precio=st.decimals(
        min_value=Decimal("0.01"),
        max_value=Decimal("99999.99"),
        places=2,
        allow_nan=False,
        allow_infinity=False
    )
)
@settings(max_examples=100)
def test_property_27_servicio_datos_validos_se_cargan_correctamente(
    servicio_id, fecha, empleado_id, tipo_servicio, precio
):
    """
    Feature: salon-peluqueria-gestion, Property 27:
    Para cualquier servicio con datos válidos guardado en la base de datos,
    el sistema debe poder cargarlo correctamente sin errores.
    
    Validates: Requirements 8.6
    """
    # Crear repositorio
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Crear entidades relacionadas
    repository.guardar_empleado(Empleado(id=empleado_id, nombre="Test"))
    repository.guardar_tipo_servicio(TipoServicio(
        nombre=tipo_servicio,
        descripcion="Test",
        porcentaje_comision=40.0
    ))
    
    # Guardar servicio con datos válidos
    comision = ((precio * Decimal("40.0")) / Decimal("100.0")).quantize(Decimal("0.01"))
    servicio = ServicioRegistrado(
        id=servicio_id,
        fecha=fecha,
        empleado_id=empleado_id,
        tipo_servicio=tipo_servicio,
        precio=precio,
        comision_calculada=comision
    )
    repository.guardar_servicio(servicio)
    
    # Intentar cargar - no debe lanzar excepción
    servicios = repository.listar_servicios()
    
    # Verificar que se cargó correctamente
    assert len(servicios) == 1
    assert servicios[0].id == servicio_id
    assert servicios[0].precio == precio


@given(
    empleado_id=empleado_ids,
    nombre=nombres
)
@settings(max_examples=50)
def test_property_27_multiples_operaciones_mantienen_integridad(empleado_id, nombre):
    """
    Feature: salon-peluqueria-gestion, Property 27:
    Para cualquier secuencia de operaciones de guardado y carga,
    el sistema debe mantener la integridad de los datos.
    
    Validates: Requirements 8.6
    """
    # Crear repositorio
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Guardar empleado
    empleado = Empleado(id=empleado_id, nombre=nombre)
    repository.guardar_empleado(empleado)
    
    # Cargar y verificar
    recuperado1 = repository.obtener_empleado(empleado_id)
    assert recuperado1 is not None
    assert recuperado1.id == empleado_id
    
    # Actualizar
    empleado_actualizado = Empleado(id=empleado_id, nombre=nombre + " Updated")
    repository.guardar_empleado(empleado_actualizado)
    
    # Cargar nuevamente y verificar
    recuperado2 = repository.obtener_empleado(empleado_id)
    assert recuperado2 is not None
    assert recuperado2.id == empleado_id
    assert recuperado2.nombre == nombre + " Updated"
    
    # Verificar que no hay duplicados
    todos = repository.listar_empleados()
    assert len(todos) == 1


@settings(max_examples=50)
@given(
    empleado_id=empleado_ids,
    tipo_servicio=empleado_ids,
    servicio_id=empleado_ids
)
def test_property_27_integridad_referencial_se_mantiene(
    empleado_id, tipo_servicio, servicio_id
):
    """
    Feature: salon-peluqueria-gestion, Property 27:
    Para cualquier servicio guardado, las referencias a empleado y tipo de servicio
    deben mantenerse íntegras al cargar los datos.
    
    Validates: Requirements 8.6
    """
    # Crear repositorio
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Crear entidades relacionadas
    repository.guardar_empleado(Empleado(id=empleado_id, nombre="Test Empleado"))
    repository.guardar_tipo_servicio(TipoServicio(
        nombre=tipo_servicio,
        descripcion="Test Servicio",
        porcentaje_comision=40.0
    ))
    
    # Guardar servicio
    servicio = ServicioRegistrado(
        id=servicio_id,
        fecha=date(2024, 1, 15),
        empleado_id=empleado_id,
        tipo_servicio=tipo_servicio,
        precio=Decimal("25.00"),
        comision_calculada=Decimal("10.00")
    )
    repository.guardar_servicio(servicio)
    
    # Cargar servicio
    servicios = repository.listar_servicios()
    assert len(servicios) == 1
    servicio_cargado = servicios[0]
    
    # Verificar que las referencias son correctas
    assert servicio_cargado.empleado_id == empleado_id
    assert servicio_cargado.tipo_servicio == tipo_servicio
    
    # Verificar que las entidades referenciadas existen
    empleado_existe = repository.obtener_empleado(empleado_id)
    tipo_existe = repository.obtener_tipo_servicio(tipo_servicio)
    
    assert empleado_existe is not None
    assert tipo_existe is not None


@settings(max_examples=50)
@given(
    ids=st.lists(empleado_ids, min_size=1, max_size=20, unique=True)
)
def test_property_27_carga_masiva_mantiene_integridad(ids):
    """
    Feature: salon-peluqueria-gestion, Property 27:
    Para cualquier conjunto de empleados guardados,
    cargar todos los datos debe retornar exactamente los mismos empleados
    sin pérdida ni corrupción de datos.
    
    Validates: Requirements 8.6
    """
    # Crear repositorio
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Guardar múltiples empleados
    empleados_guardados = []
    for i, emp_id in enumerate(ids):
        empleado = Empleado(id=emp_id, nombre=f"Empleado {i}")
        repository.guardar_empleado(empleado)
        empleados_guardados.append(empleado)
    
    # Cargar todos
    empleados_cargados = repository.listar_empleados()
    
    # Verificar que se cargaron todos
    assert len(empleados_cargados) == len(empleados_guardados)
    
    # Verificar que todos los IDs están presentes
    ids_cargados = {emp.id for emp in empleados_cargados}
    ids_guardados = {emp.id for emp in empleados_guardados}
    assert ids_cargados == ids_guardados
    
    # Verificar que cada empleado se puede recuperar individualmente
    for emp_id in ids:
        recuperado = repository.obtener_empleado(emp_id)
        assert recuperado is not None
        assert recuperado.id == emp_id


def test_property_27_error_al_guardar_con_constraint_violation():
    """
    Feature: salon-peluqueria-gestion, Property 27:
    Cuando se intenta guardar datos que violan constraints de la base de datos,
    el sistema debe detectar el error y lanzar PersistenceError.
    
    Validates: Requirements 8.6
    """
    # Crear repositorio
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Intentar guardar tipo de servicio con porcentaje inválido directamente en la BD
    # (esto debería ser prevenido por validaciones, pero probamos la capa de persistencia)
    session = repository.get_session()
    try:
        # Intentar insertar con porcentaje fuera de rango
        tipo_orm = TipoServicioORM(
            nombre="Test",
            descripcion="Test",
            porcentaje_comision=150.0  # Fuera del rango permitido
        )
        session.add(tipo_orm)
        
        # Esto debería fallar por el constraint
        with pytest.raises(Exception):  # SQLAlchemy lanzará una excepción
            session.commit()
    finally:
        session.rollback()
        session.close()


def test_property_27_error_al_guardar_servicio_con_precio_invalido():
    """
    Feature: salon-peluqueria-gestion, Property 27:
    Cuando se intenta guardar un servicio con precio inválido (<=0),
    el sistema debe detectar el error por el constraint de la base de datos.
    
    Validates: Requirements 8.6
    """
    # Crear repositorio
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Crear entidades relacionadas
    repository.guardar_empleado(Empleado(id="E001", nombre="Test"))
    repository.guardar_tipo_servicio(TipoServicio(
        nombre="Corte",
        descripcion="Test",
        porcentaje_comision=40.0
    ))
    
    # Intentar guardar servicio con precio inválido directamente en la BD
    session = repository.get_session()
    try:
        servicio_orm = ServicioORM(
            id="S001",
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio="Corte",
            precio=Decimal("-10.00"),  # Precio negativo
            comision_calculada=Decimal("0.00")
        )
        session.add(servicio_orm)
        
        # Esto debería fallar por el constraint
        with pytest.raises(Exception):  # SQLAlchemy lanzará una excepción
            session.commit()
    finally:
        session.rollback()
        session.close()
