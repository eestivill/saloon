"""
Pruebas de propiedad para el módulo de validación.
"""
from datetime import date, timedelta
from decimal import Decimal
from hypothesis import given, strategies as st

from app.validators import Validator
from app.result import Ok, Err
from app.errors import ValidationError


# Property 6: Validación de Rango de Porcentaje de Comisión
@given(
    porcentaje=st.floats(
        min_value=-10000.0,
        max_value=10000.0,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_property_6_validacion_rango_porcentaje_comision(porcentaje):
    """
    **Validates: Requirements 2.2**
    
    Feature: salon-peluqueria-gestion, Property 6:
    Para cualquier porcentaje fuera del rango [0, 100], 
    intentar crear o actualizar un tipo de servicio debe fallar con un error de validación.
    
    Para cualquier porcentaje dentro del rango [0, 100], debe ser válido.
    """
    resultado = Validator.validar_porcentaje_comision(porcentaje)
    
    if 0 <= porcentaje <= 100:
        # Porcentaje válido
        assert isinstance(resultado, Ok)
        assert resultado.value == porcentaje
    else:
        # Porcentaje inválido
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "entre 0 y 100" in resultado.error.message
        assert resultado.error.field == "porcentaje_comision"


# Property 11: Validación de Precio Positivo
@given(
    precio=st.decimals(
        min_value=Decimal("-10000"),
        max_value=Decimal("10000"),
        allow_nan=False,
        allow_infinity=False,
        places=2
    )
)
def test_property_11_validacion_precio_positivo(precio):
    """
    **Validates: Requirements 3.2**
    
    Feature: salon-peluqueria-gestion, Property 11:
    Para cualquier precio menor o igual a cero, 
    intentar registrar un servicio debe fallar con un error de validación.
    
    Para cualquier precio mayor que cero, debe ser válido.
    """
    resultado = Validator.validar_precio(precio)
    
    if precio > 0:
        # Precio válido
        assert isinstance(resultado, Ok)
        assert resultado.value == precio
    else:
        # Precio inválido (menor o igual a cero)
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "mayor que cero" in resultado.error.message
        assert resultado.error.field == "precio"


# Property 25: Validación de Rango de Fechas
@given(
    fecha_inicio=st.one_of(
        st.none(),
        st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31))
    ),
    fecha_fin=st.one_of(
        st.none(),
        st.dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31))
    )
)
def test_property_25_validacion_rango_fechas(fecha_inicio, fecha_fin):
    """
    **Validates: Requirements 7.4**
    
    Feature: salon-peluqueria-gestion, Property 25:
    Para cualquier fecha_inicio y fecha_fin donde fecha_inicio > fecha_fin, 
    la operación debe fallar con un error de validación.
    
    Para cualquier otro caso (fecha_inicio <= fecha_fin, o alguna es None), debe ser válido.
    """
    resultado = Validator.validar_rango_fechas(fecha_inicio, fecha_fin)
    
    if fecha_inicio is not None and fecha_fin is not None and fecha_inicio > fecha_fin:
        # Rango inválido
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "no puede ser posterior" in resultado.error.message
        assert resultado.error.field == "fecha_inicio"
    else:
        # Rango válido
        assert isinstance(resultado, Ok)
        assert resultado.value == (fecha_inicio, fecha_fin)


# Propiedad adicional: Validación de identificador único
@given(
    id_nuevo=st.text(min_size=1, max_size=50),
    ids_existentes=st.sets(st.text(min_size=1, max_size=50), max_size=20)
)
def test_property_validacion_identificador_unico(id_nuevo, ids_existentes):
    """
    Propiedad: Un identificador es válido si y solo si no existe en el conjunto de existentes.
    """
    resultado = Validator.validar_identificador_unico(id_nuevo, ids_existentes)
    
    if id_nuevo in ids_existentes:
        # ID duplicado
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "ya existe" in resultado.error.message
        assert resultado.error.field == "id"
    else:
        # ID único
        assert isinstance(resultado, Ok)
        assert resultado.value == id_nuevo
