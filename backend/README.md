# Backend - Sistema de Gestión de Salón de Peluquería

API REST desarrollada con FastAPI para gestionar empleados, tipos de servicios, registros de servicios y cálculos de comisiones.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)

## Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- SQLite 3 (incluido en Python)

## Instalación

### 1. Crear entorno virtual

```bash
# En el directorio backend/
python -m venv venv
```

### 2. Activar entorno virtual

**En Linux/macOS:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración

### Variables de Entorno

Copiar el archivo `.env.example` a `.env` y ajustar las variables según sea necesario:

```bash
cp .env.example .env
```

Variables disponibles:

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a la base de datos SQLite | `sqlite:///./salon.db` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS (separados por comas) | `http://localhost:5173` |
| `APP_NAME` | Nombre de la aplicación | `Sistema de Gestión de Salón` |
| `APP_VERSION` | Versión de la aplicación | `1.0.0` |
| `DEBUG` | Modo debug (True/False) | `True` |
| `LOG_LEVEL` | Nivel de logging (DEBUG, INFO, WARNING, ERROR) | `INFO` |

### Base de Datos

La aplicación utiliza SQLite como base de datos. Al iniciar por primera vez, se creará automáticamente el archivo `salon.db` con todas las tablas necesarias.

## Ejecución

### Servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

**Documentación interactiva:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Servidor de producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing

El proyecto incluye tres tipos de tests: unitarios, de propiedades y de integración de API.

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar tests con cobertura

```bash
pytest --cov=app --cov-report=html
```

El reporte de cobertura se generará en `htmlcov/index.html`

### Ejecutar tests por categoría

#### Tests unitarios
```bash
pytest tests/unit/
```

Prueban funciones individuales y casos de borde específicos.

#### Tests de propiedades (Property-Based Testing)
```bash
pytest tests/property/
```

Verifican propiedades universales con datos generados aleatoriamente usando Hypothesis.

**Ejecutar con más iteraciones:**
```bash
pytest tests/property/ --hypothesis-iterations=1000
```

#### Tests de API
```bash
pytest tests/api/
```

Prueban los endpoints de FastAPI de forma integrada.

### Tests específicos

```bash
# Ejecutar un archivo específico
pytest tests/unit/test_models.py

# Ejecutar un test específico
pytest tests/unit/test_models.py::test_crear_empleado

# Ejecutar tests con verbose
pytest -v

# Ejecutar tests y mostrar print statements
pytest -s
```

### Cobertura de código

El proyecto mantiene una cobertura de código superior al 80%. Para ver el reporte:

```bash
pytest --cov=app --cov-report=term-missing
```

## Estructura del Proyecto

```
backend/
├── app/                    # Código de la aplicación
│   ├── __init__.py
│   ├── main.py            # Aplicación FastAPI principal y endpoints
│   ├── models.py          # Modelos de dominio (Empleado, TipoServicio, ServicioRegistrado)
│   ├── orm_models.py      # Modelos SQLAlchemy ORM (EmpleadoORM, TipoServicioORM, ServicioORM)
│   ├── schemas.py         # Esquemas Pydantic para validación de request/response
│   ├── repository.py      # Capa de acceso a datos (DataRepository, SQLAlchemyRepository)
│   ├── manager.py         # Lógica de negocio (SalonManager)
│   ├── validators.py      # Validaciones de negocio
│   └── errors.py          # Tipos de error personalizados
├── tests/                 # Tests
│   ├── unit/             # Tests unitarios
│   │   ├── test_models.py
│   │   ├── test_validators.py
│   │   ├── test_repository.py
│   │   ├── test_manager_servicios.py
│   │   └── test_schemas.py
│   ├── property/         # Tests basados en propiedades (Hypothesis)
│   │   ├── test_property_validators.py
│   │   ├── test_property_persistence.py
│   │   ├── test_property_manager_servicios.py
│   │   └── test_property_formato_monetario.py
│   ├── api/              # Tests de integración de API
│   │   ├── test_empleados_endpoints.py
│   │   ├── test_tipos_servicios_endpoints.py
│   │   ├── test_servicios_endpoints.py
│   │   └── test_reportes_endpoints.py
│   └── integration/      # Tests de integración backend-frontend
│       └── test_backend_frontend_integration.py
├── alembic/              # Migraciones de base de datos
│   ├── versions/         # Scripts de migración
│   └── env.py           # Configuración de Alembic
├── requirements.txt      # Dependencias Python
├── .env.example         # Ejemplo de variables de entorno
├── .env                 # Variables de entorno (no versionado)
├── .gitignore          # Archivos ignorados por Git
├── alembic.ini         # Configuración de Alembic
├── pytest.ini          # Configuración de pytest
└── README.md           # Este archivo
```

