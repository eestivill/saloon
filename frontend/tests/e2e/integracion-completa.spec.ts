import { test, expect } from '@playwright/test';

/**
 * Pruebas E2E de integración backend-frontend completa.
 * 
 * Verifica:
 * - CORS funciona correctamente desde el frontend
 * - Todas las llamadas API funcionan end-to-end
 * - Manejo de errores se muestra correctamente en UI
 * - Persistencia: datos persisten después de recargar la página
 */

test.describe('Integración Backend-Frontend Completa', () => {
  test.beforeEach(async ({ page }) => {
    // Navegar a la aplicación
    await page.goto('http://localhost:5173');
  });

  test('flujo completo: crear empleado, tipo de servicio, registrar servicio y verificar persistencia', async ({ page }) => {
    // 1. Crear empleado
    await page.click('text=Empleados');
    await page.click('text=Nuevo Empleado');
    
    await page.fill('input[name="id"]', 'E999');
    await page.fill('input[name="nombre"]', 'Test Usuario');
    await page.click('button:has-text("Guardar")');
    
    // Verificar que aparece en la lista
    await expect(page.locator('text=Test Usuario')).toBeVisible();
    
    // 2. Crear tipo de servicio
    await page.click('text=Tipos de Servicios');
    await page.click('text=Nuevo Tipo de Servicio');
    
    await page.fill('input[name="nombre"]', 'Test Servicio');
    await page.fill('input[name="descripcion"]', 'Servicio de prueba');
    await page.fill('input[name="porcentaje_comision"]', '45');
    await page.click('button:has-text("Guardar")');
    
    // Verificar que aparece en la lista
    await expect(page.locator('text=Test Servicio')).toBeVisible();
    await expect(page.locator('text=45%')).toBeVisible();
    
    // 3. Registrar servicio
    await page.click('text=Servicios');
    await page.click('text=Nuevo Servicio');
    
    // Seleccionar empleado
    await page.selectOption('select[name="empleado_id"]', 'E999');
    
    // Seleccionar tipo de servicio
    await page.selectOption('select[name="tipo_servicio"]', 'Test Servicio');
    
    // Ingresar fecha y precio
    await page.fill('input[name="fecha"]', '2024-01-15');
    await page.fill('input[name="precio"]', '100');
    
    await page.click('button:has-text("Guardar")');
    
    // Verificar que aparece en la lista
    await expect(page.locator('text=Test Usuario')).toBeVisible();
    await expect(page.locator('text=Test Servicio')).toBeVisible();
    await expect(page.locator('text=$100')).toBeVisible();
    
    // 4. Verificar persistencia: recargar página
    await page.reload();
    
    // Verificar que el servicio sigue ahí
    await expect(page.locator('text=Test Usuario')).toBeVisible();
    await expect(page.locator('text=Test Servicio')).toBeVisible();
    
    // 5. Verificar en reportes
    await page.click('text=Reportes');
    
    // Verificar ingresos
    await expect(page.locator('text=Ingresos')).toBeVisible();
    await expect(page.locator('text=$100')).toBeVisible();
    
    // Verificar pago de empleado
    await page.selectOption('select[name="empleado"]', 'E999');
    await expect(page.locator('text=$45')).toBeVisible(); // 45% de 100
  });

  test('manejo de errores: empleado duplicado muestra error en UI', async ({ page }) => {
    // Crear empleado
    await page.click('text=Empleados');
    await page.click('text=Nuevo Empleado');
    
    await page.fill('input[name="id"]', 'E888');
    await page.fill('input[name="nombre"]', 'Usuario Uno');
    await page.click('button:has-text("Guardar")');
    
    // Intentar crear empleado con mismo ID
    await page.click('text=Nuevo Empleado');
    await page.fill('input[name="id"]', 'E888');
    await page.fill('input[name="nombre"]', 'Usuario Dos');
    await page.click('button:has-text("Guardar")');
    
    // Verificar que se muestra mensaje de error
    await expect(page.locator('text=ya existe')).toBeVisible();
  });

  test('manejo de errores: porcentaje inválido muestra error en UI', async ({ page }) => {
    await page.click('text=Tipos de Servicios');
    await page.click('text=Nuevo Tipo de Servicio');
    
    await page.fill('input[name="nombre"]', 'Servicio Inválido');
    await page.fill('input[name="descripcion"]', 'Descripción');
    await page.fill('input[name="porcentaje_comision"]', '150'); // Inválido
    await page.click('button:has-text("Guardar")');
    
    // Verificar que se muestra mensaje de error
    await expect(page.locator('.error, .text-red-500')).toBeVisible();
  });

  test('manejo de errores: servicio con empleado inexistente muestra error', async ({ page }) => {
    // Crear tipo de servicio
    await page.click('text=Tipos de Servicios');
    await page.click('text=Nuevo Tipo de Servicio');
    
    await page.fill('input[name="nombre"]', 'Servicio Test');
    await page.fill('input[name="descripcion"]', 'Descripción');
    await page.fill('input[name="porcentaje_comision"]', '40');
    await page.click('button:has-text("Guardar")');
    
    // Intentar registrar servicio sin empleado
    await page.click('text=Servicios');
    await page.click('text=Nuevo Servicio');
    
    // No seleccionar empleado, solo llenar otros campos
    await page.selectOption('select[name="tipo_servicio"]', 'Servicio Test');
    await page.fill('input[name="fecha"]', '2024-01-15');
    await page.fill('input[name="precio"]', '100');
    await page.click('button:has-text("Guardar")');
    
    // Verificar que se muestra mensaje de error
    await expect(page.locator('.error, .text-red-500')).toBeVisible();
  });

  test('filtrado de servicios funciona correctamente', async ({ page }) => {
    // Setup: crear dos empleados y servicios
    await page.click('text=Empleados');
    
    // Empleado 1
    await page.click('text=Nuevo Empleado');
    await page.fill('input[name="id"]', 'E111');
    await page.fill('input[name="nombre"]', 'Empleado Uno');
    await page.click('button:has-text("Guardar")');
    
    // Empleado 2
    await page.click('text=Nuevo Empleado');
    await page.fill('input[name="id"]', 'E222');
    await page.fill('input[name="nombre"]', 'Empleado Dos');
    await page.click('button:has-text("Guardar")');
    
    // Crear tipo de servicio
    await page.click('text=Tipos de Servicios');
    await page.click('text=Nuevo Tipo de Servicio');
    await page.fill('input[name="nombre"]', 'Corte');
    await page.fill('input[name="descripcion"]', 'Corte de cabello');
    await page.fill('input[name="porcentaje_comision"]', '40');
    await page.click('button:has-text("Guardar")');
    
    // Registrar servicios para ambos empleados
    await page.click('text=Servicios');
    
    // Servicio para E111
    await page.click('text=Nuevo Servicio');
    await page.selectOption('select[name="empleado_id"]', 'E111');
    await page.selectOption('select[name="tipo_servicio"]', 'Corte');
    await page.fill('input[name="fecha"]', '2024-01-15');
    await page.fill('input[name="precio"]', '50');
    await page.click('button:has-text("Guardar")');
    
    // Servicio para E222
    await page.click('text=Nuevo Servicio');
    await page.selectOption('select[name="empleado_id"]', 'E222');
    await page.selectOption('select[name="tipo_servicio"]', 'Corte');
    await page.fill('input[name="fecha"]', '2024-01-16');
    await page.fill('input[name="precio"]', '60');
    await page.click('button:has-text("Guardar")');
    
    // Filtrar por empleado E111
    await page.selectOption('select[name="filtro_empleado"]', 'E111');
    
    // Verificar que solo aparece el servicio de E111
    await expect(page.locator('text=Empleado Uno')).toBeVisible();
    await expect(page.locator('text=Empleado Dos')).not.toBeVisible();
  });

  test('persistencia después de cerrar y reabrir navegador', async ({ page, context }) => {
    // Crear datos
    await page.click('text=Empleados');
    await page.click('text=Nuevo Empleado');
    await page.fill('input[name="id"]', 'E777');
    await page.fill('input[name="nombre"]', 'Persistente');
    await page.click('button:has-text("Guardar")');
    
    // Cerrar página y crear nueva (simula cerrar navegador)
    await page.close();
    
    // Abrir nueva página
    const newPage = await context.newPage();
    await newPage.goto('http://localhost:5173');
    
    // Verificar que los datos persisten
    await newPage.click('text=Empleados');
    await expect(newPage.locator('text=Persistente')).toBeVisible();
  });

  test('CORS permite llamadas desde frontend', async ({ page }) => {
    // Interceptar llamadas de red
    let corsError = false;
    
    page.on('console', msg => {
      if (msg.type() === 'error' && msg.text().includes('CORS')) {
        corsError = true;
      }
    });
    
    // Hacer una llamada API
    await page.click('text=Empleados');
    
    // Esperar a que cargue
    await page.waitForTimeout(1000);
    
    // Verificar que no hubo errores CORS
    expect(corsError).toBe(false);
  });

  test('ordenamiento de servicios por fecha descendente', async ({ page }) => {
    // Setup
    await page.click('text=Empleados');
    await page.click('text=Nuevo Empleado');
    await page.fill('input[name="id"]', 'E555');
    await page.fill('input[name="nombre"]', 'Test');
    await page.click('button:has-text("Guardar")');
    
    await page.click('text=Tipos de Servicios');
    await page.click('text=Nuevo Tipo de Servicio');
    await page.fill('input[name="nombre"]', 'Corte');
    await page.fill('input[name="descripcion"]', 'Corte');
    await page.fill('input[name="porcentaje_comision"]', '40');
    await page.click('button:has-text("Guardar")');
    
    // Registrar servicios en orden no secuencial
    await page.click('text=Servicios');
    
    // Servicio 1: 2024-01-15
    await page.click('text=Nuevo Servicio');
    await page.selectOption('select[name="empleado_id"]', 'E555');
    await page.selectOption('select[name="tipo_servicio"]', 'Corte');
    await page.fill('input[name="fecha"]', '2024-01-15');
    await page.fill('input[name="precio"]', '50');
    await page.click('button:has-text("Guardar")');
    
    // Servicio 2: 2024-01-20 (más reciente)
    await page.click('text=Nuevo Servicio');
    await page.selectOption('select[name="empleado_id"]', 'E555');
    await page.selectOption('select[name="tipo_servicio"]', 'Corte');
    await page.fill('input[name="fecha"]', '2024-01-20');
    await page.fill('input[name="precio"]', '60');
    await page.click('button:has-text("Guardar")');
    
    // Servicio 3: 2024-01-10 (más antiguo)
    await page.click('text=Nuevo Servicio');
    await page.selectOption('select[name="empleado_id"]', 'E555');
    await page.selectOption('select[name="tipo_servicio"]', 'Corte');
    await page.fill('input[name="fecha"]', '2024-01-10');
    await page.fill('input[name="precio"]', '40');
    await page.click('button:has-text("Guardar")');
    
    // Verificar que están ordenados por fecha descendente
    const servicios = await page.locator('.servicio-card, [data-testid="servicio"]').all();
    
    // El primero debe ser 2024-01-20
    await expect(servicios[0]).toContainText('2024-01-20');
    
    // El último debe ser 2024-01-10
    await expect(servicios[servicios.length - 1]).toContainText('2024-01-10');
  });

  test('cálculo de comisiones es correcto end-to-end', async ({ page }) => {
    // Setup
    await page.click('text=Empleados');
    await page.click('text=Nuevo Empleado');
    await page.fill('input[name="id"]', 'E333');
    await page.fill('input[name="nombre"]', 'Test Comisión');
    await page.click('button:has-text("Guardar")');
    
    await page.click('text=Tipos de Servicios');
    await page.click('text=Nuevo Tipo de Servicio');
    await page.fill('input[name="nombre"]', 'Servicio 50%');
    await page.fill('input[name="descripcion"]', 'Servicio con 50% comisión');
    await page.fill('input[name="porcentaje_comision"]', '50');
    await page.click('button:has-text("Guardar")');
    
    // Registrar servicio de $200
    await page.click('text=Servicios');
    await page.click('text=Nuevo Servicio');
    await page.selectOption('select[name="empleado_id"]', 'E333');
    await page.selectOption('select[name="tipo_servicio"]', 'Servicio 50%');
    await page.fill('input[name="fecha"]', '2024-01-15');
    await page.fill('input[name="precio"]', '200');
    await page.click('button:has-text("Guardar")');
    
    // Verificar comisión en la lista de servicios
    await expect(page.locator('text=$100')).toBeVisible(); // 50% de 200
    
    // Verificar en reportes
    await page.click('text=Reportes');
    await page.selectOption('select[name="empleado"]', 'E333');
    
    // Debe mostrar $100 de comisión
    await expect(page.locator('text=$100')).toBeVisible();
  });
});
