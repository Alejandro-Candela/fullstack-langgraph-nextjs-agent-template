"""Script de prueba para verificar que todo se puede importar correctamente."""

print("🔍 Verificando importaciones...")

try:
    print("1. Importando FastAPI...")
    from fastapi import FastAPI
    print("   ✅ FastAPI OK")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

try:
    print("2. Importando Pydantic...")
    from pydantic import BaseModel
    print("   ✅ Pydantic OK")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

try:
    print("3. Importando SQLAlchemy...")
    from sqlalchemy.ext.asyncio import AsyncSession
    print("   ✅ SQLAlchemy OK")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

try:
    print("4. Importando LangGraph...")
    from langgraph.graph import StateGraph
    print("   ✅ LangGraph OK")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

try:
    print("5. Verificando configuración...")
    import os
    os.environ.setdefault("DATABASE_URL", "postgresql://user:password@localhost:5434/mydb")
    os.environ.setdefault("OPENAI_API_KEY", "test")
    os.environ.setdefault("CORS_ORIGINS", "http://localhost:3000")
    
    from app.config import settings
    print(f"   ✅ Config OK - Puerto: {settings.port}")
except Exception as e:
    print(f"   ❌ Error en config: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

try:
    print("6. Importando app principal...")
    from app.main import app
    print("   ✅ App principal OK")
except Exception as e:
    print(f"   ❌ Error en app: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n✅ ¡Todas las verificaciones pasaron!")
print(f"📊 Configuración cargada:")
print(f"   - Puerto: {settings.port}")
print(f"   - Database: {settings.database_url}")
print(f"   - CORS Origins: {settings.cors_origins}")
print(f"   - Environment: {settings.environment}")
print("\n🚀 Puedes ejecutar: python run.py")

