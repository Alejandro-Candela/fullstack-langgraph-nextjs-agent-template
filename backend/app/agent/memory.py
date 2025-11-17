"""Memory and checkpointing for LangGraph agent."""

import logging
from typing import List, Optional

from langchain_core.messages import BaseMessage
from langgraph.checkpoint.postgres import PostgresSaver

from app.config import settings

logger = logging.getLogger(__name__)

# Global checkpointer instance
_checkpointer: Optional[PostgresSaver] = None


def create_postgres_checkpointer() -> PostgresSaver:
    """
    Create a PostgresSaver instance using environment variables.
    
    Returns:
        PostgresSaver instance for agent state persistence.
    """
    connection_string = settings.database_url_with_ssl
    
    # LangGraph PostgresSaver uses psycopg (sync), not asyncpg
    # Convert asyncpg URL back to standard postgresql://
    if connection_string.startswith("postgresql+asyncpg://"):
        connection_string = connection_string.replace("postgresql+asyncpg://", "postgresql://", 1)
    
    checkpointer = PostgresSaver.from_conn_string(connection_string)
    
    # Setup the checkpointer (creates tables if needed)
    checkpointer.setup()
    
    logger.info("PostgreSQL checkpointer initialized")
    return checkpointer


def get_checkpointer() -> PostgresSaver:
    """
    Get or create the global checkpointer instance.
    
    Returns:
        Global PostgresSaver instance.
    """
    global _checkpointer
    if _checkpointer is None:
        _checkpointer = create_postgres_checkpointer()
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
        checkpointer = get_checkpointer()
        
        # Get the latest checkpoint for this thread
        checkpoint = checkpointer.get({"configurable": {"thread_id": thread_id}})
        
        if checkpoint and "channel_values" in checkpoint:
            messages = checkpoint["channel_values"].get("messages", [])
            return messages if isinstance(messages, list) else []
        
        return []
        
    except Exception as e:
        logger.error(f"Failed to get history for thread {thread_id}: {e}")
        return []