### Arquitectura del Backend

El backend sigue una arquitectura en capas:

1. **Capa de API (main.py)**: Endpoints FastAPI que reciben requests HTTP
2. **Capa de Validación (schemas.py)**: Validación de datos con Pydantic
3. **Capa de Negocio (manager.py)**: Lógica de negocio y reglas del dominio
4. **Capa de Acceso a Datos (repository.py)**: Abstracción de persistencia
5. **Capa de Persistencia (orm_models.py)**: Modelos SQLAlchemy y base de datos

### Flujo de una Request

```
HTTP Request
    ↓
FastAPI Endpoint (main.py)
    ↓
Validación Pydantic (schemas.py)
    ↓
SalonManager (manager.py)
    ↓
Validaciones de Negocio (validators.py)
    ↓
DataRepository (repository.py)
    ↓
SQLAlchemy ORM (orm_models.py)
    ↓
SQLite Database
```

## API Endpoints

La API REST expone los siguientes endpoints. Todos los endpoints están bajo el prefijo `/api`.

### Empleados

#### Listar todos los empleados
```http
GET /api/empleados
```

**Respuesta exitosa (200):**
```json
[
  {
    "id": "E001",
    "nombre": "Juan Pérez"
  },
  {
    "id": "E002",
    "nombre": "María García"
  }
]
```

#### Obtener empleado por ID
```http
GET /api/empleados/{id}
```

**Parámetros:**
- `id` (path): Identificador único del empleado

**Respuesta exitosa (200):**
```json
{
  "id": "E001",
  "nombre": "Juan Pérez"
}
```

**Errores:**
- `404`: Empleado no encontrado

#### Crear nuevo empleado
```http
POST /api/empleados
```

**Body:**
```json
{
  "id": "E001",
  "nombre": "Juan Pérez"
}
```

**Respuesta exitosa (201):**
```json
{
  "id": "E001",
  "nombre": "Juan Pérez"
}
```

**Errores:**
- `400`: Datos inválidos
- `409`: ID de empleado ya existe

#### Actualizar empleado
```http
PUT /api/empleados/{id}
```

**Parámetros:**
- `id` (path): Identificador único del empleado

**Body:**
```json
{
  "nombre": "Juan Carlos Pérez"
}
```

**Respuesta exitosa (200):**
```json
{
  "id": "E001",
  "nombre": "Juan Carlos Pérez"
}
```

**Errores:**
- `404`: Empleado no encontrado
- `400`: Datos inválidos

#### Eliminar empleado
```http
DELETE /api/empleados/{id}
```

**Parámetros:**
- `id` (path): Identificador único del empleado

**Respuesta exitosa (204):** Sin contenido

**Errores:**
- `404`: Empleado no encontrado

---

### Tipos de Servicios

#### Listar todos los tipos de servicios
```http
GET /api/tipos-servicios
```

**Respuesta exitosa (200):**
```json
[
  {
    "nombre": "Corte Básico",
    "descripcion": "Corte de cabello estándar",
    "porcentaje_comision": 40.0
  },
  {
    "nombre": "Tinte Completo",
    "descripcion": "Tinte de cabello completo",
    "porcentaje_comision": 35.0
  }
]
```

#### Obtener tipo de servicio por nombre
```http
GET /api/tipos-servicios/{nombre}
```

**Parámetros:**
- `nombre` (path): Nombre del tipo de servicio

**Respuesta exitosa (200):**
```json
{
  "nombre": "Corte Básico",
  "descripcion": "Corte de cabello estándar",
  "porcentaje_comision": 40.0
}
```

