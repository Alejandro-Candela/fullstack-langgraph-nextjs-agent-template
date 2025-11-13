"""Script para recrear las tablas del checkpointer de LangGraph."""

import asyncio
import sys
import psycopg
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.config import settings

# Fix para Windows: usar SelectorEventLoop en lugar de ProactorEventLoop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def migrate_checkpointer():
    """Recrea las tablas del checkpointer con el schema actualizado."""
    
    connection_string = settings.database_url_with_ssl
    
    # Convert asyncpg URL to standard postgresql://
    if connection_string.startswith("postgresql+asyncpg://"):
        connection_string = connection_string.replace("postgresql+asyncpg://", "postgresql://", 1)
    
    print("🔍 Conectando a la base de datos...")
    print(f"   URL: {connection_string.split('@')[1] if '@' in connection_string else 'localhost'}")
    
    try:
        # Connect to database with autocommit for CONCURRENTLY operations
        async with await psycopg.AsyncConnection.connect(
            connection_string,
            autocommit=True
        ) as conn:
            print("\n✅ Conectado a PostgreSQL")
            
            # Drop old tables
            print("\n🗑️  Eliminando tablas antiguas del checkpointer...")
            async with conn.cursor() as cur:
                await cur.execute("DROP TABLE IF EXISTS checkpoint_writes CASCADE;")
                await cur.execute("DROP TABLE IF EXISTS checkpoints CASCADE;")
                await cur.execute("DROP TABLE IF EXISTS checkpoint_migrations CASCADE;")
            print("   ✅ Tablas antiguas eliminadas")
            
        # Create new pool and checkpointer
        print("\n📦 Creando nuevo checkpointer...")
        pool = AsyncConnectionPool(
            conninfo=connection_string,
            min_size=1,
            max_size=10,
            kwargs={"autocommit": True},  # Required for CREATE INDEX CONCURRENTLY
        )
        await pool.open()
        
        checkpointer = AsyncPostgresSaver(pool)
        
        # Setup creates the new tables with correct schema
        print("🔨 Creando tablas con el schema actualizado...")
        await checkpointer.setup()
        
        await pool.close()
        
        print("\n✅ ¡Migración completada exitosamente!")
        print("   Las tablas del checkpointer han sido recreadas con el schema correcto.")
        print("   Ahora puedes ejecutar: python run.py")
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 70)
    print("  Migración de Checkpointer de LangGraph")
    print("=" * 70)
    print("\n⚠️  ADVERTENCIA: Esto eliminará el historial de conversaciones existente.")
    print("   Las tablas del checkpointer serán recreadas.\n")
    
    response = input("¿Continuar? (s/n): ")
    
    if response.lower() == 's':
        asyncio.run(migrate_checkpointer())
    else:
        print("\n❌ Migración cancelada.")

