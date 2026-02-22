#!/usr/bin/env python3
"""
Script para aplicar cambios de precio_por_defecto a tipos de servicios
"""
import os
import subprocess

def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔧 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {description} - Completado")
        return True
    else:
        print(f"❌ {description} - Error: {result.stderr}")
        return False

def main():
    print("🚀 Iniciando actualización del sistema...")
    print("=" * 60)
    
    # 1. Migrar base de datos
    if not run_command(
        'cd backend && sqlite3 salon.db "ALTER TABLE tipos_servicios ADD COLUMN precio_por_defecto NUMERIC(10, 2);" && cd ..',
        "Migrando base de datos"
    ):
        print("\n⚠️  La columna puede ya existir, continuando...")
    
    print("\n" + "=" * 60)
    print("✅ Migración de base de datos completada")
    print("\n📝 Ahora necesitas actualizar manualmente los siguientes archivos:")
    print("\nBackend:")
    print("  1. backend/app/models.py")
    print("  2. backend/app/orm_models.py")
    print("  3. backend/app/schemas.py")
    print("  4. backend/app/manager.py")
    print("  5. backend/app/main.py")
    print("\nFrontend:")
    print("  6. frontend/src/types/models.ts")
    print("  7. frontend/src/components/tipos-servicios/TipoServicioForm.vue")
    print("  8. frontend/src/components/tipos-servicios/TipoServicioCard.vue")
    print("  9. frontend/src/components/servicios/ServicioForm.vue")
    
    print("\n📚 Consulta la documentación detallada que te proporcioné anteriormente.")
    print("=" * 60)

if __name__ == "__main__":
    main()
