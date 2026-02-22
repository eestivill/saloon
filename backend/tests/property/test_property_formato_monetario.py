"""
Pruebas de propiedad para el formato monetario en reportes.
"""
from hypothesis import given, strategies as st, settings, assume
from datetime import date
from decimal import Decimal
import re

from app.manager import SalonManager
from app.repository import SQLAlchemyRepository
from app.result import Ok


# Estrategias de generación de datos

# Estrategia para generar fechas válidas
fechas_validas = st.dates(
    min_value=date(2020, 1, 1),
    max_value=date(2030, 12, 31)
)

# Estrategia para generar IDs de empleados válidos
empleado_ids_validos = st.text(
    min_size=1,
    max_size=20,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'),
        min_codepoint=ord('A'),
        max_codepoint=ord('z')
    )
).filter(lambda x: x.strip() != '')

# Estrategia para generar nombres de tipos de servicios válidos
tipo_servicio_nombres_validos = st.text(
    min_size=1,
    max_size=30,
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Zs'),
        min_codepoint=ord('A'),
        max_codepoint=ord('z')
    )
).filter(lambda x: x.strip() != '')

# Estrategia para generar precios válidos
precios_validos = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("10000.00"),
    places=2
)

# Estrategia para generar porcentajes válidos
porcentajes_validos = st.floats(min_value=0.0, max_value=100.0)


def validar_formato_monetario(valor: Decimal) -> bool:
    """
    Valida que un valor Decimal tenga formato monetario apropiado.
    
    El formato apropiado incluye:
    - Separador decimal (punto)
    - Máximo 2 decimales
    - Valor numérico válido
    
    Args:
        valor: Valor Decimal a validar
        
    Returns:
        True si el formato es válido, False en caso contrario
    """
    # Convertir a string para verificar formato
    valor_str = str(valor)
    
    # Verificar que es un número válido
    try:
        float(valor_str)
    except ValueError:
        return False
    
    # Verificar que tiene separador decimal o es entero
    if '.' in valor_str:
        partes = valor_str.split('.')
        # Verificar que tiene máximo 2 decimales
        if len(partes) == 2 and len(partes[1]) <= 2:
            return True
        return False
    else:
        # Es un entero, formato válido
        return True


@given(
    servicios=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=0,
        max_size=20
    ),
    empleado_id=empleado_ids_validos,
    tipo_servicio_nombre=tipo_servicio_nombres_validos,
    porcentaje_comision=porcentajes_validos
)
@settings(max_examples=100)
def test_property_16_formato_monetario_ingresos(
    servicios, empleado_id, tipo_servicio_nombre, porcentaje_comision
):
    """
    Feature: salon-peluqueria-gestion, Property 16:
    Para cualquier valor monetario mostrado (ingresos), el formato debe incluir
    separadores decimales apropiados.
    
    **Validates: Requirements 4.3**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    resultado_empleado = manager.crear_empleado(empleado_id, "Nombre Test")
    assume(isinstance(resultado_empleado, Ok))
    
    resultado_tipo = manager.crear_tipo_servicio(
        tipo_servicio_nombre,
        "Descripción test",
        porcentaje_comision
    )
    assume(isinstance(resultado_tipo, Ok))
    
    # Registrar servicios
    for fecha, precio in servicios:
        resultado = manager.registrar_servicio(
            fecha=fecha,
            empleado_id=empleado_id,
            tipo_servicio=tipo_servicio_nombre,
            precio=precio
        )
        assume(isinstance(resultado, Ok))
    
    # Calcular ingresos
    ingresos = manager.calcular_ingresos_totales()
    
    # Verificar formato monetario
    assert isinstance(ingresos, Decimal), "Los ingresos deben ser un Decimal"
    assert validar_formato_monetario(ingresos), f"El formato monetario de {ingresos} no es válido"
    
    # Verificar que el valor es no negativo
    assert ingresos >= Decimal("0"), "Los ingresos no pueden ser negativos"


@given(
    servicios=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=1,
        max_size=20
    ),
    empleado_id=empleado_ids_validos,
    tipo_servicio_nombre=tipo_servicio_nombres_validos,
    porcentaje_comision=porcentajes_validos
)
@settings(max_examples=100)
def test_property_16_formato_monetario_beneficios(
    servicios, empleado_id, tipo_servicio_nombre, porcentaje_comision
):
    """
    Feature: salon-peluqueria-gestion, Property 16:
    Para cualquier valor monetario mostrado (beneficios), el formato debe incluir
    separadores decimales apropiados.
    
    **Validates: Requirements 4.3**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    resultado_empleado = manager.crear_empleado(empleado_id, "Nombre Test")
    assume(isinstance(resultado_empleado, Ok))
    
    resultado_tipo = manager.crear_tipo_servicio(
        tipo_servicio_nombre,
        "Descripción test",
        porcentaje_comision
    )
    assume(isinstance(resultado_tipo, Ok))
    
    # Registrar servicios
    for fecha, precio in servicios:
        resultado = manager.registrar_servicio(
            fecha=fecha,
            empleado_id=empleado_id,
            tipo_servicio=tipo_servicio_nombre,
            precio=precio
        )
        assume(isinstance(resultado, Ok))
    
    # Calcular beneficios
    beneficios = manager.calcular_beneficios()
    
    # Verificar formato monetario
    assert isinstance(beneficios, Decimal), "Los beneficios deben ser un Decimal"
    assert validar_formato_monetario(beneficios), f"El formato monetario de {beneficios} no es válido"


