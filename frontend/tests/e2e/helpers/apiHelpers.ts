import { APIRequestContext } from '@playwright/test';

/**
 * Helpers para interactuar con la API durante tests E2E
 */

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Crea un empleado a través de la API
 */
export async function crearEmpleadoAPI(
  request: APIRequestContext,
  empleado: { id: string; nombre: string }
) {
  const response = await request.post(`${API_BASE_URL}/empleados`, {
    data: empleado,
  });
  return response;
}

/**
 * Crea un tipo de servicio a través de la API
 */
export async function crearTipoServicioAPI(
  request: APIRequestContext,
  tipoServicio: { nombre: string; descripcion: string; porcentaje_comision: number }
) {
  const response = await request.post(`${API_BASE_URL}/tipos-servicios`, {
    data: tipoServicio,
  });
  return response;
}

/**
 * Crea un servicio a través de la API
 */
export async function crearServicioAPI(
  request: APIRequestContext,
  servicio: { fecha: string; empleado_id: string; tipo_servicio: string; precio: number }
) {
  const response = await request.post(`${API_BASE_URL}/servicios`, {
    data: servicio,
  });
  return response;
}

/**
 * Limpia todos los datos de la base de datos
 * Nota: Esto requiere que el backend tenga endpoints de limpieza o
 * que se reinicie la base de datos entre tests
 */
export async function limpiarBaseDatos(request: APIRequestContext) {
  // Obtener todos los servicios y eliminarlos
  const serviciosResponse = await request.get(`${API_BASE_URL}/servicios`);
  if (serviciosResponse.ok()) {
    const servicios = await serviciosResponse.json();
    for (const servicio of servicios) {
      await request.delete(`${API_BASE_URL}/servicios/${servicio.id}`);
    }
  }

  // Obtener todos los tipos de servicios y eliminarlos
  const tiposResponse = await request.get(`${API_BASE_URL}/tipos-servicios`);
  if (tiposResponse.ok()) {
    const tipos = await tiposResponse.json();
    for (const tipo of tipos) {
      await request.delete(`${API_BASE_URL}/tipos-servicios/${encodeURIComponent(tipo.nombre)}`);
    }
  }

  // Obtener todos los empleados y eliminarlos
  const empleadosResponse = await request.get(`${API_BASE_URL}/empleados`);
  if (empleadosResponse.ok()) {
    const empleados = await empleadosResponse.json();
    for (const empleado of empleados) {
      await request.delete(`${API_BASE_URL}/empleados/${empleado.id}`);
    }
  }
}

/**
 * Configura datos de prueba básicos
 */
export async function configurarDatosPrueba(
  request: APIRequestContext,
  empleados: any[],
  tiposServicios: any[],
  servicios: any[] = []
) {
  // Crear empleados
  for (const empleado of empleados) {
    await crearEmpleadoAPI(request, empleado);
  }

  // Crear tipos de servicios
  for (const tipo of tiposServicios) {
    await crearTipoServicioAPI(request, tipo);
  }

  // Crear servicios si se proporcionan
  for (const servicio of servicios) {
    await crearServicioAPI(request, servicio);
  }
}
