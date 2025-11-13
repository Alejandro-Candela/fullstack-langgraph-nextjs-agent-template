"""Memory and checkpointing for LangGraph agent."""

import logging
import sys
import asyncio
from typing import List, Optional

from langchain_core.messages import BaseMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

from app.config import settings

# Fix para Windows: usar SelectorEventLoop para compatibilidad con psycopg async
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logger = logging.getLogger(__name__)

# Global connection pool for async checkpointer
_connection_pool: Optional[AsyncConnectionPool] = None
_checkpointer: Optional[AsyncPostgresSaver] = None


def get_connection_string() -> str:
    """Get the PostgreSQL connection string for psycopg."""
    connection_string = settings.database_url_with_ssl
    
    # Convert asyncpg URL back to standard postgresql://
    if connection_string.startswith("postgresql+asyncpg://"):
        connection_string = connection_string.replace("postgresql+asyncpg://", "postgresql://", 1)
    
    return connection_string


async def create_postgres_checkpointer() -> AsyncPostgresSaver:
    """
    Create an AsyncPostgresSaver instance using a connection pool.
    
    Returns:
        AsyncPostgresSaver instance for agent state persistence.
    """
    global _connection_pool
    
    connection_string = get_connection_string()
    
    # Create an async connection pool if it doesn't exist
    if _connection_pool is None:
        _connection_pool = AsyncConnectionPool(
            conninfo=connection_string,
            min_size=1,
            max_size=10,
            kwargs={"autocommit": True},  # Required for CREATE INDEX CONCURRENTLY
        )
        await _connection_pool.open()
        logger.info("PostgreSQL async connection pool created")
    
    # Create async checkpointer with the pool
    checkpointer = AsyncPostgresSaver(_connection_pool)
    
    # Setup creates the necessary tables
    try:
        await checkpointer.setup()
        logger.info("PostgreSQL async checkpointer initialized and setup completed")
    except Exception as e:
        logger.warning(f"Checkpointer setup warning (may already exist): {e}")
    
    return checkpointer


async def get_checkpointer() -> AsyncPostgresSaver:
    """
    Get or create the global async checkpointer instance.
    
    Returns:
        Global AsyncPostgresSaver instance.
    """
    global _checkpointer
    if _checkpointer is None:
        _checkpointer = await create_postgres_checkpointer()
    return _checkpointer


async def get_history(thread_id: str) -> List[BaseMessage]:
    """
    Retrieve the message history for a specific thread.
    
    Args:
        thread_id: The ID of the thread to retrieve history for.
        
    Returns:
        List of messages associated with the thread.
    """
    try:
        checkpointer = await get_checkpointer()
        
        # Get the latest checkpoint for this thread (using async method)
        checkpoint = await checkpointer.aget({"configurable": {"thread_id": thread_id}})
        
        if checkpoint and "channel_values" in checkpoint:
            messages = checkpoint["channel_values"].get("messages", [])
            return messages if isinstance(messages, list) else []
        
        return []
        
    except Exception as e:
        logger.error(f"Failed to get history for thread {thread_id}: {e}")
        return []

