<template>
  <div class="container mx-auto px-4 py-6">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <h2 class="text-2xl font-bold text-gray-800">Empleados</h2>
      <button
        @click="mostrarFormulario = true"
        class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition"
      >
        + Nuevo Empleado
      </button>
    </div>

    <LoadingSpinner v-if="loading" />
    <ErrorMessage v-else-if="error" :message="error" />

    <div v-else-if="empleadosOrdenados.length === 0" class="text-center py-12">
      <p class="text-gray-500 text-lg">No hay empleados registrados</p>
      <p class="text-gray-400 text-sm mt-2">Haz clic en "Nuevo Empleado" para agregar uno</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <EmpleadoCard
        v-for="empleado in empleadosOrdenados"
        :key="empleado.id"
        :empleado="empleado"
        @editar="editarEmpleado"
        @eliminar="confirmarEliminar"
      />
    </div>

    <EmpleadoForm
      v-if="mostrarFormulario"
      :empleado="empleadoSeleccionado"
      @guardar="guardarEmpleado"
      @cancelar="cerrarFormulario"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useEmpleadosStore } from '@/stores/empleados';
import { storeToRefs } from 'pinia';
import EmpleadoCard from './EmpleadoCard.vue';
import EmpleadoForm from './EmpleadoForm.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ErrorMessage from '@/components/common/ErrorMessage.vue';
import type { Empleado } from '@/types/models';

const store = useEmpleadosStore();
const { empleadosOrdenados, loading, error } = storeToRefs(store);

const mostrarFormulario = ref(false);
const empleadoSeleccionado = ref<Empleado | null>(null);

onMounted(() => {
  store.cargarEmpleados();
});

function editarEmpleado(empleado: Empleado) {
  empleadoSeleccionado.value = empleado;
  mostrarFormulario.value = true;
}

function cerrarFormulario() {
  mostrarFormulario.value = false;
  empleadoSeleccionado.value = null;
}

async function guardarEmpleado(data: { id: string; nombre: string }) {
  try {
    if (empleadoSeleccionado.value) {
      await store.actualizarEmpleado(empleadoSeleccionado.value.id, { nombre: data.nombre });
    } else {
      await store.crearEmpleado(data);
    }
    cerrarFormulario();
  } catch (e) {
    // Error is handled by the store
    console.error('Error al guardar empleado:', e);
  }
}

function confirmarEliminar(id: string) {
  if (confirm('¿Estás seguro de que deseas eliminar este empleado?')) {
    eliminarEmpleado(id);
  }
}

async function eliminarEmpleado(id: string) {
  try {
    await store.eliminarEmpleado(id);
  } catch (e) {
    // Error is handled by the store
    console.error('Error al eliminar empleado:', e);
  }
}
</script>
