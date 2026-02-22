"""
Tests para los endpoints de servicios de la API REST.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import date
from decimal import Decimal

from app.main import app, salon_manager
from app.repository import SQLAlchemyRepository


@pytest.fixture(autouse=True)
def reset_database():
    """Fixture que reinicia la base de datos antes de cada test."""
    # Crear una nueva instancia del repositorio con base de datos en memoria
    import app.main as main_module
    main_module.repository = SQLAlchemyRepository("sqlite:///:memory:")
    main_module.salon_manager = main_module.SalonManager(main_module.repository)
    
    # Actualizar la referencia global
    global salon_manager
    salon_manager = main_module.salon_manager
    
    yield
    
    # Cleanup después del test
    # (la base de datos en memoria se limpia automáticamente)


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba para la API."""
    return TestClient(app)


@pytest.fixture
def setup_data(client):
    """Fixture que configura datos de prueba (empleado y tipo de servicio)."""
    # Crear empleado
    client.post("/api/empleados", json={"id": "E001", "nombre": "Juan Pérez"})
    
    # Crear tipo de servicio
    client.post("/api/tipos-servicios", json={
        "nombre": "Corte",
        "descripcion": "Corte de cabello",
        "porcentaje_comision": 40.0
    })
    
    yield
    
    # Cleanup: eliminar todos los servicios, empleados y tipos de servicios
    # (esto se hace automáticamente con la base de datos en memoria)


