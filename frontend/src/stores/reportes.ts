import { defineStore } from 'pinia';
import { ref } from 'vue';
import { reportesAPI, empleadosAPI } from '@/services/api';
import type { IngresosResponse, BeneficiosResponse, DesglosePago } from '@/types/models';

export const useReportesStore = defineStore('reportes', () => {
  const ingresos = ref<IngresosResponse | null>(null);
  const beneficios = ref<BeneficiosResponse | null>(null);
  const pagoEmpleado = ref<DesglosePago | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function calcularIngresos(filtros?: { fecha_inicio?: string; fecha_fin?: string }) {
    loading.value = true;
    error.value = null;
    try {
      const response = await reportesAPI.ingresos(filtros);
      ingresos.value = response.data;
      return response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al calcular ingresos';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function calcularBeneficios(filtros?: { fecha_inicio?: string; fecha_fin?: string }) {
    loading.value = true;
    error.value = null;
    try {
      const response = await reportesAPI.beneficios(filtros);
      beneficios.value = response.data;
      return response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al calcular beneficios';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function calcularPagoEmpleado(
    empleadoId: string,
    filtros?: { fecha_inicio?: string; fecha_fin?: string }
  ) {
    loading.value = true;
    error.value = null;
    try {
      const response = await empleadosAPI.obtenerPago(empleadoId, filtros);
      pagoEmpleado.value = response.data;
      return response.data;
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al calcular pago de empleado';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return {
    ingresos,
    beneficios,
    pagoEmpleado,
    loading,
    error,
    calcularIngresos,
    calcularBeneficios,
    calcularPagoEmpleado,
  };
});
