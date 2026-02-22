import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { empleadosAPI } from '@/services/api';
import type { Empleado } from '@/types/models';

export const useEmpleadosStore = defineStore('empleados', () => {
  const empleados = ref<Empleado[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const empleadosOrdenados = computed(() =>
    [...empleados.value].sort((a, b) => a.nombre.localeCompare(b.nombre))
  );

  async function cargarEmpleados() {
    loading.value = true;
    error.value = null;
    try {
      const response = await empleadosAPI.listar();
      empleados.value = response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cargar empleados';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function crearEmpleado(data: { id: string; nombre: string }) {
    loading.value = true;
    error.value = null;
    try {
      const response = await empleadosAPI.crear(data);
      empleados.value.push(response.data);
      return response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al crear empleado';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function actualizarEmpleado(id: string, data: { nombre: string }) {
    loading.value = true;
    error.value = null;
    try {
      const response = await empleadosAPI.actualizar(id, data);
      const index = empleados.value.findIndex((emp) => emp.id === id);
      if (index !== -1) {
        empleados.value[index] = response.data;
      }
      return response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al actualizar empleado';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function eliminarEmpleado(id: string) {
    loading.value = true;
    error.value = null;
    try {
      await empleadosAPI.eliminar(id);
      empleados.value = empleados.value.filter((emp) => emp.id !== id);
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al eliminar empleado';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return {
    empleados,
    empleadosOrdenados,
    loading,
    error,
    cargarEmpleados,
    crearEmpleado,
    actualizarEmpleado,
    eliminarEmpleado,
  };
});
