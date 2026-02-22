# Diseño Técnico: Sistema de Gestión de Salón de Peluquería

## Overview

El sistema de gestión de salón de peluquería es una aplicación web mobile-first que permite registrar servicios realizados, calcular ingresos totales y gestionar el pago a empleados basado en comisiones. El diseño se centra en tres entidades principales: Empleados, Tipos de Servicios y Registros de Servicios.

La arquitectura sigue un patrón cliente-servidor con separación clara entre frontend (Vue 3 + TypeScript) y backend (FastAPI + Python). El backend expone una API REST que el frontend consume. El sistema utiliza SQLite para persistencia de datos, garantizando mejor rendimiento y capacidades de consulta que archivos JSON.

### Objetivos del Diseño

- Proporcionar una API REST clara y documentada para gestionar empleados, tipos de servicios y registros de servicios
- Ofrecer una interfaz web responsive con diseño mobile-first para acceso desde cualquier dispositivo
- Calcular automáticamente comisiones basadas en porcentajes configurables por tipo de servicio
- Permitir consultas flexibles por empleado, fecha y tipo de servicio
- Garantizar la integridad y persistencia de los datos mediante base de datos relacional
- Proporcionar una experiencia de usuario fluida y moderna con Vue 3

## Architecture

El sistema sigue una arquitectura cliente-servidor con separación clara entre frontend y backend:

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Cliente)                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Vue 3 + TypeScript + Tailwind CSS          │    │
│  │  - Componentes reactivos                           │    │
│  │  - Gestión de estado (Pinia)                       │    │
│  │  - Validación de formularios                       │    │
│  │  - Diseño mobile-first responsive                  │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          │ HTTP/JSON                         │
│                          ▼                                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Servidor)                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              FastAPI (Python)                      │    │
│  │  - Endpoints REST                                  │    │
│  │  - Validación con Pydantic                         │    │
│  │  - Documentación automática (OpenAPI)             │    │
│  │  - CORS configurado                                │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Business Logic Layer                     │    │
│  │  - SalonManager                                    │    │
│  │  - Cálculo de comisiones                           │    │
│  │  - Validaciones de negocio                         │    │
│  │  - Filtrado y consultas                            │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Data Access Layer                        │    │
│  │  - Repository pattern                              │    │
│  │  - SQLAlchemy ORM                                  │    │
│  │  - Gestión de transacciones                        │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │              SQLite Database                       │    │
│  │  - Tabla: empleados                                │    │
│  │  - Tabla: tipos_servicios                          │    │
│  │  - Tabla: servicios                                │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

1. **Registro de Servicio**: 
   - Usuario interactúa con formulario Vue → 
   - POST /api/servicios → 
   - FastAPI endpoint → 
   - SalonManager → 
   - Validación → 
   - Repository → 
   - SQLite → 
   - Respuesta JSON → 
   - Actualización UI reactiva

2. **Cálculo de Comisiones**: 
   - Usuario solicita reporte → 
   - GET /api/empleados/{id}/pago → 
   - FastAPI endpoint → 
   - SalonManager → 
   - Consulta SQLite → 
   - Cálculo → 
   - Respuesta JSON → 
   - Renderizado en Vue

3. **Consultas**: 
   - Usuario aplica filtros → 
   - GET /api/servicios?empleado_id=X&fecha_inicio=Y → 
   - FastAPI endpoint → 
   - SalonManager → 
   - Query SQLite → 
   - Respuesta JSON → 
   - Tabla/lista reactiva en Vue

### Tecnologías Clave

**Frontend**:
- Vue 3 (Composition API)
- TypeScript para type safety
- Tailwind CSS para diseño mobile-first
- Pinia para gestión de estado
- Axios para llamadas HTTP
- Vite como build tool

**Backend**:
- FastAPI para API REST
- Pydantic para validación de datos
- SQLAlchemy como ORM
- SQLite como base de datos
- Uvicorn como servidor ASGI

## Components and Interfaces

### Backend Components

#### 1. FastAPI Application

Aplicación principal que expone la API REST.

```python
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from datetime import date
from decimal import Decimal

app = FastAPI(
    title="Sistema de Gestión de Salón de Peluquería",
    description="API REST para gestión de empleados, servicios y comisiones",
    version="1.0.0"
)

# Configuración CORS para permitir acceso desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL del frontend en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. API Endpoints

**Empleados**:

```python
# GET /api/empleados - Listar todos los empleados
@app.get("/api/empleados", response_model=List[EmpleadoResponse])
async def listar_empleados()

# GET /api/empleados/{id} - Obtener empleado por ID
@app.get("/api/empleados/{id}", response_model=EmpleadoResponse)
async def obtener_empleado(id: str)

# POST /api/empleados - Crear nuevo empleado
@app.post("/api/empleados", response_model=EmpleadoResponse, status_code=201)
async def crear_empleado(empleado: EmpleadoCreate)

# PUT /api/empleados/{id} - Actualizar empleado
@app.put("/api/empleados/{id}", response_model=EmpleadoResponse)
async def actualizar_empleado(id: str, empleado: EmpleadoUpdate)

# DELETE /api/empleados/{id} - Eliminar empleado
@app.delete("/api/empleados/{id}", status_code=204)
async def eliminar_empleado(id: str)
```

**Tipos de Servicios**:

```python
# GET /api/tipos-servicios - Listar todos los tipos de servicios
@app.get("/api/tipos-servicios", response_model=List[TipoServicioResponse])
async def listar_tipos_servicios()

# GET /api/tipos-servicios/{nombre} - Obtener tipo de servicio
@app.get("/api/tipos-servicios/{nombre}", response_model=TipoServicioResponse)
async def obtener_tipo_servicio(nombre: str)

# POST /api/tipos-servicios - Crear nuevo tipo de servicio
@app.post("/api/tipos-servicios", response_model=TipoServicioResponse, status_code=201)
async def crear_tipo_servicio(tipo: TipoServicioCreate)

# PUT /api/tipos-servicios/{nombre} - Actualizar tipo de servicio
@app.put("/api/tipos-servicios/{nombre}", response_model=TipoServicioResponse)
async def actualizar_tipo_servicio(nombre: str, tipo: TipoServicioUpdate)

# DELETE /api/tipos-servicios/{nombre} - Eliminar tipo de servicio
@app.delete("/api/tipos-servicios/{nombre}", status_code=204)
async def eliminar_tipo_servicio(nombre: str)
```

**Servicios**:

```python
# GET /api/servicios - Listar servicios con filtros opcionales
@app.get("/api/servicios", response_model=List[ServicioResponse])
async def listar_servicios(
    empleado_id: Optional[str] = Query(None),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None)
)

# GET /api/servicios/{id} - Obtener servicio por ID
@app.get("/api/servicios/{id}", response_model=ServicioResponse)
async def obtener_servicio(id: str)

