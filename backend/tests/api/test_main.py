"""
Tests para la configuración de la aplicación FastAPI.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Fixture que proporciona un cliente de prueba."""
    return TestClient(app)


class TestFastAPIConfiguration:
    """Tests para verificar la configuración de FastAPI."""
    
    def test_app_tiene_titulo_correcto(self):
        """Verifica que la aplicación tiene el título correcto."""
        assert app.title == "Sistema de Gestión de Salón de Peluquería"
    
    def test_app_tiene_descripcion_correcta(self):
        """Verifica que la aplicación tiene la descripción correcta."""
        assert app.description == "API REST para gestión de empleados, servicios y comisiones"
    
    def test_app_tiene_version_correcta(self):
        """Verifica que la aplicación tiene la versión correcta."""
        assert app.version == "1.0.0"
    
    def test_cors_middleware_esta_configurado(self):
        """Verifica que el middleware CORS está configurado."""
        # Verificar que hay middleware configurado
        assert len(app.user_middleware) > 0
        
        # Buscar el middleware CORS
        cors_middleware_found = False
        for middleware in app.user_middleware:
            if "CORSMiddleware" in str(middleware):
                cors_middleware_found = True
                break
        
        assert cors_middleware_found, "CORS middleware no está configurado"
    
    def test_root_endpoint_funciona(self, client):
        """Verifica que el endpoint raíz funciona correctamente."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"
    
    def test_health_check_endpoint_funciona(self, client):
        """Verifica que el endpoint de health check funciona."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_salon_manager_esta_inicializado(self):
        """Verifica que el SalonManager está inicializado."""
        from app.main import salon_manager
        assert salon_manager is not None
        assert hasattr(salon_manager, 'repository')
    
    def test_repository_esta_inicializado(self):
        """Verifica que el repositorio está inicializado."""
        from app.main import repository
        assert repository is not None
        assert hasattr(repository, 'engine')
        assert hasattr(repository, 'SessionLocal')


class TestExceptionHandlers:
    """Tests para verificar los exception handlers."""
    
    def test_exception_handlers_estan_registrados(self):
        """Verifica que los exception handlers están registrados."""
        # Verificar que hay exception handlers configurados
        assert len(app.exception_handlers) > 0
    
    def test_endpoint_inexistente_retorna_404(self, client):
        """Verifica que un endpoint inexistente retorna 404."""
        response = client.get("/api/endpoint-inexistente")
        assert response.status_code == 404


class TestLogging:
    """Tests para verificar la configuración de logging."""
    
    def test_logging_middleware_registra_peticiones(self, client):
        """Verifica que el middleware de logging está activo."""
        # Hacer una petición
        response = client.get("/health")
        assert response.status_code == 200
        
        # El middleware debería haber registrado la petición
        # (esto se verifica en los logs, aquí solo verificamos que no hay errores)
