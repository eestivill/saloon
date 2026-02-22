"""
Pruebas de integración backend-frontend.

Verifica:
- CORS está configurado correctamente
- Todas las llamadas API funcionan correctamente
- Manejo de errores end-to-end
- Persistencia de datos
"""
import pytest
from fastapi.testclient import TestClient
from datetime import date
from decimal import Decimal
import os
import tempfile

from app.main import app
from app.repository import SQLAlchemyRepository
from app.manager import SalonManager


@pytest.fixture(autouse=True)
def setup_test_db():
    """Configura una base de datos temporal para cada test."""
    # Crear base de datos temporal
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    
    # Reemplazar el repositorio y manager con uno que use la BD temporal
    from app import main
    main.repository = SQLAlchemyRepository(f"sqlite:///{temp_db.name}")
    main.salon_manager = SalonManager(main.repository)
    
    yield
    
    # Limpiar después del test
    try:
        os.unlink(temp_db.name)
    except:
        pass


@pytest.fixture
def client():
    """Cliente de prueba para FastAPI."""
    return TestClient(app)


class TestCORSConfiguration:
    """Pruebas de configuración CORS."""
    
    def test_cors_headers_present(self, client):
        """Verifica que los headers CORS están presentes en las respuestas."""
        response = client.options(
            "/api/empleados",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Verificar que la respuesta incluye headers CORS
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
    
    def test_cors_allows_all_methods(self, client):
        """Verifica que CORS permite todos los métodos HTTP."""
        response = client.options(
            "/api/empleados",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        assert response.status_code in [200, 204]
        assert "access-control-allow-methods" in response.headers
    
    def test_cors_allows_credentials(self, client):
        """Verifica que CORS permite credenciales."""
        response = client.get(
            "/api/empleados",
            headers={"Origin": "http://localhost:5173"}
        )
        
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"


class TestEmpleadosAPIIntegration:
    """Pruebas de integración para endpoints de empleados."""
    
    def test_flujo_completo_empleados(self, client):
        """Prueba el flujo completo: crear, listar, obtener, actualizar, eliminar."""
        # 1. Crear empleado
        response = client.post(
            "/api/empleados",
            json={"id": "E001", "nombre": "Juan Pérez"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "E001"
        assert data["nombre"] == "Juan Pérez"
        
        # 2. Listar empleados
        response = client.get("/api/empleados")
        assert response.status_code == 200
        empleados = response.json()
        assert len(empleados) >= 1
        assert any(e["id"] == "E001" for e in empleados)
        
        # 3. Obtener empleado específico
        response = client.get("/api/empleados/E001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "E001"
        assert data["nombre"] == "Juan Pérez"
        
        # 4. Actualizar empleado
        response = client.put(
            "/api/empleados/E001",
            json={"nombre": "Juan Carlos Pérez"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Juan Carlos Pérez"
        
        # 5. Eliminar empleado
        response = client.delete("/api/empleados/E001")
        assert response.status_code == 204
        
        # 6. Verificar que fue eliminado
        response = client.get("/api/empleados/E001")
        assert response.status_code == 404


class TestTiposServiciosAPIIntegration:
    """Pruebas de integración para endpoints de tipos de servicios."""
    
    def test_flujo_completo_tipos_servicios(self, client):
        """Prueba el flujo completo de tipos de servicios."""
        # 1. Crear tipo de servicio
        response = client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte Básico",
                "descripcion": "Corte de cabello básico",
                "porcentaje_comision": 40.0
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Corte Básico"
        assert data["porcentaje_comision"] == 40.0
        
        # 2. Listar tipos de servicios
        response = client.get("/api/tipos-servicios")
        assert response.status_code == 200
        tipos = response.json()
        assert len(tipos) >= 1
        assert any(t["nombre"] == "Corte Básico" for t in tipos)
        
        # 3. Obtener tipo específico
        response = client.get("/api/tipos-servicios/Corte Básico")
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Corte Básico"
        
        # 4. Actualizar tipo de servicio
        response = client.put(
            "/api/tipos-servicios/Corte Básico",
            json={"porcentaje_comision": 45.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["porcentaje_comision"] == 45.0
        
        # 5. Eliminar tipo de servicio
        response = client.delete("/api/tipos-servicios/Corte Básico")
        assert response.status_code == 204


class TestServiciosAPIIntegration:
    """Pruebas de integración para endpoints de servicios."""
    
    def test_flujo_completo_servicios(self, client):
        """Prueba el flujo completo de servicios."""
        # Setup: crear empleado y tipo de servicio
        client.post(
            "/api/empleados",
            json={"id": "E001", "nombre": "Juan"}
        )
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte de cabello",
                "porcentaje_comision": 40.0
            }
        )
        
        # 1. Registrar servicio
        response = client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 25.00
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["empleado_id"] == "E001"
        assert data["tipo_servicio"] == "Corte"
        assert float(data["precio"]) == 25.00
        assert float(data["comision_calculada"]) == 10.00  # 40% de 25
        servicio_id = data["id"]
        
        # 2. Listar servicios
        response = client.get("/api/servicios")
        assert response.status_code == 200
        servicios = response.json()
        assert len(servicios) >= 1
        
        # 3. Filtrar por empleado
        response = client.get("/api/servicios?empleado_id=E001")
        assert response.status_code == 200
        servicios = response.json()
        assert all(s["empleado_id"] == "E001" for s in servicios)
        
        # 4. Obtener servicio específico
        response = client.get(f"/api/servicios/{servicio_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == servicio_id
        
        # 5. Eliminar servicio
        response = client.delete(f"/api/servicios/{servicio_id}")
        assert response.status_code == 204


class TestReportesAPIIntegration:
    """Pruebas de integración para endpoints de reportes."""
    
    def test_calcular_ingresos(self, client):
        """Prueba el cálculo de ingresos."""
        # Setup
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Registrar servicios
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 25.00
            }
        )
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-16",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 30.00
            }
        )
        
        # Calcular ingresos
        response = client.get("/api/reportes/ingresos")
        assert response.status_code == 200
        data = response.json()
        assert float(data["total"]) == 55.00
    
    def test_calcular_beneficios(self, client):
        """Prueba el cálculo de beneficios."""
        # Setup
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Registrar servicio
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 100.00
            }
        )
        
        # Calcular beneficios
        response = client.get("/api/reportes/beneficios")
        assert response.status_code == 200
        data = response.json()
        assert float(data["ingresos"]) == 100.00
        assert float(data["comisiones"]) == 40.00
        assert float(data["beneficios"]) == 60.00
    
    def test_calcular_pago_empleado(self, client):
        """Prueba el cálculo de pago de empleado."""
        # Setup
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Registrar servicios
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 25.00
            }
        )
        
        # Calcular pago
        response = client.get("/api/empleados/E001/pago")
        assert response.status_code == 200
        data = response.json()
        assert data["empleado_id"] == "E001"
        assert data["empleado_nombre"] == "Juan"
        assert len(data["servicios"]) == 1
        assert float(data["total"]) == 10.00  # 40% de 25


