"""
Tests para los endpoints de reportes de la API REST.
"""
import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from app.main import app, salon_manager


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """Limpia la base de datos antes de cada test."""
    # Limpiar servicios
    servicios = salon_manager.obtener_servicios()
    for servicio in servicios:
        salon_manager.repository.eliminar_servicio(servicio.id)
    
    # Limpiar tipos de servicios
    tipos = salon_manager.listar_tipos_servicios()
    for tipo in tipos:
        salon_manager.repository.eliminar_tipo_servicio(tipo.nombre)
    
    # Limpiar empleados
    empleados = salon_manager.listar_empleados()
    for empleado in empleados:
        salon_manager.repository.eliminar_empleado(empleado.id)
    
    yield


@pytest.fixture
def setup_datos_basicos(client):
    """Fixture que crea datos básicos para las pruebas."""
    # Crear empleado
    client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
    
    # Crear tipo de servicio
    client.post("/api/tipos-servicios", json={
        "nombre": "Corte",
        "descripcion": "Corte de cabello",
        "porcentaje_comision": 40.0
    })
    
    return {"empleado_id": "E001", "tipo_servicio": "Corte"}


class TestCalcularIngresos:
    """Tests para el endpoint GET /api/reportes/ingresos."""
    
    def test_ingresos_sin_servicios_retorna_cero(self, client):
        """Verifica que sin servicios registrados los ingresos son cero."""
        response = client.get("/api/reportes/ingresos")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["total"]) == Decimal("0")
        assert data["fecha_inicio"] is None
        assert data["fecha_fin"] is None
    
    def test_ingresos_con_servicios(self, client, setup_datos_basicos):
        """Verifica que los ingresos se calculan correctamente."""
        # Registrar servicios
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-16",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 30.00
        })
        
        # Calcular ingresos
        response = client.get("/api/reportes/ingresos")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["total"]) == Decimal("55.00")
    
    def test_ingresos_con_filtro_fecha_inicio(self, client, setup_datos_basicos):
        """Verifica que el filtro de fecha_inicio funciona correctamente."""
        # Registrar servicios en diferentes fechas
        client.post("/api/servicios", json={
            "fecha": "2024-01-10",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 20.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-20",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 30.00
        })
        
        # Filtrar desde 2024-01-15
        response = client.get("/api/reportes/ingresos?fecha_inicio=2024-01-15")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["total"]) == Decimal("30.00")
        assert data["fecha_inicio"] == "2024-01-15"
    
    def test_ingresos_con_filtro_fecha_fin(self, client, setup_datos_basicos):
        """Verifica que el filtro de fecha_fin funciona correctamente."""
        # Registrar servicios en diferentes fechas
        client.post("/api/servicios", json={
            "fecha": "2024-01-10",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 20.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-20",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 30.00
        })
        
        # Filtrar hasta 2024-01-15
        response = client.get("/api/reportes/ingresos?fecha_fin=2024-01-15")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["total"]) == Decimal("20.00")
        assert data["fecha_fin"] == "2024-01-15"
    
    def test_ingresos_con_rango_fechas(self, client, setup_datos_basicos):
        """Verifica que el filtro por rango de fechas funciona correctamente."""
        # Registrar servicios en diferentes fechas
        client.post("/api/servicios", json={
            "fecha": "2024-01-05",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 15.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-25",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 35.00
        })
        
        # Filtrar rango 2024-01-10 a 2024-01-20
        response = client.get("/api/reportes/ingresos?fecha_inicio=2024-01-10&fecha_fin=2024-01-20")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["total"]) == Decimal("25.00")
        assert data["fecha_inicio"] == "2024-01-10"
        assert data["fecha_fin"] == "2024-01-20"
    
    def test_ingresos_con_rango_fechas_invalido_retorna_400(self, client):
        """Verifica que un rango de fechas inválido retorna 400."""
        response = client.get("/api/reportes/ingresos?fecha_inicio=2024-01-20&fecha_fin=2024-01-10")
        assert response.status_code == 400
        
        error = response.json()
        assert "detail" in error
        assert error["detail"]["error"] == "validation_error"


class TestCalcularBeneficios:
    """Tests para el endpoint GET /api/reportes/beneficios."""
    
    def test_beneficios_sin_servicios_retorna_cero(self, client):
        """Verifica que sin servicios los beneficios son cero."""
        response = client.get("/api/reportes/beneficios")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["ingresos"]) == Decimal("0")
        assert Decimal(data["comisiones"]) == Decimal("0")
        assert Decimal(data["beneficios"]) == Decimal("0")
    
    def test_beneficios_con_servicios(self, client, setup_datos_basicos):
        """Verifica que los beneficios se calculan correctamente."""
        # Registrar servicio con precio 100 y comisión 40%
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 100.00
        })
        
        # Calcular beneficios
        response = client.get("/api/reportes/beneficios")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["ingresos"]) == Decimal("100.00")
        assert Decimal(data["comisiones"]) == Decimal("40.00")
        assert Decimal(data["beneficios"]) == Decimal("60.00")
    
    def test_beneficios_con_multiples_servicios(self, client, setup_datos_basicos):
        """Verifica el cálculo de beneficios con múltiples servicios."""
        # Registrar servicios
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 50.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-16",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 30.00
        })
        
        # Calcular beneficios
        response = client.get("/api/reportes/beneficios")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["ingresos"]) == Decimal("80.00")
        assert Decimal(data["comisiones"]) == Decimal("32.00")  # 40% de 80
        assert Decimal(data["beneficios"]) == Decimal("48.00")
    
    def test_beneficios_con_filtro_fechas(self, client, setup_datos_basicos):
        """Verifica que el filtro de fechas funciona en beneficios."""
        # Registrar servicios en diferentes fechas
        client.post("/api/servicios", json={
            "fecha": "2024-01-10",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 100.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-20",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 50.00
        })
        
        # Filtrar desde 2024-01-15
        response = client.get("/api/reportes/beneficios?fecha_inicio=2024-01-15")
        assert response.status_code == 200
        
        data = response.json()
        assert Decimal(data["ingresos"]) == Decimal("50.00")
        assert Decimal(data["comisiones"]) == Decimal("20.00")
        assert Decimal(data["beneficios"]) == Decimal("30.00")
    
    def test_beneficios_con_rango_fechas_invalido_retorna_400(self, client):
        """Verifica que un rango de fechas inválido retorna 400."""
        response = client.get("/api/reportes/beneficios?fecha_inicio=2024-01-20&fecha_fin=2024-01-10")
        assert response.status_code == 400
        
        error = response.json()
        assert "detail" in error
        assert error["detail"]["error"] == "validation_error"


