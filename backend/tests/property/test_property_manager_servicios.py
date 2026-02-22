"""
Pruebas de propiedad para la gestión de servicios en SalonManager.
"""
from hypothesis import given, strategies as st, settings, assume
from datetime import date
from decimal import Decimal

from app.manager import SalonManager
from app.repository import SQLAlchemyRepository
from app.result import Ok, Err
from app.errors import ValidationError, NotFoundError


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


@given(
    fecha=fechas_validas,
    empleado_id=empleado_ids_validos,
    tipo_servicio_nombre=tipo_servicio_nombres_validos,
    precio=precios_validos,
    porcentaje_comision=porcentajes_validos
)
@settings(max_examples=100)
def test_property_10_registro_servicio_con_todos_atributos(
    fecha, empleado_id, tipo_servicio_nombre, precio, porcentaje_comision
):
    """
    Feature: salon-peluqueria-gestion, Property 10:
    Para cualquier fecha, empleado existente, tipo de servicio existente y precio válido,
    registrar un servicio debe crear un registro con todos esos atributos más un ID único
    y la comisión calculada.
    
    **Validates: Requirements 3.1**
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
        fecha=fecha,
        empleado_id=empleado_id,
        tipo_servicio=tipo_servicio_nombre,
        precio=precio
    )
    
    # Verificar que el resultado es exitoso
    assert isinstance(resultado, Ok)
    servicio = resultado.value
    
    # Verificar que todos los atributos están presentes
    assert servicio.id is not None
    assert len(servicio.id) > 0
    assert servicio.fecha == fecha
    assert servicio.empleado_id == empleado_id
    assert servicio.tipo_servicio == tipo_servicio_nombre
    assert servicio.precio == precio
    assert servicio.comision_calculada is not None
    
    # Verificar que la comisión está calculada correctamente (redondeada a 2 decimales)
    comision_esperada = (precio * Decimal(str(porcentaje_comision)) / Decimal("100")).quantize(Decimal("0.01"))
    assert servicio.comision_calculada == comision_esperada


@given(
    fecha=fechas_validas,
    empleado_id_valido=empleado_ids_validos,
    empleado_id_invalido=empleado_ids_validos,
    tipo_servicio_valido=tipo_servicio_nombres_validos,
    tipo_servicio_invalido=tipo_servicio_nombres_validos,
    precio=precios_validos,
    porcentaje_comision=porcentajes_validos
)
@settings(max_examples=100)
def test_property_12_validacion_integridad_referencial(
    fecha, empleado_id_valido, empleado_id_invalido,
    tipo_servicio_valido, tipo_servicio_invalido,
    precio, porcentaje_comision
):
    """
    Feature: salon-peluqueria-gestion, Property 12:
    Para cualquier intento de registrar un servicio con un empleado_id o tipo_servicio
    que no exista en el sistema, la operación debe fallar con un error de referencia no encontrada.
    
    **Validates: Requirements 3.3, 3.4**
    """
    # Asegurar que los IDs inválidos son diferentes de los válidos
    assume(empleado_id_invalido != empleado_id_valido)
    assume(tipo_servicio_invalido != tipo_servicio_valido)
    
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear solo empleado válido y tipo de servicio válido
    resultado_empleado = manager.crear_empleado(empleado_id_valido, "Nombre Test")
    assume(isinstance(resultado_empleado, Ok))
    
    resultado_tipo = manager.crear_tipo_servicio(
        tipo_servicio_valido,
        "Descripción test",
        porcentaje_comision
    )
    assume(isinstance(resultado_tipo, Ok))
    
    # Test 1: Intentar registrar con empleado inexistente
    resultado_empleado_invalido = manager.registrar_servicio(
        fecha=fecha,
        empleado_id=empleado_id_invalido,
        tipo_servicio=tipo_servicio_valido,
        precio=precio
    )
    
    assert isinstance(resultado_empleado_invalido, Err)
    assert isinstance(resultado_empleado_invalido.error, NotFoundError)
    assert resultado_empleado_invalido.error.entity == "Empleado"
    assert resultado_empleado_invalido.error.identifier == empleado_id_invalido
    
    # Test 2: Intentar registrar con tipo de servicio inexistente
    resultado_tipo_invalido = manager.registrar_servicio(
        fecha=fecha,
        empleado_id=empleado_id_valido,
        tipo_servicio=tipo_servicio_invalido,
        precio=precio
    )
    
    assert isinstance(resultado_tipo_invalido, Err)
    assert isinstance(resultado_tipo_invalido.error, NotFoundError)
    assert resultado_tipo_invalido.error.entity == "TipoServicio"
    assert resultado_tipo_invalido.error.identifier == tipo_servicio_invalido


@given(
    fecha=fechas_validas,
    empleado_id=empleado_ids_validos,
    tipo_servicio_nombre=tipo_servicio_nombres_validos,
    precio=precios_validos,
    porcentaje_comision=porcentajes_validos
)
@settings(max_examples=100)
def test_property_18_calculo_comision_individual(
    fecha, empleado_id, tipo_servicio_nombre, precio, porcentaje_comision
):
    """
    Feature: salon-peluqueria-gestion, Property 18:
    Para cualquier servicio registrado, la comisión calculada debe ser igual al precio
    del servicio multiplicado por el porcentaje de comisión del tipo de servicio asociado
    (dividido por 100).
    
    **Validates: Requirements 2.7, 5.1**
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
        fecha=fecha,
        empleado_id=empleado_id,
        tipo_servicio=tipo_servicio_nombre,
        precio=precio
    )
    
    # Verificar que el resultado es exitoso
    assert isinstance(resultado, Ok)
    servicio = resultado.value
    
    # Calcular comisión esperada (redondeada a 2 decimales)
    comision_esperada = (precio * Decimal(str(porcentaje_comision)) / Decimal("100")).quantize(Decimal("0.01"))
    
    # Verificar que la comisión calculada es correcta
    assert servicio.comision_calculada == comision_esperada
    
    # Verificar que la comisión está dentro del rango válido [0, precio]
    assert Decimal("0") <= servicio.comision_calculada <= precio


