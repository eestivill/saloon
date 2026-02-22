#!/usr/bin/env python3
"""
Script de corrección: Agregar precio_por_defecto en TiposServiciosList y store
"""
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("🔧 Corrigiendo precio_por_defecto en tipos de servicios...")
print("=" * 60)

try:
    # ========================================================================
    # 1. Corregir frontend/src/stores/tiposServicios.ts
    # ========================================================================
    print("\n📝 Actualizando frontend/src/stores/tiposServicios.ts...")
    
    with open('frontend/src/stores/tiposServicios.ts', 'r') as f:
        store_content = f.read()
    
    # Crear backup
    with open(f'frontend/src/stores/tiposServicios.ts.backup_{timestamp}', 'w') as f:
        f.write(store_content)
    
    # Actualizar el tipo de crearTipoServicio
    store_content = store_content.replace(
        '''  async function crearTipoServicio(data: {
    nombre: string;
    descripcion: string;
    porcentaje_comision: number;
  }) {''',
        '''  async function crearTipoServicio(data: {
    nombre: string;
    descripcion: string;
    porcentaje_comision: number;
    precio_por_defecto?: number | null;
  }) {'''
    )
    
    with open('frontend/src/stores/tiposServicios.ts', 'w') as f:
        f.write(store_content)
    
    print("✅ frontend/src/stores/tiposServicios.ts actualizado")
    
    # ========================================================================
    # 2. Corregir frontend/src/components/tipos-servicios/TiposServiciosList.vue
    # ========================================================================
    print("\n📝 Actualizando TiposServiciosList.vue...")
    
    with open('frontend/src/components/tipos-servicios/TiposServiciosList.vue', 'r') as f:
        list_content = f.read()
    
    # Crear backup
    with open(f'frontend/src/components/tipos-servicios/TiposServiciosList.vue.backup_{timestamp}', 'w') as f:
        f.write(list_content)
    
    # Actualizar el tipo del parámetro data en guardarTipoServicio
    list_content = list_content.replace(
        '''async function guardarTipoServicio(data: {
  nombre: string;
  descripcion: string;
  porcentaje_comision: number;
}) {''',
        '''async function guardarTipoServicio(data: {
  nombre: string;
  descripcion: string;
  porcentaje_comision: number;
  precio_por_defecto?: number | null;
}) {'''
    )
    
    # Actualizar la llamada a actualizarTipoServicio para incluir precio_por_defecto
    list_content = list_content.replace(
        '''    if (tipoSeleccionado.value) {
      await store.actualizarTipoServicio(tipoSeleccionado.value.nombre, {
        descripcion: data.descripcion,
        porcentaje_comision: data.porcentaje_comision,
      });
    } else {
      await store.crearTipoServicio(data);
    }''',
        '''    if (tipoSeleccionado.value) {
      await store.actualizarTipoServicio(tipoSeleccionado.value.nombre, {
        descripcion: data.descripcion,
        porcentaje_comision: data.porcentaje_comision,
        precio_por_defecto: data.precio_por_defecto,
      });
    } else {
      await store.crearTipoServicio(data);
    }'''
    )
    
    with open('frontend/src/components/tipos-servicios/TiposServiciosList.vue', 'w') as f:
        f.write(list_content)
    
    print("✅ TiposServiciosList.vue actualizado")
    
    print("\n" + "=" * 60)
    print("✅ Corrección completada!")
    print(f"📦 Backups creados con timestamp: {timestamp}")
    print("=" * 60)
    print("\n💡 El frontend se recargará automáticamente")
    print("   Ahora el precio_por_defecto se guardará correctamente al crear/editar")
    print("")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