# POST /api/servicios - Registrar nuevo servicio
@app.post("/api/servicios", response_model=ServicioResponse, status_code=201)
async def registrar_servicio(servicio: ServicioCreate)

# DELETE /api/servicios/{id} - Eliminar servicio
@app.delete("/api/servicios/{id}", status_code=204)
async def eliminar_servicio(id: str)
```

**Reportes y Cálculos**:

```python
# GET /api/reportes/ingresos - Calcular ingresos totales
@app.get("/api/reportes/ingresos", response_model=IngresosResponse)
async def calcular_ingresos(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None)
)

# GET /api/reportes/beneficios - Calcular beneficios
@app.get("/api/reportes/beneficios", response_model=BeneficiosResponse)
async def calcular_beneficios(
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None)
)

# GET /api/empleados/{id}/pago - Calcular pago de empleado
@app.get("/api/empleados/{id}/pago", response_model=DesglosePagoResponse)
async def calcular_pago_empleado(
    id: str,
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None)
)
```

#### 3. Pydantic Models (Request/Response)

Modelos para validación de entrada y serialización de respuestas.

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date
from decimal import Decimal

# Empleados
class EmpleadoCreate(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=100)

class EmpleadoUpdate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)

class EmpleadoResponse(BaseModel):
    id: str
    nombre: str
    
    class Config:
        orm_mode = True

# Tipos de Servicios
class TipoServicioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    descripcion: str = Field(..., max_length=200)
    porcentaje_comision: float = Field(..., ge=0, le=100)

class TipoServicioUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, max_length=200)
    porcentaje_comision: Optional[float] = Field(None, ge=0, le=100)

class TipoServicioResponse(BaseModel):
    nombre: str
    descripcion: str
    porcentaje_comision: float
    
    class Config:
        orm_mode = True

# Servicios
class ServicioCreate(BaseModel):
    fecha: date
    empleado_id: str
    tipo_servicio: str
    precio: Decimal = Field(..., gt=0)
    
    @validator('precio')
    def validar_precio_positivo(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor que cero')
        return v

class ServicioResponse(BaseModel):
    id: str
    fecha: date
    empleado_id: str
    tipo_servicio: str
    precio: Decimal
    comision_calculada: Decimal
    
    class Config:
        orm_mode = True

# Reportes
class IngresosResponse(BaseModel):
    total: Decimal
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]

class BeneficiosResponse(BaseModel):
    ingresos: Decimal
    comisiones: Decimal
    beneficios: Decimal
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]

class ServicioDetalle(BaseModel):
    fecha: date
    tipo_servicio: str
    precio: Decimal
    comision: Decimal

class DesglosePagoResponse(BaseModel):
    empleado_id: str
    empleado_nombre: str
    servicios: List[ServicioDetalle]
    total: Decimal
```

#### 4. SalonManager (Business Logic)

Componente principal que coordina todas las operaciones del sistema (sin cambios en la lógica).

```python
class SalonManager:
    def __init__(self, data_repository: DataRepository):
        """Inicializa el gestor con un repositorio de datos"""
        
    # Gestión de Empleados
    def crear_empleado(self, id: str, nombre: str) -> Result[Empleado, Error]
    def obtener_empleado(self, id: str) -> Optional[Empleado]
    def listar_empleados(self) -> List[Empleado]
    def actualizar_empleado(self, id: str, nombre: str) -> Result[Empleado, Error]
    
    # Gestión de Tipos de Servicios
    def crear_tipo_servicio(self, nombre: str, descripcion: str, 
                           porcentaje_comision: float) -> Result[TipoServicio, Error]
    def obtener_tipo_servicio(self, nombre: str) -> Optional[TipoServicio]
    def listar_tipos_servicios(self) -> List[TipoServicio]
    def actualizar_tipo_servicio(self, nombre: str, 
                                 porcentaje_comision: float) -> Result[TipoServicio, Error]
    
    # Registro de Servicios
    def registrar_servicio(self, fecha: date, empleado_id: str, 
                          tipo_servicio: str, precio: Decimal) -> Result[ServicioRegistrado, Error]
    def obtener_servicios(self, empleado_id: Optional[str] = None,
                         fecha_inicio: Optional[date] = None,
                         fecha_fin: Optional[date] = None) -> List[ServicioRegistrado]
    
    # Cálculos Financieros
    def calcular_ingresos_totales(self, fecha_inicio: Optional[date] = None,
                                 fecha_fin: Optional[date] = None) -> Decimal
    def calcular_beneficios(self, fecha_inicio: Optional[date] = None,
                           fecha_fin: Optional[date] = None) -> Decimal
    def calcular_pago_empleado(self, empleado_id: str,
                              fecha_inicio: Optional[date] = None,
                              fecha_fin: Optional[date] = None) -> DesglosePago
```

#### 5. DataRepository (SQLAlchemy)

Interfaz para el acceso a datos con implementación basada en SQLAlchemy.

```python
from sqlalchemy import create_engine, Column, String, Float, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

# Modelos ORM
class EmpleadoORM(Base):
    __tablename__ = 'empleados'
    id = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False)

class TipoServicioORM(Base):
    __tablename__ = 'tipos_servicios'
    nombre = Column(String(50), primary_key=True)
    descripcion = Column(String(200), nullable=False)
    porcentaje_comision = Column(Float, nullable=False)

class ServicioORM(Base):
    __tablename__ = 'servicios'
    id = Column(String(50), primary_key=True)
    fecha = Column(Date, nullable=False)
    empleado_id = Column(String(50), nullable=False)
    tipo_servicio = Column(String(50), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    comision_calculada = Column(Numeric(10, 2), nullable=False)

class DataRepository(ABC):
    @abstractmethod
    def guardar_empleado(self, empleado: Empleado) -> None
    
    @abstractmethod
    def obtener_empleado(self, id: str) -> Optional[Empleado]
    
    @abstractmethod
    def listar_empleados(self) -> List[Empleado]
    
    @abstractmethod
    def guardar_tipo_servicio(self, tipo: TipoServicio) -> None
    
    @abstractmethod
    def obtener_tipo_servicio(self, nombre: str) -> Optional[TipoServicio]
    
    @abstractmethod
    def listar_tipos_servicios(self) -> List[TipoServicio]
    
    @abstractmethod
    def guardar_servicio(self, servicio: ServicioRegistrado) -> None
    
    @abstractmethod
    def listar_servicios(self) -> List[ServicioRegistrado]

class SQLAlchemyRepository(DataRepository):
    def __init__(self, database_url: str = "sqlite:///salon.db"):
        """Inicializa el repositorio con la URL de la base de datos"""
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def get_session(self) -> Session:
        """Obtiene una sesión de base de datos"""
        return self.SessionLocal()
```

#### 6. Validation Module

Módulo de validaciones reutilizables (sin cambios).

