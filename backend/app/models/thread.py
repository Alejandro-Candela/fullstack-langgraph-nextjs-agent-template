"""Thread model for storing conversation metadata."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Thread(Base):
    """
    Thread model - stores minimal metadata for conversation threads.
    
    Actual conversation history is stored in LangGraph checkpoints for efficient state management.
    """
    
    __tablename__ = "Thread"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String, nullable=False)
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
        return f"<Thread(id={self.id}, title={self.title})>"

