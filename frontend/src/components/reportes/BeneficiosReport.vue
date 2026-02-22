<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Reporte de Beneficios</h2>

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
        @click="cargarBeneficios"
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

    <!-- Visualización de beneficios -->
    <div v-if="beneficios !== null && !loading" class="space-y-4">
      <!-- Período -->
      <div class="text-center text-sm text-gray-600 mb-4">
        <span v-if="filtros.fecha_inicio || filtros.fecha_fin">
          Período: 
          {{ filtros.fecha_inicio ? formatearFecha(filtros.fecha_inicio) : 'Inicio' }} - 
          {{ filtros.fecha_fin ? formatearFecha(filtros.fecha_fin) : 'Hoy' }}
        </span>
        <span v-else>Total General</span>
      </div>

      <!-- Tarjetas de métricas -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Ingresos -->
        <div class="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <p class="text-sm text-gray-600 mb-1">Ingresos</p>
          <p class="text-2xl font-bold text-blue-700">
            {{ formatearMoneda(beneficios.ingresos) }}
          </p>
        </div>

        <!-- Comisiones -->
        <div class="bg-orange-50 rounded-lg p-4 border border-orange-200">
          <p class="text-sm text-gray-600 mb-1">Comisiones</p>
          <p class="text-2xl font-bold text-orange-700">
            {{ formatearMoneda(beneficios.comisiones) }}
          </p>
        </div>

        <!-- Beneficios -->
        <div class="bg-green-50 rounded-lg p-4 border border-green-200">
          <p class="text-sm text-gray-600 mb-1">Beneficios</p>
          <p class="text-2xl font-bold text-green-700">
            {{ formatearMoneda(beneficios.beneficios) }}
          </p>
        </div>
      </div>

      <!-- Resumen visual -->
      <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Desglose</h3>
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-gray-700">Ingresos Totales:</span>
            <span class="font-semibold text-gray-900">{{ formatearMoneda(beneficios.ingresos) }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-700">Comisiones Pagadas:</span>
            <span class="font-semibold text-orange-700">- {{ formatearMoneda(beneficios.comisiones) }}</span>
          </div>
          <div class="border-t border-gray-300 pt-3 flex justify-between items-center">
            <span class="text-lg font-semibold text-gray-800">Beneficio Neto:</span>
            <span class="text-2xl font-bold text-green-700">{{ formatearMoneda(beneficios.beneficios) }}</span>
          </div>
        </div>

        <!-- Porcentaje de beneficio -->
        <div class="mt-4 pt-4 border-t border-gray-200">
          <div class="flex justify-between items-center text-sm">
            <span class="text-gray-600">Margen de Beneficio:</span>
            <span class="font-semibold" :class="margenColor">
              {{ calcularMargen() }}%
            </span>
          </div>
        </div>
      </div>
    </div>

    <LoadingSpinner v-if="loading" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { reportesAPI } from '@/services/api';
import type { BeneficiosResponse } from '@/types/models';
import ErrorMessage from '@/components/common/ErrorMessage.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';

const beneficios = ref<BeneficiosResponse | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const filtros = reactive({
  fecha_inicio: '',
  fecha_fin: '',
});

const margenColor = computed(() => {
  if (!beneficios.value || beneficios.value.ingresos === 0) return 'text-gray-600';
  const margen = (beneficios.value.beneficios / beneficios.value.ingresos) * 100;
  if (margen >= 50) return 'text-green-600';
  if (margen >= 30) return 'text-yellow-600';
  return 'text-red-600';
});

async function cargarBeneficios() {
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

    const response = await reportesAPI.beneficios(params);
    beneficios.value = response.data;
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Error al cargar beneficios';
  } finally {
    loading.value = false;
  }
}

function limpiarFiltros() {
  filtros.fecha_inicio = '';
  filtros.fecha_fin = '';
  beneficios.value = null;
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

function calcularMargen(): string {
  if (!beneficios.value || beneficios.value.ingresos === 0) return '0.00';
  const margen = (beneficios.value.beneficios / beneficios.value.ingresos) * 100;
  return margen.toFixed(2);
}

onMounted(() => {
  cargarBeneficios();
});
</script>