```python
class Validator:
    @staticmethod
    def validar_porcentaje_comision(porcentaje: float) -> Result[float, Error]
        """Valida que el porcentaje esté entre 0 y 100"""
        
    @staticmethod
    def validar_precio(precio: Decimal) -> Result[Decimal, Error]
        """Valida que el precio sea mayor que cero"""
        
    @staticmethod
    def validar_rango_fechas(fecha_inicio: Optional[date], 
                            fecha_fin: Optional[date]) -> Result[Tuple[date, date], Error]
        """Valida que fecha_inicio <= fecha_fin"""
        
    @staticmethod
    def validar_identificador_unico(id: str, existentes: Set[str]) -> Result[str, Error]
        """Valida que el identificador no exista"""
```

### Frontend Components (Vue 3)

#### 1. Estructura de Componentes

```
src/
├── components/
│   ├── empleados/
│   │   ├── EmpleadosList.vue
│   │   ├── EmpleadoForm.vue
│   │   └── EmpleadoCard.vue
│   ├── servicios/
│   │   ├── ServiciosList.vue
│   │   ├── ServicioForm.vue
│   │   ├── ServicioFilters.vue
│   │   └── ServicioCard.vue
│   ├── tipos-servicios/
│   │   ├── TiposServiciosList.vue
│   │   ├── TipoServicioForm.vue
│   │   └── TipoServicioCard.vue
│   ├── reportes/
│   │   ├── IngresosReport.vue
│   │   ├── BeneficiosReport.vue
│   │   └── PagoEmpleadoReport.vue
│   └── common/
│       ├── AppHeader.vue
│       ├── AppNavigation.vue
│       ├── LoadingSpinner.vue
│       └── ErrorMessage.vue
├── stores/
│   ├── empleados.ts
│   ├── servicios.ts
│   ├── tiposServicios.ts
│   └── reportes.ts
├── services/
│   └── api.ts
├── types/
│   └── models.ts
├── views/
│   ├── HomeView.vue
│   ├── EmpleadosView.vue
│   ├── ServiciosView.vue
│   ├── TiposServiciosView.vue
│   └── ReportesView.vue
├── router/
│   └── index.ts
├── App.vue
└── main.ts
```

#### 2. API Service (Axios)

```typescript
// src/services/api.ts
import axios from 'axios';
import type { 
  Empleado, 
  TipoServicio, 
  Servicio, 
  DesglosePago 
} from '@/types/models';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const empleadosAPI = {
  listar: () => api.get<Empleado[]>('/empleados'),
  obtener: (id: string) => api.get<Empleado>(`/empleados/${id}`),
  crear: (data: { id: string; nombre: string }) => 
    api.post<Empleado>('/empleados', data),
  actualizar: (id: string, data: { nombre: string }) => 
    api.put<Empleado>(`/empleados/${id}`, data),
  eliminar: (id: string) => api.delete(`/empleados/${id}`),
  obtenerPago: (id: string, params?: { fecha_inicio?: string; fecha_fin?: string }) =>
    api.get<DesglosePago>(`/empleados/${id}/pago`, { params }),
};

export const tiposServiciosAPI = {
  listar: () => api.get<TipoServicio[]>('/tipos-servicios'),
  obtener: (nombre: string) => api.get<TipoServicio>(`/tipos-servicios/${nombre}`),
  crear: (data: { nombre: string; descripcion: string; porcentaje_comision: number }) =>
    api.post<TipoServicio>('/tipos-servicios', data),
  actualizar: (nombre: string, data: Partial<TipoServicio>) =>
    api.put<TipoServicio>(`/tipos-servicios/${nombre}`, data),
  eliminar: (nombre: string) => api.delete(`/tipos-servicios/${nombre}`),
};

export const serviciosAPI = {
  listar: (params?: { empleado_id?: string; fecha_inicio?: string; fecha_fin?: string }) =>
    api.get<Servicio[]>('/servicios', { params }),
  obtener: (id: string) => api.get<Servicio>(`/servicios/${id}`),
  crear: (data: { fecha: string; empleado_id: string; tipo_servicio: string; precio: number }) =>
    api.post<Servicio>('/servicios', data),
  eliminar: (id: string) => api.delete(`/servicios/${id}`),
};

export const reportesAPI = {
  ingresos: (params?: { fecha_inicio?: string; fecha_fin?: string }) =>
    api.get('/reportes/ingresos', { params }),
  beneficios: (params?: { fecha_inicio?: string; fecha_fin?: string }) =>
    api.get('/reportes/beneficios', { params }),
};
```

#### 3. Pinia Store Example

```typescript
// src/stores/empleados.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { empleadosAPI } from '@/services/api';
import type { Empleado } from '@/types/models';

export const useEmpleadosStore = defineStore('empleados', () => {
  const empleados = ref<Empleado[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const empleadosOrdenados = computed(() => 
    [...empleados.value].sort((a, b) => a.nombre.localeCompare(b.nombre))
  );

  async function cargarEmpleados() {
    loading.value = true;
    error.value = null;
    try {
      const response = await empleadosAPI.listar();
      empleados.value = response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cargar empleados';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function crearEmpleado(data: { id: string; nombre: string }) {
    loading.value = true;
    error.value = null;
    try {
      const response = await empleadosAPI.crear(data);
      empleados.value.push(response.data);
      return response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al crear empleado';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return {
    empleados,
    empleadosOrdenados,
    loading,
    error,
    cargarEmpleados,
    crearEmpleado,
  };
});
```

#### 4. Vue Component Example (Mobile-First)

```vue
<!-- src/components/empleados/EmpleadosList.vue -->
<template>
  <div class="container mx-auto px-4 py-6">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <h2 class="text-2xl font-bold text-gray-800">Empleados</h2>
      <button 
        @click="mostrarFormulario = true"
        class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition"
      >
        + Nuevo Empleado
      </button>
    </div>

    <LoadingSpinner v-if="loading" />
    <ErrorMessage v-else-if="error" :message="error" />
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <EmpleadoCard 
        v-for="empleado in empleadosOrdenados" 
        :key="empleado.id"
        :empleado="empleado"
        @editar="editarEmpleado"
        @eliminar="eliminarEmpleado"
      />
    </div>

    <EmpleadoForm 
      v-if="mostrarFormulario"
      :empleado="empleadoSeleccionado"
      @guardar="guardarEmpleado"
      @cancelar="cerrarFormulario"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useEmpleadosStore } from '@/stores/empleados';
import { storeToRefs } from 'pinia';
import EmpleadoCard from './EmpleadoCard.vue';
import EmpleadoForm from './EmpleadoForm.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';

const store = useEmpleadosStore();
const { empleadosOrdenados, loading, error } = storeToRefs(store);

const mostrarFormulario = ref(false);
const empleadoSeleccionado = ref(null);

onMounted(() => {
  store.cargarEmpleados();
});

function editarEmpleado(empleado: any) {
  empleadoSeleccionado.value = empleado;
  mostrarFormulario.value = true;
}

function cerrarFormulario() {
  mostrarFormulario.value = false;
  empleadoSeleccionado.value = null;
}

async function guardarEmpleado(data: any) {
  await store.crearEmpleado(data);
  cerrarFormulario();
}
</script>
```

