"""Thread service for managing conversation threads."""

import logging
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.thread import Thread
from app.schemas.thread import ThreadCreate, ThreadUpdate

logger = logging.getLogger(__name__)


async def ensure_thread(
    session: AsyncSession,
    thread_id: str,
    initial_message: str = ""
) -> Thread:
    """
    Ensure a thread exists, creating it if necessary.
    
    Args:
        session: Database session.
        thread_id: Thread ID to ensure.
        initial_message: Initial message to use as title if creating new thread.
        
    Returns:
        Thread instance.
    """
    # Check if thread exists
    result = await session.execute(
        select(Thread).where(Thread.id == thread_id)
    )
    thread = result.scalar_one_or_none()
    
    if thread:
        return thread
    
    # Create new thread
    title = initial_message[:50] if initial_message else "New Conversation"
    thread = Thread(
        id=thread_id,
        title=title,
    )
    
    session.add(thread)
    await session.commit()
    await session.refresh(thread)
    
    logger.info(f"Created new thread: {thread_id}")
    return thread


async def get_thread(session: AsyncSession, thread_id: str) -> Optional[Thread]:
    """
    Get a thread by ID.
    
    Args:
        session: Database session.
        thread_id: Thread ID.
        
    Returns:
        Thread instance or None if not found.
    """
    result = await session.execute(
        select(Thread).where(Thread.id == thread_id)
    )
    return result.scalar_one_or_none()


async def list_threads(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Thread]:
    """
    List all threads ordered by update time.
    
    Args:
        session: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        
    Returns:
        List of threads.
    """
    result = await session.execute(
        select(Thread)
        .order_by(Thread.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def create_thread(session: AsyncSession, thread_data: ThreadCreate) -> Thread:
    """
    Create a new thread.
    
    Args:
        session: Database session.
        thread_data: Thread creation data.
        
    Returns:
        Created thread.
    """
    thread = Thread(
        id=str(uuid4()),
        title=thread_data.title,
    )
    
    session.add(thread)
    await session.commit()
    await session.refresh(thread)
    
    logger.info(f"Created thread: {thread.id}")
    return thread


async def update_thread(
    session: AsyncSession,
    thread_id: str,
    thread_data: ThreadUpdate
) -> Optional[Thread]:
    """
    Update a thread.
    
    Args:
        session: Database session.
        thread_id: Thread ID to update.
        thread_data: Update data.
        
    Returns:
        Updated thread or None if not found.
    """
    thread = await get_thread(session, thread_id)
    
    if not thread:
        return None
    
    if thread_data.title is not None:
        thread.title = thread_data.title
    
    await session.commit()
    await session.refresh(thread)
    
    logger.info(f"Updated thread: {thread_id}")
    return thread


async def delete_thread(session: AsyncSession, thread_id: str) -> bool:
    """
    Delete a thread.
    
    Args:
        session: Database session.
        thread_id: Thread ID to delete.
        
    Returns:
        True if deleted, False if not found.
    """
    thread = await get_thread(session, thread_id)
    
    if not thread:
        return False
    
    await session.delete(thread)
    await session.commit()
    
    logger.info(f"Deleted thread: {thread_id}")
    return True

