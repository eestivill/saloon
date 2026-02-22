#!/bin/bash

# Script para actualizar el sistema con el campo precio_por_defecto
# Autor: Sistema de actualización automática
# Fecha: 2024

set -e  # Salir si hay algún error

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Actualización: Agregar Precio por Defecto               ║${NC}"
echo -e "${BLUE}║  a Tipos de Servicios                                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Función para crear backup
backup_file() {
    if [ -f "$1" ]; then
        cp "$1" "$1.backup_$(date +%Y%m%d_%H%M%S)"
        echo -e "${GREEN}✓ Backup creado: $1${NC}"
    fi
}

# Función para mostrar progreso
show_progress() {
    echo -e "\n${YELLOW}▶ $1${NC}"
}

# ============================================================================
# PASO 1: MIGRAR BASE DE DATOS
# ============================================================================

show_progress "Paso 1/10: Migrando base de datos..."
cd backend
sqlite3 salon.db "ALTER TABLE tipos_servicios ADD COLUMN precio_por_defecto NUMERIC(10, 2);" 2>/dev/null || echo -e "${YELLOW}⚠ Columna puede ya existir${NC}"
cd ..
echo -e "${GREEN}✓ Base de datos actualizada${NC}"

# ============================================================================
# PASO 2: ACTUALIZAR backend/app/models.py
# ============================================================================

show_progress "Paso 2/10: Actualizando backend/app/models.py..."
backup_file "backend/app/models.py"

cat > backend/app/models.py << 'MODELS_PY'
"""
Modelos de dominio para el sistema de gestión de salón de peluquería.
"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List, Any, Dict, Optional


@dataclass
class Empleado:
    """Modelo de dominio para un empleado del salón."""
    id: str
    nombre: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el empleado a diccionario."""
        return {
            "id": self.id,
            "nombre": self.nombre
        }
    
    @classmethod
    def from_orm(cls, orm_obj: Any) -> 'Empleado':
        """Crea un Empleado desde un objeto ORM."""
        return cls(
            id=orm_obj.id,
            nombre=orm_obj.nombre
        )


@dataclass
class TipoServicio:
    """Modelo de dominio para un tipo de servicio."""
    nombre: str
    descripcion: str
    porcentaje_comision: float
    precio_por_defecto: Optional[Decimal] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el tipo de servicio a diccionario."""
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "porcentaje_comision": self.porcentaje_comision,
            "precio_por_defecto": str(self.precio_por_defecto) if self.precio_por_defecto else None
        }
    
    @classmethod
    def from_orm(cls, orm_obj: Any) -> 'TipoServicio':
        """Crea un TipoServicio desde un objeto ORM."""
        return cls(
            nombre=orm_obj.nombre,
            descripcion=orm_obj.descripcion,
            porcentaje_comision=orm_obj.porcentaje_comision,
            precio_por_defecto=orm_obj.precio_por_defecto
        )


@dataclass
class ServicioRegistrado:
    """Modelo de dominio para un servicio registrado."""
    id: str
    fecha: date
    empleado_id: str
    tipo_servicio: str
    precio: Decimal
    comision_calculada: Decimal
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el servicio a diccionario."""
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "empleado_id": self.empleado_id,
            "tipo_servicio": self.tipo_servicio,
            "precio": str(self.precio),
            "comision_calculada": str(self.comision_calculada)
        }
    
    @classmethod
    def from_orm(cls, orm_obj: Any) -> 'ServicioRegistrado':
        """Crea un ServicioRegistrado desde un objeto ORM."""
        return cls(
            id=orm_obj.id,
            fecha=orm_obj.fecha,
            empleado_id=orm_obj.empleado_id,
            tipo_servicio=orm_obj.tipo_servicio,
            precio=orm_obj.precio,
            comision_calculada=orm_obj.comision_calculada
        )


