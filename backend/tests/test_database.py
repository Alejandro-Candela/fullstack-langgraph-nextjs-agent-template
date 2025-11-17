"""Test database models and operations."""

import pytest
from sqlalchemy import select

from app.models.thread import Thread
from app.models.mcp_server import MCPServer, MCPServerType


@pytest.mark.asyncio
async def test_create_thread(db_session):
    """Test creating a thread."""
    thread = Thread(
        id="test-thread-1",
        title="Test Thread",
    )
    
    db_session.add(thread)
    await db_session.commit()
    await db_session.refresh(thread)
    
    assert thread.id == "test-thread-1"
    assert thread.title == "Test Thread"
    assert thread.created_at is not None
    assert thread.updated_at is not None


@pytest.mark.asyncio
async def test_create_stdio_mcp_server(db_session):
    """Test creating a stdio MCP server."""
    server = MCPServer(
        name="test-server",
        type=MCPServerType.stdio,
        enabled=True,
        command="npx",
        args=["@modelcontextprotocol/server-filesystem", "/tmp"],
        env={"LOG_LEVEL": "info"},
    )
    
    db_session.add(server)
    await db_session.commit()
    await db_session.refresh(server)
    
    assert server.name == "test-server"
    assert server.type == MCPServerType.stdio
    assert server.command == "npx"
    assert server.enabled is True


@pytest.mark.asyncio
async def test_create_http_mcp_server(db_session):
    """Test creating an HTTP MCP server."""
    server = MCPServer(
        name="test-http",
        type=MCPServerType.http,
        enabled=True,
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer token"},
    )
    
    db_session.add(server)
    await db_session.commit()
    await db_session.refresh(server)
    
    assert server.name == "test-http"
    assert server.type == MCPServerType.http
    assert server.url == "https://api.example.com/mcp"


@pytest.mark.asyncio
async def test_query_enabled_servers(db_session):
    """Test querying enabled MCP servers."""
    # Create enabled server
    server1 = MCPServer(
        name="enabled-server",
        type=MCPServerType.stdio,
        enabled=True,
        command="test",
    )
    
    # Create disabled server
    server2 = MCPServer(
        name="disabled-server",
        type=MCPServerType.stdio,
        enabled=False,
        command="test",
    )
    
    db_session.add_all([server1, server2])
    await db_session.commit()
    
    # Query enabled servers
    result = await db_session.execute(
        select(MCPServer).where(MCPServer.enabled == True)  # noqa: E712
    )
    servers = result.scalars().all()
    
    assert len(servers) == 1
    assert servers[0].name == "enabled-server"

