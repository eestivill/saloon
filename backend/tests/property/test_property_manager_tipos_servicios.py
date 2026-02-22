"""
Pruebas de propiedad para la gestión de tipos de servicios en SalonManager.
"""
import pytest
from hypothesis import given, strategies as st, settings

from app.manager import SalonManager
from app.repository import SQLAlchemyRepository
from app.result import Ok, Err
from app.errors import ValidationError, DuplicateError


# Estrategias para generar datos válidos
tipo_servicio_nombre_strategy = st.text(
    min_size=1,
    max_size=50,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Zs'),
        whitelist_characters='áéíóúñÁÉÍÓÚÑ'
    )
)

tipo_servicio_descripcion_strategy = st.text(
    min_size=1,
    max_size=200,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Zs', 'Nd', 'Po'),
        whitelist_characters='áéíóúñÁÉÍÓÚÑ'
    )
)

porcentaje_valido_strategy = st.floats(
    min_value=0.0,
    max_value=100.0,
    allow_nan=False,
    allow_infinity=False
)

porcentaje_invalido_strategy = st.one_of(
    st.floats(min_value=-1000.0, max_value=-0.01, allow_nan=False, allow_infinity=False),
    st.floats(min_value=100.01, max_value=1000.0, allow_nan=False, allow_infinity=False)
)


@pytest.fixture
def manager():
    """Fixture que proporciona un SalonManager con base de datos en memoria."""
    repository = SQLAlchemyRepository("sqlite:///:memory:")
    return SalonManager(repository)


@given(
    nombre=tipo_servicio_nombre_strategy,
    descripcion=tipo_servicio_descripcion_strategy,
    porcentaje=porcentaje_valido_strategy
)
@settings(max_examples=100)
def test_property_5_creacion_tipos_servicio_con_atributos_validos(nombre, descripcion, porcentaje):
    """
    **Validates: Requirements 2.1**
    
    Property 5: Creación de Tipos de Servicio con Atributos Válidos
    
    Para cualquier nombre único, descripción y porcentaje de comisión válido (0-100), 
    crear un tipo de servicio debe resultar en un tipo almacenado con exactamente esos atributos.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Crear tipo de servicio
    resultado = manager.crear_tipo_servicio(nombre, descripcion, porcentaje)
    
    # Verificar que se creó exitosamente
    assert isinstance(resultado, Ok)
    tipo = resultado.value
    assert tipo.nombre == nombre
    assert tipo.descripcion == descripcion
    assert tipo.porcentaje_comision == porcentaje
    
    # Verificar que está almacenado con los mismos atributos
    tipo_recuperado = manager.obtener_tipo_servicio(nombre)
    assert tipo_recuperado is not None
    assert tipo_recuperado.nombre == nombre
    assert tipo_recuperado.descripcion == descripcion
    assert tipo_recuperado.porcentaje_comision == porcentaje


@given(
    porcentaje=porcentaje_invalido_strategy
)
@settings(max_examples=100)
def test_property_6_validacion_rango_porcentaje_comision(porcentaje):
    """
    **Validates: Requirements 2.2**
    
    Property 6: Validación de Rango de Porcentaje de Comisión
    
    Para cualquier porcentaje fuera del rango [0, 100], intentar crear o actualizar 
    un tipo de servicio debe fallar con un error de validación.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Intentar crear con porcentaje inválido
    resultado_crear = manager.crear_tipo_servicio(
        "Servicio Test",
        "Descripción",
        porcentaje
    )
    
    assert isinstance(resultado_crear, Err)
    assert isinstance(resultado_crear.error, ValidationError)
    
    # Crear un tipo de servicio válido primero
    manager.crear_tipo_servicio("Servicio Valido", "Descripción", 50.0)
    
    # Intentar actualizar con porcentaje inválido
    resultado_actualizar = manager.actualizar_tipo_servicio(
        "Servicio Valido",
        porcentaje
    )
    
    assert isinstance(resultado_actualizar, Err)
    assert isinstance(resultado_actualizar.error, ValidationError)
    
    # Verificar que el tipo de servicio no se modificó
    tipo = manager.obtener_tipo_servicio("Servicio Valido")
    assert tipo.porcentaje_comision == 50.0


