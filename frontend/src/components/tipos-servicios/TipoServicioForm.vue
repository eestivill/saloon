<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
      <div class="p-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">
          {{ tipo ? 'Editar Tipo de Servicio' : 'Nuevo Tipo de Servicio' }}
        </h2>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Nombre <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.nombre"
              type="text"
              required
              :disabled="!!tipo"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              :class="{ 'border-red-500': errors.nombre }"
              placeholder="Ej: Corte Básico"
            />
            <p v-if="errors.nombre" class="text-red-500 text-sm mt-1">{{ errors.nombre }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Descripción <span class="text-red-500">*</span>
            </label>
            <textarea
              v-model="formData.descripcion"
              required
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.descripcion }"
              placeholder="Descripción del servicio"
            />
            <p v-if="errors.descripcion" class="text-red-500 text-sm mt-1">{{ errors.descripcion }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Porcentaje de Comisión (%) <span class="text-red-500">*</span>
            </label>
            <input
              v-model.number="formData.porcentaje_comision"
              type="number"
              required
              min="0"
              max="100"
              step="0.01"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.porcentaje_comision }"
              placeholder="Ej: 40"
            />
            <p v-if="errors.porcentaje_comision" class="text-red-500 text-sm mt-1">
              {{ errors.porcentaje_comision }}
            </p>
            <p class="text-gray-500 text-xs mt-1">Debe estar entre 0 y 100</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Precio por Defecto ($)
            </label>
            <input
              v-model.number="formData.precio_por_defecto"
              type="number"
              min="0.01"
              step="0.01"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.precio_por_defecto }"
              placeholder="Ej: 25.00 (opcional)"
            />
            <p v-if="errors.precio_por_defecto" class="text-red-500 text-sm mt-1">{{ errors.precio_por_defecto }}</p>
            <p class="text-gray-500 text-xs mt-1">Opcional. Se usará como precio sugerido al registrar servicios</p>
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
import type { TipoServicio } from '@/types/models';

const props = defineProps<{
  tipo?: TipoServicio | null;
}>();

const emit = defineEmits<{
  guardar: [data: { nombre: string; descripcion: string; porcentaje_comision: number; precio_por_defecto?: number | null }];
  cancelar: [];
}>();

const formData = reactive({
  nombre: '',
  descripcion: '',
  porcentaje_comision: 0,
  precio_por_defecto: null as number | null,
});

const errors = reactive({
  nombre: '',
  descripcion: '',
  porcentaje_comision: '',
  precio_por_defecto: '',
});

const loading = ref(false);

onMounted(() => {
  if (props.tipo) {
    formData.nombre = props.tipo.nombre;
    formData.descripcion = props.tipo.descripcion;
    formData.porcentaje_comision = props.tipo.porcentaje_comision;
    formData.precio_por_defecto = props.tipo.precio_por_defecto || null;
  }
});

function validateForm(): boolean {
  errors.nombre = '';
  errors.descripcion = '';
  errors.porcentaje_comision = '';
  errors.precio_por_defecto = '';

  let isValid = true;

  if (!formData.nombre.trim()) {
    errors.nombre = 'El nombre es requerido';
    isValid = false;
  }

  if (!formData.descripcion.trim()) {
    errors.descripcion = 'La descripción es requerida';
    isValid = false;
  }

  if (formData.porcentaje_comision < 0 || formData.porcentaje_comision > 100) {
    errors.porcentaje_comision = 'El porcentaje debe estar entre 0 y 100';
    isValid = false;
  }

  if (isNaN(formData.porcentaje_comision)) {
    errors.porcentaje_comision = 'El porcentaje debe ser un número válido';
    isValid = false;
  }

  if (formData.precio_por_defecto !== null && formData.precio_por_defecto !== undefined && formData.precio_por_defecto <= 0) {
    errors.precio_por_defecto = 'El precio debe ser mayor que cero';
    isValid = false;
  }

  return isValid;
}

async function handleSubmit() {
  if (!validateForm()) return;

  loading.value = true;
  try {
    emit('guardar', {
      nombre: formData.nombre.trim(),
      descripcion: formData.descripcion.trim(),
      porcentaje_comision: formData.porcentaje_comision,
      precio_por_defecto: formData.precio_por_defecto,
    });
  } finally {
    loading.value = false;
  }
}
</script>
