import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Database configuration
# Using localhost:5434 as defined in docker-compose.yml for the host
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5434")
MAINTENANCE_DB = "postgres"
TEST_DB_NAME = "langgraph_agent_test"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{MAINTENANCE_DB}"

async def create_test_db():
    print(f"Connecting to {DATABASE_URL}...")
    engine = create_async_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        # Check if database exists
        result = await conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'")
        )
        exists = result.scalar()

        if not exists:
            print(f"Creating database {TEST_DB_NAME}...")
            await conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))
            print(f"Database {TEST_DB_NAME} created successfully.")
        else:
            print(f"Database {TEST_DB_NAME} already exists.")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_test_db())
