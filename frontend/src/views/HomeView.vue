<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-2">Sistema de Gestión de Stephany Mondragón</h1>
    <p class="text-gray-600 mb-8">
      Bienvenido al sistema de gestión para salón de peluquería
    </p>

    <!-- Dashboard de estadísticas -->
    <div class="mb-8">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Resumen General</h2>
      
      <LoadingSpinner v-if="cargando" />
      
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <!-- Total Empleados -->
        <div class="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow-md">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm opacity-90 mb-1">Empleados</p>
              <p class="text-3xl font-bold">{{ totalEmpleados }}</p>
            </div>
            <div class="text-4xl opacity-80">
              👥
            </div>
          </div>
        </div>

        <!-- Total Tipos de Servicios -->
        <div class="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-lg shadow-md">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm opacity-90 mb-1">Tipos de Servicios</p>
              <p class="text-3xl font-bold">{{ totalTiposServicios }}</p>
            </div>
            <div class="text-4xl opacity-80">
              ✂️
            </div>
          </div>
        </div>

        <!-- Total Servicios -->
        <div class="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow-md">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm opacity-90 mb-1">Servicios Registrados</p>
              <p class="text-3xl font-bold">{{ totalServicios }}</p>
            </div>
            <div class="text-4xl opacity-80">
              📋
            </div>
          </div>
        </div>

        <!-- Ingresos Totales -->
        <div class="bg-gradient-to-br from-orange-500 to-orange-600 text-white p-6 rounded-lg shadow-md">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm opacity-90 mb-1">Ingresos Totales</p>
              <p class="text-2xl font-bold">{{ formatearMoneda(ingresosTotal) }}</p>
            </div>
            <div class="text-4xl opacity-80">
              💰
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Accesos rápidos -->
    <div>
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Accesos Rápidos</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <router-link
          to="/empleados"
          class="bg-blue-500 hover:bg-blue-600 text-white p-6 rounded-lg shadow-md transition transform hover:scale-105"
        >
          <h2 class="text-xl font-semibold mb-2">Empleados</h2>
          <p class="text-sm opacity-90">Gestionar empleados del salón</p>
        </router-link>

        <router-link
          to="/tipos-servicios"
          class="bg-green-500 hover:bg-green-600 text-white p-6 rounded-lg shadow-md transition transform hover:scale-105"
        >
          <h2 class="text-xl font-semibold mb-2">Tipos de Servicios</h2>
          <p class="text-sm opacity-90">Configurar servicios y comisiones</p>
        </router-link>

        <router-link
          to="/servicios"
          class="bg-purple-500 hover:bg-purple-600 text-white p-6 rounded-lg shadow-md transition transform hover:scale-105"
        >
          <h2 class="text-xl font-semibold mb-2">Servicios</h2>
          <p class="text-sm opacity-90">Registrar servicios realizados</p>
        </router-link>

        <router-link
          to="/reportes"
          class="bg-orange-500 hover:bg-orange-600 text-white p-6 rounded-lg shadow-md transition transform hover:scale-105"
        >
          <h2 class="text-xl font-semibold mb-2">Reportes</h2>
          <p class="text-sm opacity-90">Ver ingresos y pagos</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useEmpleadosStore } from '@/stores/empleados';
import { useTiposServiciosStore } from '@/stores/tiposServicios';
import { useServiciosStore } from '@/stores/servicios';
import { useReportesStore } from '@/stores/reportes';
import { storeToRefs } from 'pinia';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';

const empleadosStore = useEmpleadosStore();
const tiposServiciosStore = useTiposServiciosStore();
const serviciosStore = useServiciosStore();
const reportesStore = useReportesStore();

const { empleados } = storeToRefs(empleadosStore);
const { tiposServicios } = storeToRefs(tiposServiciosStore);
const { servicios } = storeToRefs(serviciosStore);
const { ingresos } = storeToRefs(reportesStore);

const cargando = ref(true);

const totalEmpleados = computed(() => empleados.value.length);
const totalTiposServicios = computed(() => tiposServicios.value.length);
const totalServicios = computed(() => servicios.value.length);
const ingresosTotal = computed(() => ingresos.value?.total || 0);

function formatearMoneda(valor: number): string {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(valor);
}

onMounted(async () => {
  try {
    // Cargar datos en paralelo
    await Promise.all([
      empleadosStore.cargarEmpleados(),
      tiposServiciosStore.cargarTiposServicios(),
      serviciosStore.cargarServicios(),
      reportesStore.calcularIngresos(),
    ]);
  } catch (error) {
    console.error('Error al cargar datos del dashboard:', error);
  } finally {
    cargando.value = false;
  }
});
</script>
