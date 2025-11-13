"""Thread CRUD endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.thread import ThreadCreate, ThreadRead, ThreadUpdate, ThreadListResponse
from app.services.thread_service import (
    list_threads,
    get_thread,
    create_thread,
    update_thread,
    delete_thread,
)

router = APIRouter()


@router.get("/threads", response_model=ThreadListResponse)
async def list_all_threads(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    List all conversation threads.
    
    Args:
        skip: Number of records to skip (pagination).
        limit: Maximum number of records to return.
        
    Returns:
        List of threads with total count.
    """
    threads = await list_threads(db, skip=skip, limit=limit)
    thread_reads = [
        ThreadRead(
            id=t.id,
            title=t.title,
            createdAt=t.created_at,
            updatedAt=t.updated_at,
        )
        for t in threads
    ]
    
    return ThreadListResponse(threads=thread_reads, total=len(thread_reads))


@router.get("/threads/{thread_id}", response_model=ThreadRead)
async def get_thread_by_id(
    thread_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific thread by ID.
    
    Args:
        thread_id: Thread ID to retrieve.
        
    Returns:
        Thread details.
        
    Raises:
        HTTPException: If thread not found.
    """
    thread = await get_thread(db, thread_id)
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thread {thread_id} not found",
        )
    
    return ThreadRead(
        id=thread.id,
        title=thread.title,
        createdAt=thread.created_at,
        updatedAt=thread.updated_at,
    )


@router.post("/threads", response_model=ThreadRead, status_code=status.HTTP_201_CREATED)
async def create_new_thread(
    thread_data: ThreadCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new conversation thread.
    
    Args:
        thread_data: Thread creation data.
        
    Returns:
        Created thread.
    """
    thread = await create_thread(db, thread_data)
    
    return ThreadRead(
        id=thread.id,
        title=thread.title,
        createdAt=thread.created_at,
        updatedAt=thread.updated_at,
    )


@router.put("/threads/{thread_id}", response_model=ThreadRead)
async def update_thread_by_id(
    thread_id: str,
    thread_data: ThreadUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update a thread.
    
    Args:
        thread_id: Thread ID to update.
        thread_data: Update data.
        
    Returns:
        Updated thread.
        
    Raises:
        HTTPException: If thread not found.
    """
    thread = await update_thread(db, thread_id, thread_data)
    
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thread {thread_id} not found",
        )
    
    return ThreadRead(
        id=thread.id,
        title=thread.title,
        createdAt=thread.created_at,
        updatedAt=thread.updated_at,
    )


@router.delete("/threads/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thread_by_id(
    thread_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a thread.
    
    Args:
        thread_id: Thread ID to delete.
        
    Raises:
        HTTPException: If thread not found.
    """
    success = await delete_thread(db, thread_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thread {thread_id} not found",
        )
    
    return None

