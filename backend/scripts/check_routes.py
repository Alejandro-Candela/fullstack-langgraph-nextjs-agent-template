"""Script para verificar todas las rutas registradas en FastAPI."""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Verificando rutas de FastAPI...\n")

try:
    from app.main import app
    
    print("✅ App importada correctamente\n")
    print("📋 Rutas registradas:\n")
    
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = ', '.join(route.methods)
            print(f"   {methods:10} {route.path}")
    
    print("\n✅ Todas las rutas listadas")
    
except Exception as e:
    print(f"❌ Error importando la app: {e}")
    import traceback
    traceback.print_exc()

