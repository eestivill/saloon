"""
Pruebas unitarias para el patrón Result.
"""
import pytest
from app.result import Ok, Err, Result
from app.errors import ValidationError, NotFoundError, DuplicateError, PersistenceError


class TestResultPattern:
    """Pruebas para el patrón Result."""
    
    def test_ok_contiene_valor(self):
        """Verifica que Ok contiene el valor correcto."""
        resultado = Ok(42)
        assert resultado.value == 42
    
    def test_ok_con_string(self):
        """Verifica que Ok funciona con strings."""
        resultado = Ok("éxito")
        assert resultado.value == "éxito"
    
    def test_ok_con_objeto(self):
        """Verifica que Ok funciona con objetos complejos."""
        data = {"id": "E001", "nombre": "Juan"}
        resultado = Ok(data)
        assert resultado.value == data
    
    def test_err_contiene_error(self):
        """Verifica que Err contiene el error correcto."""
        error = ValidationError(message="Campo inválido", field="nombre")
        resultado = Err(error)
        assert resultado.error == error
        assert resultado.error.message == "Campo inválido"
        assert resultado.error.field == "nombre"
    
    def test_isinstance_ok(self):
        """Verifica que se puede verificar el tipo con isinstance."""
        resultado = Ok(42)
        assert isinstance(resultado, Ok)
        assert not isinstance(resultado, Err)
    
    def test_isinstance_err(self):
        """Verifica que se puede verificar el tipo con isinstance."""
        resultado = Err(ValidationError("error"))
        assert isinstance(resultado, Err)
        assert not isinstance(resultado, Ok)


class TestValidationError:
    """Pruebas para ValidationError."""
    
    def test_crear_validation_error_con_campo(self):
        """Verifica que se puede crear un error de validación con campo."""
        error = ValidationError(message="El precio debe ser positivo", field="precio")
        assert error.message == "El precio debe ser positivo"
        assert error.field == "precio"
    
    def test_crear_validation_error_sin_campo(self):
        """Verifica que se puede crear un error de validación sin campo."""
        error = ValidationError(message="Datos inválidos")
        assert error.message == "Datos inválidos"
        assert error.field is None


class TestNotFoundError:
    """Pruebas para NotFoundError."""
    
    def test_crear_not_found_error(self):
        """Verifica que se puede crear un error de no encontrado."""
        error = NotFoundError(entity="Empleado", identifier="E001")
        assert error.entity == "Empleado"
        assert error.identifier == "E001"


class TestDuplicateError:
    """Pruebas para DuplicateError."""
    
    def test_crear_duplicate_error(self):
        """Verifica que se puede crear un error de duplicado."""
        error = DuplicateError(entity="Empleado", identifier="E001")
        assert error.entity == "Empleado"
        assert error.identifier == "E001"


class TestPersistenceError:
    """Pruebas para PersistenceError."""
    
    def test_crear_persistence_error_con_contexto(self):
        """Verifica que se puede crear un error de persistencia con contexto."""
        error = PersistenceError(
            message="Error al guardar en base de datos",
            context="SQLAlchemy"
        )
        assert error.message == "Error al guardar en base de datos"
        assert error.context == "SQLAlchemy"
    
    def test_crear_persistence_error_sin_contexto(self):
        """Verifica que se puede crear un error de persistencia sin contexto."""
        error = PersistenceError(message="Error de persistencia")
        assert error.message == "Error de persistencia"
        assert error.context is None


class TestResultUsagePatterns:
    """Pruebas de patrones de uso del Result."""
    
    def test_funcion_que_retorna_ok(self):
        """Verifica una función que retorna Ok."""
        def dividir(a: int, b: int) -> Result[float, ValidationError]:
            if b == 0:
                return Err(ValidationError("No se puede dividir por cero", "divisor"))
            return Ok(a / b)
        
        resultado = dividir(10, 2)
        assert isinstance(resultado, Ok)
        assert resultado.value == 5.0
    
    def test_funcion_que_retorna_err(self):
        """Verifica una función que retorna Err."""
        def dividir(a: int, b: int) -> Result[float, ValidationError]:
            if b == 0:
                return Err(ValidationError("No se puede dividir por cero", "divisor"))
            return Ok(a / b)
        
        resultado = dividir(10, 0)
        assert isinstance(resultado, Err)
        assert resultado.error.message == "No se puede dividir por cero"
        assert resultado.error.field == "divisor"
    
    def test_pattern_matching_con_match(self):
        """Verifica el uso de pattern matching con match/case."""
        def procesar_resultado(resultado: Result[int, ValidationError]) -> str:
            match resultado:
                case Ok(value):
                    return f"Éxito: {value}"
                case Err(error):
                    return f"Error: {error.message}"
        
        assert procesar_resultado(Ok(42)) == "Éxito: 42"
        assert procesar_resultado(Err(ValidationError("error"))) == "Error: error"
