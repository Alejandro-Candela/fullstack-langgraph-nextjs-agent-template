"""Test thread API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_thread(client: AsyncClient, sample_thread_data):
    """Test creating a new thread."""
    response = await client.post("/api/agent/threads", json=sample_thread_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_thread_data["title"]
    assert "id" in data
    assert "createdAt" in data


@pytest.mark.asyncio
async def test_list_threads(client: AsyncClient, sample_thread_data):
    """Test listing threads."""
    # Create a thread first
    await client.post("/api/agent/threads", json=sample_thread_data)
    
    # List threads
    response = await client.get("/api/agent/threads")
    
    assert response.status_code == 200
    data = response.json()
    assert "threads" in data
    assert "total" in data
    assert len(data["threads"]) > 0


@pytest.mark.asyncio
async def test_get_thread(client: AsyncClient, sample_thread_data):
    """Test getting a specific thread."""
    # Create thread
    create_response = await client.post("/api/agent/threads", json=sample_thread_data)
    thread_id = create_response.json()["id"]
    
    # Get thread
    response = await client.get(f"/api/agent/threads/{thread_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == thread_id
    assert data["title"] == sample_thread_data["title"]


@pytest.mark.asyncio
async def test_update_thread(client: AsyncClient, sample_thread_data):
    """Test updating a thread."""
    # Create thread
    create_response = await client.post("/api/agent/threads", json=sample_thread_data)
    thread_id = create_response.json()["id"]
    
    # Update thread
    update_data = {"title": "Updated Title"}
    response = await client.put(f"/api/agent/threads/{thread_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_thread(client: AsyncClient, sample_thread_data):
    """Test deleting a thread."""
    # Create thread
    create_response = await client.post("/api/agent/threads", json=sample_thread_data)
    thread_id = create_response.json()["id"]
    
    # Delete thread
    response = await client.delete(f"/api/agent/threads/{thread_id}")
    
    assert response.status_code == 204
    
    # Verify deleted
    get_response = await client.get(f"/api/agent/threads/{thread_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_thread(client: AsyncClient):
    """Test getting a thread that doesn't exist."""
    response = await client.get("/api/agent/threads/nonexistent-id")
    assert response.status_code == 404

