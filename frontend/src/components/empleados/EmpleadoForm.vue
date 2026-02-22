<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
      <div class="p-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">
          {{ empleado ? 'Editar Empleado' : 'Nuevo Empleado' }}
        </h2>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              ID <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.id"
              type="text"
              required
              :disabled="!!empleado"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              :class="{ 'border-red-500': errors.id }"
              placeholder="Ej: E001"
            />
            <p v-if="errors.id" class="text-red-500 text-sm mt-1">{{ errors.id }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Nombre <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.nombre"
              type="text"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.nombre }"
              placeholder="Nombre completo"
            />
            <p v-if="errors.nombre" class="text-red-500 text-sm mt-1">{{ errors.nombre }}</p>
          </div>

          <div class="flex gap-3 pt-4">
            <button
              type="button"
              @click="$emit('cancelar')"
              class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="loading"
              class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import type { Empleado } from '@/types/models';

const props = defineProps<{
  empleado?: Empleado | null;
}>();

const emit = defineEmits<{
  guardar: [data: { id: string; nombre: string }];
  cancelar: [];
}>();

const formData = reactive({
  id: '',
  nombre: '',
});

const errors = reactive({
  id: '',
  nombre: '',
});

const loading = ref(false);

onMounted(() => {
  if (props.empleado) {
    formData.id = props.empleado.id;
    formData.nombre = props.empleado.nombre;
  }
});

function validateForm(): boolean {
  errors.id = '';
  errors.nombre = '';

  let isValid = true;

  if (!formData.id.trim()) {
    errors.id = 'El ID es requerido';
    isValid = false;
  }

  if (!formData.nombre.trim()) {
    errors.nombre = 'El nombre es requerido';
    isValid = false;
  }

  return isValid;
}

async function handleSubmit() {
  if (!validateForm()) return;

  loading.value = true;
  try {
    emit('guardar', {
      id: formData.id.trim(),
      nombre: formData.nombre.trim(),
    });
  } finally {
    loading.value = false;
  }
}
</script>
