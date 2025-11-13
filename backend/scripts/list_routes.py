"""Lista todas las rutas registradas en FastAPI."""

from app.main import app

print("📋 Rutas registradas en FastAPI:\n")
print(f"{'METHOD':<10} {'PATH':<50} {'NAME':<30}")
print("-" * 90)

for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        methods = ', '.join(sorted(route.methods - {'HEAD', 'OPTIONS'}))
        name = getattr(route, 'name', '')
        print(f"{methods:<10} {route.path:<50} {name:<30}")

print("\n✅ Total de rutas:", len([r for r in app.routes if hasattr(r, 'methods')]))

# Buscar específicamente la ruta de tools
print("\n🔍 Buscando rutas con 'tools':")
tools_routes = [r for r in app.routes if hasattr(r, 'path') and 'tools' in r.path.lower()]
if tools_routes:
    for route in tools_routes:
        methods = ', '.join(sorted(route.methods - {'HEAD', 'OPTIONS'})) if hasattr(route, 'methods') else 'N/A'
        print(f"   {methods:<10} {route.path}")
else:
    print("   ❌ No se encontraron rutas con 'tools'")

