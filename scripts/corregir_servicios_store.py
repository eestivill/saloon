#!/usr/bin/env python3
"""
Script de corrección: Convertir precio y comision_calculada a números en el store
"""
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("🔧 Corrigiendo conversión de tipos en servicios store...")
print("=" * 60)

try:
    # Leer el store de servicios
    with open('frontend/src/stores/servicios.ts', 'r') as f:
        content = f.read()
    
    # Crear backup
    with open(f'frontend/src/stores/servicios.ts.backup_{timestamp}', 'w') as f:
        f.write(content)
    
    # Agregar función de transformación después de los imports
    content = content.replace(
        '''import { defineStore } from 'pinia';
import { ref } from 'vue';
import { serviciosAPI } from '@/services/api';
import type { Servicio, ServiciosFiltros } from '@/types/models';

export const useServiciosStore = defineStore('servicios', () => {''',
        '''import { defineStore } from 'pinia';
import { ref } from 'vue';
import { serviciosAPI } from '@/services/api';
import type { Servicio, ServiciosFiltros } from '@/types/models';

// Función helper para convertir strings a números
function parseServicio(servicio: any): Servicio {
  return {
    ...servicio,
    precio: typeof servicio.precio === 'string' ? parseFloat(servicio.precio) : servicio.precio,
    comision_calculada: typeof servicio.comision_calculada === 'string' ? parseFloat(servicio.comision_calculada) : servicio.comision_calculada,
  };
}

export const useServiciosStore = defineStore('servicios', () => {'''
    )
    
    # Actualizar cargarServicios para usar parseServicio
    content = content.replace(
        '''    try {
      const response = await serviciosAPI.listar(filtros);
      servicios.value = response.data;
    } catch (e: any) {''',
        '''    try {
      const response = await serviciosAPI.listar(filtros);
      servicios.value = response.data.map(parseServicio);
    } catch (e: any) {'''
    )
    
    # Actualizar registrarServicio para usar parseServicio
    content = content.replace(
        '''    try {
      const response = await serviciosAPI.crear(data);
      servicios.value.push(response.data);
      return response.data;
    } catch (e: any) {''',
        '''    try {
      const response = await serviciosAPI.crear(data);
      const servicioParseado = parseServicio(response.data);
      servicios.value.push(servicioParseado);
      return servicioParseado;
    } catch (e: any) {'''
    )
    
    with open('frontend/src/stores/servicios.ts', 'w') as f:
        f.write(content)
    
    print("✅ frontend/src/stores/servicios.ts corregido")
    print("\n" + "=" * 60)
    print("✅ Corrección completada!")
    print(f"📦 Backup: frontend/src/stores/servicios.ts.backup_{timestamp}")
    print("=" * 60)
    print("\n💡 El frontend se recargará automáticamente")
    print("   Ahora podrás crear servicios sin errores")
    print("")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
