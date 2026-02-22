"""
Pruebas de propiedad para la gestión de empleados en SalonManager.
"""
import pytest
from hypothesis import given, strategies as st, settings

from app.manager import SalonManager
from app.repository import SQLAlchemyRepository
from app.result import Ok, Err
from app.errors import DuplicateError


# Estrategias para generar datos válidos
empleado_id_strategy = st.text(
    min_size=1,
    max_size=50,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'),
        whitelist_characters='-_'
    )
)

empleado_nombre_strategy = st.text(
    min_size=1,
    max_size=100,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Zs'),
        whitelist_characters='áéíóúñÁÉÍÓÚÑ'
    )
)


@pytest.fixture
def manager():
    """Fixture que proporciona un SalonManager con base de datos en memoria."""
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    return SalonManager(repository)


@given(
    id_empleado=empleado_id_strategy,
    nombre=empleado_nombre_strategy
)
@settings(max_examples=100)
def test_property_1_creacion_empleados_con_atributos_validos(id_empleado, nombre):
    """
    **Validates: Requirements 1.1**
    
    Property 1: Creación de Empleados con Atributos Válidos
    
    Para cualquier nombre e identificador únicos proporcionados, 
    crear un empleado debe resultar en un empleado almacenado con exactamente esos atributos.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Crear empleado
    resultado = manager.crear_empleado(id_empleado, nombre)
    
    # Verificar que se creó exitosamente
    assert isinstance(resultado, Ok)
    empleado = resultado.value
    assert empleado.id == id_empleado
    assert empleado.nombre == nombre
    
    # Verificar que está almacenado con los mismos atributos
    empleado_recuperado = manager.obtener_empleado(id_empleado)
    assert empleado_recuperado is not None
    assert empleado_recuperado.id == id_empleado
    assert empleado_recuperado.nombre == nombre


@given(
    id_empleado=empleado_id_strategy,
    nombre1=empleado_nombre_strategy,
    nombre2=empleado_nombre_strategy
)
@settings(max_examples=100)
def test_property_2_unicidad_identificadores_empleados(id_empleado, nombre1, nombre2):
    """
    **Validates: Requirements 1.2**
    
    Property 2: Unicidad de Identificadores de Empleados
    
    Para cualquier sistema con empleados existentes, intentar crear un segundo empleado 
    con un identificador ya existente debe fallar, mientras que el primer empleado 
    permanece sin cambios.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Crear primer empleado
    resultado1 = manager.crear_empleado(id_empleado, nombre1)
    assert isinstance(resultado1, Ok)
    
    # Intentar crear segundo empleado con mismo ID
    resultado2 = manager.crear_empleado(id_empleado, nombre2)
    
    # Verificar que falla
    assert isinstance(resultado2, Err)
    assert isinstance(resultado2.error, DuplicateError)
    assert resultado2.error.identifier == id_empleado
    
    # Verificar que el primer empleado permanece sin cambios
    empleado_original = manager.obtener_empleado(id_empleado)
    assert empleado_original is not None
    assert empleado_original.nombre == nombre1


@given(
    empleados=st.lists(
        st.tuples(empleado_id_strategy, empleado_nombre_strategy),
        min_size=0,
        max_size=20,
        unique_by=lambda x: x[0]  # IDs únicos
    )
)
@settings(max_examples=100)
def test_property_3_consulta_completa_empleados(empleados):
    """
    **Validates: Requirements 1.4**
    
    Property 3: Consulta Completa de Empleados
    
    Para cualquier conjunto de empleados creados, consultar la lista de empleados 
    debe retornar todos y solo esos empleados.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Crear todos los empleados
    empleados_creados = []
    for id_emp, nombre in empleados:
        resultado = manager.crear_empleado(id_emp, nombre)
        if isinstance(resultado, Ok):
            empleados_creados.append((id_emp, nombre))
    
    # Listar empleados
    lista_empleados = manager.listar_empleados()
    
    # Verificar que la cantidad es correcta
    assert len(lista_empleados) == len(empleados_creados)
    
    # Verificar que todos los empleados creados están en la lista
    ids_en_lista = {emp.id for emp in lista_empleados}
    ids_creados = {id_emp for id_emp, _ in empleados_creados}
    assert ids_en_lista == ids_creados
    
    # Verificar que cada empleado tiene los atributos correctos
    empleados_dict = {id_emp: nombre for id_emp, nombre in empleados_creados}
    for empleado in lista_empleados:
        assert empleado.nombre == empleados_dict[empleado.id]


@given(
    id_empleado=empleado_id_strategy,
    nombre_original=empleado_nombre_strategy,
    nombre_nuevo=empleado_nombre_strategy
)
@settings(max_examples=100)
def test_property_4_actualizacion_empleados_preserva_identidad(
    id_empleado, nombre_original, nombre_nuevo
):
    """
    **Validates: Requirements 1.5**
    
    Property 4: Actualización de Empleados Preserva Identidad
    
    Para cualquier empleado existente, actualizar su nombre debe preservar su 
    identificador y reflejar el nuevo nombre en consultas posteriores.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Crear empleado
    resultado_crear = manager.crear_empleado(id_empleado, nombre_original)
    assert isinstance(resultado_crear, Ok)
    
    # Actualizar empleado
    resultado_actualizar = manager.actualizar_empleado(id_empleado, nombre_nuevo)
    assert isinstance(resultado_actualizar, Ok)
    
    empleado_actualizado = resultado_actualizar.value
    
    # Verificar que el ID se preserva
    assert empleado_actualizado.id == id_empleado
    
    # Verificar que el nombre se actualizó
    assert empleado_actualizado.nombre == nombre_nuevo
    
    # Verificar que la actualización se refleja en consultas posteriores
    empleado_recuperado = manager.obtener_empleado(id_empleado)
    assert empleado_recuperado is not None
    assert empleado_recuperado.id == id_empleado
    assert empleado_recuperado.nombre == nombre_nuevo
    
    # Verificar que solo hay un empleado (no se duplicó)
    lista_empleados = manager.listar_empleados()
    assert len(lista_empleados) == 1
    assert lista_empleados[0].id == id_empleado
