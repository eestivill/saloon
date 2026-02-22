import axios from 'axios';
import type {
  Empleado,
  TipoServicio,
  Servicio,
  DesglosePago,
  IngresosResponse,
  BeneficiosResponse,
} from '@/types/models';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 400:
          console.error('Error de validación:', data.message);
          break;
        case 404:
          console.error('Recurso no encontrado:', data.message);
          break;
        case 409:
          console.error('Conflicto:', data.message);
          break;
        case 500:
          console.error('Error del servidor:', data.message);
          break;
      }
    } else if (error.request) {
      console.error('No se pudo conectar con el servidor');
    } else {
      console.error('Error:', error.message);
    }

    return Promise.reject(error);
  }
);

export const empleadosAPI = {
  listar: () => api.get<Empleado[]>('/empleados'),
  obtener: (id: string) => api.get<Empleado>(`/empleados/${id}`),
  crear: (data: { id: string; nombre: string }) => api.post<Empleado>('/empleados', data),
  actualizar: (id: string, data: { nombre: string }) =>
    api.put<Empleado>(`/empleados/${id}`, data),
  eliminar: (id: string) => api.delete(`/empleados/${id}`),
  obtenerPago: (id: string, params?: { fecha_inicio?: string; fecha_fin?: string }) =>
    api.get<DesglosePago>(`/empleados/${id}/pago`, { params }),
};

export const tiposServiciosAPI = {
  listar: () => api.get<TipoServicio[]>('/tipos-servicios'),
  obtener: (nombre: string) => api.get<TipoServicio>(`/tipos-servicios/${nombre}`),
  crear: (data: { nombre: string; descripcion: string; porcentaje_comision: number }) =>
    api.post<TipoServicio>('/tipos-servicios', data),
  actualizar: (nombre: string, data: Partial<TipoServicio>) =>
    api.put<TipoServicio>(`/tipos-servicios/${nombre}`, data),
  eliminar: (nombre: string) => api.delete(`/tipos-servicios/${nombre}`),
};

export const serviciosAPI = {
  listar: (params?: { empleado_id?: string; fecha_inicio?: string; fecha_fin?: string }) =>
    api.get<Servicio[]>('/servicios', { params }),
  obtener: (id: string) => api.get<Servicio>(`/servicios/${id}`),
  crear: (data: {
    fecha: string;
    empleado_id: string;
    tipo_servicio: string;
    precio: number;
  }) => api.post<Servicio>('/servicios', data),
  eliminar: (id: string) => api.delete(`/servicios/${id}`),
};

export const reportesAPI = {
  ingresos: (params?: { fecha_inicio?: string; fecha_fin?: string }) =>
    api.get<IngresosResponse>('/reportes/ingresos', { params }),
  beneficios: (params?: { fecha_inicio?: string; fecha_fin?: string }) =>
    api.get<BeneficiosResponse>('/reportes/beneficios', { params }),
};
