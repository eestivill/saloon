#!/usr/bin/env python3
"""
Script de corrección: Agregar campo precio_por_defecto a TipoServicioForm.vue
"""
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("🔧 Corrigiendo TipoServicioForm.vue...")
print("=" * 60)

try:
    # Leer el archivo
    with open('frontend/src/components/tipos-servicios/TipoServicioForm.vue', 'r') as f:
        content = f.read()
    
    # Crear backup
    with open(f'frontend/src/components/tipos-servicios/TipoServicioForm.vue.backup_{timestamp}', 'w') as f:
        f.write(content)
    
    # 1. Agregar campo de precio en el template después del campo de porcentaje_comision
    content = content.replace(
        '''            <p class="text-gray-500 text-xs mt-1">Debe estar entre 0 y 100</p>
          </div>

          <div class="flex gap-3 pt-4">''',
        '''            <p class="text-gray-500 text-xs mt-1">Debe estar entre 0 y 100</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Precio por Defecto ($)
            </label>
            <input
              v-model.number="formData.precio_por_defecto"
              type="number"
              min="0.01"
              step="0.01"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.precio_por_defecto }"
              placeholder="Ej: 25.00 (opcional)"
            />
            <p v-if="errors.precio_por_defecto" class="text-red-500 text-sm mt-1">{{ errors.precio_por_defecto }}</p>
            <p class="text-gray-500 text-xs mt-1">Opcional. Se usará como precio sugerido al registrar servicios</p>
          </div>

          <div class="flex gap-3 pt-4">'''
    )
    
    # 2. Agregar precio_por_defecto al tipo del emit
    content = content.replace(
        '''const emit = defineEmits<{
  guardar: [data: { nombre: string; descripcion: string; porcentaje_comision: number }];
  cancelar: [];
}>();''',
        '''const emit = defineEmits<{
  guardar: [data: { nombre: string; descripcion: string; porcentaje_comision: number; precio_por_defecto?: number | null }];
  cancelar: [];
}>();'''
    )
    
    # 3. Agregar precio_por_defecto al formData
    content = content.replace(
        '''const formData = reactive({
  nombre: '',
  descripcion: '',
  porcentaje_comision: 0,
});''',
        '''const formData = reactive({
  nombre: '',
  descripcion: '',
  porcentaje_comision: 0,
  precio_por_defecto: null as number | null,
});'''
    )
    
    # 4. Agregar precio_por_defecto en onMounted
    content = content.replace(
        '''onMounted(() => {
  if (props.tipo) {
    formData.nombre = props.tipo.nombre;
    formData.descripcion = props.tipo.descripcion;
    formData.porcentaje_comision = props.tipo.porcentaje_comision;
  }
});''',
        '''onMounted(() => {
  if (props.tipo) {
    formData.nombre = props.tipo.nombre;
    formData.descripcion = props.tipo.descripcion;
    formData.porcentaje_comision = props.tipo.porcentaje_comision;
    formData.precio_por_defecto = props.tipo.precio_por_defecto || null;
  }
});'''
    )
    
    # 5. Agregar precio_por_defecto al emit en handleSubmit
    content = content.replace(
        '''    emit('guardar', {
      nombre: formData.nombre.trim(),
      descripcion: formData.descripcion.trim(),
      porcentaje_comision: formData.porcentaje_comision,
    });''',
        '''    emit('guardar', {
      nombre: formData.nombre.trim(),
      descripcion: formData.descripcion.trim(),
      porcentaje_comision: formData.porcentaje_comision,
      precio_por_defecto: formData.precio_por_defecto,
    });'''
    )
    
    with open('frontend/src/components/tipos-servicios/TipoServicioForm.vue', 'w') as f:
        f.write(content)
    
    print("✅ TipoServicioForm.vue corregido")
    print("\n" + "=" * 60)
    print("✅ Corrección completada!")
    print(f"📦 Backup: TipoServicioForm.vue.backup_{timestamp}")
    print("=" * 60)
    print("\n💡 El frontend se recargará automáticamente")
    print("   Ahora verás el campo 'Precio por Defecto' en el formulario")
    print("")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