class TestListarServicios:
    """Tests para el endpoint GET /api/servicios"""
    
    def test_listar_servicios_vacio(self, client):
        """Debe retornar lista vacía cuando no hay servicios."""
        response = client.get("/api/servicios")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_listar_servicios_con_datos(self, client, setup_data):
        """Debe retornar todos los servicios registrados."""
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
        
        response = client.get("/api/servicios")
        assert response.status_code == 200
        servicios = response.json()
        assert len(servicios) == 2
    
    def test_listar_servicios_filtrado_por_empleado(self, client, setup_data):
        """Debe filtrar servicios por empleado_id."""
        # Crear segundo empleado
        client.post("/api/empleados", json={"id": "E002", "nombre": "María García"})
        
        # Registrar servicios para diferentes empleados
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-16",
            "empleado_id": "E002",
            "tipo_servicio": "Corte",
            "precio": 30.00
        })
        
        response = client.get("/api/servicios?empleado_id=E001")
        assert response.status_code == 200
        servicios = response.json()
        assert len(servicios) == 1
        assert servicios[0]["empleado_id"] == "E001"
    
    def test_listar_servicios_filtrado_por_fecha_inicio(self, client, setup_data):
        """Debe filtrar servicios desde fecha_inicio."""
        # Registrar servicios en diferentes fechas
        client.post("/api/servicios", json={
            "fecha": "2024-01-10",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-20",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 30.00
        })
        
        response = client.get("/api/servicios?fecha_inicio=2024-01-15")
        assert response.status_code == 200
        servicios = response.json()
        assert len(servicios) == 1
        assert servicios[0]["fecha"] == "2024-01-20"
    
    def test_listar_servicios_filtrado_por_fecha_fin(self, client, setup_data):
        """Debe filtrar servicios hasta fecha_fin."""
        # Registrar servicios en diferentes fechas
        client.post("/api/servicios", json={
            "fecha": "2024-01-10",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        client.post("/api/servicios", json={
            "fecha": "2024-01-20",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 30.00
        })
        
        response = client.get("/api/servicios?fecha_fin=2024-01-15")
        assert response.status_code == 200
        servicios = response.json()
        assert len(servicios) == 1
        assert servicios[0]["fecha"] == "2024-01-10"
    
    def test_listar_servicios_filtrado_por_rango_fechas(self, client, setup_data):
        """Debe filtrar servicios dentro del rango de fechas."""
        # Registrar servicios en diferentes fechas
        client.post("/api/servicios", json={
            "fecha": "2024-01-05",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 20.00
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
            "precio": 30.00
        })
        
        response = client.get("/api/servicios?fecha_inicio=2024-01-10&fecha_fin=2024-01-20")
        assert response.status_code == 200
        servicios = response.json()
        assert len(servicios) == 1
        assert servicios[0]["fecha"] == "2024-01-15"
    
    def test_listar_servicios_con_rango_fechas_invalido_retorna_400(self, client, setup_data):
        """Debe retornar 400 si fecha_inicio > fecha_fin."""
        response = client.get("/api/servicios?fecha_inicio=2024-01-20&fecha_fin=2024-01-10")
        assert response.status_code == 400
        assert "validation_error" in response.json()["detail"]["error"]
    
    def test_listar_servicios_ordenados_por_fecha_descendente(self, client, setup_data):
        """Debe retornar servicios ordenados por fecha descendente."""
        # Registrar servicios en orden no cronológico
        client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
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
        
        response = client.get("/api/servicios")
        assert response.status_code == 200
        servicios = response.json()
        assert len(servicios) == 3
        # Verificar orden descendente
        assert servicios[0]["fecha"] == "2024-01-20"
        assert servicios[1]["fecha"] == "2024-01-15"
        assert servicios[2]["fecha"] == "2024-01-10"


class TestObtenerServicio:
    """Tests para el endpoint GET /api/servicios/{id}"""
    
    def test_obtener_servicio_existente(self, client, setup_data):
        """Debe retornar el servicio cuando existe."""
        # Registrar servicio
        response_create = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        servicio_id = response_create.json()["id"]
        
        response = client.get(f"/api/servicios/{servicio_id}")
        assert response.status_code == 200
        servicio = response.json()
        assert servicio["id"] == servicio_id
        assert servicio["empleado_id"] == "E001"
        assert servicio["tipo_servicio"] == "Corte"
        assert float(servicio["precio"]) == 25.00
    
    def test_obtener_servicio_inexistente_retorna_404(self, client):
        """Debe retornar 404 cuando el servicio no existe."""
        response = client.get("/api/servicios/ID_INEXISTENTE")
        assert response.status_code == 404
        assert "not_found" in response.json()["detail"]["error"]


class TestRegistrarServicio:
    """Tests para el endpoint POST /api/servicios"""
    
    def test_registrar_servicio_exitoso(self, client, setup_data):
        """Debe registrar un servicio correctamente."""
        response = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        
        assert response.status_code == 201
        servicio = response.json()
        assert "id" in servicio
        assert servicio["fecha"] == "2024-01-15"
        assert servicio["empleado_id"] == "E001"
        assert servicio["tipo_servicio"] == "Corte"
        assert float(servicio["precio"]) == 25.00
        # Verificar que la comisión se calculó (40% de 25.00 = 10.00)
        assert float(servicio["comision_calculada"]) == 10.00
    
    def test_registrar_servicio_calcula_comision_automaticamente(self, client, setup_data):
        """Debe calcular la comisión automáticamente basándose en el tipo de servicio."""
        # Crear tipo de servicio con 35% de comisión
        client.post("/api/tipos-servicios", json={
            "nombre": "Tinte",
            "descripcion": "Tinte de cabello",
            "porcentaje_comision": 35.0
        })
        
        response = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Tinte",
            "precio": 100.00
        })
        
        assert response.status_code == 201
        servicio = response.json()
        # 35% de 100.00 = 35.00
        assert float(servicio["comision_calculada"]) == 35.00
    
    def test_registrar_servicio_con_empleado_inexistente_retorna_404(self, client, setup_data):
        """Debe retornar 404 si el empleado no existe."""
        response = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E999",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        
        assert response.status_code == 404
        assert "not_found" in response.json()["detail"]["error"]
        assert "Empleado" in response.json()["detail"]["message"]
    
    def test_registrar_servicio_con_tipo_servicio_inexistente_retorna_404(self, client, setup_data):
        """Debe retornar 404 si el tipo de servicio no existe."""
        response = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "TipoInexistente",
            "precio": 25.00
        })
        
        assert response.status_code == 404
        assert "not_found" in response.json()["detail"]["error"]
        assert "TipoServicio" in response.json()["detail"]["message"]
    
    def test_registrar_servicio_con_precio_cero_retorna_422(self, client, setup_data):
        """Debe retornar 422 si el precio es cero."""
        response = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 0.00
        })
        
        assert response.status_code == 422
    
    def test_registrar_servicio_con_precio_negativo_retorna_422(self, client, setup_data):
        """Debe retornar 422 si el precio es negativo."""
        response = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": -10.00
        })
        
        assert response.status_code == 422
    
    def test_registrar_servicio_sin_fecha_retorna_422(self, client, setup_data):
        """Debe retornar 422 si falta la fecha."""
        response = client.post("/api/servicios", json={
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        
        assert response.status_code == 422
    
    def test_registrar_servicio_sin_empleado_id_retorna_422(self, client, setup_data):
        """Debe retornar 422 si falta el empleado_id."""
        response = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        
        assert response.status_code == 422
    
    def test_registrar_servicio_sin_tipo_servicio_retorna_422(self, client, setup_data):
        """Debe retornar 422 si falta el tipo_servicio."""
        response = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "precio": 25.00
        })
        
        assert response.status_code == 422


