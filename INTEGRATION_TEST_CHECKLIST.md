# Checklist de Pruebas de Integración Backend-Frontend

Este documento proporciona una lista de verificación manual para probar la integración completa entre el backend y el frontend del sistema de gestión de salón de peluquería.

## Requisitos Previos

- [ ] Backend corriendo en `http://localhost:8000`
- [ ] Frontend corriendo en `http://localhost:5173`
- [ ] Base de datos SQLite inicializada

## 1. Verificación de CORS

### Prueba Manual
1. Abrir DevTools del navegador (F12)
2. Ir a la pestaña Network
3. Navegar a `http://localhost:5173`
4. Hacer clic en "Empleados"
5. Verificar en Network que las llamadas a `http://localhost:8000/api/empleados` tienen:
   - Status: 200 OK
   - Response Headers incluyen:
     - `access-control-allow-origin: http://localhost:5173`
     - `access-control-allow-credentials: true`

### Resultado Esperado
✅ No hay errores CORS en la consola
✅ Las llamadas API se completan exitosamente
✅ Los headers CORS están presentes

---

## 2. Pruebas de Endpoints de Empleados

### 2.1 Crear Empleado
1. Navegar a "Empleados"
2. Hacer clic en "Nuevo Empleado"
3. Ingresar:
   - ID: `E001`
   - Nombre: `Juan Pérez`
4. Hacer clic en "Guardar"

**Resultado Esperado:**
- ✅ Empleado aparece en la lista
- ✅ No hay errores en consola
- ✅ Mensaje de éxito visible

### 2.2 Listar Empleados
1. Navegar a "Empleados"
2. Verificar que se muestra la lista de empleados

**Resultado Esperado:**
- ✅ Lista carga correctamente
- ✅ Muestra todos los empleados creados
- ✅ Spinner de carga aparece brevemente

### 2.3 Actualizar Empleado
1. En la lista de empleados, hacer clic en "Editar" para E001
2. Cambiar nombre a `Juan Carlos Pérez`
3. Guardar

**Resultado Esperado:**
- ✅ Nombre se actualiza en la lista
- ✅ Cambio persiste al recargar

### 2.4 Eliminar Empleado
1. Hacer clic en "Eliminar" para un empleado
2. Confirmar eliminación

**Resultado Esperado:**
- ✅ Empleado desaparece de la lista
- ✅ No aparece al recargar la página

### 2.5 Error: Empleado Duplicado
1. Crear empleado con ID `E002`
2. Intentar crear otro empleado con ID `E002`

**Resultado Esperado:**
- ✅ Muestra mensaje de error "ya existe"
- ✅ Status code 409 en Network tab
- ✅ Primer empleado no se modifica

---

## 3. Pruebas de Endpoints de Tipos de Servicios

### 3.1 Crear Tipo de Servicio
1. Navegar a "Tipos de Servicios"
2. Hacer clic en "Nuevo Tipo de Servicio"
3. Ingresar:
   - Nombre: `Corte Básico`
   - Descripción: `Corte de cabello básico`
   - Porcentaje: `40`
4. Guardar

**Resultado Esperado:**
- ✅ Tipo de servicio aparece en la lista
- ✅ Muestra 40% correctamente

### 3.2 Error: Porcentaje Inválido
1. Intentar crear tipo de servicio con porcentaje `150`

**Resultado Esperado:**
- ✅ Muestra mensaje de error de validación
- ✅ No se crea el tipo de servicio
- ✅ Status code 400 o 422 en Network

### 3.3 Actualizar Tipo de Servicio
1. Editar "Corte Básico"
2. Cambiar porcentaje a `45`
3. Guardar

**Resultado Esperado:**
- ✅ Porcentaje se actualiza a 45%
- ✅ Cambio persiste al recargar

---

## 4. Pruebas de Endpoints de Servicios

### 4.1 Registrar Servicio
1. Navegar a "Servicios"
2. Hacer clic en "Nuevo Servicio"
3. Seleccionar:
   - Empleado: `E001`
   - Tipo: `Corte Básico`
   - Fecha: `2024-01-15`
   - Precio: `100`
4. Guardar

