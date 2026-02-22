# Sistema de Gestión de Salón de Peluquería

Sistema web completo para gestionar empleados, servicios y comisiones de un salón de peluquería. Incluye backend API REST con FastAPI y frontend mobile-first con Vue 3.

## Características

- ✅ Gestión de empleados con identificadores únicos
- ✅ Gestión de tipos de servicios con porcentajes de comisión configurables
- ✅ Registro de servicios realizados con cálculo automático de comisiones
- ✅ Reportes de ingresos totales y beneficios
- ✅ Cálculo de pagos a empleados con desglose detallado
- ✅ Filtrado de servicios por empleado y rango de fechas
- ✅ Interfaz responsive mobile-first
- ✅ Persistencia de datos con SQLite
- ✅ API REST documentada con OpenAPI/Swagger
- ✅ Tests unitarios, de propiedades y E2E

## Tecnologías

### Backend
- **FastAPI** - Framework web moderno para Python
- **SQLAlchemy** - ORM para Python
- **SQLite** - Base de datos relacional
- **Pydantic** - Validación de datos
- **Hypothesis** - Property-based testing
- **pytest** - Framework de testing

### Frontend
- **Vue 3** - Framework progresivo de JavaScript
- **TypeScript** - Tipado estático
- **Vite** - Build tool ultrarrápido
- **Tailwind CSS** - Framework CSS utility-first
- **Pinia** - Gestión de estado
- **Axios** - Cliente HTTP
- **Playwright** - Testing E2E

## Estructura del Proyecto

```
salon-peluqueria/
├── backend/              # API REST con FastAPI
│   ├── app/             # Código de la aplicación
│   ├── tests/           # Tests (unit, property, api)
│   ├── requirements.txt # Dependencias Python
│   └── README.md        # Documentación del backend
├── frontend/            # Aplicación web con Vue 3
│   ├── src/            # Código fuente
│   ├── tests/          # Tests (unit, e2e)
│   ├── package.json    # Dependencias Node.js
│   └── README.md       # Documentación del frontend
└── README.md           # Este archivo
```

## Inicio Rápido

### Requisitos Previos

- Python 3.10 o superior
- Node.js 18 o superior
- npm 9 o superior

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd salon-peluqueria
```

### 2. Configurar y ejecutar el backend

```bash
# Ir al directorio del backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload
```

El backend estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

### 3. Configurar y ejecutar el frontend

```bash
# Abrir nueva terminal
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## Scripts de Desarrollo

Esta sección documenta todos los comandos disponibles para desarrollo, testing y ejecución del proyecto.

### Backend

Todos los comandos del backend deben ejecutarse desde el directorio `backend/` con el entorno virtual activado.

#### Servidor de Desarrollo
```bash
# Iniciar servidor de desarrollo con hot-reload
uvicorn app.main:app --reload

# El servidor estará disponible en http://localhost:8000
# Documentación interactiva en http://localhost:8000/docs
```

#### Testing
```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app --cov-report=html

# Ejecutar solo tests unitarios
pytest tests/unit/

# Ejecutar solo tests de propiedades (property-based)
pytest tests/property/

# Ejecutar solo tests de API
pytest tests/api/

# Ejecutar tests con más iteraciones para property-based testing
pytest tests/property/ --hypothesis-iterations=1000
```

#### Otros Comandos
```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear/actualizar base de datos
alembic upgrade head

# Formatear código
black app/ tests/

# Linting
ruff check app/ tests/
```

### Frontend

Todos los comandos del frontend deben ejecutarse desde el directorio `frontend/`.

#### Servidor de Desarrollo
```bash
# Iniciar servidor de desarrollo con hot-reload
npm run dev

# El servidor estará disponible en http://localhost:5173
```

#### Testing
```bash
# Ejecutar tests unitarios (modo watch)
npm run test:unit

# Ejecutar tests unitarios una vez
npm run test:run

# Ejecutar tests con interfaz gráfica
npm run test:ui

# Ejecutar tests E2E
npm run test:e2e

# Ejecutar tests E2E con interfaz gráfica
npm run test:e2e:ui

# Ejecutar tests E2E en modo headed (ver navegador)
npm run test:e2e:headed

# Ejecutar tests E2E en modo debug
npm run test:e2e:debug

# Ver reporte de tests E2E
npm run test:e2e:report
```

#### Build y Preview
```bash
# Compilar para producción
npm run build

# Previsualizar build de producción
npm run preview
```