class TestErrorHandling:
    """Pruebas de manejo de errores end-to-end."""
    
    def test_crear_empleado_duplicado_retorna_409(self, client):
        """Verifica que crear un empleado duplicado retorna 409."""
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        
        response = client.post("/api/empleados", json={"id": "E001", "nombre": "Pedro"})
        assert response.status_code == 409
        data = response.json()
        assert "detail" in data
        assert "error" in data["detail"]
        assert data["detail"]["error"] == "duplicate_error"
    
    def test_obtener_empleado_inexistente_retorna_404(self, client):
        """Verifica que obtener un empleado inexistente retorna 404."""
        response = client.get("/api/empleados/NOEXISTE")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "error" in data["detail"]
        assert data["detail"]["error"] == "not_found"
    
    def test_crear_tipo_servicio_porcentaje_invalido_retorna_400(self, client):
        """Verifica que un porcentaje inválido retorna 400 o 422 (Pydantic)."""
        response = client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 150.0  # Inválido
            }
        )
        # Pydantic puede retornar 422 antes de que llegue a la validación de negocio
        assert response.status_code in [400, 422]
        data = response.json()
        assert "detail" in data
    
    def test_registrar_servicio_empleado_inexistente_retorna_404(self, client):
        """Verifica que registrar servicio con empleado inexistente retorna 404."""
        # Crear tipo de servicio
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Intentar registrar servicio con empleado inexistente
        response = client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "NOEXISTE",
                "tipo_servicio": "Corte",
                "precio": 25.00
            }
        )
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "error" in data["detail"]
        assert data["detail"]["error"] == "not_found"
    
    def test_registrar_servicio_tipo_inexistente_retorna_404(self, client):
        """Verifica que registrar servicio con tipo inexistente retorna 404."""
        # Crear empleado
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        
        # Intentar registrar servicio con tipo inexistente
        response = client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "NOEXISTE",
                "precio": 25.00
            }
        )
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "error" in data["detail"]
        assert data["detail"]["error"] == "not_found"
    
    def test_rango_fechas_invalido_retorna_400(self, client):
        """Verifica que un rango de fechas inválido retorna 400."""
        response = client.get(
            "/api/servicios?fecha_inicio=2024-12-31&fecha_fin=2024-01-01"
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "error" in data["detail"]
        assert data["detail"]["error"] == "validation_error"


class TestPersistence:
    """Pruebas de persistencia de datos."""
    
    def test_datos_persisten_entre_requests(self, client):
        """Verifica que los datos persisten entre diferentes requests."""
        # Crear empleado
        response = client.post(
            "/api/empleados",
            json={"id": "E001", "nombre": "Juan"}
        )
        assert response.status_code == 201
        
        # Verificar que persiste en un nuevo request
        response = client.get("/api/empleados/E001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "E001"
        assert data["nombre"] == "Juan"
    
    def test_servicios_persisten_con_comision_calculada(self, client):
        """Verifica que los servicios persisten con la comisión calculada."""
        # Setup
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Registrar servicio
        response = client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 25.00
            }
        )
        servicio_id = response.json()["id"]
        
        # Verificar que persiste con comisión calculada
        response = client.get(f"/api/servicios/{servicio_id}")
        assert response.status_code == 200
        data = response.json()
        assert float(data["comision_calculada"]) == 10.00
    
    def test_actualizacion_tipo_servicio_no_afecta_servicios_existentes(self, client):
        """Verifica que actualizar un tipo de servicio no afecta servicios ya registrados."""
        # Setup
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Registrar servicio con comisión 40%
        response = client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 100.00
            }
        )
        servicio_id = response.json()["id"]
        
        # Actualizar porcentaje de comisión a 50%
        client.put(
            "/api/tipos-servicios/Corte",
            json={"porcentaje_comision": 50.0}
        )
        
        # Verificar que el servicio existente mantiene la comisión original
        response = client.get(f"/api/servicios/{servicio_id}")
        data = response.json()
        assert float(data["comision_calculada"]) == 40.00  # Mantiene 40%, no 50%