class TestEliminarServicio:
    """Tests para el endpoint DELETE /api/servicios/{id}"""
    
    def test_eliminar_servicio_existente(self, client, setup_data):
        """Debe eliminar un servicio correctamente."""
        # Registrar servicio
        response_create = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        servicio_id = response_create.json()["id"]
        
        # Eliminar servicio
        response = client.delete(f"/api/servicios/{servicio_id}")
        assert response.status_code == 204
        
        # Verificar que ya no existe
        response_get = client.get(f"/api/servicios/{servicio_id}")
        assert response_get.status_code == 404
    
    def test_eliminar_servicio_inexistente_retorna_404(self, client):
        """Debe retornar 404 cuando el servicio no existe."""
        response = client.delete("/api/servicios/ID_INEXISTENTE")
        assert response.status_code == 404
        assert "not_found" in response.json()["detail"]["error"]
    
    def test_eliminar_servicio_no_afecta_otros(self, client, setup_data):
        """Debe eliminar solo el servicio especificado."""
        # Registrar dos servicios
        response1 = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        response2 = client.post("/api/servicios", json={
            "fecha": "2024-01-16",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 30.00
        })
        
        servicio_id1 = response1.json()["id"]
        servicio_id2 = response2.json()["id"]
        
        # Eliminar el primero
        client.delete(f"/api/servicios/{servicio_id1}")
        
        # Verificar que el segundo sigue existiendo
        response_get = client.get(f"/api/servicios/{servicio_id2}")
        assert response_get.status_code == 200


class TestIntegracionServicios:
    """Tests de integración para el flujo completo de servicios."""
    
    def test_flujo_completo_crud_servicio(self, client, setup_data):
        """Debe permitir crear, leer y eliminar un servicio."""
        # Crear servicio
        response_create = client.post("/api/servicios", json={
            "fecha": "2024-01-15",
            "empleado_id": "E001",
            "tipo_servicio": "Corte",
            "precio": 25.00
        })
        assert response_create.status_code == 201
        servicio_id = response_create.json()["id"]
        
        # Leer servicio
        response_get = client.get(f"/api/servicios/{servicio_id}")
        assert response_get.status_code == 200
        assert response_get.json()["id"] == servicio_id
        
        # Eliminar servicio
        response_delete = client.delete(f"/api/servicios/{servicio_id}")
        assert response_delete.status_code == 204
        
        # Verificar que ya no existe
        response_get_after = client.get(f"/api/servicios/{servicio_id}")
        assert response_get_after.status_code == 404
    
    def test_listar_servicios_despues_de_operaciones(self, client, setup_data):
        """Debe reflejar correctamente las operaciones en la lista."""
        # Crear tres servicios
        ids = []
        for i in range(3):
            response = client.post("/api/servicios", json={
                "fecha": f"2024-01-{15+i}",
                "empleado_id": "E001",
                "tipo_servicio": "Corte",
                "precio": 25.00 + i * 5
            })
            ids.append(response.json()["id"])
        
        # Verificar que hay 3 servicios
        response_list = client.get("/api/servicios")
        assert len(response_list.json()) == 3
        
        # Eliminar uno
        client.delete(f"/api/servicios/{ids[1]}")
        
        # Verificar que ahora hay 2
        response_list_after = client.get("/api/servicios")
        assert len(response_list_after.json()) == 2
        
        # Verificar que el eliminado no está
        servicios = response_list_after.json()
        servicios_ids = [s["id"] for s in servicios]
        assert ids[1] not in servicios_ids
        assert ids[0] in servicios_ids
        assert ids[2] in servicios_ids
