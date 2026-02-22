"""
Pruebas de API para endpoints de tipos de servicios.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """Limpia la base de datos antes de cada test."""
    from app.main import salon_manager
    
    # Limpiar servicios
    servicios = salon_manager.repository.listar_servicios()
    for servicio in servicios:
        from app.orm_models import ServicioORM
        session = salon_manager.repository.get_session()
        try:
            session.query(ServicioORM).filter_by(id=servicio.id).delete()
            session.commit()
        finally:
            session.close()
    
    # Limpiar tipos de servicios
    tipos = salon_manager.repository.listar_tipos_servicios()
    for tipo in tipos:
        salon_manager.repository.eliminar_tipo_servicio(tipo.nombre)
    
    # Limpiar empleados
    empleados = salon_manager.repository.listar_empleados()
    for empleado in empleados:
        salon_manager.repository.eliminar_empleado(empleado.id)
    
    yield


class TestListarTiposServicios:
    """Pruebas para el endpoint GET /api/tipos-servicios"""
    
    def test_listar_tipos_servicios_vacio(self, client):
        """Debe retornar lista vacía cuando no hay tipos de servicios."""
        response = client.get("/api/tipos-servicios")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_listar_tipos_servicios_con_datos(self, client):
        """Debe retornar todos los tipos de servicios registrados."""
        # Crear tipos de servicios
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        client.post("/api/tipos-servicios", json={
            "nombre": "Tinte Completo",
            "descripcion": "Tinte de cabello completo",
            "porcentaje_comision": 35.0
        })
        
        response = client.get("/api/tipos-servicios")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(t["nombre"] == "Corte Básico" for t in data)
        assert any(t["nombre"] == "Tinte Completo" for t in data)


class TestObtenerTipoServicio:
    """Pruebas para el endpoint GET /api/tipos-servicios/{nombre}"""
    
    def test_obtener_tipo_servicio_existente(self, client):
        """Debe retornar el tipo de servicio cuando existe."""
        # Crear tipo de servicio
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        
        response = client.get("/api/tipos-servicios/Corte Básico")
        
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Corte Básico"
        assert data["descripcion"] == "Corte de cabello básico"
        assert data["porcentaje_comision"] == 40.0
    
    def test_obtener_tipo_servicio_inexistente_retorna_404(self, client):
        """Debe retornar 404 cuando el tipo de servicio no existe."""
        response = client.get("/api/tipos-servicios/NoExiste")
        
        assert response.status_code == 404
        assert "not_found" in response.json()["detail"]["error"]


class TestCrearTipoServicio:
    """Pruebas para el endpoint POST /api/tipos-servicios"""
    
    def test_crear_tipo_servicio_exitoso(self, client):
        """Debe crear un tipo de servicio con datos válidos."""
        response = client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Corte Básico"
        assert data["descripcion"] == "Corte de cabello básico"
        assert data["porcentaje_comision"] == 40.0
    
    def test_crear_tipo_servicio_con_nombre_duplicado_retorna_409(self, client):
        """Debe retornar 409 cuando el nombre ya existe."""
        # Crear primer tipo de servicio
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        
        # Intentar crear con el mismo nombre
        response = client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Otra descripción",
            "porcentaje_comision": 50.0
        })
        
        assert response.status_code == 409
        assert "duplicate_error" in response.json()["detail"]["error"]
    
    def test_crear_tipo_servicio_con_porcentaje_invalido_retorna_422(self, client):
        """Debe retornar 422 cuando el porcentaje es inválido."""
        response = client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 150.0  # Fuera del rango [0, 100]
        })
        
        assert response.status_code == 422
    
    def test_crear_tipo_servicio_sin_nombre_retorna_422(self, client):
        """Debe retornar 422 cuando falta el nombre."""
        response = client.post("/api/tipos-servicios", json={
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        
        assert response.status_code == 422


class TestActualizarTipoServicio:
    """Pruebas para el endpoint PUT /api/tipos-servicios/{nombre}"""
    
    def test_actualizar_tipo_servicio_existente(self, client):
        """Debe actualizar un tipo de servicio existente."""
        # Crear tipo de servicio
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        
        # Actualizar
        response = client.put("/api/tipos-servicios/Corte Básico", json={
            "porcentaje_comision": 45.0
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["porcentaje_comision"] == 45.0
        assert data["nombre"] == "Corte Básico"
    
    def test_actualizar_tipo_servicio_inexistente_retorna_404(self, client):
        """Debe retornar 404 cuando el tipo de servicio no existe."""
        response = client.put("/api/tipos-servicios/NoExiste", json={
            "porcentaje_comision": 45.0
        })
        
        assert response.status_code == 404
    
    def test_actualizar_tipo_servicio_con_porcentaje_invalido_retorna_422(self, client):
        """Debe retornar 422 cuando el porcentaje es inválido."""
        # Crear tipo de servicio
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        
        # Intentar actualizar con porcentaje inválido
        response = client.put("/api/tipos-servicios/Corte Básico", json={
            "porcentaje_comision": 150.0
        })
        
        assert response.status_code == 422
    
    def test_actualizar_descripcion_tipo_servicio(self, client):
        """Debe actualizar la descripción de un tipo de servicio."""
        # Crear tipo de servicio
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        
        # Actualizar descripción
        response = client.put("/api/tipos-servicios/Corte Básico", json={
            "descripcion": "Nueva descripción"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["descripcion"] == "Nueva descripción"
        assert data["porcentaje_comision"] == 40.0  # Se mantiene


class TestEliminarTipoServicio:
    """Pruebas para el endpoint DELETE /api/tipos-servicios/{nombre}"""
    
    def test_eliminar_tipo_servicio_existente(self, client):
        """Debe eliminar un tipo de servicio existente."""
        # Crear tipo de servicio
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        
        # Eliminar
        response = client.delete("/api/tipos-servicios/Corte Básico")
        
        assert response.status_code == 204
        
        # Verificar que ya no existe
        response = client.get("/api/tipos-servicios/Corte Básico")
        assert response.status_code == 404
    
    def test_eliminar_tipo_servicio_inexistente_retorna_404(self, client):
        """Debe retornar 404 cuando el tipo de servicio no existe."""
        response = client.delete("/api/tipos-servicios/NoExiste")
        
        assert response.status_code == 404
    
    def test_eliminar_tipo_servicio_no_afecta_otros(self, client):
        """Debe eliminar solo el tipo de servicio especificado."""
        # Crear dos tipos de servicios
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        client.post("/api/tipos-servicios", json={
            "nombre": "Tinte Completo",
            "descripcion": "Tinte de cabello completo",
            "porcentaje_comision": 35.0
        })
        
        # Eliminar uno
        client.delete("/api/tipos-servicios/Corte Básico")
        
        # Verificar que el otro sigue existiendo
        response = client.get("/api/tipos-servicios/Tinte Completo")
        assert response.status_code == 200


class TestIntegracionTiposServicios:
    """Pruebas de integración para el flujo completo de tipos de servicios."""
    
    def test_flujo_completo_crud_tipo_servicio(self, client):
        """Debe permitir crear, leer, actualizar y eliminar un tipo de servicio."""
        # Crear
        response = client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        assert response.status_code == 201
        
        # Leer
        response = client.get("/api/tipos-servicios/Corte Básico")
        assert response.status_code == 200
        assert response.json()["porcentaje_comision"] == 40.0
        
        # Actualizar
        response = client.put("/api/tipos-servicios/Corte Básico", json={
            "porcentaje_comision": 45.0
        })
        assert response.status_code == 200
        assert response.json()["porcentaje_comision"] == 45.0
        
        # Eliminar
        response = client.delete("/api/tipos-servicios/Corte Básico")
        assert response.status_code == 204
        
        # Verificar que ya no existe
        response = client.get("/api/tipos-servicios/Corte Básico")
        assert response.status_code == 404
    
    def test_listar_tipos_servicios_despues_de_operaciones(self, client):
        """Debe reflejar correctamente los cambios en la lista."""
        # Crear tres tipos de servicios
        client.post("/api/tipos-servicios", json={
            "nombre": "Corte Básico",
            "descripcion": "Corte de cabello básico",
            "porcentaje_comision": 40.0
        })
        client.post("/api/tipos-servicios", json={
            "nombre": "Tinte Completo",
            "descripcion": "Tinte de cabello completo",
            "porcentaje_comision": 35.0
        })
        client.post("/api/tipos-servicios", json={
            "nombre": "Peinado",
            "descripcion": "Peinado especial",
            "porcentaje_comision": 30.0
        })
        
        # Verificar lista
        response = client.get("/api/tipos-servicios")
        assert len(response.json()) == 3
        
        # Eliminar uno
        client.delete("/api/tipos-servicios/Tinte Completo")
        
        # Verificar lista actualizada
        response = client.get("/api/tipos-servicios")
        assert len(response.json()) == 2
        assert not any(t["nombre"] == "Tinte Completo" for t in response.json())
