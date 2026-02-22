#!/usr/bin/env python3
"""
Script parte 4: Actualizar archivos del frontend
para agregar soporte de precio_por_defecto
"""
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("🚀 Script Parte 4: Actualizando frontend...")
print("=" * 60)

try:
    # ========================================================================
    # 1. ACTUALIZAR frontend/src/types/models.ts
    # ========================================================================
    print("\n📝 Actualizando frontend/src/types/models.ts...")
    
    with open('frontend/src/types/models.ts', 'r') as f:
        models = f.read()
    
    # Crear backup
    with open(f'frontend/src/types/models.ts.backup_{timestamp}', 'w') as f:
        f.write(models)
    
    # Agregar precio_por_defecto a TipoServicio
    models = models.replace(
        'export interface TipoServicio {\n  nombre: string;\n  descripcion: string;\n  porcentaje_comision: number;\n}',
        'export interface TipoServicio {\n  nombre: string;\n  descripcion: string;\n  porcentaje_comision: number;\n  precio_por_defecto?: number | null;\n}'
    )
    
    # Agregar precio_por_defecto a TipoServicioFormData
    models = models.replace(
        'export interface TipoServicioFormData {\n  nombre: string;\n  descripcion: string;\n  porcentaje_comision: number;\n}',
        'export interface TipoServicioFormData {\n  nombre: string;\n  descripcion: string;\n  porcentaje_comision: number;\n  precio_por_defecto?: number | null;\n}'
    )
    
    with open('frontend/src/types/models.ts', 'w') as f:
        f.write(models)
    
    print("✅ frontend/src/types/models.ts actualizado")
    
    # ========================================================================
    # 2. ACTUALIZAR frontend/src/components/tipos-servicios/TipoServicioForm.vue
    # ========================================================================
    print("\n📝 Actualizando frontend/src/components/tipos-servicios/TipoServicioForm.vue...")
    
    with open('frontend/src/components/tipos-servicios/TipoServicioForm.vue', 'r') as f:
        form = f.read()
    
    # Crear backup
    with open(f'frontend/src/components/tipos-servicios/TipoServicioForm.vue.backup_{timestamp}', 'w') as f:
        f.write(form)
    
    # Agregar campo de precio después del campo de porcentaje_comision
    form = form.replace(
        '''          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Porcentaje de Comisión (%) <span class="text-red-500">*</span>
            </label>
            <input
              v-model.number="formData.porcentaje_comision"
              type="number"
              required
              min="0"
              max="100"
              step="0.01"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.porcentaje_comision }"
              placeholder="Ej: 15"
            />
            <p v-if="errors.porcentaje_comision" class="text-red-500 text-sm mt-1">{{ errors.porcentaje_comision }}</p>
            <p class="text-gray-500 text-xs mt-1">Debe estar entre 0 y 100</p>
          </div>

          <div class="flex gap-3 pt-4">''',
        '''          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Porcentaje de Comisión (%) <span class="text-red-500">*</span>
            </label>
            <input
              v-model.number="formData.porcentaje_comision"
              type="number"
              required
              min="0"
              max="100"
              step="0.01"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.porcentaje_comision }"
              placeholder="Ej: 15"
            />
            <p v-if="errors.porcentaje_comision" class="text-red-500 text-sm mt-1">{{ errors.porcentaje_comision }}</p>
            <p class="text-gray-500 text-xs mt-1">Debe estar entre 0 y 100</p>
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
    
    # Agregar precio_por_defecto al formData en el script
    form = form.replace(
        'const formData = reactive({\n  nombre: props.tipo?.nombre || \'\',\n  descripcion: props.tipo?.descripcion || \'\',\n  porcentaje_comision: props.tipo?.porcentaje_comision || 0,\n});',
        'const formData = reactive({\n  nombre: props.tipo?.nombre || \'\',\n  descripcion: props.tipo?.descripcion || \'\',\n  porcentaje_comision: props.tipo?.porcentaje_comision || 0,\n  precio_por_defecto: props.tipo?.precio_por_defecto || null,\n});'
    )
    
    # Agregar validación de precio_por_defecto
    form = form.replace(
        'const errors = reactive({\n  nombre: \'\',\n  descripcion: \'\',\n  porcentaje_comision: \'\',\n});',
        'const errors = reactive({\n  nombre: \'\',\n  descripcion: \'\',\n  porcentaje_comision: \'\',\n  precio_por_defecto: \'\',\n});'
    )
    
    # Agregar validación en validateForm
    form = form.replace(
        '''function validateForm(): boolean {
  errors.nombre = '';
  errors.descripcion = '';
  errors.porcentaje_comision = '';

  let isValid = true;''',
        '''function validateForm(): boolean {
  errors.nombre = '';
  errors.descripcion = '';
  errors.porcentaje_comision = '';
  errors.precio_por_defecto = '';

  let isValid = true;'''
    )
    
    # Agregar validación de precio_por_defecto antes del return
    form = form.replace(
        '''  if (isNaN(formData.porcentaje_comision)) {
    errors.porcentaje_comision = 'El porcentaje debe ser un número válido';
    isValid = false;
  }

  return isValid;
}''',
        '''  if (isNaN(formData.porcentaje_comision)) {
    errors.porcentaje_comision = 'El porcentaje debe ser un número válido';
    isValid = false;
  }

  if (formData.precio_por_defecto !== null && formData.precio_por_defecto !== undefined && formData.precio_por_defecto <= 0) {
    errors.precio_por_defecto = 'El precio debe ser mayor que cero';
    isValid = false;
  }

  return isValid;
}'''
    )
    
    # Actualizar el emit para incluir precio_por_defecto
    form = form.replace(
        '''    emit('guardar', {
      nombre: formData.nombre,
      descripcion: formData.descripcion,
      porcentaje_comision: formData.porcentaje_comision,
    });''',
        '''    emit('guardar', {
      nombre: formData.nombre,
      descripcion: formData.descripcion,
      porcentaje_comision: formData.porcentaje_comision,
      precio_por_defecto: formData.precio_por_defecto,
    });'''
    )
    
    with open('frontend/src/components/tipos-servicios/TipoServicioForm.vue', 'w') as f:
        f.write(form)
    
    print("✅ frontend/src/components/tipos-servicios/TipoServicioForm.vue actualizado")
    
    # ========================================================================
    # 3. ACTUALIZAR frontend/src/components/tipos-servicios/TipoServicioCard.vue
    # ========================================================================
    print("\n📝 Actualizando frontend/src/components/tipos-servicios/TipoServicioCard.vue...")
    
    with open('frontend/src/components/tipos-servicios/TipoServicioCard.vue', 'r') as f:
        card = f.read()
    
    # Crear backup
    with open(f'frontend/src/components/tipos-servicios/TipoServicioCard.vue.backup_{timestamp}', 'w') as f:
        f.write(card)
    
    # Agregar badge de precio después del badge de comisión
    card = card.replace(
        '''        <div class="mt-2 inline-flex items-center px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
          Comisión: {{ tipo.porcentaje_comision }}%
        </div>
      </div>''',
        '''        <div class="mt-2 flex gap-2 flex-wrap">
          <span class="inline-flex items-center px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
            Comisión: {{ tipo.porcentaje_comision }}%
          </span>
          <span v-if="tipo.precio_por_defecto" class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            Precio: ${{ tipo.precio_por_defecto }}
          </span>
        </div>
      </div>'''
    )
    
    with open('frontend/src/components/tipos-servicios/TipoServicioCard.vue', 'w') as f:
        f.write(card)
    
    print("✅ frontend/src/components/tipos-servicios/TipoServicioCard.vue actualizado")
    
    # ========================================================================
    # 4. ACTUALIZAR frontend/src/components/servicios/ServicioForm.vue
    # ========================================================================
    print("\n📝 Actualizando frontend/src/components/servicios/ServicioForm.vue...")
    
    with open('frontend/src/components/servicios/ServicioForm.vue', 'r') as f:
        servicio_form = f.read()
    
    # Crear backup
    with open(f'frontend/src/components/servicios/ServicioForm.vue.backup_{timestamp}', 'w') as f:
        f.write(servicio_form)
    
    # Agregar @change al select de tipo_servicio para auto-llenar precio
    servicio_form = servicio_form.replace(
        '''            <select
              v-model="formData.tipo_servicio"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.tipo_servicio }"
            >''',
        '''            <select
              v-model="formData.tipo_servicio"
              @change="onTipoServicioChange"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              :class="{ 'border-red-500': errors.tipo_servicio }"
            >'''
    )
    
    # Agregar computed property y método onTipoServicioChange antes de validateForm
    servicio_form = servicio_form.replace(
        '''function validateForm(): boolean {''',
        '''// Computed property para obtener el precio sugerido del tipo de servicio seleccionado
const precioSugerido = computed(() => {
  if (!formData.tipo_servicio) return null;
  const tipo = tiposServiciosStore.tiposServicios.find(t => t.nombre === formData.tipo_servicio);
  return tipo?.precio_por_defecto || null;
});

// Auto-llenar precio cuando se selecciona un tipo de servicio
function onTipoServicioChange() {
  const tipo = tiposServiciosStore.tiposServicios.find(t => t.nombre === formData.tipo_servicio);
  if (tipo?.precio_por_defecto) {
    formData.precio = tipo.precio_por_defecto;
  }
}

function validateForm(): boolean {'''
    )
    
    # Agregar import de computed
    servicio_form = servicio_form.replace(
        "import { ref, reactive, onMounted } from 'vue';",
        "import { ref, reactive, onMounted, computed } from 'vue';"
    )
    
    # Agregar hint de precio sugerido en el campo de precio
    servicio_form = servicio_form.replace(
        '''            <p v-if="errors.precio" class="text-red-500 text-sm mt-1">{{ errors.precio }}</p>
            <p class="text-gray-500 text-xs mt-1">Debe ser mayor que cero</p>
          </div>''',
        '''            <p v-if="errors.precio" class="text-red-500 text-sm mt-1">{{ errors.precio }}</p>
            <p v-if="precioSugerido" class="text-blue-600 text-xs mt-1">💡 Precio sugerido: ${{ precioSugerido }}</p>
            <p class="text-gray-500 text-xs mt-1">Debe ser mayor que cero</p>
          </div>'''
    )
    
    with open('frontend/src/components/servicios/ServicioForm.vue', 'w') as f:
        f.write(servicio_form)
    
    print("✅ frontend/src/components/servicios/ServicioForm.vue actualizado")
    
    print("\n" + "=" * 60)
    print("✅ Parte 4 completada exitosamente!")
    print(f"📦 Backups creados: *.backup_{timestamp}")
    print("=" * 60)
    print("\n📝 Archivos actualizados:")
    print("  ✓ frontend/src/types/models.ts")
    print("  ✓ frontend/src/components/tipos-servicios/TipoServicioForm.vue")
    print("  ✓ frontend/src/components/tipos-servicios/TipoServicioCard.vue")
    print("  ✓ frontend/src/components/servicios/ServicioForm.vue")
    print("\n🎉 ¡Actualización completa!")
    print("\n📋 Próximos pasos:")
    print("  1. Reinicia el backend: Ctrl+C en el terminal del backend y ejecuta 'uvicorn app.main:app --reload'")
    print("  2. El frontend se recargará automáticamente")
    print("  3. Prueba crear un tipo de servicio con precio por defecto")
    print("  4. Verifica que al registrar un servicio se auto-llene el precio")
    print("")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
