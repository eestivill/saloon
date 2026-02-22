<template>
  <div class="bg-white rounded-lg shadow-md p-4 mb-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Filtros</h3>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Empleado
        </label>
        <select
          v-model="filtros.empleado_id"
          class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Todos los empleados</option>
          <option v-for="empleado in empleadosOrdenados" :key="empleado.id" :value="empleado.id">
            {{ empleado.nombre }}
          </option>
        </select>
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

    <div class="flex gap-3 mt-4">
      <button
        @click="aplicarFiltros"
        class="flex-1 sm:flex-none px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
      >
        Aplicar Filtros
      </button>
      <button
        @click="limpiarFiltros"
        class="flex-1 sm:flex-none px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
      >
        Limpiar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useEmpleadosStore } from '@/stores/empleados';
import { storeToRefs } from 'pinia';
import type { ServiciosFiltros } from '@/types/models';

const emit = defineEmits<{
  filtrar: [filtros: ServiciosFiltros];
}>();

const empleadosStore = useEmpleadosStore();
const { empleadosOrdenados } = storeToRefs(empleadosStore);

const filtros = reactive<ServiciosFiltros>({
  empleado_id: '',
  fecha_inicio: '',
  fecha_fin: '',
});

function aplicarFiltros() {
  const filtrosActivos: ServiciosFiltros = {};
  
  if (filtros.empleado_id) {
    filtrosActivos.empleado_id = filtros.empleado_id;
  }
  
  if (filtros.fecha_inicio) {
    filtrosActivos.fecha_inicio = filtros.fecha_inicio;
  }
  
  if (filtros.fecha_fin) {
    filtrosActivos.fecha_fin = filtros.fecha_fin;
  }
  
  emit('filtrar', filtrosActivos);
}

function limpiarFiltros() {
  filtros.empleado_id = '';
  filtros.fecha_inicio = '';
  filtros.fecha_fin = '';
  emit('filtrar', {});
}
</script>
