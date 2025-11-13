"""Pytest configuration and fixtures."""

import pytest
import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.database import Base, get_db
from app.main import app
from httpx import AsyncClient, ASGITransport

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5434/langgraph_agent_test"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=True,
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with overridden database dependency."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_thread_data():
    """Sample thread data for testing."""
    return {
        "title": "Test Thread",
    }


@pytest.fixture
def sample_mcp_server_stdio():
    """Sample stdio MCP server data."""
    return {
        "name": "test-stdio-server",
        "type": "stdio",
        "enabled": True,
        "command": "npx",
        "args": ["@modelcontextprotocol/server-filesystem", "/tmp"],
        "env": {"LOG_LEVEL": "info"},
    }


@pytest.fixture
def sample_mcp_server_http():
    """Sample HTTP MCP server data."""
    return {
        "name": "test-http-server",
        "type": "http",
        "enabled": True,
        "url": "https://api.example.com/mcp",
        "headers": {"Authorization": "Bearer token"},
    }