**Errores:**
- `404`: Tipo de servicio no encontrado

#### Crear nuevo tipo de servicio
```http
POST /api/tipos-servicios
```

**Body:**
```json
{
  "nombre": "Corte Básico",
  "descripcion": "Corte de cabello estándar",
  "porcentaje_comision": 40.0
}
```

**Validaciones:**
- `porcentaje_comision` debe estar entre 0 y 100

**Respuesta exitosa (201):**
```json
{
  "nombre": "Corte Básico",
  "descripcion": "Corte de cabello estándar",
  "porcentaje_comision": 40.0
}
```

**Errores:**
- `400`: Datos inválidos (porcentaje fuera de rango)
- `409`: Nombre de tipo de servicio ya existe

#### Actualizar tipo de servicio
```http
PUT /api/tipos-servicios/{nombre}
```

**Parámetros:**
- `nombre` (path): Nombre del tipo de servicio

**Body:**
```json
{
  "descripcion": "Corte de cabello premium",
  "porcentaje_comision": 45.0
}
```

**Respuesta exitosa (200):**
```json
{
  "nombre": "Corte Básico",
  "descripcion": "Corte de cabello premium",
  "porcentaje_comision": 45.0
}
```

**Errores:**
- `404`: Tipo de servicio no encontrado
- `400`: Datos inválidos

#### Eliminar tipo de servicio
```http
DELETE /api/tipos-servicios/{nombre}
```

**Parámetros:**
- `nombre` (path): Nombre del tipo de servicio

**Respuesta exitosa (204):** Sin contenido

**Errores:**
- `404`: Tipo de servicio no encontrado

---

### Servicios

#### Listar servicios con filtros opcionales
```http
GET /api/servicios?empleado_id={id}&fecha_inicio={fecha}&fecha_fin={fecha}
```

**Parámetros de consulta (opcionales):**
- `empleado_id`: Filtrar por ID de empleado
- `fecha_inicio`: Filtrar desde esta fecha (formato: YYYY-MM-DD)
- `fecha_fin`: Filtrar hasta esta fecha (formato: YYYY-MM-DD)

**Ejemplo:**
```http
GET /api/servicios?empleado_id=E001&fecha_inicio=2024-01-01&fecha_fin=2024-01-31
```

**Respuesta exitosa (200):**
```json
[
  {
    "id": "S001",
    "fecha": "2024-01-15",
    "empleado_id": "E001",
    "tipo_servicio": "Corte Básico",
    "precio": 25.00,
    "comision_calculada": 10.00
  }
]
```

**Nota:** Los servicios se retornan ordenados por fecha descendente (más recientes primero).

#### Obtener servicio por ID
```http
GET /api/servicios/{id}
```

**Parámetros:**
- `id` (path): Identificador único del servicio

**Respuesta exitosa (200):**
```json
{
  "id": "S001",
  "fecha": "2024-01-15",
  "empleado_id": "E001",
  "tipo_servicio": "Corte Básico",
  "precio": 25.00,
  "comision_calculada": 10.00
}
```

**Errores:**
- `404`: Servicio no encontrado

#### Registrar nuevo servicio
```http
POST /api/servicios
```

**Body:**
```json
{
  "fecha": "2024-01-15",
  "empleado_id": "E001",
  "tipo_servicio": "Corte Básico",
  "precio": 25.00
}
```

**Validaciones:**
- `precio` debe ser mayor que 0
- `empleado_id` debe existir
- `tipo_servicio` debe existir

**Respuesta exitosa (201):**
```json
{
  "id": "S001",
  "fecha": "2024-01-15",
  "empleado_id": "E001",
  "tipo_servicio": "Corte Básico",
  "precio": 25.00,
  "comision_calculada": 10.00
}
```

**Nota:** La comisión se calcula automáticamente basándose en el porcentaje del tipo de servicio.

**Errores:**
- `400`: Datos inválidos (precio <= 0)
- `404`: Empleado o tipo de servicio no encontrado

#### Eliminar servicio
```http
DELETE /api/servicios/{id}
```