@given(
    precio=st.decimals(
        min_value=Decimal("-1000.00"),
        max_value=Decimal("0.00"),
        places=2
    )
)
@settings(max_examples=100)
def test_property_11_validacion_precio_positivo(precio):
    """
    Feature: salon-peluqueria-gestion, Property 11:
    Para cualquier precio menor o igual a cero, intentar registrar un servicio
    debe fallar con un error de validación.
    
    **Validates: Requirements 3.2**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado("E001", "Test")
    manager.crear_tipo_servicio("Corte", "Desc", 40.0)
    
    # Intentar registrar servicio con precio inválido
    resultado = manager.registrar_servicio(
        fecha=date(2024, 1, 15),
        empleado_id="E001",
        tipo_servicio="Corte",
        precio=precio
    )
    
    # Verificar que falla con error de validación
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, ValidationError)


# Property tests for service queries and financial calculations

@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            empleado_ids_validos,
            precios_validos
        ),
        min_size=0,
        max_size=20
    ),
    fecha_inicio=fechas_validas,
    fecha_fin=fechas_validas
)
@settings(max_examples=100)
def test_property_14_filtrado_ingresos_por_rango_fechas(servicios_data, fecha_inicio, fecha_fin):
    """
    Feature: salon-peluqueria-gestion, Property 14:
    Para cualquier conjunto de servicios y rango de fechas [fecha_inicio, fecha_fin],
    los ingresos calculados deben incluir solo servicios cuya fecha esté dentro del rango inclusivo.
    
    **Validates: Requirements 4.2, 7.1, 7.2, 7.3**
    """
    # Asegurar que fecha_inicio <= fecha_fin
    if fecha_inicio > fecha_fin:
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio
    
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear tipo de servicio
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Crear empleados únicos y registrar servicios
    empleados_creados = set()
    suma_esperada = Decimal("0")
    
    for fecha, empleado_id, precio in servicios_data:
        # Crear empleado si no existe
        if empleado_id not in empleados_creados:
            resultado = manager.crear_empleado(empleado_id, f"Empleado {empleado_id}")
            if isinstance(resultado, Ok):
                empleados_creados.add(empleado_id)
            else:
                continue
        
        # Registrar servicio
        manager.registrar_servicio(fecha, empleado_id, "Corte", precio)
        
        # Sumar al total esperado si está en el rango
        if fecha_inicio <= fecha <= fecha_fin:
            suma_esperada += precio
    
    # Calcular ingresos filtrados
    ingresos = manager.calcular_ingresos_totales(fecha_inicio, fecha_fin)
    
    # Verificar que coincide con la suma esperada
    assert ingresos == suma_esperada


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=1,
        max_size=20
    ),
    empleado_id=empleado_ids_validos
)
@settings(max_examples=100)
def test_property_22_filtrado_servicios_por_empleado(servicios_data, empleado_id):
    """
    Feature: salon-peluqueria-gestion, Property 22:
    Para cualquier empleado_id y conjunto de servicios, consultar servicios por empleado
    debe retornar todos y solo los servicios donde empleado_id coincide.
    
    **Validates: Requirements 6.1**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleados y tipo de servicio
    manager.crear_empleado(empleado_id, "Empleado Principal")
    manager.crear_empleado("OTRO", "Otro Empleado")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Registrar servicios para el empleado principal
    for fecha, precio in servicios_data:
        manager.registrar_servicio(fecha, empleado_id, "Corte", precio)
    
    # Registrar algunos servicios para otro empleado
    manager.registrar_servicio(date(2024, 1, 1), "OTRO", "Corte", Decimal("25.00"))
    manager.registrar_servicio(date(2024, 1, 2), "OTRO", "Corte", Decimal("30.00"))
    
    # Obtener servicios del empleado principal
    servicios = manager.obtener_servicios(empleado_id=empleado_id)
    
    # Verificar que todos los servicios son del empleado correcto
    assert len(servicios) == len(servicios_data)
    assert all(s.empleado_id == empleado_id for s in servicios)


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=2,
        max_size=20
    ),
    empleado_id=empleado_ids_validos
)
@settings(max_examples=100)
def test_property_23_ordenamiento_descendente_por_fecha(servicios_data, empleado_id):
    """
    Feature: salon-peluqueria-gestion, Property 23:
    Para cualquier lista de servicios retornada, los servicios deben estar ordenados
    por fecha de forma descendente (más recientes primero).
    
    **Validates: Requirements 6.2**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado(empleado_id, "Empleado Test")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Registrar servicios
    for fecha, precio in servicios_data:
        manager.registrar_servicio(fecha, empleado_id, "Corte", precio)
    
    # Obtener servicios
    servicios = manager.obtener_servicios()
    
    # Verificar ordenamiento descendente
    if len(servicios) >= 2:
        for i in range(len(servicios) - 1):
            assert servicios[i].fecha >= servicios[i + 1].fecha


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            tipo_servicio_nombres_validos,
            precios_validos,
            porcentajes_validos
        ),
        min_size=1,
        max_size=20
    ),
    empleado_id=empleado_ids_validos
)
@settings(max_examples=100)
def test_property_24_servicios_contienen_informacion_completa(servicios_data, empleado_id):
    """
    Feature: salon-peluqueria-gestion, Property 24:
    Para cualquier servicio en una consulta, debe incluir fecha, tipo de servicio,
    precio y comisión calculada.
    
    **Validates: Requirements 6.4**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado
    manager.crear_empleado(empleado_id, "Empleado Test")
    
    # Crear tipos de servicios únicos y registrar servicios
    tipos_creados = set()
    
    for fecha, tipo_nombre, precio, porcentaje in servicios_data:
        # Crear tipo de servicio si no existe
        if tipo_nombre not in tipos_creados:
            resultado = manager.crear_tipo_servicio(tipo_nombre, "Descripción", porcentaje)
            if isinstance(resultado, Ok):
                tipos_creados.add(tipo_nombre)
            else:
                continue
        
        # Registrar servicio
        manager.registrar_servicio(fecha, empleado_id, tipo_nombre, precio)
    
    # Obtener servicios
    servicios = manager.obtener_servicios()
    
    # Verificar que cada servicio tiene información completa
    for servicio in servicios:
        assert servicio.fecha is not None
        assert servicio.tipo_servicio is not None
        assert servicio.tipo_servicio != ""
        assert servicio.precio is not None
        assert servicio.precio > 0
        assert servicio.comision_calculada is not None
        assert servicio.comision_calculada >= 0


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=0,
        max_size=20
    ),
    empleado_id=empleado_ids_validos
)
@settings(max_examples=20)
def test_property_13_calculo_correcto_ingresos_totales(servicios_data, empleado_id):
    """
    Feature: salon-peluqueria-gestion, Property 13:
    Para cualquier conjunto de servicios registrados, la suma de ingresos totales
    debe ser igual a la suma de los precios de todos los servicios.
    
    **Validates: Requirements 4.1**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado(empleado_id, "Empleado Test")
    manager.crear_tipo_servicio("Corte", "Corte básico", 40.0)
    
    # Registrar servicios y calcular suma esperada
    suma_esperada = Decimal("0")
    for fecha, precio in servicios_data:
        manager.registrar_servicio(fecha, empleado_id, "Corte", precio)
        suma_esperada += precio
    
    # Calcular ingresos
    ingresos = manager.calcular_ingresos_totales()
    
    # Verificar que coincide con la suma esperada
    assert ingresos == suma_esperada


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos,
            porcentajes_validos
        ),
        min_size=1,
        max_size=20
    ),
    empleado_id=empleado_ids_validos
)
@settings(max_examples=20)
def test_property_15_calculo_beneficios_como_ingresos_menos_comisiones(servicios_data, empleado_id):
    """
    Feature: salon-peluqueria-gestion, Property 15:
    Para cualquier conjunto de servicios en un período, los beneficios deben ser iguales
    a la suma de precios menos la suma de comisiones de todos los servicios en ese período.
    
    **Validates: Requirements 4.2**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado
    manager.crear_empleado(empleado_id, "Empleado Test")
    
    # Registrar servicios con diferentes porcentajes de comisión
    for i, (fecha, precio, porcentaje) in enumerate(servicios_data):
        # Crear tipo de servicio único para cada servicio
        tipo_nombre = f"Servicio{i}"
        manager.crear_tipo_servicio(tipo_nombre, "Descripción", porcentaje)
        
        # Registrar servicio
        manager.registrar_servicio(fecha, empleado_id, tipo_nombre, precio)
    
    # Obtener los servicios registrados para calcular la suma esperada
    servicios_registrados = manager.obtener_servicios()
    suma_ingresos = sum((s.precio for s in servicios_registrados), Decimal("0"))
    suma_comisiones = sum((s.comision_calculada for s in servicios_registrados), Decimal("0"))
    
    # Calcular beneficios
    beneficios = manager.calcular_beneficios()
    beneficios_esperados = suma_ingresos - suma_comisiones
    
    # Verificar que coincide exactamente (sin tolerancia, ya que usamos los mismos valores)
    assert beneficios == beneficios_esperados


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=1,
        max_size=20
    ),
    empleado_id=empleado_ids_validos,
    porcentaje_comision=porcentajes_validos
)
@settings(max_examples=20)
def test_property_17_ingresos_se_actualizan_inmediatamente(servicios_data, empleado_id, porcentaje_comision):
    """
    Feature: salon-peluqueria-gestion, Property 17:
    Para cualquier estado del sistema, agregar un nuevo servicio debe incrementar
    los ingresos totales inmediatamente por el precio de ese servicio.
    
    **Validates: Requirements 4.5**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado(empleado_id, "Empleado Test")
    manager.crear_tipo_servicio("Corte", "Corte básico", porcentaje_comision)
    
    # Registrar servicios uno por uno y verificar que los ingresos se actualizan
    ingresos_acumulados = Decimal("0")
    
    for fecha, precio in servicios_data:
        # Registrar servicio
        manager.registrar_servicio(fecha, empleado_id, "Corte", precio)
        ingresos_acumulados += precio
        
        # Verificar que los ingresos se actualizaron inmediatamente
        ingresos_actuales = manager.calcular_ingresos_totales()
        assert ingresos_actuales == ingresos_acumulados


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=1,
        max_size=20
    ),
    empleado_id=empleado_ids_validos,
    porcentaje_comision=porcentajes_validos
)
@settings(max_examples=100)
def test_property_19_suma_comisiones_por_empleado(servicios_data, empleado_id, porcentaje_comision):
    """
    Feature: salon-peluqueria-gestion, Property 19:
    Para cualquier empleado con servicios registrados, el pago total debe ser igual
    a la suma de todas las comisiones de sus servicios.
    
    **Validates: Requirements 5.2**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado(empleado_id, "Empleado Test")
    manager.crear_tipo_servicio("Corte", "Corte básico", porcentaje_comision)
    
    # Registrar servicios y calcular suma de comisiones esperada
    suma_comisiones_esperada = Decimal("0")
    
    for fecha, precio in servicios_data:
        resultado = manager.registrar_servicio(fecha, empleado_id, "Corte", precio)
        # Usar la comisión redondeada que se almacenó en la base de datos
        if isinstance(resultado, Ok):
            suma_comisiones_esperada += resultado.value.comision_calculada
    
    # Calcular pago del empleado
    desglose = manager.calcular_pago_empleado(empleado_id)
    
    # Verificar que el total coincide exactamente con la suma de comisiones almacenadas
    assert desglose.total == suma_comisiones_esperada


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            precios_validos
        ),
        min_size=1,
        max_size=20
    ),
    empleado_id=empleado_ids_validos,
    porcentaje_comision=porcentajes_validos,
    fecha_inicio=fechas_validas,
    fecha_fin=fechas_validas
)
@settings(max_examples=100)
def test_property_20_filtrado_pagos_por_periodo(servicios_data, empleado_id, porcentaje_comision, fecha_inicio, fecha_fin):
    """
    Feature: salon-peluqueria-gestion, Property 20:
    Para cualquier empleado y rango de fechas, el pago calculado debe incluir solo
    las comisiones de servicios dentro del rango especificado.
    
    **Validates: Requirements 5.3**
    """
    # Asegurar que fecha_inicio <= fecha_fin
    if fecha_inicio > fecha_fin:
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio
    
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado(empleado_id, "Empleado Test")
    manager.crear_tipo_servicio("Corte", "Corte básico", porcentaje_comision)
    
    # Registrar servicios y calcular suma de comisiones esperada en el rango
    suma_comisiones_esperada = Decimal("0")
    
    for fecha, precio in servicios_data:
        resultado = manager.registrar_servicio(fecha, empleado_id, "Corte", precio)
        
        # Sumar comisión si está en el rango (usar la comisión redondeada almacenada)
        if fecha_inicio <= fecha <= fecha_fin and isinstance(resultado, Ok):
            suma_comisiones_esperada += resultado.value.comision_calculada
    
    # Calcular pago del empleado en el período
    desglose = manager.calcular_pago_empleado(empleado_id, fecha_inicio, fecha_fin)
    
    # Verificar que el total coincide exactamente con la suma de comisiones almacenadas
    assert desglose.total == suma_comisiones_esperada


