# Frontend - Sistema de Gestión de Salón de Peluquería

Aplicación web mobile-first desarrollada con Vue 3, TypeScript, Vite y Tailwind CSS para gestionar empleados, servicios y reportes de un salón de peluquería.

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Scripts Disponibles](#scripts-disponibles)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Componentes Principales](#componentes-principales)
- [Stores (Pinia)](#stores-pinia)
- [Rutas](#rutas)
- [Diseño Mobile-First](#diseño-mobile-first)
- [Testing](#testing)
- [Desarrollo](#desarrollo)
- [Tecnologías](#tecnologías)

## Requisitos

- Node.js 18 o superior
- npm 9 o superior
- Backend ejecutándose en `http://localhost:8000`

## Instalación

```bash
# En el directorio frontend/
npm install
```

## Configuración

### Variables de Entorno

El proyecto incluye un archivo `.env.example` con la configuración por defecto.

**Configuración inicial** (opcional):
```bash
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

**Nota**: Si no creas el archivo `.env`, la aplicación usará `http://localhost:8000/api` por defecto.

### API Backend

La URL del backend está configurada en `src/services/api.ts` para usar la variable de entorno:

```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
});
```

Para cambiar la URL del backend en producción, configura la variable de entorno `VITE_API_URL`.

## Scripts Disponibles

### Desarrollo

```bash
npm run dev
```

Inicia el servidor de desarrollo en `http://localhost:5173` con hot-reload.

### Build

```bash
npm run build
```

Compila TypeScript y construye la aplicación optimizada para producción en `dist/`.

**Proceso:**
1. Verifica tipos con TypeScript
2. Construye assets con Vite
3. Optimiza y minifica código
4. Genera archivos estáticos en `dist/`

### Preview

```bash
npm run preview
```

Previsualiza la build de producción localmente en `http://localhost:4173`.

### Linting y Formato

```bash
npm run lint          # Ejecuta ESLint
npm run lint:fix      # Ejecuta ESLint y corrige errores automáticamente
npm run format        # Formatea el código con Prettier
```

### Testing

#### Tests Unitarios (Vitest)

```bash
npm run test          # Ejecuta tests en modo watch
npm run test:ui       # Ejecuta tests con interfaz gráfica
npm run test:run      # Ejecuta tests una vez (CI)
npm run test:coverage # Ejecuta tests con reporte de cobertura
```

#### Tests E2E (Playwright)

```bash
npm run test:e2e           # Ejecuta tests E2E en modo headless
npm run test:e2e:ui        # Ejecuta tests E2E con interfaz gráfica
npm run test:e2e:headed    # Ejecuta tests E2E mostrando el navegador
npm run test:e2e:debug     # Ejecuta tests E2E en modo debug
npm run test:e2e:report    # Muestra reporte HTML de tests E2E
```

**Nota importante:** Los tests E2E requieren que el backend esté ejecutándose en `http://localhost:8000`.

**Preparación para tests E2E:**
```bash
# Terminal 1: Iniciar backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Iniciar frontend
cd frontend
npm run dev

# Terminal 3: Ejecutar tests E2E
cd frontend
npm run test:e2e
```

Ver [tests/e2e/README.md](tests/e2e/README.md) para más información sobre pruebas E2E.

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/           # Componentes reutilizables
│   │   ├── common/          # Componentes comunes
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppNavigation.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   ├── ErrorMessage.vue
│   │   │   └── SuccessMessage.vue
│   │   ├── empleados/       # Componentes de empleados
│   │   │   ├── EmpleadosList.vue
│   │   │   ├── EmpleadoForm.vue
│   │   │   └── EmpleadoCard.vue
│   │   ├── servicios/       # Componentes de servicios
│   │   │   ├── ServiciosList.vue
│   │   │   ├── ServicioForm.vue
│   │   │   ├── ServicioCard.vue
│   │   │   └── ServicioFilters.vue
│   │   ├── tipos-servicios/ # Componentes de tipos de servicios
│   │   │   ├── TiposServiciosList.vue
│   │   │   ├── TipoServicioForm.vue
│   │   │   └── TipoServicioCard.vue
│   │   └── reportes/        # Componentes de reportes
│   │       ├── IngresosReport.vue
│   │       ├── BeneficiosReport.vue
│   │       └── PagoEmpleadoReport.vue
│   ├── views/               # Vistas de las rutas
│   │   ├── HomeView.vue
│   │   ├── EmpleadosView.vue
│   │   ├── ServiciosView.vue
│   │   ├── TiposServiciosView.vue
│   │   └── ReportesView.vue
│   ├── stores/              # Stores de Pinia (gestión de estado)
│   │   ├── empleados.ts
│   │   ├── servicios.ts
│   │   ├── tiposServicios.ts
│   │   └── reportes.ts
│   ├── services/            # Servicios API
│   │   └── api.ts          # Cliente Axios y endpoints
│   ├── types/               # Definiciones de tipos TypeScript
│   │   └── models.ts       # Interfaces de datos
│   ├── router/              # Configuración de Vue Router
│   │   └── index.ts
│   ├── assets/              # Assets estáticos
│   ├── App.vue              # Componente raíz
│   └── main.ts              # Punto de entrada
├── tests/
│   ├── unit/                # Tests unitarios (Vitest)
│   └── e2e/                 # Tests E2E (Playwright)
├── public/                  # Archivos públicos estáticos
├── dist/                    # Build de producción (generado)
├── .eslintrc.cjs           # Configuración de ESLint
├── .prettierrc.json        # Configuración de Prettier
├── tailwind.config.js      # Configuración de Tailwind CSS
├── vite.config.ts          # Configuración de Vite
├── vitest.config.ts        # Configuración de Vitest
├── playwright.config.ts    # Configuración de Playwright
├── tsconfig.json           # Configuración de TypeScript
├── package.json            # Dependencias y scripts
└── README.md               # Este archivo
```

## Componentes Principales

### Componentes Comunes

#### AppHeader.vue
Encabezado de la aplicación con título y navegación.

#### AppNavigation.vue
Menú de navegación responsive con hamburger menu en móvil.

#### LoadingSpinner.vue
Spinner de carga animado.

#### ErrorMessage.vue
Componente para mostrar mensajes de error con estilos consistentes.

#### SuccessMessage.vue
Componente para mostrar mensajes de éxito.

### Componentes de Empleados

#### EmpleadosList.vue
Lista de empleados en grid responsive con opciones de crear, editar y eliminar.

#### EmpleadoForm.vue
Formulario para crear/editar empleados con validación.

#### EmpleadoCard.vue
Tarjeta individual de empleado con acciones.

### Componentes de Servicios

#### ServiciosList.vue
Lista de servicios con filtros y ordenamiento.

#### ServicioForm.vue
Formulario para registrar servicios con selects de empleado y tipo de servicio.

#### ServicioCard.vue
Tarjeta de servicio mostrando fecha, empleado, tipo, precio y comisión.

#### ServicioFilters.vue
Filtros por empleado y rango de fechas.

### Componentes de Tipos de Servicios

#### TiposServiciosList.vue
Lista de tipos de servicios con porcentajes de comisión.

#### TipoServicioForm.vue
Formulario para crear/editar tipos de servicios con validación de porcentaje.

#### TipoServicioCard.vue
Tarjeta de tipo de servicio mostrando nombre, descripción y comisión.

### Componentes de Reportes

#### IngresosReport.vue
Reporte de ingresos totales con filtros de fecha.

#### BeneficiosReport.vue
Reporte de beneficios (ingresos - comisiones) con desglose.

#### PagoEmpleadoReport.vue
Reporte de pago a empleado con desglose de servicios.

## Stores (Pinia)

La aplicación usa Pinia para gestión de estado global. Cada store maneja una entidad del dominio.

### useEmpleadosStore

```typescript
import { useEmpleadosStore } from '@/stores/empleados';

const store = useEmpleadosStore();

// Estado
store.empleados          // Lista de empleados
store.loading            // Estado de carga
store.error              // Mensaje de error

// Computed
store.empleadosOrdenados // Empleados ordenados alfabéticamente

// Acciones
await store.cargarEmpleados()
await store.crearEmpleado({ id: 'E001', nombre: 'Juan' })
await store.actualizarEmpleado('E001', { nombre: 'Juan Pérez' })
await store.eliminarEmpleado('E001')
```

### useTiposServiciosStore

```typescript
import { useTiposServiciosStore } from '@/stores/tiposServicios';

const store = useTiposServiciosStore();

// Acciones
await store.cargarTiposServicios()
await store.crearTipoServicio({
  nombre: 'Corte',
  descripcion: 'Corte de cabello',
  porcentaje_comision: 40
})
```

### useServiciosStore

```typescript
import { useServiciosStore } from '@/stores/servicios';

const store = useServiciosStore();

// Acciones
await store.cargarServicios()
await store.filtrarServicios({
  empleado_id: 'E001',
  fecha_inicio: '2024-01-01',
  fecha_fin: '2024-01-31'
})
await store.registrarServicio({
  fecha: '2024-01-15',
  empleado_id: 'E001',
  tipo_servicio: 'Corte',
  precio: 25.00
})
```

### useReportesStore

```typescript
import { useReportesStore } from '@/stores/reportes';

const store = useReportesStore();

// Acciones
await store.calcularIngresos({ fecha_inicio: '2024-01-01', fecha_fin: '2024-01-31' })
await store.calcularBeneficios({ fecha_inicio: '2024-01-01', fecha_fin: '2024-01-31' })
await store.calcularPagoEmpleado('E001', { fecha_inicio: '2024-01-01' })
```

## Rutas

La aplicación usa Vue Router para navegación:

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/` | HomeView | Dashboard con resumen de estadísticas |
| `/empleados` | EmpleadosView | Gestión de empleados |
| `/tipos-servicios` | TiposServiciosView | Gestión de tipos de servicios |
| `/servicios` | ServiciosView | Registro y consulta de servicios |
| `/reportes` | ReportesView | Reportes de ingresos y pagos |

### Navegación Programática

```typescript
import { useRouter } from 'vue-router';

const router = useRouter();

// Navegar a otra ruta
router.push('/empleados');

// Navegar con parámetros
router.push({ name: 'empleados', params: { id: 'E001' } });

// Navegar atrás
router.back();
```

## Diseño Mobile-First

La aplicación está diseñada con un enfoque mobile-first usando Tailwind CSS:

### Breakpoints

| Breakpoint | Ancho mínimo | Uso |
|------------|--------------|-----|
| `sm` | 640px | Tablets pequeñas |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Desktops grandes |

### Patrones Responsive

#### Grid Adaptativo
```vue
<!-- 1 columna en móvil, 2 en tablet, 3 en desktop -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Contenido -->
</div>
```

#### Botones Full-Width en Móvil
```vue
<!-- Full width en móvil, auto en desktop -->
<button class="w-full sm:w-auto px-6 py-2">
  Guardar
</button>
```

#### Navegación Responsive
- Móvil: Menú hamburguesa colapsable
- Desktop: Menú horizontal visible

#### Formularios Optimizados
- Inputs con tamaño táctil (min-height: 44px)
- Labels claros y visibles
- Validación en tiempo real
- Mensajes de error descriptivos

### Pruebas de Responsive

Para probar en diferentes tamaños:

```bash
# Ejecutar tests E2E con diferentes viewports
npm run test:e2e
```

Los tests E2E incluyen pruebas en viewports de:
- Móvil: 375x667 (iPhone SE)
- Tablet: 768x1024 (iPad)
- Desktop: 1920x1080

## Testing

### Tests Unitarios (Vitest)

Los tests unitarios verifican componentes, stores y funciones de forma aislada.

**Ubicación:** `tests/unit/`

**Ejecutar:**
```bash
npm run test          # Modo watch
npm run test:run      # Una vez
npm run test:coverage # Con cobertura
```

**Ejemplo de test de componente:**
```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import EmpleadoCard from '@/components/empleados/EmpleadoCard.vue';

describe('EmpleadoCard', () => {
  it('muestra información del empleado', () => {
    const wrapper = mount(EmpleadoCard, {
      props: {
        empleado: { id: 'E001', nombre: 'Juan Pérez' }
      }
    });
    
    expect(wrapper.text()).toContain('Juan Pérez');
    expect(wrapper.text()).toContain('E001');
  });
});
```

**Ejemplo de test de store:**
```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useEmpleadosStore } from '@/stores/empleados';

describe('useEmpleadosStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('carga empleados correctamente', async () => {
    const store = useEmpleadosStore();
    await store.cargarEmpleados();
    
    expect(store.empleados).toBeDefined();
    expect(store.loading).toBe(false);
  });
});
```

### Tests E2E (Playwright)

Los tests E2E verifican flujos completos de usuario en un navegador real.

**Ubicación:** `tests/e2e/`

**Ejecutar:**
```bash
npm run test:e2e        # Headless
npm run test:e2e:headed # Con navegador visible
npm run test:e2e:ui     # Con interfaz gráfica
npm run test:e2e:debug  # Modo debug
```

**Ejemplo de test E2E:**
```typescript
import { test, expect } from '@playwright/test';

test('crear nuevo empleado', async ({ page }) => {
  await page.goto('http://localhost:5173/empleados');
  
  // Click en botón nuevo
  await page.click('text=Nuevo Empleado');
  
  // Llenar formulario
  await page.fill('input[name="id"]', 'E001');
  await page.fill('input[name="nombre"]', 'Juan Pérez');
  
  // Enviar
  await page.click('button[type="submit"]');
  
  // Verificar que aparece en la lista
  await expect(page.locator('text=Juan Pérez')).toBeVisible();
});
```

**Configuración de tests E2E:**

Ver [tests/e2e/README.md](tests/e2e/README.md) y [tests/e2e/SETUP.md](tests/e2e/SETUP.md) para:
- Configuración detallada
- Helpers y utilidades
- Mejores prácticas
- Solución de problemas

## Desarrollo

### Agregar un Nuevo Componente

1. **Crear el archivo** en `src/components/[categoria]/NombreComponente.vue`

2. **Usar Composition API con `<script setup>`:**

```vue
<template>
  <div class="p-4">
    <h2 class="text-xl font-bold">{{ titulo }}</h2>
    <button @click="handleClick" class="bg-blue-600 text-white px-4 py-2 rounded">
      {{ textoBoton }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// Props
interface Props {
  titulo: string;
  textoBoton?: string;
}

const props = withDefaults(defineProps<Props>(), {
  textoBoton: 'Click aquí'
});

// Emits
const emit = defineEmits<{
  click: [];
}>();

// Estado local
const contador = ref(0);

// Métodos
function handleClick() {
  contador.value++;
  emit('click');
}
</script>
```

3. **Aplicar estilos con Tailwind CSS** (evitar CSS custom)

4. **Crear test unitario** en `tests/unit/components/[categoria]/NombreComponente.spec.ts`

### Agregar una Nueva Vista

1. **Crear el archivo** en `src/views/NombreView.vue`

2. **Registrar la ruta** en `src/router/index.ts`:

```typescript
{
  path: '/nueva-ruta',
  name: 'nueva',
  component: () => import('@/views/NuevaView.vue')
}
```

3. **Agregar enlace** en la navegación de `App.vue`:

```vue
<router-link to="/nueva-ruta" class="nav-link">
  Nueva Sección
</router-link>
```

### Agregar un Nuevo Store

1. **Crear el archivo** en `src/stores/nuevoStore.ts`:

```typescript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { nuevoAPI } from '@/services/api';
import type { NuevoTipo } from '@/types/models';

export const useNuevoStore = defineStore('nuevo', () => {
  // Estado
  const items = ref<NuevoTipo[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Computed
  const itemsOrdenados = computed(() => 
    [...items.value].sort((a, b) => a.nombre.localeCompare(b.nombre))
  );

  // Acciones
  async function cargarItems() {
    loading.value = true;
    error.value = null;
    try {
      const response = await nuevoAPI.listar();
      items.value = response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cargar items';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return {
    items,
    loading,
    error,
    itemsOrdenados,
    cargarItems,
  };
});
```

2. **Usar en componentes:**

```vue
<script setup lang="ts">
import { onMounted } from 'vue';
import { useNuevoStore } from '@/stores/nuevoStore';
import { storeToRefs } from 'pinia';

const store = useNuevoStore();
const { items, loading, error } = storeToRefs(store);

onMounted(() => {
  store.cargarItems();
});
</script>
```

### Agregar Nuevos Endpoints de API

En `src/services/api.ts`:

```typescript
export const nuevoAPI = {
  listar: () => api.get<NuevoTipo[]>('/nuevo'),
  obtener: (id: string) => api.get<NuevoTipo>(`/nuevo/${id}`),
  crear: (data: NuevoTipoCreate) => api.post<NuevoTipo>('/nuevo', data),
  actualizar: (id: string, data: NuevoTipoUpdate) => 
    api.put<NuevoTipo>(`/nuevo/${id}`, data),
  eliminar: (id: string) => api.delete(`/nuevo/${id}`),
};
```

### Manejo de Errores

El interceptor de Axios maneja errores automáticamente:

```typescript
// En componentes/stores
try {
  await store.crearEmpleado(data);
  // Mostrar mensaje de éxito
} catch (e: any) {
  // El error ya está en store.error
  // Mostrar ErrorMessage component
}
```

### Formato de Código

Antes de hacer commit:

```bash
npm run format  # Formatea con Prettier
npm run lint    # Verifica con ESLint
```

### Convenciones de Código

- **Componentes:** PascalCase (EmpleadoCard.vue)
- **Archivos TypeScript:** camelCase (empleados.ts)
- **Stores:** use + PascalCase + Store (useEmpleadosStore)
- **Props/Emits:** Siempre tipados con TypeScript
- **Estilos:** Usar Tailwind CSS, evitar CSS custom
- **Imports:** Usar alias `@/` para src/

## Tecnologías

### Core

- **Vue 3** (v3.4+) - Framework progresivo de JavaScript con Composition API
- **TypeScript** (v5.3+) - Tipado estático para JavaScript
- **Vite** (v5.0+) - Build tool y dev server ultrarrápido

### Routing y Estado

- **Vue Router** (v4.2+) - Enrutamiento oficial para Vue.js
- **Pinia** (v2.1+) - Store oficial para Vue 3 (reemplazo de Vuex)

### HTTP y Estilos

- **Axios** (v1.6+) - Cliente HTTP basado en promesas
- **Tailwind CSS** (v3.4+) - Framework CSS utility-first

### Desarrollo

- **ESLint** (v8.56+) - Linter para JavaScript/TypeScript
- **Prettier** (v3.2+) - Formateador de código
- **TypeScript ESLint** - Reglas de ESLint para TypeScript

### Testing

- **Vitest** (v1.2+) - Framework de testing unitario (compatible con Vite)
- **Vue Test Utils** (v2.4+) - Utilidades oficiales para testing de Vue
- **Playwright** (v1.41+) - Framework de testing E2E
- **@vue/test-utils** - Testing utilities para Vue 3

### Build y Tooling

- **PostCSS** - Procesador de CSS (usado por Tailwind)
- **Autoprefixer** - Añade prefijos de navegador automáticamente

## Ejemplos de Uso

### Ejemplo 1: Crear y usar un componente

```vue
<!-- src/components/MiComponente.vue -->
<template>
  <div class="bg-white p-4 rounded shadow">
    <h3 class="text-lg font-bold mb-2">{{ titulo }}</h3>
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  titulo: string;
}>();
</script>
```

```vue
<!-- Usar en otro componente -->
<template>
  <MiComponente titulo="Hola Mundo">
    <p>Contenido del componente</p>
  </MiComponente>
</template>

<script setup lang="ts">
import MiComponente from '@/components/MiComponente.vue';
</script>
```

### Ejemplo 2: Formulario con validación

```vue
<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <label class="block text-sm font-medium mb-1">Nombre</label>
      <input
        v-model="formData.nombre"
        type="text"
        required
        class="w-full px-3 py-2 border rounded"
        :class="{ 'border-red-500': errors.nombre }"
      />
      <p v-if="errors.nombre" class="text-red-500 text-sm mt-1">
        {{ errors.nombre }}
      </p>
    </div>
    
    <button
      type="submit"
      :disabled="loading"
      class="w-full bg-blue-600 text-white py-2 rounded disabled:opacity-50"
    >
      {{ loading ? 'Guardando...' : 'Guardar' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';

const formData = reactive({
  nombre: '',
});

const errors = reactive({
  nombre: '',
});

const loading = ref(false);

function validateForm() {
  errors.nombre = '';
  
  if (!formData.nombre.trim()) {
    errors.nombre = 'El nombre es requerido';
    return false;
  }
  
  return true;
}

async function handleSubmit() {
  if (!validateForm()) return;
  
  loading.value = true;
  try {
    // Enviar datos...
  } catch (e) {
    // Manejar error...
  } finally {
    loading.value = false;
  }
}
</script>
```

### Ejemplo 3: Consumir API con store

```vue
<template>
  <div>
    <LoadingSpinner v-if="loading" />
    <ErrorMessage v-else-if="error" :message="error" />
    <div v-else>
      <div v-for="empleado in empleados" :key="empleado.id">
        {{ empleado.nombre }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useEmpleadosStore } from '@/stores/empleados';
import { storeToRefs } from 'pinia';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';

const store = useEmpleadosStore();
const { empleados, loading, error } = storeToRefs(store);

onMounted(async () => {
  await store.cargarEmpleados();
});
</script>
```

## Solución de Problemas

### Error: "Cannot find module '@/...'"

Verifica que el alias `@` esté configurado en `vite.config.ts`:

```typescript
resolve: {
  alias: {
    '@': fileURLToPath(new URL('./src', import.meta.url))
  }
}
```

### Error: "Failed to fetch" en API calls

1. Verifica que el backend esté ejecutándose en `http://localhost:8000`
2. Verifica CORS en el backend
3. Verifica la URL en `src/services/api.ts`

### Tests E2E fallan

1. Asegúrate de que backend y frontend estén ejecutándose
2. Verifica las URLs en `playwright.config.ts`
3. Limpia la base de datos de prueba antes de ejecutar tests

### Estilos de Tailwind no se aplican

1. Verifica que el archivo esté incluido en `tailwind.config.js`:

```javascript
content: [
  "./index.html",
  "./src/**/*.{vue,js,ts,jsx,tsx}",
],
```

2. Reinicia el servidor de desarrollo

### TypeScript muestra errores

```bash
# Verificar tipos
npm run type-check

# Limpiar y reinstalar
rm -rf node_modules package-lock.json
npm install
```

## Notas

- El proyecto usa TypeScript estricto
- Todos los componentes deben ser tipados
- Se recomienda usar Composition API con `<script setup>`
- Los estilos deben usar Tailwind CSS (evitar CSS custom cuando sea posible)
- Seguir convenciones de Vue 3 y mejores prácticas

## Recursos

- [Documentación de Vue 3](https://vuejs.org/)
- [Documentación de TypeScript](https://www.typescriptlang.org/)
- [Documentación de Vite](https://vitejs.dev/)
- [Documentación de Pinia](https://pinia.vuejs.org/)
- [Documentación de Tailwind CSS](https://tailwindcss.com/)
- [Documentación de Playwright](https://playwright.dev/)
