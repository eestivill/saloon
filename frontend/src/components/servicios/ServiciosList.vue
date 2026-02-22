<template>
  <div class="container mx-auto px-4 py-6">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <h2 class="text-2xl font-bold text-gray-800">Servicios</h2>
      <button
        @click="mostrarFormulario = true"
        class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition"
      >
        + Registrar Servicio
      </button>
    </div>

    <ServicioFilters @filtrar="aplicarFiltros" />

    <LoadingSpinner v-if="loading" />
    <ErrorMessage v-else-if="error" :message="error" />

    <div v-else-if="serviciosOrdenados.length === 0" class="text-center py-12">
      <p class="text-gray-500 text-lg">No hay servicios registrados</p>
      <p class="text-gray-400 text-sm mt-2">Haz clic en "Registrar Servicio" para agregar uno</p>
    </div>

    <div v-else>
      <!-- Vista de tabla para pantallas grandes -->
      <div class="hidden md:block overflow-x-auto">
        <table class="min-w-full bg-white rounded-lg shadow-md overflow-hidden">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Fecha
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Empleado
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Tipo de Servicio
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Precio
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Comisión
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="servicio in serviciosOrdenados" :key="servicio.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatearFecha(servicio.fecha) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ obtenerNombreEmpleado(servicio.empleado_id) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ servicio.tipo_servicio }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${{ servicio.precio.toFixed(0) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${{ servicio.comision_calculada.toFixed(0) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <button
                  @click="confirmarEliminar(servicio.id)"
                  class="px-3 py-1 bg-red-600 hover:bg-red-700 text-white rounded transition text-xs"
                >
                  Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Vista de tarjetas para móviles -->
      <div class="md:hidden grid grid-cols-1 gap-4">
        <ServicioCard
          v-for="servicio in serviciosOrdenados"
          :key="servicio.id"
          :servicio="servicio"
          @eliminar="confirmarEliminar"
        />
      </div>
    </div>

    <ServicioForm
      v-if="mostrarFormulario"
      @guardar="guardarServicio"
      @cancelar="cerrarFormulario"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useServiciosStore } from '@/stores/servicios';
import { useEmpleadosStore } from '@/stores/empleados';
import { storeToRefs } from 'pinia';
import ServicioCard from './ServicioCard.vue';
import ServicioForm from './ServicioForm.vue';
import ServicioFilters from './ServicioFilters.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';
import type { ServiciosFiltros } from '@/types/models';

const serviciosStore = useServiciosStore();
const empleadosStore = useEmpleadosStore();

const { servicios, loading, error } = storeToRefs(serviciosStore);

const mostrarFormulario = ref(false);

// Ordenar servicios por fecha descendente (más recientes primero)
const serviciosOrdenados = computed(() => {
  return [...servicios.value].sort((a, b) => {
    return new Date(b.fecha).getTime() - new Date(a.fecha).getTime();
  });
});

onMounted(async () => {
  await serviciosStore.cargarServicios();
  // Cargar empleados para mostrar nombres
  if (empleadosStore.empleados.length === 0) {
    await empleadosStore.cargarEmpleados();
  }
});

function cerrarFormulario() {
  mostrarFormulario.value = false;
}

async function guardarServicio(data: {
  fecha: string;
  empleado_id: string;
  tipo_servicio: string;
  precio: number;
}) {
  try {
    await serviciosStore.registrarServicio(data);
    cerrarFormulario();
  } catch (e) {
    console.error('Error al registrar servicio:', e);
  }
}

function confirmarEliminar(id: string) {
  if (confirm('¿Estás seguro de que deseas eliminar este servicio?')) {
    eliminarServicio(id);
  }
}

async function eliminarServicio(id: string) {
  try {
    await serviciosStore.eliminarServicio(id);
  } catch (e) {
    console.error('Error al eliminar servicio:', e);
  }
}

async function aplicarFiltros(filtros: ServiciosFiltros) {
  try {
    await serviciosStore.filtrarServicios(filtros);
  } catch (e) {
    console.error('Error al filtrar servicios:', e);
  }
}

function obtenerNombreEmpleado(empleadoId: string): string {
  const empleado = empleadosStore.empleados.find(e => e.id === empleadoId);
  return empleado ? empleado.nombre : empleadoId;
}

function formatearFecha(fecha: string): string {
  const date = new Date(fecha);
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}
</script>
