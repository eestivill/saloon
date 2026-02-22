<template>
  <div class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
    <div class="flex flex-col gap-3">
      <div class="flex-1">
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-lg font-semibold text-gray-800">{{ servicio.tipo_servicio }}</h3>
          <span class="text-sm text-gray-500">{{ formatearFecha(servicio.fecha) }}</span>
        </div>
        
        <div class="space-y-1 text-sm">
          <p class="text-gray-600">
            <span class="font-medium">Empleado:</span> {{ nombreEmpleado }}
          </p>
          <p class="text-gray-600">
            <span class="font-medium">Precio:</span> ${{ servicio.precio.toFixed(2) }}
          </p>
          <p class="text-gray-600">
            <span class="font-medium">Comisión:</span> ${{ servicio.comision_calculada.toFixed(2) }}
          </p>
        </div>
      </div>
      
      <div class="flex gap-2 w-full pt-2 border-t">
        <button
          @click="$emit('eliminar', servicio.id)"
          class="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition text-sm"
        >
          Eliminar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Servicio } from '@/types/models';
import { useEmpleadosStore } from '@/stores/empleados';

const props = defineProps<{
  servicio: Servicio;
}>();

defineEmits<{
  eliminar: [id: string];
}>();

const empleadosStore = useEmpleadosStore();

const nombreEmpleado = computed(() => {
  const empleado = empleadosStore.empleados.find(e => e.id === props.servicio.empleado_id);
  return empleado ? empleado.nombre : props.servicio.empleado_id;
});

function formatearFecha(fecha: string): string {
  const date = new Date(fecha);
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}
</script>