## Data Models

### Backend Models (Python)

#### Domain Models

```python
@dataclass
class Empleado:
    id: str              # Identificador único
    nombre: str          # Nombre del empleado
    
    def to_dict(self) -> dict:
        """Serializa a diccionario"""
        return {"id": self.id, "nombre": self.nombre}
        
    @classmethod
    def from_orm(cls, orm_obj: EmpleadoORM) -> 'Empleado':
        """Crea desde objeto ORM"""
        return cls(id=orm_obj.id, nombre=orm_obj.nombre)
```

```python
@dataclass
class TipoServicio:
    nombre: str                    # Nombre único del tipo de servicio
    descripcion: str               # Descripción del servicio
    porcentaje_comision: float     # Porcentaje entre 0 y 100
    
    def to_dict(self) -> dict:
        """Serializa a diccionario"""
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "porcentaje_comision": self.porcentaje_comision
        }
        
    @classmethod
    def from_orm(cls, orm_obj: TipoServicioORM) -> 'TipoServicio':
        """Crea desde objeto ORM"""
        return cls(
            nombre=orm_obj.nombre,
            descripcion=orm_obj.descripcion,
            porcentaje_comision=orm_obj.porcentaje_comision
        )
```

```python
@dataclass
class ServicioRegistrado:
    id: str                    # Identificador único generado automáticamente
    fecha: date                # Fecha del servicio
    empleado_id: str           # Referencia al empleado
    tipo_servicio: str         # Referencia al tipo de servicio
    precio: Decimal            # Precio del servicio
    comision_calculada: Decimal  # Comisión calculada al momento del registro
    
    def to_dict(self) -> dict:
        """Serializa a diccionario"""
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "empleado_id": self.empleado_id,
            "tipo_servicio": self.tipo_servicio,
            "precio": str(self.precio),
            "comision_calculada": str(self.comision_calculada)
        }
        
    @classmethod
    def from_orm(cls, orm_obj: ServicioORM) -> 'ServicioRegistrado':
        """Crea desde objeto ORM"""
        return cls(
            id=orm_obj.id,
            fecha=orm_obj.fecha,
            empleado_id=orm_obj.empleado_id,
            tipo_servicio=orm_obj.tipo_servicio,
            precio=orm_obj.precio,
            comision_calculada=orm_obj.comision_calculada
        )
```

```python
@dataclass
class DesglosePago:
    empleado_id: str
    empleado_nombre: str
    servicios: List[ServicioDetalle]
    total: Decimal
    
@dataclass
class ServicioDetalle:
    fecha: date
    tipo_servicio: str
    precio: Decimal
    comision: Decimal
```

#### SQLAlchemy ORM Models

```python
from sqlalchemy import Column, String, Float, Date, Numeric, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EmpleadoORM(Base):
    __tablename__ = 'empleados'
    
    id = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<Empleado(id='{self.id}', nombre='{self.nombre}')>"

class TipoServicioORM(Base):
    __tablename__ = 'tipos_servicios'
    
    nombre = Column(String(50), primary_key=True)
    descripcion = Column(String(200), nullable=False)
    porcentaje_comision = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"<TipoServicio(nombre='{self.nombre}', comision={self.porcentaje_comision}%)>"

class ServicioORM(Base):
    __tablename__ = 'servicios'
    
    id = Column(String(50), primary_key=True)
    fecha = Column(Date, nullable=False, index=True)
    empleado_id = Column(String(50), nullable=False, index=True)
    tipo_servicio = Column(String(50), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    comision_calculada = Column(Numeric(10, 2), nullable=False)
    
    # Índices para mejorar rendimiento de consultas
    __table_args__ = (
        Index('idx_empleado_fecha', 'empleado_id', 'fecha'),
        Index('idx_fecha', 'fecha'),
    )
    
    def __repr__(self):
        return f"<Servicio(id='{self.id}', empleado='{self.empleado_id}', fecha={self.fecha})>"
```

### Frontend Models (TypeScript)

```typescript
// src/types/models.ts

export interface Empleado {
  id: string;
  nombre: string;
}

export interface TipoServicio {
  nombre: string;
  descripcion: string;
  porcentaje_comision: number;
}

export interface Servicio {
  id: string;
  fecha: string;  // ISO date string
  empleado_id: string;
  tipo_servicio: string;
  precio: number;
  comision_calculada: number;
}

export interface ServicioDetalle {
  fecha: string;
  tipo_servicio: string;
  precio: number;
  comision: number;
}

export interface DesglosePago {
  empleado_id: string;
  empleado_nombre: string;
  servicios: ServicioDetalle[];
  total: number;
}

export interface IngresosResponse {
  total: number;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface BeneficiosResponse {
  ingresos: number;
  comisiones: number;
  beneficios: number;
  fecha_inicio?: string;
  fecha_fin?: string;
}

// Tipos para formularios
export interface EmpleadoFormData {
  id: string;
  nombre: string;
}

export interface TipoServicioFormData {
  nombre: string;
  descripcion: string;
  porcentaje_comision: number;
}

export interface ServicioFormData {
  fecha: string;
  empleado_id: string;
  tipo_servicio: string;
  precio: number;
}

// Tipos para filtros
export interface ServiciosFiltros {
  empleado_id?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}
```

### Result Type (Backend)

```python
from typing import TypeVar, Generic, Union

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Ok(Generic[T]):
    value: T

@dataclass
class Err(Generic[E]):
    error: E

Result = Union[Ok[T], Err[E]]
```

### Error Types (Backend)

```python
@dataclass
class ValidationError:
    message: str
    field: Optional[str] = None

@dataclass
class NotFoundError:
    entity: str
    identifier: str

@dataclass
class DuplicateError:
    entity: str
    identifier: str

@dataclass
class PersistenceError:
    message: str
    context: Optional[str] = None
```

### Database Schema (SQLite)

```sql
-- Tabla de empleados
CREATE TABLE empleados (
    id VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla de tipos de servicios
CREATE TABLE tipos_servicios (
    nombre VARCHAR(50) PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL,
    porcentaje_comision REAL NOT NULL CHECK (porcentaje_comision >= 0 AND porcentaje_comision <= 100)
);

-- Tabla de servicios registrados
CREATE TABLE servicios (
    id VARCHAR(50) PRIMARY KEY,
    fecha DATE NOT NULL,
    empleado_id VARCHAR(50) NOT NULL,
    tipo_servicio VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0),
    comision_calculada DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id),
    FOREIGN KEY (tipo_servicio) REFERENCES tipos_servicios(nombre)
);

-- Índices para optimizar consultas
CREATE INDEX idx_servicios_empleado_fecha ON servicios(empleado_id, fecha);
CREATE INDEX idx_servicios_fecha ON servicios(fecha);
```


