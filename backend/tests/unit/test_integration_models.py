"""
Pruebas de integración para verificar que todos los componentes funcionan juntos.
"""
from datetime import date
from decimal import Decimal
import pytest

from app import (
    Empleado,
    TipoServicio,
    ServicioRegistrado,
    ServicioDetalle,
    DesglosePago,
    Ok,
    Err,
    ValidationError,
    NotFoundError,
    DuplicateError,
)


class TestIntegrationModelsAndResult:
    """Pruebas de integración entre modelos y Result."""
    
    def test_crear_empleado_exitoso_retorna_ok(self):
        """Verifica que crear un empleado exitoso retorna Ok."""
        def crear_empleado(id: str, nombre: str):
            if not id or not nombre:
                return Err(ValidationError("ID y nombre son requeridos"))
            return Ok(Empleado(id=id, nombre=nombre))
        
        resultado = crear_empleado("E001", "Juan Pérez")
        assert isinstance(resultado, Ok)
        assert resultado.value.id == "E001"
        assert resultado.value.nombre == "Juan Pérez"
    
    def test_crear_empleado_sin_datos_retorna_err(self):
        """Verifica que crear un empleado sin datos retorna Err."""
        def crear_empleado(id: str, nombre: str):
            if not id or not nombre:
                return Err(ValidationError("ID y nombre son requeridos"))
            return Ok(Empleado(id=id, nombre=nombre))
        
        resultado = crear_empleado("", "")
        assert isinstance(resultado, Err)
        assert resultado.error.message == "ID y nombre son requeridos"
    
    def test_validar_porcentaje_comision(self):
        """Verifica la validación de porcentaje de comisión."""
        def crear_tipo_servicio(nombre: str, descripcion: str, porcentaje: float):
            if porcentaje < 0 or porcentaje > 100:
                return Err(ValidationError(
                    "El porcentaje debe estar entre 0 y 100",
                    "porcentaje_comision"
                ))
            return Ok(TipoServicio(
                nombre=nombre,
                descripcion=descripcion,
                porcentaje_comision=porcentaje
            ))
        
        # Caso válido
        resultado = crear_tipo_servicio("Corte", "Corte básico", 40.0)
        assert isinstance(resultado, Ok)
        assert resultado.value.porcentaje_comision == 40.0
        
        # Caso inválido - porcentaje negativo
        resultado = crear_tipo_servicio("Corte", "Corte básico", -10.0)
        assert isinstance(resultado, Err)
        assert resultado.error.field == "porcentaje_comision"
        
        # Caso inválido - porcentaje mayor a 100
        resultado = crear_tipo_servicio("Corte", "Corte básico", 150.0)
        assert isinstance(resultado, Err)
        assert resultado.error.field == "porcentaje_comision"
    
    def test_calcular_comision_servicio(self):
        """Verifica el cálculo de comisión para un servicio."""
        tipo_servicio = TipoServicio(
            nombre="Corte Básico",
            descripcion="Corte de cabello",
            porcentaje_comision=40.0
        )
        
        precio = Decimal("25.00")
        comision = precio * Decimal(str(tipo_servicio.porcentaje_comision)) / Decimal("100")
        
        servicio = ServicioRegistrado(
            id="S001",
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio=tipo_servicio.nombre,
            precio=precio,
            comision_calculada=comision
        )
        
        assert servicio.comision_calculada == Decimal("10.00")
    
    def test_desglose_pago_completo(self):
        """Verifica el flujo completo de desglose de pago."""
        # Crear servicios
        servicios = [
            ServicioDetalle(
                fecha=date(2024, 1, 15),
                tipo_servicio="Corte Básico",
                precio=Decimal("25.00"),
                comision=Decimal("10.00")
            ),
            ServicioDetalle(
                fecha=date(2024, 1, 16),
                tipo_servicio="Tinte",
                precio=Decimal("50.00"),
                comision=Decimal("17.50")
            ),
            ServicioDetalle(
                fecha=date(2024, 1, 17),
                tipo_servicio="Peinado",
                precio=Decimal("30.00"),
                comision=Decimal("12.00")
            )
        ]
        
        # Calcular total
        total = sum(s.comision for s in servicios)
        
        # Crear desglose
        desglose = DesglosePago(
            empleado_id="E001",
            empleado_nombre="Juan Pérez",
            servicios=servicios,
            total=total
        )
        
        assert desglose.total == Decimal("39.50")
        assert len(desglose.servicios) == 3
        
        # Verificar serialización
        data = desglose.to_dict()
        assert data["total"] == "39.50"
        assert len(data["servicios"]) == 3
    
    def test_buscar_empleado_no_existente(self):
        """Verifica el manejo de empleado no encontrado."""
        empleados = {
            "E001": Empleado(id="E001", nombre="Juan"),
            "E002": Empleado(id="E002", nombre="María")
        }
        
        def buscar_empleado(id: str):
            if id not in empleados:
                return Err(NotFoundError(entity="Empleado", identifier=id))
            return Ok(empleados[id])
        
        # Caso exitoso
        resultado = buscar_empleado("E001")
        assert isinstance(resultado, Ok)
        assert resultado.value.nombre == "Juan"
        
        # Caso no encontrado
        resultado = buscar_empleado("E999")
        assert isinstance(resultado, Err)
        assert resultado.error.entity == "Empleado"
        assert resultado.error.identifier == "E999"
    
    def test_prevenir_duplicados(self):
        """Verifica la prevención de duplicados."""
        empleados = {"E001": Empleado(id="E001", nombre="Juan")}
        
        def crear_empleado(id: str, nombre: str):
            if id in empleados:
                return Err(DuplicateError(entity="Empleado", identifier=id))
            empleado = Empleado(id=id, nombre=nombre)
            empleados[id] = empleado
            return Ok(empleado)
        
        # Crear nuevo empleado
        resultado = crear_empleado("E002", "María")
        assert isinstance(resultado, Ok)
        assert "E002" in empleados
        
        # Intentar crear duplicado
        resultado = crear_empleado("E001", "Pedro")
        assert isinstance(resultado, Err)
        assert resultado.error.entity == "Empleado"
        assert resultado.error.identifier == "E001"
        # Verificar que el original no cambió
        assert empleados["E001"].nombre == "Juan"
