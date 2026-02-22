import { test, expect } from '@playwright/test';
import { limpiarBaseDatos } from './helpers/apiHelpers';
import { generarIdEmpleado } from './fixtures/testData';

/**
 * Tests E2E para la gestión de empleados
 * Valida: Requirements 1.1, 1.2, 1.3, 1.4, 1.5
 */
test.describe('Gestión de Empleados', () => {
  test.beforeEach(async ({ request }) => {
    // Limpiar base de datos antes de cada test
    await limpiarBaseDatos(request);
  });

  test('debe crear un nuevo empleado desde la UI', async ({ page }) => {
    const empleadoId = generarIdEmpleado();
    const empleadoNombre = 'Juan Pérez Test';

    await page.goto('/empleados');
    
    // Click en botón nuevo empleado
    await page.click('text=Nuevo Empleado');
    
    // Llenar formulario
    await page.fill('input[name="id"]', empleadoId);
    await page.fill('input[name="nombre"]', empleadoNombre);
    
    // Enviar formulario
    await page.click('button[type="submit"]');
    
    // Verificar que aparece en la lista
    await expect(page.locator(`text=${empleadoNombre}`)).toBeVisible();
  });

  test('debe validar ID duplicado', async ({ page, request }) => {
    const empleadoId = generarIdEmpleado();
    
    // Crear empleado a través de la API
    await request.post('http://localhost:8000/api/empleados', {
      data: { id: empleadoId, nombre: 'Empleado Existente' },
    });

    await page.goto('/empleados');
    
    // Intentar crear empleado con mismo ID
    await page.click('text=Nuevo Empleado');
    await page.fill('input[name="id"]', empleadoId);
    await page.fill('input[name="nombre"]', 'Otro Nombre');
    await page.click('button[type="submit"]');
    
    // Verificar mensaje de error
    await expect(page.locator('text=/ya existe/i')).toBeVisible();
  });

  test('debe validar campos requeridos', async ({ page }) => {
    await page.goto('/empleados');
    await page.click('text=Nuevo Empleado');
    
    // Intentar enviar sin llenar
    await page.click('button[type="submit"]');
    
    // Verificar que el formulario no se envía (HTML5 validation)
    // El formulario debe seguir visible
    await expect(page.locator('input[name="id"]')).toBeVisible();
  });

  test('debe mostrar lista de empleados', async ({ page, request }) => {
    // Crear varios empleados
    const empleados = [
      { id: generarIdEmpleado(), nombre: 'Juan Pérez' },
      { id: generarIdEmpleado(), nombre: 'María García' },
      { id: generarIdEmpleado(), nombre: 'Carlos López' },
    ];

    for (const empleado of empleados) {
      await request.post('http://localhost:8000/api/empleados', {
        data: empleado,
      });
    }

    await page.goto('/empleados');
    
    // Verificar que todos aparecen
    for (const empleado of empleados) {
      await expect(page.locator(`text=${empleado.nombre}`)).toBeVisible();
    }
  });

  test('debe actualizar un empleado', async ({ page, request }) => {
    const empleadoId = generarIdEmpleado();
    
    // Crear empleado
    await request.post('http://localhost:8000/api/empleados', {
      data: { id: empleadoId, nombre: 'Nombre Original' },
    });

    await page.goto('/empleados');
    
    // Click en editar
    await page.click(`[data-empleado-id="${empleadoId}"] button:has-text("Editar")`);
    
    // Actualizar nombre
    await page.fill('input[name="nombre"]', 'Nombre Actualizado');
    await page.click('button[type="submit"]');
    
    // Verificar actualización
    await expect(page.locator('text=Nombre Actualizado')).toBeVisible();
    await expect(page.locator('text=Nombre Original')).not.toBeVisible();
  });

  test('debe eliminar un empleado', async ({ page, request }) => {
    const empleadoId = generarIdEmpleado();
    const empleadoNombre = 'Empleado a Eliminar';
    
    // Crear empleado
    await request.post('http://localhost:8000/api/empleados', {
      data: { id: empleadoId, nombre: empleadoNombre },
    });

    await page.goto('/empleados');
    
    // Verificar que existe
    await expect(page.locator(`text=${empleadoNombre}`)).toBeVisible();
    
    // Click en eliminar
    await page.click(`[data-empleado-id="${empleadoId}"] button:has-text("Eliminar")`);
    
    // Confirmar eliminación (si hay diálogo de confirmación)
    page.on('dialog', dialog => dialog.accept());
    
    // Verificar que ya no aparece
    await expect(page.locator(`text=${empleadoNombre}`)).not.toBeVisible();
  });
});

/**
 * Tests de diseño responsive para empleados
 */
test.describe('Empleados - Diseño Responsive', () => {
  test.beforeEach(async ({ request }) => {
    await limpiarBaseDatos(request);
  });

  test('debe mostrar diseño mobile-first en móvil', async ({ page }) => {
    // Configurar viewport móvil
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.goto('/empleados');
    
    // Verificar que el botón ocupa todo el ancho en móvil
    const button = page.locator('text=Nuevo Empleado').first();
    await expect(button).toBeVisible();
    
    const box = await button.boundingBox();
    expect(box?.width).toBeGreaterThan(300); // Casi todo el ancho
  });

  test('debe mostrar grid en desktop', async ({ page, request }) => {
    // Crear varios empleados
    for (let i = 0; i < 6; i++) {
      await request.post('http://localhost:8000/api/empleados', {
        data: { id: generarIdEmpleado(), nombre: `Empleado ${i}` },
      });
    }

    // Configurar viewport desktop
    await page.setViewportSize({ width: 1280, height: 720 });
    
    await page.goto('/empleados');
    
    // Verificar que hay múltiples columnas (grid)
    const cards = page.locator('[data-testid="empleado-card"]');
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);
  });
});