## Correctness Properties

*Una propiedad es una característica o comportamiento que debe mantenerse verdadero en todas las ejecuciones válidas de un sistema - esencialmente, una declaración formal sobre lo que el sistema debe hacer. Las propiedades sirven como puente entre las especificaciones legibles por humanos y las garantías de corrección verificables por máquinas.*

### Property 1: Creación de Empleados con Atributos Válidos

*Para cualquier* nombre e identificador únicos proporcionados, crear un empleado debe resultar en un empleado almacenado con exactamente esos atributos.

**Validates: Requirements 1.1**

### Property 2: Unicidad de Identificadores de Empleados

*Para cualquier* sistema con empleados existentes, intentar crear un segundo empleado con un identificador ya existente debe fallar, mientras que el primer empleado permanece sin cambios.

**Validates: Requirements 1.2**

### Property 3: Consulta Completa de Empleados

*Para cualquier* conjunto de empleados creados, consultar la lista de empleados debe retornar todos y solo esos empleados.

**Validates: Requirements 1.4**

### Property 4: Actualización de Empleados Preserva Identidad

*Para cualquier* empleado existente, actualizar su nombre debe preservar su identificador y reflejar el nuevo nombre en consultas posteriores.

**Validates: Requirements 1.5**

### Property 5: Creación de Tipos de Servicio con Atributos Válidos

*Para cualquier* nombre único, descripción y porcentaje de comisión válido (0-100), crear un tipo de servicio debe resultar en un tipo almacenado con exactamente esos atributos.

**Validates: Requirements 2.1**

### Property 6: Validación de Rango de Porcentaje de Comisión

*Para cualquier* porcentaje fuera del rango [0, 100], intentar crear o actualizar un tipo de servicio debe fallar con un error de validación.

**Validates: Requirements 2.2**

### Property 7: Unicidad de Nombres de Tipos de Servicio

*Para cualquier* sistema con tipos de servicio existentes, intentar crear un segundo tipo con un nombre ya existente debe fallar.

**Validates: Requirements 2.3**

### Property 8: Consulta Completa de Tipos de Servicios

*Para cualquier* conjunto de tipos de servicios creados, consultar la lista debe retornar todos y solo esos tipos.

**Validates: Requirements 2.5**

### Property 9: Actualización de Porcentaje de Comisión

*Para cualquier* tipo de servicio existente y porcentaje válido, actualizar el porcentaje debe reflejarse en consultas posteriores y en nuevos servicios registrados.

**Validates: Requirements 2.6**

### Property 10: Registro de Servicio con Todos los Atributos

*Para cualquier* fecha, empleado existente, tipo de servicio existente y precio válido, registrar un servicio debe crear un registro con todos esos atributos más un ID único y la comisión calculada.

**Validates: Requirements 3.1**

### Property 11: Validación de Precio Positivo

*Para cualquier* precio menor o igual a cero, intentar registrar un servicio debe fallar con un error de validación.

**Validates: Requirements 3.2**

### Property 12: Validación de Integridad Referencial

*Para cualquier* intento de registrar un servicio con un empleado_id o tipo_servicio que no exista en el sistema, la operación debe fallar con un error de referencia no encontrada.

**Validates: Requirements 3.3, 3.4**

### Property 13: Cálculo Correcto de Ingresos Totales

*Para cualquier* conjunto de servicios registrados, la suma de ingresos totales debe ser igual a la suma de los precios de todos los servicios.

**Validates: Requirements 4.1**

### Property 14: Filtrado de Ingresos por Rango de Fechas

*Para cualquier* conjunto de servicios y rango de fechas [fecha_inicio, fecha_fin], los ingresos calculados deben incluir solo servicios cuya fecha esté dentro del rango inclusivo.

**Validates: Requirements 4.2, 7.1, 7.2, 7.3**

### Property 15: Cálculo de Beneficios como Ingresos Menos Comisiones

*Para cualquier* conjunto de servicios en un período, los beneficios deben ser iguales a la suma de precios menos la suma de comisiones de todos los servicios en ese período.

**Validates: Requirements 4.2**

### Property 16: Formato Monetario Contiene Símbolos Apropiados

*Para cualquier* valor monetario mostrado (ingresos o beneficios), el formato debe incluir separadores decimales y símbolos de moneda apropiados.

**Validates: Requirements 4.3**

### Property 17: Ingresos se Actualizan Inmediatamente

*Para cualquier* estado del sistema, agregar un nuevo servicio debe incrementar los ingresos totales inmediatamente por el precio de ese servicio.

**Validates: Requirements 4.5**

### Property 18: Cálculo de Comisión Individual

*Para cualquier* servicio registrado, la comisión calculada debe ser igual al precio del servicio multiplicado por el porcentaje de comisión del tipo de servicio asociado (dividido por 100).

**Validates: Requirements 2.7, 5.1**

### Property 19: Suma de Comisiones por Empleado

*Para cualquier* empleado con servicios registrados, el pago total debe ser igual a la suma de todas las comisiones de sus servicios.

**Validates: Requirements 5.2**

### Property 20: Filtrado de Pagos por Período

*Para cualquier* empleado y rango de fechas, el pago calculado debe incluir solo las comisiones de servicios dentro del rango especificado.

**Validates: Requirements 5.3**

### Property 21: Desglose de Pago Contiene Todos los Servicios

*Para cualquier* empleado, el desglose de pago debe incluir todos los servicios realizados por ese empleado con fecha, tipo, precio y comisión, más el total correcto.

**Validates: Requirements 5.4**

### Property 22: Filtrado de Servicios por Empleado

*Para cualquier* empleado_id y conjunto de servicios, consultar servicios por empleado debe retornar todos y solo los servicios donde empleado_id coincide.

**Validates: Requirements 6.1**

### Property 23: Ordenamiento Descendente por Fecha

*Para cualquier* lista de servicios retornada, los servicios deben estar ordenados por fecha de forma descendente (más recientes primero).

**Validates: Requirements 6.2**

### Property 24: Servicios Contienen Información Completa

*Para cualquier* servicio en una consulta, debe incluir fecha, tipo de servicio, precio y comisión calculada.

**Validates: Requirements 6.4**

### Property 25: Validación de Rango de Fechas

*Para cualquier* fecha_inicio y fecha_fin donde fecha_inicio > fecha_fin, la operación debe fallar con un error de validación.

**Validates: Requirements 7.4**

### Property 26: Persistencia Round-Trip para Todas las Entidades

*Para cualquier* entidad (Empleado, TipoServicio o ServicioRegistrado) creada y guardada, cargar los datos desde persistencia debe recuperar una entidad equivalente con todos sus atributos intactos.

**Validates: Requirements 3.6, 8.1, 8.2, 8.3, 8.4**

### Property 27: Validación de Integridad al Cargar Datos