#### Calidad de Código
```bash
# Instalar dependencias
npm install

# Linting
npm run lint

# Linting con auto-fix
npm run lint:fix

# Formatear código
npm run format
```

### Comandos Rápidos

Para desarrollo diario, estos son los comandos más utilizados:

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # En Windows: venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Tests Backend
cd backend
source venv/bin/activate
pytest

# Terminal 4: Tests Frontend
cd frontend
npm run test:unit
```

## Uso

### Flujo Básico

1. **Crear empleados**: Ir a "Empleados" y agregar empleados con ID y nombre
2. **Crear tipos de servicios**: Ir a "Tipos de Servicios" y definir servicios con sus porcentajes de comisión
3. **Registrar servicios**: Ir a "Servicios" y registrar servicios realizados
4. **Ver reportes**: Ir a "Reportes" para ver ingresos, beneficios y pagos a empleados

### Ejemplos de API

#### Crear un empleado
```bash
curl -X POST http://localhost:8000/api/empleados \
  -H "Content-Type: application/json" \
  -d '{"id": "E001", "nombre": "Juan Pérez"}'
```

#### Crear un tipo de servicio
```bash
curl -X POST http://localhost:8000/api/tipos-servicios \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Corte Básico",
    "descripcion": "Corte de cabello estándar",
    "porcentaje_comision": 40.0
  }'
```

#### Registrar un servicio
```bash
curl -X POST http://localhost:8000/api/servicios \
  -H "Content-Type: application/json" \
  -d '{
    "fecha": "2024-01-15",
    "empleado_id": "E001",
    "tipo_servicio": "Corte Básico",
    "precio": 25.00
  }'
```

#### Consultar pago de empleado
```bash
curl http://localhost:8000/api/empleados/E001/pago
```

## Testing

### Backend

```bash
cd backend

# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=app --cov-report=html

# Solo tests unitarios
pytest tests/unit/

# Solo tests de propiedades
pytest tests/property/

# Solo tests de API
pytest tests/api/
```

### Frontend

```bash
cd frontend

# Tests unitarios
npm run test

# Tests E2E (requiere backend ejecutándose)
npm run test:e2e

# Tests con cobertura
npm run test:coverage
```

## Documentación

- **Backend**: Ver [backend/README.md](backend/README.md) para documentación detallada de la API
- **Frontend**: Ver [frontend/README.md](frontend/README.md) para documentación del frontend
- **API Interactiva**: `http://localhost:8000/docs` (Swagger UI)
- **Tests E2E**: Ver [frontend/tests/e2e/README.md](frontend/tests/e2e/README.md)

## API Endpoints

### Empleados
- `GET /api/empleados` - Listar empleados
- `POST /api/empleados` - Crear empleado
- `GET /api/empleados/{id}` - Obtener empleado
- `PUT /api/empleados/{id}` - Actualizar empleado
- `DELETE /api/empleados/{id}` - Eliminar empleado

### Tipos de Servicios
- `GET /api/tipos-servicios` - Listar tipos de servicios
- `POST /api/tipos-servicios` - Crear tipo de servicio
- `GET /api/tipos-servicios/{nombre}` - Obtener tipo de servicio
- `PUT /api/tipos-servicios/{nombre}` - Actualizar tipo de servicio
- `DELETE /api/tipos-servicios/{nombre}` - Eliminar tipo de servicio

### Servicios
- `GET /api/servicios` - Listar servicios (con filtros)
- `POST /api/servicios` - Registrar servicio
- `GET /api/servicios/{id}` - Obtener servicio
- `DELETE /api/servicios/{id}` - Eliminar servicio

### Reportes
- `GET /api/reportes/ingresos` - Calcular ingresos totales
- `GET /api/reportes/beneficios` - Calcular beneficios
- `GET /api/empleados/{id}/pago` - Calcular pago de empleado

Ver documentación completa en `http://localhost:8000/docs`

## Arquitectura

### Backend (FastAPI)

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

### Frontend (Vue 3)

```
Usuario
    ↓
Vue Component
    ↓
Pinia Store (estado global)
    ↓
API Service (axios)
    ↓
HTTP Request → Backend API
```

## Variables de Entorno

El proyecto utiliza archivos `.env` para configuración. Cada módulo incluye un archivo `.env.example` con valores por defecto que puedes copiar.

### Backend (.env)

**Ubicación**: `backend/.env`

**Configuración inicial**:
```bash
cd backend
cp .env.example .env
```

**Variables disponibles**:

