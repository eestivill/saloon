"""
Pruebas unitarias para el módulo de validación.
"""
import pytest
from datetime import date
from decimal import Decimal

from app.validators import Validator
from app.result import Ok, Err
from app.errors import ValidationError


class TestValidarPorcentajeComision:
    """Pruebas para validar_porcentaje_comision()"""
    
    def test_porcentaje_cero_es_valido(self):
        """Caso de borde: porcentaje 0 es válido"""
        resultado = Validator.validar_porcentaje_comision(0)
        assert isinstance(resultado, Ok)
        assert resultado.value == 0
    
    def test_porcentaje_cien_es_valido(self):
        """Caso de borde: porcentaje 100 es válido"""
        resultado = Validator.validar_porcentaje_comision(100)
        assert isinstance(resultado, Ok)
        assert resultado.value == 100
    
    def test_porcentaje_medio_es_valido(self):
        """Porcentaje en rango medio es válido"""
        resultado = Validator.validar_porcentaje_comision(50.5)
        assert isinstance(resultado, Ok)
        assert resultado.value == 50.5
    
    def test_porcentaje_negativo_es_invalido(self):
        """Caso de borde: porcentaje negativo es inválido"""
        resultado = Validator.validar_porcentaje_comision(-1)
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "entre 0 y 100" in resultado.error.message
        assert resultado.error.field == "porcentaje_comision"
    
    def test_porcentaje_mayor_cien_es_invalido(self):
        """Caso de borde: porcentaje > 100 es inválido"""
        resultado = Validator.validar_porcentaje_comision(101)
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "entre 0 y 100" in resultado.error.message
        assert resultado.error.field == "porcentaje_comision"


class TestValidarPrecio:
    """Pruebas para validar_precio()"""
    
    def test_precio_positivo_es_valido(self):
        """Precio positivo es válido"""
        resultado = Validator.validar_precio(Decimal("25.50"))
        assert isinstance(resultado, Ok)
        assert resultado.value == Decimal("25.50")
    
    def test_precio_minimo_es_valido(self):
        """Caso de borde: precio mínimo 0.01 es válido"""
        resultado = Validator.validar_precio(Decimal("0.01"))
        assert isinstance(resultado, Ok)
        assert resultado.value == Decimal("0.01")
    
    def test_precio_cero_es_invalido(self):
        """Caso de borde: precio 0 es inválido"""
        resultado = Validator.validar_precio(Decimal("0"))
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "mayor que cero" in resultado.error.message
        assert resultado.error.field == "precio"
    
    def test_precio_negativo_es_invalido(self):
        """Precio negativo es inválido"""
        resultado = Validator.validar_precio(Decimal("-10"))
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "mayor que cero" in resultado.error.message
        assert resultado.error.field == "precio"


class TestValidarRangoFechas:
    """Pruebas para validar_rango_fechas()"""
    
    def test_rango_valido(self):
        """Rango de fechas válido (inicio <= fin)"""
        fecha_inicio = date(2024, 1, 1)
        fecha_fin = date(2024, 12, 31)
        resultado = Validator.validar_rango_fechas(fecha_inicio, fecha_fin)
        assert isinstance(resultado, Ok)
        assert resultado.value == (fecha_inicio, fecha_fin)
    
    def test_fechas_iguales_es_valido(self):
        """Caso de borde: fechas iguales es válido"""
        fecha = date(2024, 6, 15)
        resultado = Validator.validar_rango_fechas(fecha, fecha)
        assert isinstance(resultado, Ok)
        assert resultado.value == (fecha, fecha)
    
    def test_solo_fecha_inicio_es_valido(self):
        """Solo fecha_inicio (sin fecha_fin) es válido"""
        fecha_inicio = date(2024, 1, 1)
        resultado = Validator.validar_rango_fechas(fecha_inicio, None)
        assert isinstance(resultado, Ok)
        assert resultado.value == (fecha_inicio, None)
    
    def test_solo_fecha_fin_es_valido(self):
        """Solo fecha_fin (sin fecha_inicio) es válido"""
        fecha_fin = date(2024, 12, 31)
        resultado = Validator.validar_rango_fechas(None, fecha_fin)
        assert isinstance(resultado, Ok)
        assert resultado.value == (None, fecha_fin)
    
    def test_ambas_fechas_none_es_valido(self):
        """Ambas fechas None es válido"""
        resultado = Validator.validar_rango_fechas(None, None)
        assert isinstance(resultado, Ok)
        assert resultado.value == (None, None)
    
    def test_fecha_inicio_posterior_a_fin_es_invalido(self):
        """Fecha inicio posterior a fecha fin es inválido"""
        fecha_inicio = date(2024, 12, 31)
        fecha_fin = date(2024, 1, 1)
        resultado = Validator.validar_rango_fechas(fecha_inicio, fecha_fin)
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "no puede ser posterior" in resultado.error.message
        assert resultado.error.field == "fecha_inicio"


class TestValidarIdentificadorUnico:
    """Pruebas para validar_identificador_unico()"""
    
    def test_identificador_unico_es_valido(self):
        """Identificador que no existe es válido"""
        existentes = {"E001", "E002", "E003"}
        resultado = Validator.validar_identificador_unico("E004", existentes)
        assert isinstance(resultado, Ok)
        assert resultado.value == "E004"
    
    def test_conjunto_vacio_es_valido(self):
        """Caso de borde: conjunto vacío, cualquier ID es válido"""
        resultado = Validator.validar_identificador_unico("E001", set())
        assert isinstance(resultado, Ok)
        assert resultado.value == "E001"
    
    def test_identificador_duplicado_es_invalido(self):
        """Identificador que ya existe es inválido"""
        existentes = {"E001", "E002", "E003"}
        resultado = Validator.validar_identificador_unico("E002", existentes)
        assert isinstance(resultado, Err)
        assert isinstance(resultado.error, ValidationError)
        assert "ya existe" in resultado.error.message
        assert "E002" in resultado.error.message
        assert resultado.error.field == "id"
