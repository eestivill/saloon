# Configuración de Pruebas E2E

## Instalación Inicial

### 1. Instalar Playwright

Las dependencias ya están instaladas en el proyecto. Si necesitas reinstalar:

```bash
npm install -D @playwright/test playwright
```

### 2. Instalar Navegadores

Playwright necesita descargar los navegadores para ejecutar las pruebas:

```bash
npx playwright install
```

Esto descargará Chromium, Firefox y WebKit.

Para instalar solo navegadores específicos:

```bash
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit
```

### 3. Verificar Instalación

Ejecuta el test de ejemplo para verificar que todo funciona:

```bash
npm run test:e2e
```

## Requisitos Previos

### Backend en Ejecución

Las pruebas E2E requieren que el backend esté ejecutándose en `http://localhost:8000`.

Desde el directorio `backend/`:

```bash
# Activar entorno virtual
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows

# Ejecutar servidor
uvicorn app.main:app --reload
```

### Frontend en Ejecución

El frontend se inicia automáticamente cuando ejecutas las pruebas E2E gracias a la configuración `webServer` en `playwright.config.ts`.

Si prefieres iniciarlo manualmente:

```bash
npm run dev
```

## Estructura de Archivos

```
frontend/
├── playwright.config.ts          # Configuración de Playwright
├── tests/
│   └── e2e/
│       ├── fixtures/             # Datos de prueba
│       │   └── testData.ts
│       ├── helpers/              # Funciones auxiliares
│       │   └── apiHelpers.ts
│       ├── example.spec.ts       # Test de ejemplo
│       ├── empleados.spec.ts     # Tests de empleados
│       ├── README.md             # Documentación de tests
│       └── SETUP.md              # Este archivo
└── package.json                  # Scripts de test
```

## Scripts Disponibles

### Ejecutar Tests

```bash
# Ejecutar todos los tests E2E
npm run test:e2e

# Ejecutar con interfaz gráfica
npm run test:e2e:ui

# Ejecutar en modo headed (ver navegador)
npm run test:e2e:headed

# Ejecutar en modo debug
npm run test:e2e:debug

# Ver reporte HTML
npm run test:e2e:report
```

### Ejecutar Tests Específicos

```bash
# Ejecutar un archivo específico
npx playwright test empleados.spec.ts

# Ejecutar un test específico
npx playwright test -g "debe crear un nuevo empleado"

# Ejecutar en un navegador específico
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project="Mobile Chrome"
```

## Configuración de Navegadores

Por defecto, los tests se ejecutan en:
- Desktop Chrome (Chromium)
- Desktop Firefox
- Desktop Safari (WebKit)
- Mobile Chrome (Pixel 5)
- Mobile Safari (iPhone 12)

Para ejecutar solo en navegadores específicos, edita `playwright.config.ts`:

```typescript
projects: [
  {
    name: 'chromium',
    use: { ...devices['Desktop Chrome'] },
  },
  // Comenta los navegadores que no quieras usar
],
```

## Configuración de CI/CD

### GitHub Actions

Ejemplo de configuración para GitHub Actions:

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Install Playwright Browsers
        run: |
          cd frontend
          npx playwright install --with-deps
      
      - name: Start Backend
        run: |
          cd backend
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          uvicorn app.main:app &
          sleep 5
      
      - name: Run E2E tests
        run: |
          cd frontend
          npm run test:e2e
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

## Solución de Problemas

### Error: "Browser not found"

Instala los navegadores:

```bash
npx playwright install
```

### Error: "Cannot connect to backend"

Verifica que el backend esté ejecutándose en `http://localhost:8000`:

```bash
curl http://localhost:8000/docs
```

### Error: "Port 5173 already in use"

El frontend ya está ejecutándose. Detén el proceso o usa la configuración `reuseExistingServer: true` en `playwright.config.ts`.

### Tests lentos

Reduce el número de navegadores en `playwright.config.ts` o ejecuta solo en Chromium:

```bash
npx playwright test --project=chromium
```

### Debugging

Para ver qué está pasando durante un test:

```bash
# Modo headed (ver navegador)
npm run test:e2e:headed

# Modo debug (paso a paso)
npm run test:e2e:debug

# Ver trace de un test fallido
npx playwright show-trace test-results/path-to-trace.zip
```

## Mejores Prácticas

1. **Limpiar datos entre tests**: Usa `beforeEach` para limpiar la base de datos
2. **Usar fixtures**: Reutiliza datos de prueba desde `fixtures/testData.ts`
3. **Selectores estables**: Usa `data-testid` o selectores por rol
4. **Tests independientes**: Cada test debe poder ejecutarse solo
5. **Esperas explícitas**: Usa `await expect().toBeVisible()` en lugar de `waitForTimeout`

## Recursos

- [Documentación de Playwright](https://playwright.dev)
- [Guía de Mejores Prácticas](https://playwright.dev/docs/best-practices)
- [API Reference](https://playwright.dev/docs/api/class-test)
- [Selectores](https://playwright.dev/docs/selectors)
- [Debugging](https://playwright.dev/docs/debug)
