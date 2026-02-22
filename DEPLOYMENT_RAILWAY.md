# Despliegue en Railway.app ($5 USD gratis/mes)

## Ventajas de Railway

✅ **$5 USD de crédito gratis al mes** (suficiente para apps pequeñas)
✅ **SQLite con volumen persistente** (tus datos se mantienen)
✅ **No se duerme** (siempre activo)
✅ **Muy fácil de usar**
✅ **Despliegue automático desde GitHub**

## Pasos para Desplegar

### 1. Crear cuenta en Railway

1. Ve a https://railway.app
2. Haz clic en "Login" o "Start a New Project"
3. Inicia sesión con GitHub (recomendado)

### 2. Desplegar Backend

1. En Railway, haz clic en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Conecta tu repositorio
4. Railway detectará automáticamente que es un proyecto Python
5. Configura:
   - **Root Directory**: `backend`
   - Railway detectará automáticamente `requirements.txt`
6. Haz clic en **"Deploy"**

### 3. Agregar Volumen para SQLite

1. En el dashboard del backend, ve a **"Settings"**
2. Busca la sección **"Volumes"**
3. Haz clic en **"+ New Volume"**
4. Configura:
   - **Mount Path**: `/data`
   - **Size**: 1 GB (suficiente)
5. Guarda y espera a que se redespliegue

### 4. Obtener URL del Backend

1. En el dashboard del backend, ve a **"Settings"**
2. Busca **"Domains"**
3. Haz clic en **"Generate Domain"**
4. Copia la URL (algo como: `https://tu-app.up.railway.app`)

### 5. Desplegar Frontend

1. En Railway, haz clic en **"New"** → **"GitHub Repo"**
2. Selecciona el mismo repositorio
3. Configura:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npx serve -s dist -l $PORT`
4. Agrega variable de entorno:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://TU-BACKEND-URL.up.railway.app/api`
5. Haz clic en **"Deploy"**

### 6. Generar Dominio para Frontend

1. En el dashboard del frontend, ve a **"Settings"**
2. Busca **"Domains"**
3. Haz clic en **"Generate Domain"**
4. Copia la URL del frontend

### 7. Actualizar CORS en Backend

1. Ve al dashboard del backend en Railway
2. Haz clic en **"Variables"**
3. Agrega una nueva variable:
   - **Key**: `FRONTEND_URL`
   - **Value**: La URL del frontend que acabas de generar
4. El backend se redesplegará automáticamente

## URLs de tu Aplicación

Después del despliegue:

- **Frontend**: `https://tu-frontend.up.railway.app`
- **Backend**: `https://tu-backend.up.railway.app`
- **API Docs**: `https://tu-backend.up.railway.app/docs`

## Actualizar la Aplicación

```bash
git add .
git commit -m "Cambios"
git push