# Pruebas E2E con Playwright

Este directorio contiene las pruebas end-to-end (E2E) del sistema de gestión de salón de peluquería.

## Estructura

```
tests/e2e/
├── fixtures/          # Datos de prueba reutilizables
│   └── testData.ts    # Fixtures de empleados, servicios, etc.
├── helpers/           # Funciones auxiliares
│   └── apiHelpers.ts  # Helpers para interactuar con la API
├── example.spec.ts    # Test de ejemplo
└── README.md          # Este archivo
```

## Configuración

Las pruebas E2E están configuradas con Playwright y se ejecutan en múltiples navegadores:
- Chromium (Chrome/Edge)
- Firefox
- WebKit (Safari)
- Mobile Chrome (Pixel 5)
- Mobile Safari (iPhone 12)

## Comandos

### Ejecutar todas las pruebas E2E
```bash
npm run test:e2e
```

### Ejecutar pruebas con interfaz gráfica
```bash
npm run test:e2e:ui
```

### Ejecutar pruebas en modo headed (ver el navegador)
```bash
npm run test:e2e:headed
```

### Ejecutar pruebas en modo debug
```bash
npm run test:e2e:debug
```

### Ver reporte de pruebas
```bash
npm run test:e2e:report
```

### Ejecutar pruebas en un navegador específico
```bash
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
npx playwright test --project="Mobile Chrome"
```

## Escribir Pruebas

### Estructura básica de un test

```typescript
import { test, expect } from '@playwright/test';

test.describe('Nombre del módulo', () => {
  test('debe hacer algo específico', async ({ page }) => {
    // Navegar a la página
    await page.goto('/ruta');
    
    // Interactuar con elementos
    await page.click('button');
    await page.fill('input[name="campo"]', 'valor');
    
    // Verificar resultados
    await expect(page.locator('selector')).toBeVisible();
    await expect(page.locator('selector')).toHaveText('texto esperado');
  });
});
```

### Usar fixtures de datos

```typescript
import { testEmpleados, testTiposServicios } from './fixtures/testData';

test('debe crear un empleado', async ({ page }) => {
  const empleado = testEmpleados[0];
  
  await page.goto('/empleados');
  await page.click('text=Nuevo Empleado');
  await page.fill('input[name="id"]', empleado.id);
  await page.fill('input[name="nombre"]', empleado.nombre);
  await page.click('button[type="submit"]');
  
  await expect(page.locator(`text=${empleado.nombre}`)).toBeVisible();
});
```

### Configurar datos de prueba con la API

```typescript
import { test, expect } from '@playwright/test';
import { configurarDatosPrueba, limpiarBaseDatos } from './helpers/apiHelpers';
import { testEmpleados, testTiposServicios } from './fixtures/testData';

test.describe('Servicios', () => {
  test.beforeEach(async ({ request }) => {
    // Limpiar base de datos antes de cada test
    await limpiarBaseDatos(request);
    
    // Configurar datos de prueba
    await configurarDatosPrueba(request, testEmpleados, testTiposServicios);
  });

  test('debe registrar un servicio', async ({ page }) => {
    await page.goto('/servicios');
    // ... resto del test
  });
});
```

## Selectores Recomendados

### Por rol (preferido)
```typescript
await page.getByRole('button', { name: 'Guardar' });
await page.getByRole('textbox', { name: 'Nombre' });
```

### Por texto
```typescript
await page.getByText('Empleados');
await page.getByLabel('ID del empleado');
```

### Por atributo de test
```typescript
await page.getByTestId('empleado-card');
```

### Por selector CSS (último recurso)
```typescript
await page.locator('.empleado-card');
await page.locator('input[name="nombre"]');
```

## Buenas Prácticas

1. **Aislar tests**: Cada test debe ser independiente y no depender del estado de otros tests
2. **Limpiar datos**: Usar `beforeEach` para limpiar y configurar datos de prueba
3. **Esperar elementos**: Usar `await expect().toBeVisible()` en lugar de `waitForTimeout`
4. **Selectores estables**: Preferir selectores por rol o texto sobre selectores CSS
5. **Tests atómicos**: Cada test debe verificar una sola funcionalidad
6. **Nombres descriptivos**: Los nombres de tests deben describir claramente qué se está probando

## Debugging

### Ver el navegador durante la ejecución
```bash
npm run test:e2e:headed
```

### Modo debug paso a paso
```bash
npm run test:e2e:debug
```

### Capturar screenshots
Los screenshots se capturan automáticamente en fallos y se guardan en `test-results/`

### Ver traces
Los traces se capturan en el primer reintento de un test fallido:
```bash
npx playwright show-trace test-results/path-to-trace.zip
```

## CI/CD

En entornos de CI, las pruebas se ejecutan con:
- 2 reintentos automáticos en caso de fallo
- 1 worker (ejecución secuencial)
- Capturas de video y screenshots en fallos

## Requisitos

- Node.js 18+
- Backend ejecutándose en `http://localhost:8000`
- Frontend ejecutándose en `http://localhost:5173` (se inicia automáticamente)

## Recursos

- [Documentación de Playwright](https://playwright.dev)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [API Reference](https://playwright.dev/docs/api/class-test)
