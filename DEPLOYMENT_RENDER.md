# Despliegue en Render.com (100% GRATIS)

## Pasos para Desplegar

### 1. Ir a Render.com

1. Ve a https://render.com
2. Haz clic en "Get Started" o "Sign Up"
3. Regístrate con tu cuenta de GitHub (recomendado)

### 2. Crear Blueprint

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Blueprint"**
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el archivo `render.yaml`
5. Haz clic en **"Apply"**

### 3. Esperar el Despliegue

- El backend tardará ~5-7 minutos
- El frontend tardará ~3-5 minutos
- Puedes ver el progreso en tiempo real en los logs

### 4. Verificar

Una vez completado, tendrás dos URLs:

- **Frontend**: https://stephany-mondragon-frontend.onrender.com
- **Backend API**: https://stephany-mondragon-backend.onrender.com
- **API Docs**: https://stephany-mondragon-backend.onrender.com/docs

### 5. Probar la Aplicación

1. Abre el frontend en tu navegador
2. Crea un empleado de prueba
3. Crea un tipo de servicio
4. Registra un servicio
5. ¡Listo!

## Actualizar la Aplicación

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción de cambios"
git push