@given(
    nombre=tipo_servicio_nombre_strategy,
    descripcion1=tipo_servicio_descripcion_strategy,
    descripcion2=tipo_servicio_descripcion_strategy,
    porcentaje1=porcentaje_valido_strategy,
    porcentaje2=porcentaje_valido_strategy
)
@settings(max_examples=100)
def test_property_7_unicidad_nombres_tipos_servicio(
    nombre, descripcion1, descripcion2, porcentaje1, porcentaje2
):
    """
    **Validates: Requirements 2.3**
    
    Property 7: Unicidad de Nombres de Tipos de Servicio
    
    Para cualquier sistema con tipos de servicio existentes, intentar crear un segundo 
    tipo con un nombre ya existente debe fallar.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Crear primer tipo de servicio
    resultado1 = manager.crear_tipo_servicio(nombre, descripcion1, porcentaje1)
    assert isinstance(resultado1, Ok)
    
    # Intentar crear segundo tipo con mismo nombre
    resultado2 = manager.crear_tipo_servicio(nombre, descripcion2, porcentaje2)
    
    # Verificar que falla
    assert isinstance(resultado2, Err)
    assert isinstance(resultado2.error, DuplicateError)
    assert resultado2.error.identifier == nombre
    
    # Verificar que el primer tipo permanece sin cambios
    tipo_original = manager.obtener_tipo_servicio(nombre)
    assert tipo_original is not None
    assert tipo_original.descripcion == descripcion1
    assert tipo_original.porcentaje_comision == porcentaje1


@given(
    tipos_servicios=st.lists(
        st.tuples(
            tipo_servicio_nombre_strategy,
            tipo_servicio_descripcion_strategy,
            porcentaje_valido_strategy
        ),
        min_size=0,
        max_size=20,
        unique_by=lambda x: x[0]  # Nombres únicos
    )
)
@settings(max_examples=100)
def test_property_8_consulta_completa_tipos_servicios(tipos_servicios):
    """
    **Validates: Requirements 2.5**
    
    Property 8: Consulta Completa de Tipos de Servicios
    
    Para cualquier conjunto de tipos de servicios creados, consultar la lista 
    debe retornar todos y solo esos tipos.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Crear todos los tipos de servicios
    tipos_creados = []
    for nombre, descripcion, porcentaje in tipos_servicios:
        resultado = manager.crear_tipo_servicio(nombre, descripcion, porcentaje)
        if isinstance(resultado, Ok):
            tipos_creados.append((nombre, descripcion, porcentaje))
    
    # Listar tipos de servicios
    lista_tipos = manager.listar_tipos_servicios()
    
    # Verificar que la cantidad es correcta
    assert len(lista_tipos) == len(tipos_creados)
    
    # Verificar que todos los tipos creados están en la lista
    nombres_en_lista = {tipo.nombre for tipo in lista_tipos}
    nombres_creados = {nombre for nombre, _, _ in tipos_creados}
    assert nombres_en_lista == nombres_creados
    
    # Verificar que cada tipo tiene los atributos correctos
    tipos_dict = {nombre: (descripcion, porcentaje) for nombre, descripcion, porcentaje in tipos_creados}
    for tipo in lista_tipos:
        descripcion_esperada, porcentaje_esperado = tipos_dict[tipo.nombre]
        assert tipo.descripcion == descripcion_esperada
        assert tipo.porcentaje_comision == porcentaje_esperado


@given(
    nombre=tipo_servicio_nombre_strategy,
    descripcion=tipo_servicio_descripcion_strategy,
    porcentaje_original=porcentaje_valido_strategy,
    porcentaje_nuevo=porcentaje_valido_strategy
)
@settings(max_examples=100)
def test_property_9_actualizacion_porcentaje_comision(
    nombre, descripcion, porcentaje_original, porcentaje_nuevo
):
    """
    **Validates: Requirements 2.6**
    
    Property 9: Actualización de Porcentaje de Comisión
    
    Para cualquier tipo de servicio existente y porcentaje válido, actualizar el 
    porcentaje debe reflejarse en consultas posteriores y en nuevos servicios registrados.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Crear tipo de servicio
    resultado_crear = manager.crear_tipo_servicio(nombre, descripcion, porcentaje_original)
    assert isinstance(resultado_crear, Ok)
    
    # Actualizar porcentaje
    resultado_actualizar = manager.actualizar_tipo_servicio(nombre, porcentaje_nuevo)
    assert isinstance(resultado_actualizar, Ok)
    
    tipo_actualizado = resultado_actualizar.value
    
    # Verificar que el nombre y descripción se preservan
    assert tipo_actualizado.nombre == nombre
    assert tipo_actualizado.descripcion == descripcion
    
    # Verificar que el porcentaje se actualizó
    assert tipo_actualizado.porcentaje_comision == porcentaje_nuevo
    
    # Verificar que la actualización se refleja en consultas posteriores
    tipo_recuperado = manager.obtener_tipo_servicio(nombre)
    assert tipo_recuperado is not None
    assert tipo_recuperado.nombre == nombre
    assert tipo_recuperado.descripcion == descripcion
    assert tipo_recuperado.porcentaje_comision == porcentaje_nuevo
    
    # Verificar que solo hay un tipo de servicio (no se duplicó)
    lista_tipos = manager.listar_tipos_servicios()
    assert len(lista_tipos) == 1
    assert lista_tipos[0].nombre == nombre
