#!/usr/bin/env python3
"""
Script parte 3: Actualizar backend/app/manager.py y backend/app/main.py
para agregar soporte de precio_por_defecto
"""
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print("🚀 Script Parte 3: Actualizando backend...")
print("=" * 60)

try:
    # ========================================================================
    # 1. ACTUALIZAR backend/app/manager.py
    # ========================================================================
    print("\n📝 Actualizando backend/app/manager.py...")
    
    with open('backend/app/manager.py', 'r') as f:
        manager = f.read()
    
    # Crear backup
    with open(f'backend/app/manager.py.backup_{timestamp}', 'w') as f:
        f.write(manager)
    
    # Modificar crear_tipo_servicio - agregar parámetro precio_por_defecto
    manager = manager.replace(
        'def crear_tipo_servicio(self, nombre: str, descripcion: str,\n                           porcentaje_comision: float)',
        'def crear_tipo_servicio(self, nombre: str, descripcion: str,\n                           porcentaje_comision: float, precio_por_defecto: Optional[Decimal] = None)'
    )
    
    # Actualizar docstring de crear_tipo_servicio
    manager = manager.replace(
        '            porcentaje_comision: Porcentaje de comisión (0-100)\n\n        Returns:',
        '            porcentaje_comision: Porcentaje de comisión (0-100)\n            precio_por_defecto: Precio por defecto opcional\n\n        Returns:'
    )
    
    # Actualizar instanciación de TipoServicio en crear_tipo_servicio
    manager = manager.replace(
        '        # Crear y guardar el tipo de servicio\n        tipo_servicio = TipoServicio(\n            nombre=nombre,\n            descripcion=descripcion,\n            porcentaje_comision=porcentaje_comision\n        )',
        '        # Crear y guardar el tipo de servicio\n        tipo_servicio = TipoServicio(\n            nombre=nombre,\n            descripcion=descripcion,\n            porcentaje_comision=porcentaje_comision,\n            precio_por_defecto=precio_por_defecto\n        )'
    )
    
    # Modificar actualizar_tipo_servicio - agregar parámetro precio_por_defecto
    manager = manager.replace(
        'def actualizar_tipo_servicio(self, nombre: str,\n                                 porcentaje_comision: float)',
        'def actualizar_tipo_servicio(self, nombre: str,\n                                 porcentaje_comision: float, precio_por_defecto: Optional[Decimal] = None)'
    )
    
    # Actualizar docstring de actualizar_tipo_servicio
    manager = manager.replace(
        '            porcentaje_comision: Nuevo porcentaje de comisión (0-100)\n\n        Returns:',
        '            porcentaje_comision: Nuevo porcentaje de comisión (0-100)\n            precio_por_defecto: Nuevo precio por defecto opcional\n\n        Returns:'
    )
    
    # Actualizar instanciación de TipoServicio en actualizar_tipo_servicio
    manager = manager.replace(
        '        # Actualizar el tipo de servicio (preservando nombre y descripción)\n        tipo_actualizado = TipoServicio(\n            nombre=nombre,\n            descripcion=tipo_existente.descripcion,\n            porcentaje_comision=porcentaje_comision\n        )',
        '        # Actualizar el tipo de servicio (preservando nombre, descripción y precio si no se proporciona)\n        nuevo_precio = precio_por_defecto if precio_por_defecto is not None else tipo_existente.precio_por_defecto\n        tipo_actualizado = TipoServicio(\n            nombre=nombre,\n            descripcion=tipo_existente.descripcion,\n            porcentaje_comision=porcentaje_comision,\n            precio_por_defecto=nuevo_precio\n        )'
    )
    
    with open('backend/app/manager.py', 'w') as f:
        f.write(manager)
    
    print("✅ backend/app/manager.py actualizado")
    
    # ========================================================================
    # 2. ACTUALIZAR backend/app/main.py
    # ========================================================================
    print("\n📝 Actualizando backend/app/main.py...")
    
    with open('backend/app/main.py', 'r') as f:
        main = f.read()
    
    # Crear backup
    with open(f'backend/app/main.py.backup_{timestamp}', 'w') as f:
        f.write(main)
    
    # Actualizar listar_tipos_servicios response
    main = main.replace(
        '        TipoServicioResponse(\n            nombre=tipo.nombre,\n            descripcion=tipo.descripcion,\n            porcentaje_comision=tipo.porcentaje_comision\n        )\n        for tipo in tipos',
        '        TipoServicioResponse(\n            nombre=tipo.nombre,\n            descripcion=tipo.descripcion,\n            porcentaje_comision=tipo.porcentaje_comision,\n            precio_por_defecto=tipo.precio_por_defecto\n        )\n        for tipo in tipos'
    )
    
    # Actualizar obtener_tipo_servicio response
    main = main.replace(
        '    return TipoServicioResponse(\n        nombre=tipo.nombre,\n        descripcion=tipo.descripcion,\n        porcentaje_comision=tipo.porcentaje_comision\n    )\n\n\n@app.post("/api/tipos-servicios"',
        '    return TipoServicioResponse(\n        nombre=tipo.nombre,\n        descripcion=tipo.descripcion,\n        porcentaje_comision=tipo.porcentaje_comision,\n        precio_por_defecto=tipo.precio_por_defecto\n    )\n\n\n@app.post("/api/tipos-servicios"'
    )
    
    # Actualizar crear_tipo_servicio call
    main = main.replace(
        '    resultado = salon_manager.crear_tipo_servicio(\n        tipo.nombre,\n        tipo.descripcion,\n        tipo.porcentaje_comision\n    )',
        '    resultado = salon_manager.crear_tipo_servicio(\n        tipo.nombre,\n        tipo.descripcion,\n        tipo.porcentaje_comision,\n        tipo.precio_por_defecto\n    )'
    )
    
    # Actualizar crear_tipo_servicio response
    main = main.replace(
        '            return TipoServicioResponse(\n                nombre=tipo_servicio.nombre,\n                descripcion=tipo_servicio.descripcion,\n                porcentaje_comision=tipo_servicio.porcentaje_comision\n            )\n        case Err(DuplicateError(entity, identifier)):',
        '            return TipoServicioResponse(\n                nombre=tipo_servicio.nombre,\n                descripcion=tipo_servicio.descripcion,\n                porcentaje_comision=tipo_servicio.porcentaje_comision,\n                precio_por_defecto=tipo_servicio.precio_por_defecto\n            )\n        case Err(DuplicateError(entity, identifier)):'
    )
    
    # Actualizar actualizar_tipo_servicio - agregar nuevo_precio
    main = main.replace(
        '    # Determinar qué actualizar\n    nueva_descripcion = tipo.descripcion if tipo.descripcion is not None else tipo_existente.descripcion\n    nuevo_porcentaje = tipo.porcentaje_comision if tipo.porcentaje_comision is not None else tipo_existente.porcentaje_comision\n    \n    # Actualizar el porcentaje de comisión\n    resultado = salon_manager.actualizar_tipo_servicio(nombre, nuevo_porcentaje)',
        '    # Determinar qué actualizar\n    nueva_descripcion = tipo.descripcion if tipo.descripcion is not None else tipo_existente.descripcion\n    nuevo_porcentaje = tipo.porcentaje_comision if tipo.porcentaje_comision is not None else tipo_existente.porcentaje_comision\n    nuevo_precio = tipo.precio_por_defecto if tipo.precio_por_defecto is not None else tipo_existente.precio_por_defecto\n    \n    # Actualizar el tipo de servicio\n    resultado = salon_manager.actualizar_tipo_servicio(nombre, nuevo_porcentaje, nuevo_precio)'
    )
    
    # Actualizar actualizar_tipo_servicio - TipoServicio con precio
    main = main.replace(
        '            # Si se proporcionó una nueva descripción, actualizarla también\n            if tipo.descripcion is not None:\n                from app.models import TipoServicio\n                tipo_con_descripcion = TipoServicio(\n                    nombre=nombre,\n                    descripcion=nueva_descripcion,\n                    porcentaje_comision=nuevo_porcentaje\n                )\n                salon_manager.repository.guardar_tipo_servicio(tipo_con_descripcion)\n                tipo_actualizado = tipo_con_descripcion',
        '            # Si se proporcionó una nueva descripción o precio, actualizarlos también\n            if tipo.descripcion is not None or tipo.precio_por_defecto is not None:\n                from app.models import TipoServicio\n                tipo_completo = TipoServicio(\n                    nombre=nombre,\n                    descripcion=nueva_descripcion,\n                    porcentaje_comision=nuevo_porcentaje,\n                    precio_por_defecto=nuevo_precio\n                )\n                salon_manager.repository.guardar_tipo_servicio(tipo_completo)\n                tipo_actualizado = tipo_completo'
    )
    
    # Actualizar actualizar_tipo_servicio response
    main = main.replace(
        '            return TipoServicioResponse(\n                nombre=tipo_actualizado.nombre,\n                descripcion=tipo_actualizado.descripcion,\n                porcentaje_comision=tipo_actualizado.porcentaje_comision\n            )\n        case Err(ValidationError(message, field)):',
        '            return TipoServicioResponse(\n                nombre=tipo_actualizado.nombre,\n                descripcion=tipo_actualizado.descripcion,\n                porcentaje_comision=tipo_actualizado.porcentaje_comision,\n                precio_por_defecto=tipo_actualizado.precio_por_defecto\n            )\n        case Err(ValidationError(message, field)):'
    )
    
    with open('backend/app/main.py', 'w') as f:
        f.write(main)
    
    print("✅ backend/app/main.py actualizado")
    
    print("\n" + "=" * 60)
    print("✅ Parte 3 completada exitosamente!")
    print(f"📦 Backups creados: *.backup_{timestamp}")
    print("=" * 60)
    print("\n📝 Archivos actualizados:")
    print("  ✓ backend/app/manager.py")
    print("  ✓ backend/app/main.py")
    print("\n⚠️  Archivos pendientes (parte 4):")
    print("  • frontend/src/types/models.ts")
    print("  • frontend/src/components/tipos-servicios/TipoServicioForm.vue")
    print("  • frontend/src/components/tipos-servicios/TipoServicioCard.vue")
    print("  • frontend/src/components/servicios/ServicioForm.vue")
    print("")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
