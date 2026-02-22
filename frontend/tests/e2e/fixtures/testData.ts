/**
 * Fixtures de datos de prueba para tests E2E
 * Estos datos se utilizan para crear un estado consistente en las pruebas
 */

export const testEmpleados = [
  {
    id: 'E001',
    nombre: 'Juan Pérez',
  },
  {
    id: 'E002',
    nombre: 'María García',
  },
  {
    id: 'E003',
    nombre: 'Carlos López',
  },
];

export const testTiposServicios = [
  {
    nombre: 'Corte Básico',
    descripcion: 'Corte de cabello básico',
    porcentaje_comision: 40.0,
  },
  {
    nombre: 'Tinte Completo',
    descripcion: 'Tinte de cabello completo',
    porcentaje_comision: 35.0,
  },
  {
    nombre: 'Peinado',
    descripcion: 'Peinado para eventos',
    porcentaje_comision: 45.0,
  },
  {
    nombre: 'Tratamiento',
    descripcion: 'Tratamiento capilar',
    porcentaje_comision: 30.0,
  },
];

export const testServicios = [
  {
    fecha: '2024-01-15',
    empleado_id: 'E001',
    tipo_servicio: 'Corte Básico',
    precio: 25.0,
  },
  {
    fecha: '2024-01-16',
    empleado_id: 'E001',
    tipo_servicio: 'Tinte Completo',
    precio: 80.0,
  },
  {
    fecha: '2024-01-17',
    empleado_id: 'E002',
    tipo_servicio: 'Peinado',
    precio: 50.0,
  },
  {
    fecha: '2024-01-18',
    empleado_id: 'E002',
    tipo_servicio: 'Corte Básico',
    precio: 25.0,
  },
  {
    fecha: '2024-01-19',
    empleado_id: 'E003',
    tipo_servicio: 'Tratamiento',
    precio: 60.0,
  },
];

/**
 * Calcula la comisión esperada para un servicio
 */
export function calcularComisionEsperada(precio: number, porcentaje: number): number {
  return (precio * porcentaje) / 100;
}

/**
 * Formatea un número como moneda
 */
export function formatearMoneda(valor: number): string {
  return `$${valor.toFixed(2)}`;
}

/**
 * Genera un ID único para empleado
 */
export function generarIdEmpleado(): string {
  return `E${Date.now().toString().slice(-6)}`;
}

/**
 * Genera un nombre único para tipo de servicio
 */
export function generarNombreTipoServicio(): string {
  return `Servicio Test ${Date.now().toString().slice(-6)}`;
}
