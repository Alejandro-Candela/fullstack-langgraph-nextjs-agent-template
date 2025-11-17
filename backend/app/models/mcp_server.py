"""MCPServer model for storing MCP server configurations."""

from datetime import datetime
from uuid import uuid4
from enum import Enum as PyEnum

from sqlalchemy import String, DateTime, Boolean, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, Dict, List, Any

from app.database import Base


class MCPServerType(str, PyEnum):
    """MCP Server transport type."""
    stdio = "stdio"
    http = "http"


class MCPServer(Base):
    """
    MCPServer model - stores dynamic configuration of MCP servers.
    
    Supports both stdio (command-line) and HTTP-based servers with flexible JSON configuration.
    """
    
    __tablename__ = "MCPServer"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    type: Mapped[MCPServerType] = mapped_column(Enum(MCPServerType), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # For stdio servers
    command: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    args: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    env: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # For http servers
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    headers: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        "createdAt",
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updatedAt",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<MCPServer(id={self.id}, name={self.name}, type={self.type}, enabled={self.enabled})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "enabled": self.enabled,
            "command": self.command,
            "args": self.args,
            "env": self.env,
            "url": self.url,
            "headers": self.headers,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }

