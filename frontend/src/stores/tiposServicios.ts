import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { tiposServiciosAPI } from '@/services/api';
import type { TipoServicio } from '@/types/models';

// Función helper para convertir strings a números
function parseTipoServicio(tipo: any): TipoServicio {
  return {
    ...tipo,
    precio_por_defecto: tipo.precio_por_defecto ? 
      (typeof tipo.precio_por_defecto === 'string' ? parseFloat(tipo.precio_por_defecto) : tipo.precio_por_defecto) 
      : null,
  };
}

export const useTiposServiciosStore = defineStore('tiposServicios', () => {
  const tiposServicios = ref<TipoServicio[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const tiposServiciosOrdenados = computed(() =>
    [...tiposServicios.value].sort((a, b) => a.nombre.localeCompare(b.nombre))
  );

  async function cargarTiposServicios() {
    loading.value = true;
    error.value = null;
    try {
      const response = await tiposServiciosAPI.listar();
      tiposServicios.value = response.data.map(parseTipoServicio);
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cargar tipos de servicios';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function crearTipoServicio(data: {
    nombre: string;
    descripcion: string;
    porcentaje_comision: number;
    precio_por_defecto?: number | null;
  }) {
    loading.value = true;
    error.value = null;
    try {
      const response = await tiposServiciosAPI.crear(data);
      const tipoParseado = parseTipoServicio(response.data);
      tiposServicios.value.push(tipoParseado);
      return tipoParseado;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al crear tipo de servicio';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function actualizarTipoServicio(
    nombre: string,
    data: Partial<TipoServicio>
  ) {
    loading.value = true;
    error.value = null;
    try {
      const response = await tiposServiciosAPI.actualizar(nombre, data);
      const tipoParseado = parseTipoServicio(response.data);
      const index = tiposServicios.value.findIndex((tipo) => tipo.nombre === nombre);
      if (index !== -1) {
        tiposServicios.value[index] = tipoParseado;
      }
      return tipoParseado;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al actualizar tipo de servicio';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function eliminarTipoServicio(nombre: string) {
    loading.value = true;
    error.value = null;
    try {
      await tiposServiciosAPI.eliminar(nombre);
      tiposServicios.value = tiposServicios.value.filter(
        (tipo) => tipo.nombre !== nombre
      );
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al eliminar tipo de servicio';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return {
    tiposServicios,
    tiposServiciosOrdenados,
    loading,
    error,
    cargarTiposServicios,
    crearTipoServicio,
    actualizarTipoServicio,
    eliminarTipoServicio,
  };
});