```env
# Configuración de Base de Datos
DATABASE_URL=sqlite:///./salon.db

# Configuración de CORS (orígenes permitidos separados por comas)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Configuración de la Aplicación
APP_NAME="Sistema de Gestión de Salón de Peluquería"
APP_VERSION=1.0.0
DEBUG=True

# Configuración de Logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a la base de datos SQLite | `sqlite:///./salon.db` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS (separados por comas) | `http://localhost:5173,http://localhost:3000` |
| `APP_NAME` | Nombre de la aplicación | `Sistema de Gestión de Salón de Peluquería` |
| `APP_VERSION` | Versión de la aplicación | `1.0.0` |
| `DEBUG` | Modo debug (True/False) | `True` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |

### Frontend (.env) - Opcional

**Ubicación**: `frontend/.env`

**Configuración inicial**:
```bash
cd frontend
cp .env.example .env
```

**Variables disponibles**:

```env
# Configuración de la API Backend
VITE_API_URL=http://localhost:8000/api
```

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `VITE_API_URL` | URL base de la API del backend | `http://localhost:8000/api` |

**Nota**: Si no se configura `VITE_API_URL`, el frontend usará `http://localhost:8000/api` por defecto (configurado en `frontend/src/services/api.ts`).

## Desarrollo

### Agregar nueva funcionalidad

1. **Backend**:
   - Agregar modelo de dominio en `backend/app/models.py`
   - Agregar modelo ORM en `backend/app/orm_models.py`
   - Agregar esquemas Pydantic en `backend/app/schemas.py`
   - Agregar lógica de negocio en `backend/app/manager.py`
   - Agregar endpoints en `backend/app/main.py`
   - Escribir tests en `backend/tests/`

2. **Frontend**:
   - Agregar tipos en `frontend/src/types/models.ts`
   - Agregar API calls en `frontend/src/services/api.ts`
   - Crear store en `frontend/src/stores/`
   - Crear componentes en `frontend/src/components/`
   - Crear vista en `frontend/src/views/`
   - Agregar ruta en `frontend/src/router/index.ts`
   - Escribir tests en `frontend/tests/`

### Formato de código

**Backend:**
```bash
cd backend
black app/ tests/
ruff check app/ tests/
```

**Frontend:**
```bash
cd frontend
npm run format
npm run lint
```

## Solución de Problemas

### Backend no inicia

1. Verifica que el entorno virtual esté activado
2. Verifica que las dependencias estén instaladas: `pip install -r requirements.txt`
3. Verifica el archivo `.env`

### Frontend no conecta con backend

1. Verifica que el backend esté ejecutándose en `http://localhost:8000`
2. Verifica CORS en `backend/.env`: `CORS_ORIGINS=http://localhost:5173`
3. Verifica la URL en `frontend/src/services/api.ts`

### Tests E2E fallan

1. Asegúrate de que backend y frontend estén ejecutándose
2. Limpia la base de datos de prueba
3. Verifica las URLs en `frontend/playwright.config.ts`

### Error "Database is locked"

SQLite tiene limitaciones de concurrencia. Para producción, considera usar PostgreSQL o MySQL.

## Características Técnicas

### Backend

- ✅ Arquitectura en capas (API, Business Logic, Data Access)
- ✅ Patrón Repository para abstracción de datos
- ✅ Patrón Result para manejo de errores
- ✅ Validación con Pydantic
- ✅ Documentación automática con OpenAPI
- ✅ CORS configurado
- ✅ Logging estructurado
- ✅ Tests unitarios, de propiedades y de integración
- ✅ Cobertura de código > 80%

### Frontend

- ✅ Diseño mobile-first responsive
- ✅ Composition API de Vue 3
- ✅ TypeScript estricto
- ✅ Gestión de estado con Pinia
- ✅ Routing con Vue Router
- ✅ Componentes reutilizables
- ✅ Validación de formularios
- ✅ Manejo de errores centralizado
- ✅ Tests unitarios y E2E

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

### Convenciones

- Seguir las guías de estilo de Python (PEP 8) y TypeScript
- Escribir tests para nueva funcionalidad
- Actualizar documentación según sea necesario
- Usar commits descriptivos

## Licencia

Este proyecto es parte del sistema de gestión de salón de peluquería.

## Contacto

Para preguntas o soporte, consulta la documentación en:
- Backend: [backend/README.md](backend/README.md)
- Frontend: [frontend/README.md](frontend/README.md)
- API Docs: http://localhost:8000/docs
