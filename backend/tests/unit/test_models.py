"""
Pruebas unitarias para los modelos de dominio.
"""
from datetime import date
from decimal import Decimal
import pytest

from app.models import (
    Empleado,
    TipoServicio,
    ServicioRegistrado,
    ServicioDetalle,
    DesglosePago
)


class TestEmpleado:
    """Pruebas para el modelo Empleado."""
    
    def test_crear_empleado(self):
        """Verifica que se puede crear un empleado con atributos válidos."""
        empleado = Empleado(id="E001", nombre="Juan Pérez")
        assert empleado.id == "E001"
        assert empleado.nombre == "Juan Pérez"
    
    def test_empleado_to_dict(self):
        """Verifica la serialización a diccionario."""
        empleado = Empleado(id="E001", nombre="Juan Pérez")
        data = empleado.to_dict()
        assert data == {"id": "E001", "nombre": "Juan Pérez"}


class TestTipoServicio:
    """Pruebas para el modelo TipoServicio."""
    
    def test_crear_tipo_servicio(self):
        """Verifica que se puede crear un tipo de servicio con atributos válidos."""
        tipo = TipoServicio(
            nombre="Corte Básico",
            descripcion="Corte de cabello básico",
            porcentaje_comision=40.0
        )
        assert tipo.nombre == "Corte Básico"
        assert tipo.descripcion == "Corte de cabello básico"
        assert tipo.porcentaje_comision == 40.0
    
    def test_tipo_servicio_to_dict(self):
        """Verifica la serialización a diccionario."""
        tipo = TipoServicio(
            nombre="Corte Básico",
            descripcion="Corte de cabello básico",
            porcentaje_comision=40.0
        )
        data = tipo.to_dict()
        assert data == {
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        }


class TestServicioRegistrado:
    """Pruebas para el modelo ServicioRegistrado."""
    
    def test_crear_servicio_registrado(self):
        """Verifica que se puede crear un servicio registrado con atributos válidos."""
        servicio = ServicioRegistrado(
            id="S001",
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio="Corte Básico",
            precio=Decimal("25.00"),
            comision_calculada=Decimal("10.00")
        )
        assert servicio.id == "S001"
        assert servicio.fecha == date(2024, 1, 15)
        assert servicio.empleado_id == "E001"
        assert servicio.tipo_servicio == "Corte Básico"
        assert servicio.precio == Decimal("25.00")
        assert servicio.comision_calculada == Decimal("10.00")
    
    def test_servicio_to_dict(self):
        """Verifica la serialización a diccionario."""
        servicio = ServicioRegistrado(
            id="S001",
            fecha=date(2024, 1, 15),
            empleado_id="E001",
            tipo_servicio="Corte Básico",
            precio=Decimal("25.00"),
            comision_calculada=Decimal("10.00")
        )
        data = servicio.to_dict()
        assert data == {
            "id": "S001",
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte Básico",
            "precio": "25.00",
            "comision_calculada": "10.00"
        }


class TestServicioDetalle:
    """Pruebas para el modelo ServicioDetalle."""
    
    def test_crear_servicio_detalle(self):
        """Verifica que se puede crear un detalle de servicio."""
        detalle = ServicioDetalle(
            fecha=date(2024, 1, 15),
            tipo_servicio="Corte Básico",
            precio=Decimal("25.00"),
            comision=Decimal("10.00")
        )
        assert detalle.fecha == date(2024, 1, 15)
        assert detalle.tipo_servicio == "Corte Básico"
        assert detalle.precio == Decimal("25.00")
        assert detalle.comision == Decimal("10.00")
    
    def test_servicio_detalle_to_dict(self):
        """Verifica la serialización a diccionario."""
        detalle = ServicioDetalle(
            fecha=date(2024, 1, 15),
            tipo_servicio="Corte Básico",
            precio=Decimal("25.00"),
            comision=Decimal("10.00")
        )
        data = detalle.to_dict()
        assert data == {
            "fecha": "2024-01-15",
            "tipo_servicio": "Corte Básico",
            "precio": "25.00",
            "comision": "10.00"
        }


class TestDesglosePago:
    """Pruebas para el modelo DesglosePago."""
    
    def test_crear_desglose_pago(self):
        """Verifica que se puede crear un desglose de pago."""
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
            )
        ]
        desglose = DesglosePago(
            empleado_id="E001",
            empleado_nombre="Juan Pérez",
            servicios=servicios,
            total=Decimal("27.50")
        )
        assert desglose.empleado_id == "E001"
        assert desglose.empleado_nombre == "Juan Pérez"
        assert len(desglose.servicios) == 2
        assert desglose.total == Decimal("27.50")
    
    def test_desglose_pago_to_dict(self):
        """Verifica la serialización a diccionario."""
        servicios = [
            ServicioDetalle(
                fecha=date(2024, 1, 15),
                tipo_servicio="Corte Básico",
                precio=Decimal("25.00"),
                comision=Decimal("10.00")
            )
        ]
        desglose = DesglosePago(
            empleado_id="E001",
            empleado_nombre="Juan Pérez",
            servicios=servicios,
            total=Decimal("10.00")
        )
        data = desglose.to_dict()
        assert data == {
            "empleado_id": "E001",
            "empleado_nombre": "Juan Pérez",
            "servicios": [
                {
                    "fecha": "2024-01-15",
                    "tipo_servicio": "Corte Básico",
                    "precio": "25.00",
                    "comision": "10.00"
                }
            ],
            "total": "10.00"
        }
    
    def test_desglose_pago_vacio(self):
        """Verifica que se puede crear un desglose sin servicios."""
        desglose = DesglosePago(
            empleado_id="E001",
            empleado_nombre="Juan Pérez",
            servicios=[],
            total=Decimal("0.00")
        )
        assert len(desglose.servicios) == 0
        assert desglose.total == Decimal("0.00")