**Resultado Esperado:**
- ✅ Servicio aparece en la lista
- ✅ Comisión calculada correctamente (40% de 100 = $40)
- ✅ Muestra empleado y tipo de servicio

### 4.2 Error: Empleado Inexistente
1. Intentar registrar servicio (manipulando el select en DevTools para usar ID inexistente)

**Resultado Esperado:**
- ✅ Muestra error "no encontrado"
- ✅ Status code 404 en Network

### 4.3 Filtrar Servicios por Empleado
1. Crear servicios para diferentes empleados
2. Usar filtro de empleado
3. Seleccionar un empleado específico

**Resultado Esperado:**
- ✅ Solo muestra servicios del empleado seleccionado
- ✅ Filtro se aplica correctamente

### 4.4 Filtrar Servicios por Fecha
1. Crear servicios en diferentes fechas
2. Usar filtros de fecha inicio y fin
3. Aplicar filtro

**Resultado Esperado:**
- ✅ Solo muestra servicios en el rango de fechas
- ✅ Fechas fuera del rango no aparecen

### 4.5 Ordenamiento por Fecha
1. Crear servicios en orden no secuencial:
   - 2024-01-15
   - 2024-01-20
   - 2024-01-10
2. Ver lista de servicios

**Resultado Esperado:**
- ✅ Servicios ordenados descendente (más reciente primero)
- ✅ Orden: 2024-01-20, 2024-01-15, 2024-01-10

---

## 5. Pruebas de Reportes

### 5.1 Calcular Ingresos
1. Navegar a "Reportes"
2. Ver sección de Ingresos
3. Verificar total

**Resultado Esperado:**
- ✅ Muestra suma correcta de todos los servicios
- ✅ Formato monetario correcto ($XXX.XX)

### 5.2 Calcular Ingresos con Filtro de Fechas
1. Aplicar filtro de fechas
2. Verificar total

**Resultado Esperado:**
- ✅ Solo suma servicios en el rango
- ✅ Total cambia al cambiar fechas

### 5.3 Calcular Beneficios
1. Ver sección de Beneficios
2. Verificar cálculo

**Resultado Esperado:**
- ✅ Muestra Ingresos totales
- ✅ Muestra Comisiones totales
- ✅ Muestra Beneficios = Ingresos - Comisiones
- ✅ Cálculo es correcto

### 5.4 Calcular Pago de Empleado
1. Seleccionar un empleado
2. Ver desglose de pago

**Resultado Esperado:**
- ✅ Muestra lista de servicios del empleado
- ✅ Muestra comisión por cada servicio
- ✅ Total es suma correcta de comisiones
- ✅ Formato monetario correcto

---

## 6. Pruebas de Persistencia

### 6.1 Persistencia Básica
1. Crear un empleado
2. Recargar la página (F5)
3. Verificar que el empleado sigue ahí

**Resultado Esperado:**
- ✅ Datos persisten después de recargar
- ✅ No se pierden datos

### 6.2 Persistencia de Servicios con Comisión
1. Registrar un servicio
2. Recargar la página
3. Verificar servicio y comisión

**Resultado Esperado:**
- ✅ Servicio persiste con comisión calculada
- ✅ Comisión no se recalcula (mantiene valor original)

### 6.3 Persistencia Después de Cerrar Navegador
1. Crear datos
2. Cerrar navegador completamente
3. Abrir navegador y volver a la aplicación

**Resultado Esperado:**
- ✅ Todos los datos persisten
- ✅ Base de datos SQLite mantiene integridad

### 6.4 Actualización de Tipo de Servicio No Afecta Servicios Existentes
1. Crear tipo de servicio con 40% comisión
2. Registrar servicio de $100 (comisión = $40)
3. Actualizar tipo de servicio a 50% comisión
4. Verificar servicio existente

**Resultado Esperado:**
- ✅ Servicio existente mantiene comisión de $40
- ✅ Nuevos servicios usan 50% comisión

---

## 7. Pruebas de Manejo de Errores End-to-End

### 7.1 Error de Validación en UI
1. Intentar crear empleado sin nombre
2. Intentar crear tipo con porcentaje negativo
3. Intentar crear servicio con precio 0

**Resultado Esperado:**
- ✅ Validación del formulario previene envío
- ✅ Mensajes de error claros en UI
- ✅ Campos inválidos resaltados en rojo

