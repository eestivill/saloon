#!/bin/bash

# Script parte 2: Actualizar archivos backend restantes
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Actualización Parte 2: Backend (schemas, manager, main) ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

backup_file() {
    if [ -f "$1" ]; then
        cp "$1" "$1.backup_$(date +%Y%m%d_%H%M%S)"
        echo -e "${GREEN}✓ Backup: $1${NC}"
    fi
}

show_progress() {
    echo -e "\n${YELLOW}▶ $1${NC}"
}

# ============================================================================
# ACTUALIZAR backend/app/schemas.py
# ============================================================================

show_progress "Paso 4/10: Actualizando backend/app/schemas.py..."
backup_file "backend/app/schemas.py"

cat > backend/app/schemas.py << 'SCHEMAS_PY'
"""
Modelos Pydantic para validación de request/response en la API REST.
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import date
from decimal import Decimal


# ============================================================================
# EMPLEADOS
# ============================================================================

class EmpleadoCreate(BaseModel):
    """Schema para crear un nuevo empleado."""
    id: str = Field(..., min_length=1, max_length=50, description="Identificador único del empleado")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del empleado")
    
    @field_validator('id')
    @classmethod
    def validar_id_no_vacio(cls, v: str) -> str:
        """Valida que el ID no sea solo espacios en blanco."""
        if not v.strip():
            raise ValueError('El ID no puede estar vacío')
        return v.strip()
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre_no_vacio(cls, v: str) -> str:
        """Valida que el nombre no sea solo espacios en blanco."""
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()


class EmpleadoUpdate(BaseModel):
    """Schema para actualizar un empleado existente."""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del empleado")
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre_no_vacio(cls, v: str) -> str:
        """Valida que el nombre no sea solo espacios en blanco."""
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()


class EmpleadoResponse(BaseModel):
    """Schema para respuesta de empleado."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    nombre: str


# ============================================================================
# TIPOS DE SERVICIOS
# ============================================================================

class TipoServicioCreate(BaseModel):
    """Schema para crear un nuevo tipo de servicio."""
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre único del tipo de servicio")
    descripcion: str = Field(..., max_length=200, description="Descripción del servicio")
    porcentaje_comision: float = Field(..., ge=0, le=100, description="Porcentaje de comisión (0-100)")
    precio_por_defecto: Optional[Decimal] = Field(None, gt=0, description="Precio por defecto (opcional)")
    
    @field_validator('nombre')
    @classmethod
    def validar_nombre_no_vacio(cls, v: str) -> str:
        """Valida que el nombre no sea solo espacios en blanco."""
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()
    
    @field_validator('porcentaje_comision')
    @classmethod
    def validar_porcentaje_rango(cls, v: float) -> float:
        """Valida que el porcentaje esté en el rango [0, 100]."""
        if v < 0 or v > 100:
            raise ValueError('El porcentaje de comisión debe estar entre 0 y 100')
        return v
    
    @field_validator('precio_por_defecto')
    @classmethod
    def validar_precio_positivo(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Valida que el precio sea positivo si se proporciona."""
        if v is not None and v <= 0:
            raise ValueError('El precio por defecto debe ser mayor que cero')
        return v


class TipoServicioUpdate(BaseModel):
    """Schema para actualizar un tipo de servicio existente."""
    descripcion: Optional[str] = Field(None, max_length=200, description="Descripción del servicio")
    porcentaje_comision: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de comisión (0-100)")
    precio_por_defecto: Optional[Decimal] = Field(None, gt=0, description="Precio por defecto (opcional)")
    
    @field_validator('porcentaje_comision')
    @classmethod
    def validar_porcentaje_rango(cls, v: Optional[float]) -> Optional[float]:
        """Valida que el porcentaje esté en el rango [0, 100]."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError('El porcentaje de comisión debe estar entre 0 y 100')
        return v
    
    @field_validator('precio_por_defecto')
    @classmethod
    def validar_precio_positivo(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Valida que el precio sea positivo si se proporciona."""
        if v is not None and v <= 0:
            raise ValueError('El precio por defecto debe ser mayor que cero')
        return v


class TipoServicioResponse(BaseModel):
    """Schema para respuesta de tipo de servicio."""
    model_config = ConfigDict(from_attributes=True)
    
    nombre: str
    descripcion: str
    porcentaje_comision: float
    precio_por_defecto: Optional[Decimal] = None


# ============================================================================
# SERVICIOS
# ============================================================================

class ServicioCreate(BaseModel):
    """Schema para registrar un nuevo servicio."""
    fecha: date = Field(..., description="Fecha del servicio")
    empleado_id: str = Field(..., description="ID del empleado que realizó el servicio")
    tipo_servicio: str = Field(..., description="Nombre del tipo de servicio")
    precio: Decimal = Field(..., gt=0, description="Precio del servicio (debe ser mayor que cero)")
    
    @field_validator('precio')
    @classmethod
    def validar_precio_positivo(cls, v: Decimal) -> Decimal:
        """Valida que el precio sea mayor que cero."""
        if v <= 0:
            raise ValueError('El precio debe ser mayor que cero')
        return v
    
    @field_validator('empleado_id')
    @classmethod
    def validar_empleado_id_no_vacio(cls, v: str) -> str:
        """Valida que el empleado_id no sea vacío."""
        if not v.strip():
            raise ValueError('El ID del empleado no puede estar vacío')
        return v.strip()
    
    @field_validator('tipo_servicio')
    @classmethod
    def validar_tipo_servicio_no_vacio(cls, v: str) -> str:
        """Valida que el tipo_servicio no sea vacío."""
        if not v.strip():
            raise ValueError('El tipo de servicio no puede estar vacío')
        return v.strip()


class ServicioResponse(BaseModel):
    """Schema para respuesta de servicio."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    fecha: date
    empleado_id: str
    tipo_servicio: str
    precio: Decimal
    comision_calculada: Decimal


# ============================================================================
# REPORTES
# ============================================================================

class IngresosResponse(BaseModel):
    """Schema para respuesta de ingresos totales."""
    total: Decimal = Field(..., description="Total de ingresos")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio del período")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin del período")


class BeneficiosResponse(BaseModel):
    """Schema para respuesta de beneficios."""
    ingresos: Decimal = Field(..., description="Total de ingresos")
    comisiones: Decimal = Field(..., description="Total de comisiones pagadas")
    beneficios: Decimal = Field(..., description="Beneficios (ingresos - comisiones)")
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio del período")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin del período")


class ServicioDetalle(BaseModel):
    """Schema para detalle de servicio en desglose de pago."""
    model_config = ConfigDict(from_attributes=True)
    
    fecha: date
    tipo_servicio: str
    precio: Decimal
    comision: Decimal


class DesglosePagoResponse(BaseModel):
    """Schema para respuesta de desglose de pago a empleado."""
    model_config = ConfigDict(from_attributes=True)
    
    empleado_id: str
    empleado_nombre: str
    servicios: List[ServicioDetalle]
    total: Decimal
SCHEMAS_PY

echo -e "${GREEN}✓ backend/app/schemas.py actualizado${NC}"

echo -e "\n${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Parte 2 completada!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📝 Archivos actualizados:${NC}"
echo "  ✓ backend/app/schemas.py"
echo ""
echo -e "${YELLOW}⚠️  Archivos pendientes:${NC}"
echo "  • backend/app/manager.py (muy largo, se actualizará en parte 3)"
echo "  • backend/app/main.py (muy largo, se actualizará en parte 3)"
echo "  • Archivos frontend (parte 4)"
echo ""

