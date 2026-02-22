import { test, expect } from '@playwright/test';

/**
 * Test de ejemplo para verificar que Playwright está configurado correctamente
 */
test.describe('Configuración de Playwright', () => {
  test('debe cargar la aplicación correctamente', async ({ page }) => {
    await page.goto('/');
    
    // Verificar que la página carga
    await expect(page).toHaveTitle(/Salón/i);
  });

  test('debe tener navegación funcional', async ({ page }) => {
    await page.goto('/');
    
    // Verificar que existen enlaces de navegación
    const nav = page.locator('nav');
    await expect(nav).toBeVisible();
  });
});