@given(
    servicios_data=st.lists(
        st.tuples(
            fechas_validas,
            tipo_servicio_nombres_validos,
            precios_validos,
            porcentajes_validos
        ),
        min_size=1,
        max_size=20
    ),
    empleado_id=empleado_ids_validos
)
@settings(max_examples=100)
def test_property_21_desglose_pago_contiene_todos_servicios(servicios_data, empleado_id):
    """
    Feature: salon-peluqueria-gestion, Property 21:
    Para cualquier empleado, el desglose de pago debe incluir todos los servicios
    realizados por ese empleado con fecha, tipo, precio y comisión, más el total correcto.
    
    **Validates: Requirements 5.4**
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado
    manager.crear_empleado(empleado_id, "Empleado Test")
    
    # Crear tipos de servicios únicos y registrar servicios
    tipos_creados = set()
    servicios_registrados = 0
    
    for fecha, tipo_nombre, precio, porcentaje in servicios_data:
        # Crear tipo de servicio si no existe
        if tipo_nombre not in tipos_creados:
            resultado = manager.crear_tipo_servicio(tipo_nombre, "Descripción", porcentaje)
            if isinstance(resultado, Ok):
                tipos_creados.add(tipo_nombre)
            else:
                continue
        
        # Registrar servicio
        resultado = manager.registrar_servicio(fecha, empleado_id, tipo_nombre, precio)
        if isinstance(resultado, Ok):
            servicios_registrados += 1
    
    # Calcular pago del empleado
    desglose = manager.calcular_pago_empleado(empleado_id)
    
    # Verificar que el desglose contiene todos los servicios
    assert len(desglose.servicios) == servicios_registrados
    
    # Verificar que cada servicio en el desglose tiene información completa
    for servicio_detalle in desglose.servicios:
        assert servicio_detalle.fecha is not None
        assert servicio_detalle.tipo_servicio is not None
        assert servicio_detalle.tipo_servicio != ""
        assert servicio_detalle.precio is not None
        assert servicio_detalle.precio > 0
        assert servicio_detalle.comision is not None
        assert servicio_detalle.comision >= 0
    
    # Verificar que el total es la suma de las comisiones
    suma_comisiones = sum((s.comision for s in desglose.servicios), Decimal("0"))
    assert abs(desglose.total - suma_comisiones) < Decimal("0.01")
