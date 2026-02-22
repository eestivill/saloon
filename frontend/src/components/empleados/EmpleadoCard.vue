<template>
  <div class="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-800">{{ empleado.nombre }}</h3>
        <p class="text-sm text-gray-500">ID: {{ empleado.id }}</p>
      </div>
      
      <div class="flex gap-2 w-full sm:w-auto">
        <button
          @click="$emit('editar', empleado)"
          class="flex-1 sm:flex-none px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition text-sm"
        >
          Editar
        </button>
        <button
          @click="$emit('eliminar', empleado.id)"
          class="flex-1 sm:flex-none px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition text-sm"
        >
          Eliminar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Empleado } from '@/types/models';

defineProps<{
  empleado: Empleado;
}>();

defineEmits<{
  editar: [empleado: Empleado];
  eliminar: [id: string];
}>();
</script>