**Parámetros:**
- `id` (path): Identificador único del servicio

**Respuesta exitosa (204):** Sin contenido

**Errores:**
- `404`: Servicio no encontrado

---

### Reportes

#### Calcular ingresos totales
```http
GET /api/reportes/ingresos?fecha_inicio={fecha}&fecha_fin={fecha}
```

**Parámetros de consulta (opcionales):**
- `fecha_inicio`: Calcular desde esta fecha (formato: YYYY-MM-DD)
- `fecha_fin`: Calcular hasta esta fecha (formato: YYYY-MM-DD)

**Ejemplo:**
```http
GET /api/reportes/ingresos?fecha_inicio=2024-01-01&fecha_fin=2024-01-31
```

**Respuesta exitosa (200):**
```json
{
  "total": 1250.00,
  "fecha_inicio": "2024-01-01",
  "fecha_fin": "2024-01-31"
}
```

#### Calcular beneficios
```http
GET /api/reportes/beneficios?fecha_inicio={fecha}&fecha_fin={fecha}
```

**Parámetros de consulta (opcionales):**
- `fecha_inicio`: Calcular desde esta fecha (formato: YYYY-MM-DD)
- `fecha_fin`: Calcular hasta esta fecha (formato: YYYY-MM-DD)

**Respuesta exitosa (200):**
```json
{
  "ingresos": 1250.00,
  "comisiones": 500.00,
  "beneficios": 750.00,
  "fecha_inicio": "2024-01-01",
  "fecha_fin": "2024-01-31"
}
```

**Nota:** Beneficios = Ingresos - Comisiones

#### Calcular pago de empleado
```http
GET /api/empleados/{id}/pago?fecha_inicio={fecha}&fecha_fin={fecha}
```

**Parámetros:**
- `id` (path): Identificador único del empleado

**Parámetros de consulta (opcionales):**
- `fecha_inicio`: Calcular desde esta fecha (formato: YYYY-MM-DD)
- `fecha_fin`: Calcular hasta esta fecha (formato: YYYY-MM-DD)

**Ejemplo:**
```http
GET /api/empleados/E001/pago?fecha_inicio=2024-01-01&fecha_fin=2024-01-31
```

**Respuesta exitosa (200):**
```json
{
  "empleado_id": "E001",
  "empleado_nombre": "Juan Pérez",
  "servicios": [
    {
      "fecha": "2024-01-15",
      "tipo_servicio": "Corte Básico",
      "precio": 25.00,
      "comision": 10.00
    },
    {
      "fecha": "2024-01-20",
      "tipo_servicio": "Tinte Completo",
      "precio": 80.00,
      "comision": 28.00
    }
  ],
  "total": 38.00
}
```

**Errores:**
- `404`: Empleado no encontrado

---

### Endpoints Adicionales

#### Root
```http
GET /
```

Retorna información básica de la API.

#### Health Check
```http
GET /health
```

Verifica el estado de la API y la conexión a la base de datos.

## Migraciones de Base de Datos

El proyecto usa Alembic para gestionar migraciones de base de datos.

### Crear una nueva migración

```bash
alembic revision --autogenerate -m "descripción de la migración"
```

### Aplicar migraciones

```bash
alembic upgrade head
```

### Revertir última migración

```bash
alembic downgrade -1
```

### Ver historial de migraciones

```bash
alembic history
```

### Ver estado actual

```bash
alembic current
```

## Desarrollo

### Agregar nuevas dependencias

```bash
pip install nombre-paquete
pip freeze > requirements.txt
```

### Formato de código

Se recomienda usar `black` y `ruff` para mantener el código consistente:

```bash
pip install black ruff
black app/ tests/
ruff check app/ tests/
```

### Estructura de un nuevo endpoint

Para agregar un nuevo endpoint, sigue este patrón:

