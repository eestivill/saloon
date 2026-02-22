#!/usr/bin/env python3
"""
Script de corrección: Convertir precio_por_defecto a número en tiposServicios store
"""
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("🔧 Corrigiendo conversión de tipos en tiposServicios store...")
print("=" * 60)

try:
    # Leer el store de tipos de servicios
    with open('frontend/src/stores/tiposServicios.ts', 'r') as f:
        content = f.read()
    
    # Crear backup
    with open(f'frontend/src/stores/tiposServicios.ts.backup_{timestamp}', 'w') as f:
        f.write(content)
    
    # Agregar función de transformación después de los imports
    content = content.replace(
        '''import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { tiposServiciosAPI } from '@/services/api';
import type { TipoServicio } from '@/types/models';

export const useTiposServiciosStore = defineStore('tiposServicios', () => {''',
        '''import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { tiposServiciosAPI } from '@/services/api';
import type { TipoServicio } from '@/types/models';

// Función helper para convertir strings a números
function parseTipoServicio(tipo: any): TipoServicio {
  return {
    ...tipo,
    precio_por_defecto: tipo.precio_por_defecto ? 
      (typeof tipo.precio_por_defecto === 'string' ? parseFloat(tipo.precio_por_defecto) : tipo.precio_por_defecto) 
      : null,
  };
}

export const useTiposServiciosStore = defineStore('tiposServicios', () => {'''
    )
    
    # Actualizar cargarTiposServicios para usar parseTipoServicio
    content = content.replace(
        '''    try {
      const response = await tiposServiciosAPI.listar();
      tiposServicios.value = response.data;
    } catch (e: any) {''',
        '''    try {
      const response = await tiposServiciosAPI.listar();
      tiposServicios.value = response.data.map(parseTipoServicio);
    } catch (e: any) {'''
    )
    
    # Actualizar crearTipoServicio para usar parseTipoServicio
    content = content.replace(
        '''    try {
      const response = await tiposServiciosAPI.crear(data);
      tiposServicios.value.push(response.data);
      return response.data;
    } catch (e: any) {''',
        '''    try {
      const response = await tiposServiciosAPI.crear(data);
      const tipoParseado = parseTipoServicio(response.data);
      tiposServicios.value.push(tipoParseado);
      return tipoParseado;
    } catch (e: any) {'''
    )
    
    # Actualizar actualizarTipoServicio para usar parseTipoServicio
    content = content.replace(
        '''    try {
      const response = await tiposServiciosAPI.actualizar(nombre, data);
      const index = tiposServicios.value.findIndex((tipo) => tipo.nombre === nombre);
      if (index !== -1) {
        tiposServicios.value[index] = response.data;
      }
      return response.data;
    } catch (e: any) {''',
        '''    try {
      const response = await tiposServiciosAPI.actualizar(nombre, data);
      const tipoParseado = parseTipoServicio(response.data);
      const index = tiposServicios.value.findIndex((tipo) => tipo.nombre === nombre);
      if (index !== -1) {
        tiposServicios.value[index] = tipoParseado;
      }
      return tipoParseado;
    } catch (e: any) {'''
    )
    
    with open('frontend/src/stores/tiposServicios.ts', 'w') as f:
        f.write(content)
    
    print("✅ frontend/src/stores/tiposServicios.ts corregido")
    print("\n" + "=" * 60)
    print("✅ Corrección completada!")
    print(f"📦 Backup: frontend/src/stores/tiposServicios.ts.backup_{timestamp}")
    print("=" * 60)
    print("\n💡 El frontend se recargará automáticamente")
    print("   Ahora al seleccionar un tipo de servicio con precio por defecto,")
    print("   el campo de precio se auto-llenará correctamente")
    print("")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
