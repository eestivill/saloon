"""
Tests para los endpoints de empleados de la API REST.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app, salon_manager


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """Limpia la base de datos antes de cada test."""
    # Limpiar todos los empleados antes de cada test
    empleados = salon_manager.listar_empleados()
    for empleado in empleados:
        salon_manager.repository.eliminar_empleado(empleado.id)
    yield


class TestListarEmpleados:
    """Tests para el endpoint GET /api/empleados."""
    
    def test_listar_empleados_vacio(self, client):
        """Verifica que listar empleados sin datos retorna lista vacía."""
        response = client.get("/api/empleados")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_listar_empleados_con_datos(self, client):
        """Verifica que listar empleados retorna todos los empleados."""
        # Crear empleados
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
        client.post("/api/empleados", json={"id": "E002", "nombre": "María García"})
        
        # Listar empleados
        response = client.get("/api/empleados")
        assert response.status_code == 200
        
        empleados = response.json()
        assert len(empleados) == 2
        
        # Verificar que contiene los empleados creados
        ids = [emp["id"] for emp in empleados]
        assert "E001" in ids
        assert "E002" in ids


class TestObtenerEmpleado:
    """Tests para el endpoint GET /api/empleados/{id}."""
    
    def test_obtener_empleado_existente(self, client):
        """Verifica que obtener un empleado existente retorna sus datos."""
        # Crear empleado
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
        
        # Obtener empleado
        response = client.get("/api/empleados/E001")
        assert response.status_code == 200
        
        empleado = response.json()
        assert empleado["id"] == "E001"
        assert empleado["nombre"] == "Juan Pérez"
    
    def test_obtener_empleado_inexistente_retorna_404(self, client):
        """Verifica que obtener un empleado inexistente retorna 404."""
        response = client.get("/api/empleados/NOEXISTE")
        assert response.status_code == 404
        
        error = response.json()
        assert "detail" in error
        assert error["detail"]["error"] == "not_found"
        assert "NOEXISTE" in error["detail"]["message"]


class TestCrearEmpleado:
    """Tests para el endpoint POST /api/empleados."""
    
    def test_crear_empleado_exitoso(self, client):
        """Verifica que crear un empleado con datos válidos retorna 201."""
        response = client.post(
            "/api/empleados",
            json={"id": "E001", "nombre": "Juan Pérez"}
        )
        
        assert response.status_code == 201
        
        empleado = response.json()
        assert empleado["id"] == "E001"
        assert empleado["nombre"] == "Juan Pérez"
    
    def test_crear_empleado_con_id_duplicado_retorna_409(self, client):
        """Verifica que crear un empleado con ID duplicado retorna 409."""
        # Crear primer empleado
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
        
        # Intentar crear segundo empleado con mismo ID
        response = client.post(
            "/api/empleados",
            json={"id": "E001", "nombre": "Pedro López"}
        )
        
        assert response.status_code == 409
        
        error = response.json()
        assert "detail" in error
        assert error["detail"]["error"] == "duplicate_error"
        assert "E001" in error["detail"]["message"]
    
    def test_crear_empleado_sin_id_retorna_422(self, client):
        """Verifica que crear un empleado sin ID retorna 422."""
        response = client.post(
            "/api/empleados",
            json={"nombre": "Juan Pérez"}
        )
        
        assert response.status_code == 422
    
    def test_crear_empleado_sin_nombre_retorna_422(self, client):
        """Verifica que crear un empleado sin nombre retorna 422."""
        response = client.post(
            "/api/empleados",
            json={"id": "E001"}
        )
        
        assert response.status_code == 422
    
    def test_crear_empleado_con_id_vacio_retorna_422(self, client):
        """Verifica que crear un empleado con ID vacío retorna 422."""
        response = client.post(
            "/api/empleados",
            json={"id": "", "nombre": "Juan Pérez"}
        )
        
        assert response.status_code == 422
    
    def test_crear_empleado_con_nombre_vacio_retorna_422(self, client):
        """Verifica que crear un empleado con nombre vacío retorna 422."""
        response = client.post(
            "/api/empleados",
            json={"id": "E001", "nombre": ""}
        )
        
        assert response.status_code == 422


class TestActualizarEmpleado:
    """Tests para el endpoint PUT /api/empleados/{id}."""
    
    def test_actualizar_empleado_existente(self, client):
        """Verifica que actualizar un empleado existente funciona correctamente."""
        # Crear empleado
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
        
        # Actualizar empleado
        response = client.put(
            "/api/empleados/E001",
            json={"nombre": "Juan Carlos Pérez"}
        )
        
        assert response.status_code == 200
        
        empleado = response.json()
        assert empleado["id"] == "E001"
        assert empleado["nombre"] == "Juan Carlos Pérez"
        
        # Verificar que el cambio persiste
        response_get = client.get("/api/empleados/E001")
        empleado_actualizado = response_get.json()
        assert empleado_actualizado["nombre"] == "Juan Carlos Pérez"
    
    def test_actualizar_empleado_inexistente_retorna_404(self, client):
        """Verifica que actualizar un empleado inexistente retorna 404."""
        response = client.put(
            "/api/empleados/NOEXISTE",
            json={"nombre": "Juan Pérez"}
        )
        
        assert response.status_code == 404
        
        error = response.json()
        assert "detail" in error
        assert error["detail"]["error"] == "not_found"
        assert "NOEXISTE" in error["detail"]["message"]
    
    def test_actualizar_empleado_sin_nombre_retorna_422(self, client):
        """Verifica que actualizar un empleado sin nombre retorna 422."""
        # Crear empleado
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
        
        # Intentar actualizar sin nombre
        response = client.put("/api/empleados/E001", json={})
        
        assert response.status_code == 422
    
    def test_actualizar_empleado_preserva_id(self, client):
        """Verifica que actualizar un empleado preserva su ID."""
        # Crear empleado
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
        
        # Actualizar empleado
        client.put("/api/empleados/E001", json={"nombre": "Nuevo Nombre"})
        
        # Verificar que el ID no cambió
        response = client.get("/api/empleados/E001")
        empleado = response.json()
        assert empleado["id"] == "E001"


class TestEliminarEmpleado:
    """Tests para el endpoint DELETE /api/empleados/{id}."""
    
    def test_eliminar_empleado_existente(self, client):
        """Verifica que eliminar un empleado existente retorna 204."""
        # Crear empleado
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
        
        # Eliminar empleado
        response = client.delete("/api/empleados/E001")
        assert response.status_code == 204
        
        # Verificar que el empleado ya no existe
        response_get = client.get("/api/empleados/E001")
        assert response_get.status_code == 404
    
    def test_eliminar_empleado_inexistente_retorna_404(self, client):
        """Verifica que eliminar un empleado inexistente retorna 404."""
        response = client.delete("/api/empleados/NOEXISTE")
        assert response.status_code == 404
        
        error = response.json()
        assert "detail" in error
        assert error["detail"]["error"] == "not_found"
        assert "NOEXISTE" in error["detail"]["message"]
    
    def test_eliminar_empleado_no_afecta_otros(self, client):
        """Verifica que eliminar un empleado no afecta a otros empleados."""
        # Crear múltiples empleados
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
        client.post("/api/empleados", json={"id": "E002", "nombre": "María García"})
        client.post("/api/empleados", json={"id": "E003", "nombre": "Pedro López"})
        
        # Eliminar un empleado
        client.delete("/api/empleados/E002")
        
        # Verificar que los otros empleados siguen existiendo
        response_e001 = client.get("/api/empleados/E001")
        assert response_e001.status_code == 200
        
        response_e003 = client.get("/api/empleados/E003")
        assert response_e003.status_code == 200
        
        # Verificar que el eliminado no existe
        response_e002 = client.get("/api/empleados/E002")
        assert response_e002.status_code == 404


class TestIntegracionEmpleados:
    """Tests de integración para el flujo completo de empleados."""
    
    def test_flujo_completo_crud_empleado(self, client):
        """Verifica el flujo completo de CRUD de un empleado."""
        # 1. Crear empleado
        response_create = client.post(
            "/api/empleados",
            json={"id": "E001", "nombre": "Juan Pérez"}
        )
        assert response_create.status_code == 201
        
        # 2. Obtener empleado
        response_get = client.get("/api/empleados/E001")
        assert response_get.status_code == 200
        assert response_get.json()["nombre"] == "Juan Pérez"
        
        # 3. Actualizar empleado
        response_update = client.put(
            "/api/empleados/E001",
            json={"nombre": "Juan Carlos Pérez"}
        )
        assert response_update.status_code == 200
        assert response_update.json()["nombre"] == "Juan Carlos Pérez"
        
        # 4. Verificar actualización
        response_get2 = client.get("/api/empleados/E001")
        assert response_get2.json()["nombre"] == "Juan Carlos Pérez"
        
        # 5. Eliminar empleado
        response_delete = client.delete("/api/empleados/E001")
        assert response_delete.status_code == 204
        
        # 6. Verificar eliminación
        response_get3 = client.get("/api/empleados/E001")
        assert response_get3.status_code == 404
    
    def test_listar_empleados_despues_de_operaciones(self, client):
        """Verifica que listar empleados refleja todas las operaciones."""
        # Crear varios empleados
        client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
        client.post("/api/empleados", json={"id": "E002", "nombre": "María"})
        client.post("/api/empleados", json={"id": "E003", "nombre": "Pedro"})
        
        # Verificar lista
        response = client.get("/api/empleados")
        assert len(response.json()) == 3
        
        # Eliminar uno
        client.delete("/api/empleados/E002")
        
        # Verificar lista actualizada
        response = client.get("/api/empleados")
        empleados = response.json()
        assert len(empleados) == 2
        
        ids = [emp["id"] for emp in empleados]
        assert "E001" in ids
        assert "E003" in ids
        assert "E002" not in ids