```python
# En app/main.py

@app.post("/api/nueva-entidad", response_model=NuevaEntidadResponse, status_code=201)
async def crear_nueva_entidad(entidad: NuevaEntidadCreate):
    """
    Crear una nueva entidad.
    
    - **campo1**: Descripción del campo
    - **campo2**: Descripción del campo
    """
    resultado = salon_manager.crear_nueva_entidad(entidad.campo1, entidad.campo2)
    
    match resultado:
        case Ok(nueva_entidad):
            return nueva_entidad
        case Err(ValidationError(message, field)):
            raise HTTPException(
                status_code=400,
                detail={"error": "validation_error", "message": message, "field": field}
            )
        case Err(DuplicateError(entity, identifier)):
            raise HTTPException(
                status_code=409,
                detail={"error": "duplicate_error", "message": f"{entity} ya existe"}
            )
```

### Manejo de Errores

El sistema utiliza el patrón Result para operaciones que pueden fallar:

```python
from app.models import Result, Ok, Err
from app.errors import ValidationError, NotFoundError, DuplicateError

# Operación exitosa
resultado = Ok(empleado)

# Operación fallida
resultado = Err(ValidationError("El precio debe ser mayor que cero", "precio"))
```

**Códigos de estado HTTP:**
- `200 OK`: Operación exitosa (GET, PUT)
- `201 Created`: Recurso creado (POST)
- `204 No Content`: Eliminación exitosa (DELETE)
- `400 Bad Request`: Error de validación
- `404 Not Found`: Recurso no encontrado
- `409 Conflict`: Conflicto de duplicación
- `500 Internal Server Error`: Error del servidor

## Tecnologías

- **FastAPI**: Framework web moderno y rápido para construir APIs
- **SQLAlchemy**: ORM (Object-Relational Mapping) para Python
- **Pydantic**: Validación de datos y serialización
- **Alembic**: Herramienta de migraciones de base de datos
- **Hypothesis**: Framework de property-based testing
- **pytest**: Framework de testing para Python
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **SQLite**: Base de datos relacional ligera

## Ejemplos de Uso

### Ejemplo 1: Crear empleado y registrar servicio

```bash
# 1. Crear empleado
curl -X POST http://localhost:8000/api/empleados \
  -H "Content-Type: application/json" \
  -d '{"id": "E001", "nombre": "Juan Pérez"}'

# 2. Crear tipo de servicio
curl -X POST http://localhost:8000/api/tipos-servicios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Corte Básico", "descripcion": "Corte de cabello", "porcentaje_comision": 40.0}'

# 3. Registrar servicio
curl -X POST http://localhost:8000/api/servicios \
  -H "Content-Type: application/json" \
  -d '{"fecha": "2024-01-15", "empleado_id": "E001", "tipo_servicio": "Corte Básico", "precio": 25.00}'

# 4. Consultar pago del empleado
curl http://localhost:8000/api/empleados/E001/pago
```

### Ejemplo 2: Consultar ingresos por período

```bash
# Ingresos de enero 2024
curl "http://localhost:8000/api/reportes/ingresos?fecha_inicio=2024-01-01&fecha_fin=2024-01-31"

# Beneficios de enero 2024
curl "http://localhost:8000/api/reportes/beneficios?fecha_inicio=2024-01-01&fecha_fin=2024-01-31"
```

### Ejemplo 3: Filtrar servicios

```bash
# Servicios de un empleado específico
curl "http://localhost:8000/api/servicios?empleado_id=E001"

# Servicios en un rango de fechas
curl "http://localhost:8000/api/servicios?fecha_inicio=2024-01-01&fecha_fin=2024-01-31"

# Servicios de un empleado en un período
curl "http://localhost:8000/api/servicios?empleado_id=E001&fecha_inicio=2024-01-01&fecha_fin=2024-01-31"
```

## Solución de Problemas

### Error: "ModuleNotFoundError"

Asegúrate de que el entorno virtual esté activado y las dependencias instaladas:

```bash
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Error: "Database is locked"

SQLite puede tener problemas con concurrencia. Para producción, considera usar PostgreSQL o MySQL.

### Error: "CORS policy"

Verifica que `CORS_ORIGINS` en `.env` incluya el origen del frontend:

```
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Tests fallan

Asegúrate de ejecutar los tests desde el directorio `backend/`:

```bash
cd backend
pytest
```

## Licencia

Este proyecto es parte del sistema de gestión de salón de peluquería.
