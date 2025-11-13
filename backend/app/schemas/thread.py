"""Thread schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ThreadBase(BaseModel):
    """Base thread schema with common fields."""
    title: str


class ThreadCreate(ThreadBase):
    """Schema for creating a new thread."""
    pass


class ThreadUpdate(BaseModel):
    """Schema for updating a thread."""
    title: Optional[str] = None


class ThreadRead(ThreadBase):
    """Schema for reading thread data."""
    id: str
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    
    class Config:
        from_attributes = True
        populate_by_name = True


class ThreadListResponse(BaseModel):
    """Response for listing threads."""
    threads: list[ThreadRead]
    total: int

