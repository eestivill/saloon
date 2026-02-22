<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-3xl font-bold text-gray-800 mb-6">Reportes Financieros</h1>

    <!-- Tabs para diferentes reportes -->
    <div class="mb-6">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-4 overflow-x-auto" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="tabActivo = tab.id"
            :class="[
              tabActivo === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm transition'
            ]"
          >
            {{ tab.nombre }}
          </button>
        </nav>
      </div>
    </div>

    <!-- Contenido de tabs -->
    <div class="mt-6">
      <IngresosReport v-if="tabActivo === 'ingresos'" />
      <BeneficiosReport v-else-if="tabActivo === 'beneficios'" />
      <PagoEmpleadoReport v-else-if="tabActivo === 'pagos'" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import IngresosReport from '@/components/reportes/IngresosReport.vue';
import BeneficiosReport from '@/components/reportes/BeneficiosReport.vue';
import PagoEmpleadoReport from '@/components/reportes/PagoEmpleadoReport.vue';

const tabs = [
  { id: 'ingresos', nombre: 'Ingresos' },
  { id: 'beneficios', nombre: 'Beneficios' },
  { id: 'pagos', nombre: 'Pagos a Empleados' },
];

const tabActivo = ref('ingresos');
</script>