*Para cualquier* archivo de datos con formato inválido o datos corruptos, el sistema debe detectar el error al cargar y reportar un mensaje de error descriptivo.

**Validates: Requirements 8.6**

## Error Handling

El sistema implementa un manejo de errores robusto tanto en el backend como en el frontend.

### Backend Error Handling

#### 1. Patrón Result para Lógica de Negocio

La capa de lógica de negocio utiliza el patrón Result para operaciones que pueden fallar:

```python
resultado = salon_manager.crear_empleado("E001", "Juan Pérez")

match resultado:
    case Ok(empleado):
        return empleado
    case Err(ValidationError(message, field)):
        raise HTTPException(status_code=400, detail={"error": message, "field": field})
    case Err(DuplicateError(entity, identifier)):
        raise HTTPException(status_code=409, detail=f"{entity} con identificador {identifier} ya existe")
```

#### 2. HTTP Status Codes

La API REST utiliza códigos de estado HTTP apropiados:

- **200 OK**: Operación exitosa (GET, PUT)
- **201 Created**: Recurso creado exitosamente (POST)
- **204 No Content**: Eliminación exitosa (DELETE)
- **400 Bad Request**: Error de validación de datos
- **404 Not Found**: Recurso no encontrado
- **409 Conflict**: Conflicto de duplicación
- **422 Unprocessable Entity**: Error de validación de Pydantic
- **500 Internal Server Error**: Error del servidor

#### 3. Categorías de Errores

**Errores de Validación (400)**:

Se producen cuando los datos de entrada no cumplen con las reglas de negocio:

- Porcentaje de comisión fuera del rango [0, 100]
- Precio de servicio menor o igual a cero
- Fecha de inicio posterior a fecha de fin
- Campos requeridos vacíos o nulos
- Formato de datos incorrecto

```python
@app.post("/api/empleados")
async def crear_empleado(empleado: EmpleadoCreate):
    resultado = salon_manager.crear_empleado(empleado.id, empleado.nombre)
    
    match resultado:
        case Ok(emp):
            return emp
        case Err(ValidationError(message, field)):
            raise HTTPException(
                status_code=400,
                detail={"error": "validation_error", "message": message, "field": field}
            )
```

**Errores de Duplicación (409)**:

Se producen cuando se intenta crear una entidad con un identificador único ya existente:

```python
case Err(DuplicateError(entity, identifier)):
    raise HTTPException(
        status_code=409,
        detail={
            "error": "duplicate_error",
            "message": f"{entity} con identificador '{identifier}' ya existe"
        }
    )
```

**Errores de Referencia No Encontrada (404)**:

Se producen cuando se referencia una entidad que no existe:

```python
case Err(NotFoundError(entity, identifier)):
    raise HTTPException(
        status_code=404,
        detail={
            "error": "not_found",
            "message": f"{entity} con identificador '{identifier}' no encontrado"
        }
    )
```

**Errores de Base de Datos (500)**:

Se producen durante operaciones de base de datos:

```python
from sqlalchemy.exc import SQLAlchemyError

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "database_error",
            "message": "Error al procesar la solicitud en la base de datos"
        }
    )
```

#### 4. Exception Handlers Globales

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "Error interno del servidor"
        }
    )
```

### Frontend Error Handling

#### 1. Interceptor de Axios

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // El servidor respondió con un código de error
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          console.error('Error de validación:', data.message);
          break;
        case 404:
          console.error('Recurso no encontrado:', data.message);
          break;
        case 409:
          console.error('Conflicto:', data.message);
          break;
        case 500:
          console.error('Error del servidor:', data.message);
          break;
      }
    } else if (error.request) {
      // La petición se hizo pero no hubo respuesta
      console.error('No se pudo conectar con el servidor');
    } else {
      // Error al configurar la petición
      console.error('Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);
```

#### 2. Manejo en Stores (Pinia)

```typescript
// src/stores/empleados.ts
async function crearEmpleado(data: EmpleadoFormData) {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await empleadosAPI.crear(data);
    empleados.value.push(response.data);
    return response.data;
  } catch (e: any) {
    if (e.response?.status === 409) {
      error.value = 'Ya existe un empleado con ese ID';
    } else if (e.response?.status === 400) {
      error.value = e.response.data.message || 'Datos inválidos';
    } else {
      error.value = 'Error al crear empleado. Intente nuevamente.';
    }
    throw e;
  } finally {
    loading.value = false;
  }
}
```

#### 3. Componentes de UI para Errores

```vue
<!-- src/components/common/ErrorMessage.vue -->
<template>
  <div class="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
    <div class="flex items-center">
      <div class="flex-shrink-0">
        <svg class="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
      </div>
      <div class="ml-3">
        <p class="text-sm text-red-700">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string;
}>();
</script>
```

#### 4. Validación en Formularios

```vue
<!-- src/components/empleados/EmpleadoForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">ID</label>
      <input
        v-model="formData.id"
        type="text"
        required
        class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        :class="{ 'border-red-500': errors.id }"
      />
      <p v-if="errors.id" class="text-red-500 text-sm mt-1">{{ errors.id }}</p>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
      <input
        v-model="formData.nombre"
        type="text"
        required
        class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
        :class="{ 'border-red-500': errors.nombre }"
      />
      <p v-if="errors.nombre" class="text-red-500 text-sm mt-1">{{ errors.nombre }}</p>
    </div>
    
    <button
      type="submit"
      :disabled="loading"
      class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg disabled:opacity-50"
    >
      {{ loading ? 'Guardando...' : 'Guardar' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

const formData = reactive({
  id: '',
  nombre: '',
});

const errors = reactive({
  id: '',
  nombre: '',
});

const loading = ref(false);

function validateForm() {
  errors.id = '';
  errors.nombre = '';
  
  if (!formData.id.trim()) {
    errors.id = 'El ID es requerido';
    return false;
  }
  
  if (!formData.nombre.trim()) {
    errors.nombre = 'El nombre es requerido';
    return false;
  }
  
  return true;
}

async function handleSubmit() {
  if (!validateForm()) return;
  
  // Enviar datos...
}
</script>
```

### Logging

El sistema debe registrar:

**Backend**:
- Todos los errores de validación (nivel WARNING)
- Todos los errores de base de datos (nivel ERROR)
- Operaciones exitosas críticas (nivel INFO): creación de empleados, registro de servicios
- Cálculos financieros (nivel DEBUG)
- Peticiones HTTP (nivel INFO con middleware)

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Middleware para logging de peticiones
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

**Frontend**:
- Errores de API (console.error)
- Acciones del usuario importantes (console.log en desarrollo)
- Integración con servicio de monitoreo en producción (ej: Sentry)

## Testing Strategy

### Enfoque Dual de Testing

El sistema requiere dos tipos complementarios de pruebas tanto en backend como en frontend:

### Backend Testing

#### 1. Unit Tests (Pruebas Unitarias)