@dataclass
class ServicioDetalle:
    """Detalle de un servicio para el desglose de pago."""
    fecha: date
    tipo_servicio: str
    precio: Decimal
    comision: Decimal
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el detalle a diccionario."""
        return {
            "fecha": self.fecha.isoformat(),
            "tipo_servicio": self.tipo_servicio,
            "precio": str(self.precio),
            "comision": str(self.comision)
        }


@dataclass
class DesglosePago:
    """Desglose de pago para un empleado."""
    empleado_id: str
    empleado_nombre: str
    servicios: List[ServicioDetalle]
    total: Decimal
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el desglose a diccionario."""
        return {
            "empleado_id": self.empleado_id,
            "empleado_nombre": self.empleado_nombre,
            "servicios": [s.to_dict() for s in self.servicios],
            "total": str(self.total)
        }
MODELS_PY

echo -e "${GREEN}✓ backend/app/models.py actualizado${NC}"

# ============================================================================
# PASO 3: ACTUALIZAR backend/app/orm_models.py
# ============================================================================

show_progress "Paso 3/10: Actualizando backend/app/orm_models.py..."
backup_file "backend/app/orm_models.py"

cat > backend/app/orm_models.py << 'ORM_MODELS_PY'
"""
Modelos ORM de SQLAlchemy para el sistema de gestión de salón de peluquería.
"""
from sqlalchemy import Column, String, Float, Date, Numeric, CheckConstraint, Index
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class EmpleadoORM(Base):
    """Modelo ORM para la tabla empleados."""
    __tablename__ = 'empleados'
    
    id = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<Empleado(id='{self.id}', nombre='{self.nombre}')>"


class TipoServicioORM(Base):
    """Modelo ORM para la tabla tipos_servicios."""
    __tablename__ = 'tipos_servicios'
    
    nombre = Column(String(50), primary_key=True)
    descripcion = Column(String(200), nullable=False)
    porcentaje_comision = Column(Float, nullable=False)
    precio_por_defecto = Column(Numeric(10, 2), nullable=True)
    
    __table_args__ = (
        CheckConstraint(
            'porcentaje_comision >= 0 AND porcentaje_comision <= 100',
            name='check_porcentaje_comision_range'
        ),
        CheckConstraint(
            'precio_por_defecto IS NULL OR precio_por_defecto > 0',
            name='check_precio_por_defecto_positive'
        ),
    )
    
    def __repr__(self):
        return f"<TipoServicio(nombre='{self.nombre}', comision={self.porcentaje_comision}%)>"


class ServicioORM(Base):
    """Modelo ORM para la tabla servicios."""
    __tablename__ = 'servicios'
    
    id = Column(String(50), primary_key=True)
    fecha = Column(Date, nullable=False, index=True)
    empleado_id = Column(String(50), nullable=False, index=True)
    tipo_servicio = Column(String(50), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    comision_calculada = Column(Numeric(10, 2), nullable=False)
    
    __table_args__ = (
        CheckConstraint('precio > 0', name='check_precio_positive'),
        Index('idx_servicios_empleado_fecha', 'empleado_id', 'fecha'),
        Index('idx_servicios_fecha', 'fecha'),
    )
    
    def __repr__(self):
        return f"<Servicio(id='{self.id}', empleado='{self.empleado_id}', fecha={self.fecha})>"
ORM_MODELS_PY

echo -e "${GREEN}✓ backend/app/orm_models.py actualizado${NC}"

echo -e "\n${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Actualización completada exitosamente!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📝 Archivos actualizados:${NC}"
echo "  ✓ Base de datos migrada"
echo "  ✓ backend/app/models.py"
echo "  ✓ backend/app/orm_models.py"
echo ""
echo -e "${YELLOW}⚠️  Archivos pendientes (actualizar manualmente):${NC}"
echo "  • backend/app/schemas.py"
echo "  • backend/app/manager.py"
echo "  • backend/app/main.py"
echo "  • frontend/src/types/models.ts"
echo "  • frontend/src/components/tipos-servicios/TipoServicioForm.vue"
echo "  • frontend/src/components/tipos-servicios/TipoServicioCard.vue"
echo "  • frontend/src/components/servicios/ServicioForm.vue"
echo ""
echo -e "${BLUE}💡 Los backups se guardaron con extensión .backup_TIMESTAMP${NC}"
echo ""

