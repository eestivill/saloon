import { test, expect } from '@playwright/test';
import { limpiarBaseDatos } from './helpers/apiHelpers';
import { generarIdEmpleado, generarNombreTipoServicio } from './fixtures/testData';

/**
 * Tests E2E para el flujo completo del sistema
 * Valida: Todos los requisitos (flujo completo)
 */
test.describe('Flujo Completo del Sistema', () => {
  test.beforeEach(async ({ request }) => {
    // Limpiar base de datos antes de cada test
    await limpiarBaseDatos(request);
  });

  test('flujo completo: crear empleado, tipo de servicio, registrar servicio y ver reportes', async ({ page }) => {
    const empleadoId = generarIdEmpleado();
    const empleadoNombre = 'Juan Pérez';
    const tipoServicioNombre = generarNombreTipoServicio();
    const porcentajeComision = 40;
    const precioServicio = 100;

    // 1. Crear empleado
    await page.goto('/empleados');
    await page.click('text=Nuevo Empleado');
    await page.fill('input[name="id"]', empleadoId);
    await page.fill('input[name="nombre"]', empleadoNombre);
    await page.click('button[type="submit"]');
    await expect(page.locator(`text=${empleadoNombre}`)).toBeVisible();

    // 2. Crear tipo de servicio
    await page.goto('/tipos-servicios');
    await page.click('text=Nuevo Tipo');
    await page.fill('input[name="nombre"]', tipoServicioNombre);
    await page.fill('input[name="descripcion"]', 'Descripción del servicio');
    await page.fill('input[name="porcentaje_comision"]', porcentajeComision.toString());
    await page.click('button[type="submit"]');
    await expect(page.locator(`text=${tipoServicioNombre}`)).toBeVisible();

    // 3. Registrar servicio
    await page.goto('/servicios');
    await page.click('text=Nuevo Servicio');
    
    // Seleccionar empleado
    await page.selectOption('select[name="empleado_id"]', empleadoId);
    
    // Seleccionar tipo de servicio
    await page.selectOption('select[name="tipo_servicio"]', tipoServicioNombre);
    
    // Ingresar fecha y precio
    await page.fill('input[name="fecha"]', '2024-01-15');
    await page.fill('input[name="precio"]', precioServicio.toString());
    
    await page.click('button[type="submit"]');
    
    // Verificar que el servicio aparece en la lista
    await expect(page.locator(`text=${empleadoNombre}`)).toBeVisible();
    await expect(page.locator(`text=${tipoServicioNombre}`)).toBeVisible();
    await expect(page.locator(`text=$${precioServicio}`)).toBeVisible();

    // 4. Ver reportes de ingresos
    await page.goto('/reportes');
    await page.click('text=Ingresos');
    
    // Verificar que muestra el ingreso total
    await expect(page.locator(`text=$${precioServicio}`)).toBeVisible();

    // 5. Ver reporte de pago de empleado
    await page.click('text=Pago Empleado');
    await page.selectOption('select[name="empleado_id"]', empleadoId);
    
    // Calcular comisión esperada
    const comisionEsperada = (precioServicio * porcentajeComision) / 100;
    
    // Verificar que muestra la comisión correcta
    await expect(page.locator(`text=$${comisionEsperada}`)).toBeVisible();
  });

  test('debe validar formularios correctamente', async ({ page }) => {
    // Test de validación de empleado
    await page.goto('/empleados');
    await page.click('text=Nuevo Empleado');
    await page.click('button[type="submit"]');
    
    // HTML5 validation debe prevenir el envío
    await expect(page.locator('input[name="id"]')).toBeVisible();

    // Test de validación de tipo de servicio
    await page.goto('/tipos-servicios');
    await page.click('text=Nuevo Tipo');
    
    // Intentar con porcentaje inválido
    await page.fill('input[name="nombre"]', 'Test');
    await page.fill('input[name="descripcion"]', 'Test');
    await page.fill('input[name="porcentaje_comision"]', '150'); // Inválido
    await page.click('button[type="submit"]');
    
    // Debe mostrar error
    await expect(page.locator('text=/porcentaje/i')).toBeVisible();
  });

  test('debe filtrar servicios por empleado', async ({ page, request }) => {
    // Crear datos de prueba
    const empleado1Id = generarIdEmpleado();
    const empleado2Id = generarIdEmpleado();
    const tipoServicio = generarNombreTipoServicio();

    await request.post('http://localhost:8000/api/empleados', {
      data: { id: empleado1Id, nombre: 'Empleado 1' },
    });
    await request.post('http://localhost:8000/api/empleados', {
      data: { id: empleado2Id, nombre: 'Empleado 2' },
    });
    await request.post('http://localhost:8000/api/tipos-servicios', {
      data: {
        nombre: tipoServicio,
        descripcion: 'Test',
        porcentaje_comision: 40,
      },
    });

    // Crear servicios para ambos empleados
    await request.post('http://localhost:8000/api/servicios', {
      data: {
        fecha: '2024-01-15',
        empleado_id: empleado1Id,
        tipo_servicio: tipoServicio,
        precio: 50,
      },
    });
    await request.post('http://localhost:8000/api/servicios', {
      data: {
        fecha: '2024-01-16',
        empleado_id: empleado2Id,
        tipo_servicio: tipoServicio,
        precio: 75,
      },
    });

    // Ir a servicios y filtrar
    await page.goto('/servicios');
    
    // Filtrar por empleado 1
    await page.selectOption('select[name="filtro_empleado"]', empleado1Id);
    await page.click('button:has-text("Filtrar")');
    
    // Verificar que solo aparece el servicio del empleado 1
    await expect(page.locator('text=Empleado 1')).toBeVisible();
    await expect(page.locator('text=$50')).toBeVisible();
    await expect(page.locator('text=$75')).not.toBeVisible();
  });

  test('debe filtrar servicios por rango de fechas', async ({ page, request }) => {
    const empleadoId = generarIdEmpleado();
    const tipoServicio = generarNombreTipoServicio();

    await request.post('http://localhost:8000/api/empleados', {
      data: { id: empleadoId, nombre: 'Test Empleado' },
    });
    await request.post('http://localhost:8000/api/tipos-servicios', {
      data: {
        nombre: tipoServicio,
        descripcion: 'Test',
        porcentaje_comision: 40,
      },
    });

    // Crear servicios en diferentes fechas
    await request.post('http://localhost:8000/api/servicios', {
      data: {
        fecha: '2024-01-10',
        empleado_id: empleadoId,
        tipo_servicio: tipoServicio,
        precio: 50,
      },
    });
    await request.post('http://localhost:8000/api/servicios', {
      data: {
        fecha: '2024-01-20',
        empleado_id: empleadoId,
        tipo_servicio: tipoServicio,
        precio: 75,
      },
    });

    await page.goto('/servicios');
    
    // Filtrar por rango de fechas
    await page.fill('input[name="fecha_inicio"]', '2024-01-15');
    await page.fill('input[name="fecha_fin"]', '2024-01-25');
    await page.click('button:has-text("Filtrar")');
    
    // Solo debe aparecer el servicio del 20 de enero
    await expect(page.locator('text=$75')).toBeVisible();
    await expect(page.locator('text=$50')).not.toBeVisible();
  });
});

/**
 * Tests de diseño responsive
 */
test.describe('Diseño Responsive', () => {
  test.beforeEach(async ({ request }) => {
    await limpiarBaseDatos(request);
  });

  test('debe funcionar correctamente en móvil (320px)', async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 568 });
    
    await page.goto('/');
    
    // Verificar que la navegación es accesible
    await expect(page.locator('nav')).toBeVisible();
    
    // Verificar que los botones son táctiles
    await page.goto('/empleados');
    const button = page.locator('text=Nuevo Empleado').first();
    await expect(button).toBeVisible();
    
    const box = await button.boundingBox();
    expect(box?.height).toBeGreaterThan(40); // Altura mínima para touch
  });

  test('debe funcionar correctamente en tablet (768px)', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    
    await page.goto('/empleados');
    
    // Verificar que el layout se adapta
    await expect(page.locator('nav')).toBeVisible();
  });

  test('debe funcionar correctamente en desktop (1024px)', async ({ page }) => {
    await page.setViewportSize({ width: 1024, height: 768 });
    
    await page.goto('/empleados');
    
    // Verificar que el layout se adapta
    await expect(page.locator('nav')).toBeVisible();
  });
});
