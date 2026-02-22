<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Reporte de Ingresos</h2>

    <!-- Filtros de fecha -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
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
        @click="cargarIngresos"
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

    <!-- Visualización de total -->
    <div v-if="ingresos !== null && !loading" class="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-6 border border-green-200">
      <div class="text-center">
        <p class="text-sm text-gray-600 mb-2">
          <span v-if="filtros.fecha_inicio || filtros.fecha_fin">
            Período: 
            {{ filtros.fecha_inicio ? formatearFecha(filtros.fecha_inicio) : 'Inicio' }} - 
            {{ filtros.fecha_fin ? formatearFecha(filtros.fecha_fin) : 'Hoy' }}
          </span>
          <span v-else>Total General</span>
        </p>
        <p class="text-4xl font-bold text-green-700">
          {{ formatearMoneda(ingresos.total) }}
        </p>
        <p class="text-sm text-gray-600 mt-2">Ingresos Totales</p>
      </div>
    </div>

    <LoadingSpinner v-if="loading" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { reportesAPI } from '@/services/api';
import type { IngresosResponse } from '@/types/models';
import ErrorMessage from '@/components/common/ErrorMessage.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';

const ingresos = ref<IngresosResponse | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const filtros = reactive({
  fecha_inicio: '',
  fecha_fin: '',
});

async function cargarIngresos() {
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

    const response = await reportesAPI.ingresos(params);
    ingresos.value = response.data;
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error al cargar ingresos';
  } finally {
    loading.value = false;
  }
}

function limpiarFiltros() {
  filtros.fecha_inicio = '';
  filtros.fecha_fin = '';
  ingresos.value = null;
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

onMounted(() => {
  cargarIngresos();
});
</script>