class TestFilteringAndSorting:
    """Pruebas de filtrado y ordenamiento."""
    
    def test_filtrar_servicios_por_empleado(self, client):
        """Verifica que el filtrado por empleado funciona correctamente."""
        # Setup
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post("/api/empleados", json={"id": "E002", "nombre": "María"})
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Registrar servicios para diferentes empleados
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 25.00
            }
        )
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-16",
                "empleado_id": "E002",
                "tipo_servicio": "Corte",
                "precio": 30.00
            }
        )
        
        # Filtrar por E001
        response = client.get("/api/servicios?empleado_id=E001")
        assert response.status_code == 200
        servicios = response.json()
        assert all(s["empleado_id"] == "E001" for s in servicios)
        assert len(servicios) == 1
    
    def test_filtrar_servicios_por_rango_fechas(self, client):
        """Verifica que el filtrado por rango de fechas funciona correctamente."""
        # Setup
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Registrar servicios en diferentes fechas
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-10",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 25.00
            }
        )
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-20",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 30.00
            }
        )
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-30",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 35.00
            }
        )
        
        # Filtrar por rango
        response = client.get(
            "/api/servicios?fecha_inicio=2024-01-15&fecha_fin=2024-01-25"
        )
        assert response.status_code == 200
        servicios = response.json()
        assert len(servicios) == 1
        assert servicios[0]["fecha"] == "2024-01-20"
    
    def test_servicios_ordenados_por_fecha_descendente(self, client):
        """Verifica que los servicios se ordenan por fecha descendente."""
        # Setup
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post(
            "/api/tipos-servicios",
            json={
                "nombre": "Corte",
                "descripcion": "Corte",
                "porcentaje_comision": 40.0
            }
        )
        
        # Registrar servicios en orden no secuencial
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-15",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 25.00
            }
        )
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-20",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 30.00
            }
        )
        client.post(
            "/api/servicios",
            json={
                "fecha": "2024-01-10",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 20.00
            }
        )
        
        # Verificar ordenamiento
        response = client.get("/api/servicios")
        assert response.status_code == 200
        servicios = response.json()
        
        # Deben estar ordenados de más reciente a más antiguo
        fechas = [s["fecha"] for s in servicios]
        assert fechas == sorted(fechas, reverse=True)