### 7.2 Error 404 en UI
1. Intentar acceder a empleado inexistente (manipular URL)

**Resultado Esperado:**
- ✅ Muestra mensaje "no encontrado"
- ✅ No rompe la aplicación

### 7.3 Error 409 en UI
1. Crear empleado duplicado

**Resultado Esperado:**
- ✅ Muestra mensaje "ya existe"
- ✅ Permite corregir y reintentar

### 7.4 Error de Conexión
1. Detener el backend
2. Intentar cargar empleados

**Resultado Esperado:**
- ✅ Muestra mensaje "no se pudo conectar con el servidor"
- ✅ No rompe la aplicación
- ✅ Permite reintentar cuando backend vuelve

---

## 8. Pruebas de Diseño Responsive

### 8.1 Vista Móvil (320px)
1. Abrir DevTools
2. Cambiar a vista móvil (iPhone SE)
3. Navegar por todas las secciones

**Resultado Esperado:**
- ✅ Menú hamburger funciona
- ✅ Formularios son usables
- ✅ Botones ocupan ancho completo
- ✅ Tablas/listas son scrolleables

### 8.2 Vista Tablet (768px)
1. Cambiar a vista tablet (iPad)
2. Verificar layout

**Resultado Esperado:**
- ✅ Grid de 2 columnas en listas
- ✅ Navegación visible
- ✅ Espaciado apropiado

### 8.3 Vista Desktop (1024px+)
1. Cambiar a vista desktop
2. Verificar layout

**Resultado Esperado:**
- ✅ Grid de 3 columnas en listas
- ✅ Navegación horizontal
- ✅ Uso eficiente del espacio

---

## 9. Pruebas de Performance

### 9.1 Tiempo de Carga
1. Abrir Network tab
2. Recargar página
3. Medir tiempo de carga

**Resultado Esperado:**
- ✅ Página carga en < 2 segundos
- ✅ API responde en < 500ms

### 9.2 Carga con Muchos Datos
1. Crear 50+ servicios
2. Navegar a lista de servicios
3. Verificar rendimiento

**Resultado Esperado:**
- ✅ Lista carga sin lag
- ✅ Scroll es fluido
- ✅ Filtros responden rápido

---

## 10. Pruebas de Seguridad Básicas

### 10.1 Validación de Entrada
1. Intentar inyectar HTML en campos de texto
2. Intentar SQL injection en campos

**Resultado Esperado:**
- ✅ HTML se escapa correctamente
- ✅ No hay vulnerabilidades SQL

### 10.2 CORS Restrictivo
1. Intentar hacer llamada API desde otro origen (usar curl o Postman)

**Resultado Esperado:**
- ✅ Solo permite origen http://localhost:5173
- ✅ Rechaza otros orígenes

---

## Resumen de Verificación

Al completar todas las pruebas, verificar:

- [ ] ✅ CORS configurado correctamente
- [ ] ✅ Todos los endpoints funcionan desde frontend
- [ ] ✅ Manejo de errores muestra mensajes apropiados en UI
- [ ] ✅ Datos persisten después de recargar página
- [ ] ✅ Datos persisten después de cerrar navegador
- [ ] ✅ Filtros funcionan correctamente
- [ ] ✅ Ordenamiento es correcto
- [ ] ✅ Cálculos de comisiones son precisos
- [ ] ✅ Diseño responsive funciona en todos los tamaños
- [ ] ✅ Performance es aceptable
- [ ] ✅ No hay errores en consola del navegador
- [ ] ✅ No hay errores en logs del backend

---

## Comandos Útiles

### Iniciar Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### Iniciar Frontend
```bash
cd frontend
npm run dev
```

### Ver Logs del Backend
```bash
# Los logs aparecen en la terminal donde se ejecutó uvicorn
```

### Limpiar Base de Datos
```bash
cd backend
rm salon.db
# La BD se recreará automáticamente al iniciar el backend
```

### Ejecutar Tests de Integración
```bash
cd backend
pytest tests/integration/test_backend_frontend_integration.py -v
```

### Ejecutar Tests E2E
```bash
cd frontend
npm run test:e2e
```
