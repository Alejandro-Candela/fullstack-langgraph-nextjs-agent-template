"""MCP Server CRUD endpoints."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.mcp_server import MCPServer
from app.schemas.mcp import (
    MCPServerCreate,
    MCPServerRead,
    MCPServerUpdate,
    MCPServerListResponse,
    MCPToolsResponse,
    MCPToolInfo,
)
from app.agent.mcp import get_mcp_tools

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=MCPServerListResponse)
async def list_mcp_servers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    List all MCP servers.
    
    Args:
        skip: Number of records to skip (pagination).
        limit: Maximum number of records to return.
        
    Returns:
        List of MCP servers with total count.
    """
    result = await db.execute(
        select(MCPServer)
        .order_by(MCPServer.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    servers = result.scalars().all()
    
    count_result = await db.execute(select(func.count(MCPServer.id)))
    total = count_result.scalar() or 0
    
    server_reads = [
        MCPServerRead(
            id=s.id,
            name=s.name,
            type=s.type.value,
            enabled=s.enabled,
            command=s.command,
            args=s.args,
            env=s.env,
            url=s.url,
            headers=s.headers,
            createdAt=s.created_at,
            updatedAt=s.updated_at,
        )
        for s in servers
    ]
    
    return MCPServerListResponse(servers=server_reads, total=total)


@router.get("/tools", response_model=MCPToolsResponse, tags=["tools"])
async def list_mcp_tools():
    """
    List all available tools from enabled MCP servers.
    
    Returns:
        List of available tools with server information.
    """
    tools = await get_mcp_tools()
    
    tool_infos = [
        MCPToolInfo(
            name=tool.name,
            description=tool.description if hasattr(tool, "description") else None,
            server="unknown",  # TODO: Extract server name if available
            schema=tool.args if hasattr(tool, "args") else None,
        )
        for tool in tools
    ]
    
    return MCPToolsResponse(tools=tool_infos, total=len(tool_infos))


@router.get("/{server_id}", response_model=MCPServerRead)
async def get_mcp_server(
    server_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific MCP server by ID.
    
    Args:
        server_id: MCP server ID.
        
    Returns:
        MCP server details.
        
    Raises:
        HTTPException: If server not found.
    """
    result = await db.execute(
        select(MCPServer).where(MCPServer.id == server_id)
    )
    server = result.scalar_one_or_none()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MCP Server {server_id} not found",
        )
    
    return MCPServerRead(
        id=server.id,
        name=server.name,
        type=server.type.value,
        enabled=server.enabled,
        command=server.command,
        args=server.args,
        env=server.env,
        url=server.url,
        headers=server.headers,
        createdAt=server.created_at,
        updatedAt=server.updated_at,
    )


@router.post("", response_model=MCPServerRead, status_code=status.HTTP_201_CREATED)
async def create_mcp_server(
    server_data: MCPServerCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new MCP server configuration.
    
    Args:
        server_data: MCP server creation data.
        
    Returns:
        Created MCP server.
        
    Raises:
        HTTPException: If server with same name already exists.
    """
    # Check if name already exists
    result = await db.execute(
        select(MCPServer).where(MCPServer.name == server_data.name)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"MCP Server with name '{server_data.name}' already exists",
        )
    
    # Create server
    server = MCPServer(
        name=server_data.name,
        type=server_data.type,
        enabled=server_data.enabled,
        command=server_data.command,
        args=server_data.args,
        env=server_data.env,
        url=server_data.url,
        headers=server_data.headers,
    )
    
    db.add(server)
    await db.commit()
    await db.refresh(server)
    
    logger.info(f"Created MCP server: {server.name}")
    
    return MCPServerRead(
        id=server.id,
        name=server.name,
        type=server.type.value,
        enabled=server.enabled,
        command=server.command,
        args=server.args,
        env=server.env,
        url=server.url,
        headers=server.headers,
        createdAt=server.created_at,
        updatedAt=server.updated_at,
    )


@router.put("/{server_id}", response_model=MCPServerRead)
async def update_mcp_server(
    server_id: str,
    server_data: MCPServerUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an MCP server configuration.
    
    Args:
        server_id: MCP server ID to update.
        server_data: Update data.
        
    Returns:
        Updated MCP server.
        
    Raises:
        HTTPException: If server not found.
    """
    result = await db.execute(
        select(MCPServer).where(MCPServer.id == server_id)
    )
    server = result.scalar_one_or_none()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MCP Server {server_id} not found",
        )
    
    # Update fields
    update_data = server_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(server, field, value)
    
    await db.commit()
    await db.refresh(server)
    
    logger.info(f"Updated MCP server: {server.name}")
    
    return MCPServerRead(
        id=server.id,
        name=server.name,
        type=server.type.value,
        enabled=server.enabled,
        command=server.command,
        args=server.args,
        env=server.env,
        url=server.url,
        headers=server.headers,
        createdAt=server.created_at,
        updatedAt=server.updated_at,
    )


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mcp_server(
    server_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete an MCP server configuration.
    
    Args:
        server_id: MCP server ID to delete.
        
    Raises:
        HTTPException: If server not found.
    """
    result = await db.execute(
        select(MCPServer).where(MCPServer.id == server_id)
    )
    server = result.scalar_one_or_none()
    
    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MCP Server {server_id} not found",
        )
    
    await db.delete(server)
    await db.commit()
    
    logger.info(f"Deleted MCP server: {server.name}")
    return None

