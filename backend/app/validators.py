"""
Módulo de validación para el sistema de gestión de salón de peluquería.
"""
from datetime import date
from decimal import Decimal
from typing import Optional, Tuple, Set

from app.result import Result, Ok, Err
from app.errors import ValidationError


class Validator:
    """Clase con métodos estáticos para validaciones del sistema."""
    
    @staticmethod
    def validar_porcentaje_comision(porcentaje: float) -> Result[float, ValidationError]:
        """
        Valida que el porcentaje de comisión esté entre 0 y 100.
        
        Args:
            porcentaje: Porcentaje a validar
            
        Returns:
            Ok(porcentaje) si es válido, Err(ValidationError) si no
        """
        if porcentaje < 0 or porcentaje > 100:
            return Err(ValidationError(
                message=f"El porcentaje de comisión debe estar entre 0 y 100, recibido: {porcentaje}",
                field="porcentaje_comision"
            ))
        return Ok(porcentaje)
    
    @staticmethod
    def validar_precio(precio: Decimal) -> Result[Decimal, ValidationError]:
        """
        Valida que el precio sea mayor que cero.
        
        Args:
            precio: Precio a validar
            
        Returns:
            Ok(precio) si es válido, Err(ValidationError) si no
        """
        if precio <= 0:
            return Err(ValidationError(
                message=f"El precio debe ser mayor que cero, recibido: {precio}",
                field="precio"
            ))
        return Ok(precio)
    
    @staticmethod
    def validar_rango_fechas(
        fecha_inicio: Optional[date],
        fecha_fin: Optional[date]
    ) -> Result[Tuple[Optional[date], Optional[date]], ValidationError]:
        """
        Valida que fecha_inicio no sea posterior a fecha_fin.
        
        Args:
            fecha_inicio: Fecha de inicio del rango (opcional)
            fecha_fin: Fecha de fin del rango (opcional)
            
        Returns:
            Ok((fecha_inicio, fecha_fin)) si es válido, Err(ValidationError) si no
        """
        if fecha_inicio is not None and fecha_fin is not None:
            if fecha_inicio > fecha_fin:
                return Err(ValidationError(
                    message=f"La fecha de inicio ({fecha_inicio}) no puede ser posterior a la fecha de fin ({fecha_fin})",
                    field="fecha_inicio"
                ))
        return Ok((fecha_inicio, fecha_fin))
    
    @staticmethod
    def validar_identificador_unico(
        id: str,
        existentes: Set[str]
    ) -> Result[str, ValidationError]:
        """
        Valida que el identificador no exista en el conjunto de existentes.
        
        Args:
            id: Identificador a validar
            existentes: Conjunto de identificadores existentes
            
        Returns:
            Ok(id) si es único, Err(ValidationError) si ya existe
        """
        if id in existentes:
            return Err(ValidationError(
                message=f"El identificador '{id}' ya existe",
                field="id"
            ))
        return Ok(id)