class TestCalcularPagoEmpleado:
    """Tests para el endpoint GET /api/empleados/{id}/pago."""
    
    def test_pago_empleado_sin_servicios(self, client, setup_datos_basicos):
        """Verifica que un empleado sin servicios tiene pago cero."""
        response = client.get("/api/empleados/E001/pago")
        assert response.status_code == 200
        
        data = response.json()
        assert data["empleado_id"] == "E001"
        assert data["empleado_nombre"] == "Juan Pérez"
        assert len(data["servicios"]) == 0
        assert Decimal(data["total"]) == Decimal("0")
    
    def test_pago_empleado_con_servicios(self, client, setup_datos_basicos):
        """Verifica que el pago del empleado se calcula correctamente."""
        # Registrar servicios
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 100.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-16",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 50.00
        })
        
        # Calcular pago
        response = client.get("/api/empleados/E001/pago")
        assert response.status_code == 200
        
        data = response.json()
        assert data["empleado_id"] == "E001"
        assert len(data["servicios"]) == 2
        assert Decimal(data["total"]) == Decimal("60.00")  # 40% de 150
    
    def test_pago_empleado_desglose_servicios(self, client, setup_datos_basicos):
        """Verifica que el desglose de servicios es correcto."""
        # Registrar servicio
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 100.00
        })
        
        # Obtener desglose
        response = client.get("/api/empleados/E001/pago")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["servicios"]) == 1
        
        servicio = data["servicios"][0]
        assert servicio["fecha"] == "2024-01-15"
        assert servicio["tipo_servicio"] == "Corte"
        assert Decimal(servicio["precio"]) == Decimal("100.00")
        assert Decimal(servicio["comision"]) == Decimal("40.00")
    
    def test_pago_empleado_con_filtro_fechas(self, client, setup_datos_basicos):
        """Verifica que el filtro de fechas funciona en el pago del empleado."""
        # Registrar servicios en diferentes fechas
        client.post("/api/servicios", json={
            "fecha": "2024-01-10",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 100.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-20",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 50.00
        })
        
        # Filtrar desde 2024-01-15
        response = client.get("/api/empleados/E001/pago?fecha_inicio=2024-01-15")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["servicios"]) == 1
        assert Decimal(data["total"]) == Decimal("20.00")  # 40% de 50
    
    def test_pago_empleado_inexistente_retorna_404(self, client):
        """Verifica que consultar el pago de un empleado inexistente retorna 404."""
        response = client.get("/api/empleados/NOEXISTE/pago")
        assert response.status_code == 404
        
        error = response.json()
        assert "detail" in error
        assert error["detail"]["error"] == "not_found"
    
    def test_pago_empleado_con_rango_fechas_invalido_retorna_400(self, client, setup_datos_basicos):
        """Verifica que un rango de fechas inválido retorna 400."""
        response = client.get("/api/empleados/E001/pago?fecha_inicio=2024-01-20&fecha_fin=2024-01-10")
        assert response.status_code == 400
        
        error = response.json()
        assert "detail" in error
        assert error["detail"]["error"] == "validation_error"


class TestFormatoMonetario:
    """Tests para verificar el formato monetario en las respuestas."""
    
    def test_ingresos_formato_decimal(self, client, setup_datos_basicos):
        """Verifica que los ingresos se retornan con formato decimal apropiado."""
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.50
        })
        
        response = client.get("/api/reportes/ingresos")
        assert response.status_code == 200
        
        data = response.json()
        # Verificar que el total es un string con formato decimal
        assert isinstance(data["total"], (str, int, float))
        total = Decimal(str(data["total"]))
        assert total == Decimal("25.50")
    
    def test_beneficios_formato_decimal(self, client, setup_datos_basicos):
        """Verifica que los beneficios se retornan con formato decimal apropiado."""
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 100.00
        })
        
        response = client.get("/api/reportes/beneficios")
        assert response.status_code == 200
        
        data = response.json()
        # Verificar formato decimal en todos los campos monetarios
        assert isinstance(data["ingresos"], (str, int, float))
        assert isinstance(data["comisiones"], (str, int, float))
        assert isinstance(data["beneficios"], (str, int, float))
    
    def test_pago_empleado_formato_decimal(self, client, setup_datos_basicos):
        """Verifica que el pago del empleado se retorna con formato decimal apropiado."""
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 100.00
        })
        
        response = client.get("/api/empleados/E001/pago")
        assert response.status_code == 200
        
        data = response.json()
        # Verificar formato decimal en el total
        assert isinstance(data["total"], (str, int, float))
        
        # Verificar formato decimal en cada servicio
        for servicio in data["servicios"]:
            assert isinstance(servicio["precio"], (str, int, float))
            assert isinstance(servicio["comision"], (str, int, float))
