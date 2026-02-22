<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Reporte de Pago a Empleado</h2>

    <!-- Selector de empleado y filtros de fecha -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Empleado *
        </label>
        <select
          v-model="empleadoSeleccionado"
          class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          :class="{ 'border-red-500': !empleadoSeleccionado && intentoConsulta }"
        >
          <option value="">Seleccione un empleado</option>
          <option v-for="empleado in empleadosOrdenados" :key="empleado.id" :value="empleado.id">
            {{ empleado.nombre }}
          </option>
        </select>
        <p v-if="!empleadoSeleccionado && intentoConsulta" class="text-red-500 text-sm mt-1">
          Debe seleccionar un empleado
        </p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Fecha Inicio
        </label>
        <input
          v-model="filtros.fecha_inicio"
          type="date"
          class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Fecha Fin
        </label>
        <input
          v-model="filtros.fecha_fin"
          type="date"
          class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
    </div>

    <div class="flex gap-3 mb-6">
      <button
        @click="cargarPago"
        :disabled="loading"
        class="flex-1 sm:flex-none px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition disabled:opacity-50"
      >
        {{ loading ? 'Cargando...' : 'Consultar' }}
      </button>
      <button
        @click="limpiarFiltros"
        class="flex-1 sm:flex-none px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
      >
        Limpiar
      </button>
    </div>

    <!-- Mensaje de error -->
    <ErrorMessage v-if="error" :message="error" />

    <!-- Visualización de pago -->
    <div v-if="desglosePago !== null && !loading" class="space-y-6">
      <!-- Información del empleado y total -->
      <div class="bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg p-6 border border-purple-200">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <p class="text-sm text-gray-600">Empleado</p>
            <p class="text-xl font-semibold text-gray-800">{{ desglosePago.empleado_nombre }}</p>
            <p class="text-xs text-gray-500 mt-1">ID: {{ desglosePago.empleado_id }}</p>
          </div>
          <div class="text-left sm:text-right">
            <p class="text-sm text-gray-600">Total a Pagar</p>
            <p class="text-3xl font-bold text-purple-700">{{ formatearMoneda(desglosePago.total) }}</p>
          </div>
        </div>
        
        <div v-if="filtros.fecha_inicio || filtros.fecha_fin" class="mt-4 pt-4 border-t border-purple-200">
          <p class="text-sm text-gray-600">
            Período: 
            {{ filtros.fecha_inicio ? formatearFecha(filtros.fecha_inicio) : 'Inicio' }} - 
            {{ filtros.fecha_fin ? formatearFecha(filtros.fecha_fin) : 'Hoy' }}
          </p>
        </div>
      </div>

      <!-- Desglose de servicios -->
      <div v-if="desglosePago.servicios.length > 0">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">
          Desglose de Servicios ({{ desglosePago.servicios.length }})
        </h3>

        <!-- Tabla responsive -->
        <div class="overflow-x-auto">
          <table class="min-w-full bg-white border border-gray-200 rounded-lg">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                  Fecha
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                  Tipo de Servicio
                </th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">
                  Precio
                </th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-700 uppercase tracking-wider">
                  Comisión
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="(servicio, index) in desglosePago.servicios" :key="index" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-sm text-gray-900 whitespace-nowrap">
                  {{ formatearFechaCorta(servicio.fecha) }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-900">
                  {{ servicio.tipo_servicio }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-900 text-right whitespace-nowrap">
                  {{ formatearMoneda(servicio.precio) }}
                </td>
                <td class="px-4 py-3 text-sm font-semibold text-purple-700 text-right whitespace-nowrap">
                  {{ formatearMoneda(servicio.comision) }}
                </td>
              </tr>
            </tbody>
            <tfoot class="bg-gray-50">
              <tr>
                <td colspan="3" class="px-4 py-3 text-sm font-semibold text-gray-800 text-right">
                  Total:
                </td>
                <td class="px-4 py-3 text-sm font-bold text-purple-700 text-right whitespace-nowrap">
                  {{ formatearMoneda(desglosePago.total) }}
                </td>
              </tr>
            </tfoot>
          </table>
        </div>

        <!-- Vista móvil alternativa (cards) -->
        <div class="md:hidden space-y-3 mt-4">
          <div
            v-for="(servicio, index) in desglosePago.servicios"
            :key="index"
            class="bg-gray-50 rounded-lg p-4 border border-gray-200"
          >
            <div class="flex justify-between items-start mb-2">
              <div>
                <p class="font-semibold text-gray-900">{{ servicio.tipo_servicio }}</p>
                <p class="text-sm text-gray-600">{{ formatearFechaCorta(servicio.fecha) }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-gray-600">Precio</p>
                <p class="font-semibold text-gray-900">{{ formatearMoneda(servicio.precio) }}</p>
              </div>
            </div>
            <div class="flex justify-between items-center pt-2 border-t border-gray-300">
              <span class="text-sm text-gray-600">Comisión</span>
              <span class="font-semibold text-purple-700">{{ formatearMoneda(servicio.comision) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sin servicios -->
      <div v-else class="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
        <p class="text-gray-700">
          No hay servicios registrados para este empleado en el período seleccionado.
        </p>
      </div>
    </div>

    <LoadingSpinner v-if="loading" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { empleadosAPI } from '@/services/api';
import { useEmpleadosStore } from '@/stores/empleados';
import { storeToRefs } from 'pinia';
import type { DesglosePago } from '@/types/models';
import ErrorMessage from '@/components/common/ErrorMessage.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';

const empleadosStore = useEmpleadosStore();
const { empleadosOrdenados } = storeToRefs(empleadosStore);

const desglosePago = ref<DesglosePago | null>(null);
const empleadoSeleccionado = ref('');
const loading = ref(false);
const error = ref<string | null>(null);
const intentoConsulta = ref(false);

const filtros = reactive({
  fecha_inicio: '',
  fecha_fin: '',
});

async function cargarPago() {
  intentoConsulta.value = true;
  
  if (!empleadoSeleccionado.value) {
    error.value = 'Debe seleccionar un empleado';
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    const params: { fecha_inicio?: string; fecha_fin?: string } = {};
    
    if (filtros.fecha_inicio) {
      params.fecha_inicio = filtros.fecha_inicio;
    }
    
    if (filtros.fecha_fin) {
      params.fecha_fin = filtros.fecha_fin;
    }

    const response = await empleadosAPI.obtenerPago(empleadoSeleccionado.value, params);
    desglosePago.value = response.data;
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error al cargar pago del empleado';
  } finally {
    loading.value = false;
  }
}

function limpiarFiltros() {
  empleadoSeleccionado.value = '';
  filtros.fecha_inicio = '';
  filtros.fecha_fin = '';
  desglosePago.value = null;
  intentoConsulta.value = false;
  error.value = null;
}

function formatearMoneda(valor: number): string {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(valor);
}

function formatearFecha(fecha: string): string {
  return new Date(fecha + 'T00:00:00').toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function formatearFechaCorta(fecha: string): string {
  return new Date(fecha + 'T00:00:00').toLocaleDateString('es-ES', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
}

onMounted(async () => {
  await empleadosStore.cargarEmpleados();
});
</script>