Las pruebas unitarias se enfocan en:

- **Ejemplos específicos**: Casos concretos que demuestran comportamiento correcto
- **Casos de borde**: Listas vacías, valores límite, primer/último elemento
- **Condiciones de error**: Validación de mensajes de error específicos
- **Integración entre componentes**: Interacción entre SalonManager y Repository

**Ejemplos de Unit Tests**:

```python
def test_crear_empleado_con_id_duplicado_retorna_error():
    """Verifica que crear un empleado con ID duplicado falla apropiadamente"""
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    manager.crear_empleado("E001", "Juan")
    resultado = manager.crear_empleado("E001", "Pedro")
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, DuplicateError)

def test_ingresos_con_lista_vacia_retorna_cero():
    """Caso de borde: sin servicios registrados"""
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    assert manager.calcular_ingresos_totales() == Decimal("0")

def test_empleado_sin_servicios_retorna_pago_cero():
    """Caso de borde: empleado sin servicios"""
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    manager.crear_empleado("E001", "Juan")
    desglose = manager.calcular_pago_empleado("E001")
    assert desglose.total == Decimal("0")
```

#### 2. API Integration Tests

Pruebas de los endpoints de FastAPI:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_crear_empleado_endpoint():
    """Prueba el endpoint POST /api/empleados"""
    response = client.post(
        "/api/empleados",
        json={"id": "E001", "nombre": "Juan Pérez"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "E001"
    assert data["nombre"] == "Juan Pérez"

def test_crear_empleado_duplicado_retorna_409():
    """Prueba que crear un empleado duplicado retorna 409"""
    client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
    response = client.post("/api/empleados", json={"id": "E001", "nombre": "Pedro"})
    assert response.status_code == 409
    assert "ya existe" in response.json()["detail"]["message"]

def test_obtener_empleado_no_existente_retorna_404():
    """Prueba que obtener un empleado inexistente retorna 404"""
    response = client.get("/api/empleados/NOEXISTE")
    assert response.status_code == 404

def test_listar_servicios_con_filtros():
    """Prueba el filtrado de servicios por empleado y fechas"""
    # Setup: crear empleado, tipo de servicio y servicios
    client.post("/api/empleados", json={"id": "E001", "nombre": "Juan"})
    client.post("/api/tipos-servicios", json={
        "nombre": "Corte",
        "descripcion": "Corte de cabello",
        "porcentaje_comision": 40.0
    })
    client.post("/api/servicios", json={
        "fecha": "2024-01-15",
        "empleado_id": "E001",
        "tipo_servicio": "Corte",
        "precio": 25.00
    })
    
    # Test: filtrar por empleado
    response = client.get("/api/servicios?empleado_id=E001")
    assert response.status_code == 200
    servicios = response.json()
    assert len(servicios) == 1
    assert servicios[0]["empleado_id"] == "E001"
```

#### 3. Property-Based Tests (Pruebas Basadas en Propiedades)

Las pruebas basadas en propiedades verifican que las propiedades universales se mantienen para cualquier entrada válida generada aleatoriamente.

**Configuración**:
- Biblioteca: **Hypothesis** (Python)
- Iteraciones mínimas: **100 por propiedad**
- Cada test debe referenciar su propiedad de diseño mediante comentario

**Ejemplos de Property-Based Tests**:

```python
from hypothesis import given, strategies as st

@given(
    nombre=st.text(min_size=1, max_size=100),
    id_empleado=st.text(min_size=1, max_size=50)
)
def test_property_1_creacion_empleados_con_atributos_validos(nombre, id_empleado):
    """
    Feature: salon-peluqueria-gestion, Property 1: 
    Para cualquier nombre e identificador únicos proporcionados, 
    crear un empleado debe resultar en un empleado almacenado con exactamente esos atributos.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    resultado = manager.crear_empleado(id_empleado, nombre)
    
    assert isinstance(resultado, Ok)
    empleado = resultado.value
    assert empleado.id == id_empleado
    assert empleado.nombre == nombre
    
    # Verificar que está almacenado
    empleado_recuperado = manager.obtener_empleado(id_empleado)
    assert empleado_recuperado is not None
    assert empleado_recuperado.id == id_empleado
    assert empleado_recuperado.nombre == nombre

@given(
    porcentaje=st.floats(min_value=-1000, max_value=1000).filter(
        lambda x: x < 0 or x > 100
    )
)
def test_property_6_validacion_rango_porcentaje_comision(porcentaje):
    """
    Feature: salon-peluqueria-gestion, Property 6:
    Para cualquier porcentaje fuera del rango [0, 100], 
    intentar crear o actualizar un tipo de servicio debe fallar con un error de validación.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    resultado = manager.crear_tipo_servicio(
        "Servicio Test", 
        "Descripción", 
        porcentaje
    )
    
    assert isinstance(resultado, Err)
    assert isinstance(resultado.error, ValidationError)

@given(
    servicios=st.lists(
        st.tuples(
            st.dates(min_value=date(2020, 1, 1), max_value=date(2025, 12, 31)),
            st.decimals(min_value=Decimal("0.01"), max_value=Decimal("10000"))
        ),
        min_size=0,
        max_size=50
    )
)
def test_property_13_calculo_correcto_ingresos_totales(servicios):
    """
    Feature: salon-peluqueria-gestion, Property 13:
    Para cualquier conjunto de servicios registrados, 
    la suma de ingresos totales debe ser igual a la suma de los precios de todos los servicios.
    """
    manager = SalonManager(SQLAlchemyRepository("sqlite:///:memory:"))
    
    # Setup: crear empleado y tipo de servicio
    manager.crear_empleado("E001", "Test")
    manager.crear_tipo_servicio("Corte", "Desc", 40.0)
    
    # Registrar servicios
    suma_esperada = Decimal("0")
    for fecha, precio in servicios:
        manager.registrar_servicio(fecha, "E001", "Corte", precio)
        suma_esperada += precio
    
    # Verificar
    ingresos = manager.calcular_ingresos_totales()
    assert ingresos == suma_esperada
```

#### 4. Database Tests

Pruebas específicas de la capa de persistencia:

```python
def test_sqlalchemy_repository_transacciones():
    """Verifica que las transacciones se manejan correctamente"""
    repo = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Crear empleado
    empleado = Empleado(id="E001", nombre="Juan")
    repo.guardar_empleado(empleado)
    
    # Verificar que se puede recuperar
    recuperado = repo.obtener_empleado("E001")
    assert recuperado is not None
    assert recuperado.id == "E001"

def test_indices_mejoran_rendimiento():
    """Verifica que los índices están creados correctamente"""
    repo = SQLAlchemyRepository("sqlite:///:memory:")
    
    # Verificar que los índices existen
    with repo.get_session() as session:
        result = session.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='servicios'"
        )
        indices = [row[0] for row in result]
        assert 'idx_servicios_empleado_fecha' in indices
        assert 'idx_servicios_fecha' in indices
```

### Frontend Testing

#### 1. Unit Tests (Vitest)

Pruebas de funciones y composables:

```typescript
// tests/unit/stores/empleados.spec.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useEmpleadosStore } from '@/stores/empleados';
import { empleadosAPI } from '@/services/api';

vi.mock('@/services/api');

describe('useEmpleadosStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('carga empleados correctamente', async () => {
    const mockEmpleados = [
      { id: 'E001', nombre: 'Juan' },
      { id: 'E002', nombre: 'María' }
    ];
    
    vi.mocked(empleadosAPI.listar).mockResolvedValue({ data: mockEmpleados });
    
    const store = useEmpleadosStore();
    await store.cargarEmpleados();
    
    expect(store.empleados).toEqual(mockEmpleados);
    expect(store.loading).toBe(false);
    expect(store.error).toBeNull();
  });

  it('maneja errores al cargar empleados', async () => {
    vi.mocked(empleadosAPI.listar).mockRejectedValue(
      new Error('Network error')
    );
    
    const store = useEmpleadosStore();
    
    await expect(store.cargarEmpleados()).rejects.toThrow();
    expect(store.error).toBeTruthy();
    expect(store.loading).toBe(false);
  });
});
```

#### 2. Component Tests (Vue Test Utils)

Pruebas de componentes Vue:

```typescript
// tests/unit/components/EmpleadosList.spec.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import EmpleadosList from '@/components/empleados/EmpleadosList.vue';
import { useEmpleadosStore } from '@/stores/empleados';

