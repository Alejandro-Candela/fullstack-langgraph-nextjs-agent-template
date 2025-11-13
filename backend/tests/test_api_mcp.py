"""Test MCP server API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_stdio_mcp_server(client: AsyncClient, sample_mcp_server_stdio):
    """Test creating a stdio MCP server."""
    response = await client.post("/api/mcp-servers", json=sample_mcp_server_stdio)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_mcp_server_stdio["name"]
    assert data["type"] == "stdio"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_http_mcp_server(client: AsyncClient, sample_mcp_server_http):
    """Test creating an HTTP MCP server."""
    response = await client.post("/api/mcp-servers", json=sample_mcp_server_http)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_mcp_server_http["name"]
    assert data["type"] == "http"
    assert data["url"] == sample_mcp_server_http["url"]


@pytest.mark.asyncio
async def test_list_mcp_servers(client: AsyncClient, sample_mcp_server_stdio):
    """Test listing MCP servers."""
    # Create a server first
    await client.post("/api/mcp-servers", json=sample_mcp_server_stdio)
    
    # List servers
    response = await client.get("/api/mcp-servers")
    
    assert response.status_code == 200
    data = response.json()
    assert "servers" in data
    assert "total" in data
    assert len(data["servers"]) > 0


@pytest.mark.asyncio
async def test_get_mcp_server(client: AsyncClient, sample_mcp_server_stdio):
    """Test getting a specific MCP server."""
    # Create server
    create_response = await client.post("/api/mcp-servers", json=sample_mcp_server_stdio)
    server_id = create_response.json()["id"]
    
    # Get server
    response = await client.get(f"/api/mcp-servers/{server_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == server_id
    assert data["name"] == sample_mcp_server_stdio["name"]


@pytest.mark.asyncio
async def test_update_mcp_server(client: AsyncClient, sample_mcp_server_stdio):
    """Test updating an MCP server."""
    # Create server
    create_response = await client.post("/api/mcp-servers", json=sample_mcp_server_stdio)
    server_id = create_response.json()["id"]
    
    # Update server
    update_data = {"enabled": False}
    response = await client.put(f"/api/mcp-servers/{server_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["enabled"] is False


@pytest.mark.asyncio
async def test_delete_mcp_server(client: AsyncClient, sample_mcp_server_stdio):
    """Test deleting an MCP server."""
    # Create server
    create_response = await client.post("/api/mcp-servers", json=sample_mcp_server_stdio)
    server_id = create_response.json()["id"]
    
    # Delete server
    response = await client.delete(f"/api/mcp-servers/{server_id}")
    
    assert response.status_code == 204
    
    # Verify deleted
    get_response = await client.get(f"/api/mcp-servers/{server_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_duplicate_server_name(client: AsyncClient, sample_mcp_server_stdio):
    """Test creating duplicate server names."""
    # Create first server
    await client.post("/api/mcp-servers", json=sample_mcp_server_stdio)
    
    # Try to create duplicate
    response = await client.post("/api/mcp-servers", json=sample_mcp_server_stdio)
    
    assert response.status_code == 400

