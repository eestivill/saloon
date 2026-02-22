<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
      <div class="p-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-6">
          Registrar Servicio
        </h2>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Fecha <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.fecha"
              type="date"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.fecha }"
            />
            <p v-if="errors.fecha" class="text-red-500 text-sm mt-1">{{ errors.fecha }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Empleado <span class="text-red-500">*</span>
            </label>
            <select
              v-model="formData.empleado_id"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.empleado_id }"
            >
              <option value="">Selecciona un empleado</option>
              <option v-for="empleado in empleadosOrdenados" :key="empleado.id" :value="empleado.id">
                {{ empleado.nombre }}
              </option>
            </select>
            <p v-if="errors.empleado_id" class="text-red-500 text-sm mt-1">{{ errors.empleado_id }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Tipo de Servicio <span class="text-red-500">*</span>
            </label>
            <select
              v-model="formData.tipo_servicio"
              @change="onTipoServicioChange"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.tipo_servicio }"
            >
              <option value="">Selecciona un tipo de servicio</option>
              <option v-for="tipo in tiposServiciosOrdenados" :key="tipo.nombre" :value="tipo.nombre">
                {{ tipo.nombre }} ({{ tipo.porcentaje_comision }}%)
              </option>
            </select>
            <p v-if="errors.tipo_servicio" class="text-red-500 text-sm mt-1">{{ errors.tipo_servicio }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Precio ($) <span class="text-red-500">*</span>
            </label>
            <input
              v-model.number="formData.precio"
              type="number"
              required
              min="0.01"
              step="0.01"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.precio }"
              placeholder="Ej: 25.00"
            />
            <p v-if="errors.precio" class="text-red-500 text-sm mt-1">{{ errors.precio }}</p>
            <p v-if="precioSugerido" class="text-blue-600 text-xs mt-1">💡 Precio sugerido: ${{ precioSugerido }}</p>
            <p class="text-gray-500 text-xs mt-1">Debe ser mayor que cero</p>
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
import { ref, reactive, onMounted, computed } from 'vue';
import { useEmpleadosStore } from '@/stores/empleados';
import { useTiposServiciosStore } from '@/stores/tiposServicios';
import { storeToRefs } from 'pinia';

const emit = defineEmits<{
  guardar: [data: { fecha: string; empleado_id: string; tipo_servicio: string; precio: number }];
  cancelar: [];
}>();

const empleadosStore = useEmpleadosStore();
const tiposServiciosStore = useTiposServiciosStore();

const { empleadosOrdenados } = storeToRefs(empleadosStore);
const { tiposServiciosOrdenados } = storeToRefs(tiposServiciosStore);

const formData = reactive({
  fecha: new Date().toISOString().split('T')[0] as string, // Fecha actual por defecto
  empleado_id: '',
  tipo_servicio: '',
  precio: 0,
});

const errors = reactive({
  fecha: '',
  empleado_id: '',
  tipo_servicio: '',
  precio: '',
});

const loading = ref(false);

onMounted(async () => {
  // Cargar empleados y tipos de servicios si no están cargados
  if (empleadosStore.empleados.length === 0) {
    await empleadosStore.cargarEmpleados();
  }
  if (tiposServiciosStore.tiposServicios.length === 0) {
    await tiposServiciosStore.cargarTiposServicios();
  }
});

// Computed property para obtener el precio sugerido del tipo de servicio seleccionado
const precioSugerido = computed(() => {
  if (!formData.tipo_servicio) return null;
  const tipo = tiposServiciosStore.tiposServicios.find(t => t.nombre === formData.tipo_servicio);
  return tipo?.precio_por_defecto || null;
});

// Auto-llenar precio cuando se selecciona un tipo de servicio
function onTipoServicioChange() {
  const tipo = tiposServiciosStore.tiposServicios.find(t => t.nombre === formData.tipo_servicio);
  if (tipo?.precio_por_defecto) {
    formData.precio = tipo.precio_por_defecto;
  }
}

function validateForm(): boolean {
  errors.fecha = '';
  errors.empleado_id = '';
  errors.tipo_servicio = '';
  errors.precio = '';

  let isValid = true;

  if (!formData.fecha) {
    errors.fecha = 'La fecha es requerida';
    isValid = false;
  }

  if (!formData.empleado_id) {
    errors.empleado_id = 'Debes seleccionar un empleado';
    isValid = false;
  }

  if (!formData.tipo_servicio) {
    errors.tipo_servicio = 'Debes seleccionar un tipo de servicio';
    isValid = false;
  }

  if (!formData.precio || formData.precio <= 0) {
    errors.precio = 'El precio debe ser mayor que cero';
    isValid = false;
  }

  if (isNaN(formData.precio)) {
    errors.precio = 'El precio debe ser un número válido';
    isValid = false;
  }

  return isValid;
}

async function handleSubmit() {
  if (!validateForm()) return;

  loading.value = true;
  try {
    emit('guardar', {
      fecha: formData.fecha,
      empleado_id: formData.empleado_id,
      tipo_servicio: formData.tipo_servicio,
      precio: formData.precio,
    });
  } finally {
    loading.value = false;
  }
}
</script>