describe('EmpleadosList', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('muestra lista de empleados', async () => {
    const store = useEmpleadosStore();
    store.empleados = [
      { id: 'E001', nombre: 'Juan' },
      { id: 'E002', nombre: 'María' }
    ];
    
    const wrapper = mount(EmpleadosList);
    
    expect(wrapper.text()).toContain('Juan');
    expect(wrapper.text()).toContain('María');
  });

  it('muestra spinner mientras carga', () => {
    const store = useEmpleadosStore();
    store.loading = true;
    
    const wrapper = mount(EmpleadosList);
    
    expect(wrapper.findComponent({ name: 'LoadingSpinner' }).exists()).toBe(true);
  });

  it('muestra mensaje de error cuando falla', () => {
    const store = useEmpleadosStore();
    store.error = 'Error al cargar empleados';
    
    const wrapper = mount(EmpleadosList);
    
    expect(wrapper.text()).toContain('Error al cargar empleados');
  });
});
```

#### 3. E2E Tests (Playwright/Cypress)

Pruebas end-to-end del flujo completo:

```typescript
// tests/e2e/empleados.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Gestión de Empleados', () => {
  test('crear nuevo empleado', async ({ page }) => {
    await page.goto('http://localhost:5173/empleados');
    
    // Click en botón nuevo empleado
    await page.click('text=Nuevo Empleado');
    
    // Llenar formulario
    await page.fill('input[name="id"]', 'E001');
    await page.fill('input[name="nombre"]', 'Juan Pérez');
    
    // Enviar formulario
    await page.click('button[type="submit"]');
    
    // Verificar que aparece en la lista
    await expect(page.locator('text=Juan Pérez')).toBeVisible();
  });

  test('validación de formulario', async ({ page }) => {
    await page.goto('http://localhost:5173/empleados');
    await page.click('text=Nuevo Empleado');
    
    // Intentar enviar sin llenar
    await page.click('button[type="submit"]');
    
    // Verificar mensajes de error
    await expect(page.locator('text=El ID es requerido')).toBeVisible();
    await expect(page.locator('text=El nombre es requerido')).toBeVisible();
  });

  test('responsive design en móvil', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('http://localhost:5173/empleados');
    
    // Verificar que el botón ocupa todo el ancho en móvil
    const button = page.locator('text=Nuevo Empleado');
    const box = await button.boundingBox();
    expect(box?.width).toBeGreaterThan(300);
  });
});
```

### Estrategias de Generación de Datos

Para property-based testing, se deben crear estrategias personalizadas:

```python
# Estrategia para generar empleados válidos
empleados_validos = st.builds(
    Empleado,
    id=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    nombre=st.text(min_size=1, max_size=100)
)

# Estrategia para generar tipos de servicio válidos
tipos_servicio_validos = st.builds(
    TipoServicio,
    nombre=st.text(min_size=1, max_size=50),
    descripcion=st.text(max_size=200),
    porcentaje_comision=st.floats(min_value=0, max_value=100)
)

# Estrategia para generar precios válidos
precios_validos = st.decimals(
    min_value=Decimal("0.01"),
    max_value=Decimal("100000"),
    places=2
)
```

### Cobertura de Testing

**Backend**:
- Unit Tests: Todos los casos de error específicos, casos de borde, ejemplos concretos
- API Tests: Todos los endpoints con casos exitosos y de error
- Property Tests: Todas las 27 propiedades de corrección definidas (mínimo 100 iteraciones)
- Database Tests: Operaciones CRUD, transacciones, índices

**Frontend**:
- Unit Tests: Stores, composables, funciones de utilidad
- Component Tests: Todos los componentes con diferentes estados (loading, error, success)
- E2E Tests: Flujos críticos de usuario (crear empleado, registrar servicio, ver reportes)

**Objetivo de cobertura de código**: 
- Backend: Mínimo 90% de cobertura en lógica de negocio
- Frontend: Mínimo 80% de cobertura en stores y componentes

### Ejecución de Tests

**Backend**:
```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar solo unit tests
pytest tests/unit/

# Ejecutar solo property tests
pytest tests/property/

# Ejecutar API tests
pytest tests/api/

# Ejecutar con cobertura
pytest --cov=app --cov-report=html tests/

# Ejecutar property tests con más iteraciones
pytest tests/property/ --hypothesis-iterations=1000
```

**Frontend**:
```bash
# Ejecutar unit tests
npm run test:unit

# Ejecutar con cobertura
npm run test:unit -- --coverage

# Ejecutar E2E tests
npm run test:e2e

# Ejecutar E2E en modo headless
npm run test:e2e:ci

# Ejecutar tests en watch mode (desarrollo)
npm run test:unit -- --watch
```

### Continuous Integration

Los tests deben ejecutarse automáticamente en CI/CD:

**Backend**:
- En cada commit a ramas de desarrollo
- En cada pull request
- Antes de cada release
- Property tests con 500 iteraciones en CI (más exhaustivo que desarrollo local)
- Tests de API con base de datos en memoria

**Frontend**:
- Unit tests en cada commit
- E2E tests en pull requests y antes de release
- Tests de accesibilidad (axe-core)
- Tests de rendimiento (Lighthouse CI)

**Pipeline Example (GitHub Actions)**:
```yaml
name: CI

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --hypothesis-iterations=500
      
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - run: npm run test:e2e:ci
```