@given(
    servicios=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=0,
        max_size=20
    ),
    empleado_id=empleado_ids_validos,
    tipo_servicio_nombre=tipo_servicio_nombres_validos,
    porcentaje_comision=porcentajes_validos
)
@settings(max_examples=100)
def test_property_16_formato_monetario_pago_empleado(
    servicios, empleado_id, tipo_servicio_nombre, porcentaje_comision
):
    """
    Feature: salon-peluqueria-gestion, Property 16:
    Para cualquier valor monetario mostrado (pago de empleado), el formato debe incluir
    separadores decimales apropiados.
    
    **Validates: Requirements 4.3**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    resultado_empleado = manager.crear_empleado(empleado_id, "Nombre Test")
    assume(isinstance(resultado_empleado, Ok))
    
    resultado_tipo = manager.crear_tipo_servicio(
        tipo_servicio_nombre,
        "Descripción test",
        porcentaje_comision
    )
    assume(isinstance(resultado_tipo, Ok))
    
    # Registrar servicios
    for fecha, precio in servicios:
        resultado = manager.registrar_servicio(
            fecha=fecha,
            empleado_id=empleado_id,
            tipo_servicio=tipo_servicio_nombre,
            precio=precio
        )
        assume(isinstance(resultado, Ok))
    
    # Calcular pago del empleado
    desglose = manager.calcular_pago_empleado(empleado_id)
    
    # Verificar formato monetario del total
    assert isinstance(desglose.total, Decimal), "El total debe ser un Decimal"
    assert validar_formato_monetario(desglose.total), f"El formato monetario de {desglose.total} no es válido"
    
    # Verificar formato monetario de cada servicio en el desglose
    for servicio_detalle in desglose.servicios:
        assert isinstance(servicio_detalle.precio, Decimal), "El precio debe ser un Decimal"
        assert validar_formato_monetario(servicio_detalle.precio), f"El formato monetario del precio {servicio_detalle.precio} no es válido"
        
        assert isinstance(servicio_detalle.comision, Decimal), "La comisión debe ser un Decimal"
        assert validar_formato_monetario(servicio_detalle.comision), f"El formato monetario de la comisión {servicio_detalle.comision} no es válido"
    
    # Verificar que el total es no negativo
    assert desglose.total >= Decimal("0"), "El pago no puede ser negativo"


@given(
    precio=precios_validos,
    porcentaje_comision=porcentajes_validos,
    empleado_id=empleado_ids_validos,
    tipo_servicio_nombre=tipo_servicio_nombres_validos
)
@settings(max_examples=100)
def test_property_16_formato_monetario_comision_calculada(
    precio, porcentaje_comision, empleado_id, tipo_servicio_nombre
):
    """
    Feature: salon-peluqueria-gestion, Property 16:
    Para cualquier comisión calculada, el formato debe incluir separadores decimales apropiados.
    
    **Validates: Requirements 4.3**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    resultado_empleado = manager.crear_empleado(empleado_id, "Nombre Test")
    assume(isinstance(resultado_empleado, Ok))
    
    resultado_tipo = manager.crear_tipo_servicio(
        tipo_servicio_nombre,
        "Descripción test",
        porcentaje_comision
    )
    assume(isinstance(resultado_tipo, Ok))
    
    # Registrar servicio
    resultado = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id=empleado_id,
        tipo_servicio=tipo_servicio_nombre,
        precio=precio
    )
    assume(isinstance(resultado, Ok))
    
    servicio = resultado.value
    
    # Verificar formato monetario de la comisión calculada
    assert isinstance(servicio.comision_calculada, Decimal), "La comisión calculada debe ser un Decimal"
    assert validar_formato_monetario(servicio.comision_calculada), f"El formato monetario de la comisión {servicio.comision_calculada} no es válido"
    
    # Verificar que la comisión es no negativa
    assert servicio.comision_calculada >= Decimal("0"), "La comisión no puede ser negativa"
    
    # Verificar que la comisión no excede el precio
    assert servicio.comision_calculada <= precio, "La comisión no puede exceder el precio del servicio"
