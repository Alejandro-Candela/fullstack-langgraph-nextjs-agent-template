"""MCP server schemas for request/response validation."""

from datetime import datetime
from typing import Optional, Dict, Any, List, Literal
from pydantic import BaseModel, Field, field_validator


class MCPServerBase(BaseModel):
    """Base MCP server schema with common fields."""
    name: str
    type: Literal["stdio", "http"]
    enabled: bool = True


class MCPServerCreate(MCPServerBase):
    """Schema for creating a new MCP server."""
    # For stdio servers
    command: Optional[str] = None
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    
    # For http servers
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    
    @field_validator("command")
    @classmethod
    def validate_stdio_has_command(cls, v, values):
        """Validate that stdio servers have a command."""
        if values.data.get("type") == "stdio" and not v:
            raise ValueError("stdio servers must have a command")
        return v
    
    @field_validator("url")
    @classmethod
    def validate_http_has_url(cls, v, values):
        """Validate that http servers have a url."""
        if values.data.get("type") == "http" and not v:
            raise ValueError("http servers must have a url")
        return v


class MCPServerUpdate(BaseModel):
    """Schema for updating an MCP server."""
    name: Optional[str] = None
    type: Optional[Literal["stdio", "http"]] = None
    enabled: Optional[bool] = None
    command: Optional[str] = None
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None


class MCPServerRead(MCPServerBase):
    """Schema for reading MCP server data."""
    id: str
    command: Optional[str] = None
    args: Optional[List[str]] = None
    env: Optional[Dict[str, str]] = None
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    
    class Config:
        from_attributes = True
        populate_by_name = True


class MCPServerListResponse(BaseModel):
    """Response for listing MCP servers."""
    servers: list[MCPServerRead]
    total: int


class MCPToolInfo(BaseModel):
    """Information about an MCP tool."""
    name: str
    description: Optional[str] = None
    server: str
    schema: Optional[Dict[str, Any]] = None


class MCPToolsResponse(BaseModel):
    """Response for listing available MCP tools."""
    tools: list[MCPToolInfo]
    total: int

