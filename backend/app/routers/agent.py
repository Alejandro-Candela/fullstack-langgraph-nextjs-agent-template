"""Agent endpoints for streaming and history."""

import logging
import json
from typing import Optional

from fastapi import APIRouter, Query, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.message import MessageOptions, MessageResponse
from app.services.agent_service import stream_response, fetch_thread_history

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/stream")
async def stream_agent_response(
    content: str = Query(..., description="User message content"),
    threadId: str = Query(..., description="Thread ID"),
    model: Optional[str] = Query(None, description="Model to use"),
    allowTool: Optional[str] = Query(None, description="Tool approval action"),
    tools: Optional[str] = Query(None, description="Comma-separated tool names"),
    approveAllTools: bool = Query(False, description="Auto-approve all tools"),
):
    """
    Stream agent responses via Server-Sent Events (SSE).
    
    Query params:
        - content: User message text
        - threadId: Conversation thread ID
        - model: Optional model name (e.g., "gpt-4", "gemini-pro")
        - allowTool: Tool approval action ("allow" or "deny")
        - tools: Comma-separated list of specific tools to enable
        - approveAllTools: Auto-approve all tool calls without human review
    """
    # Parse tools parameter
    tools_list = None
    if tools:
        tools_list = [t.strip() for t in tools.split(",") if t.strip()]
    
    # Create options
    opts = MessageOptions(
        model=model,
        tools=tools_list,
        allow_tool=allowTool if allowTool in ["allow", "deny"] else None,
        approve_all_tools=approveAllTools,
    )
    
    async def event_generator():
        """Generate SSE events."""
        try:
            # Send initial connection message
            yield ": connected\n\n"
            
            logger.info(f"Starting stream for thread={threadId}, content={content[:50]}...")
            
            # Stream agent responses
            chunk_count = 0
            async for message_response in stream_response(
                thread_id=threadId,
                user_text=content,
                opts=opts,
            ):
                # Only forward AI/tool chunks
                if message_response.type in ["ai", "tool"]:
                    chunk_count += 1
                    data = json.dumps(message_response.model_dump())
                    logger.debug(f"Sending chunk {chunk_count}: {data[:100]}...")
                    yield f"data: {data}\n\n"
            
            logger.info(f"Stream completed. Sent {chunk_count} chunks.")
            
            # Signal completion
            yield "event: done\ndata: {}\n\n"
            
        except Exception as e:
            logger.error(f"Stream error: {e}", exc_info=True)
            error_data = json.dumps({
                "message": str(e),
                "threadId": threadId,
            })
            yield f"event: error\ndata: {error_data}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Transfer-Encoding": "chunked",
        },
    )


@router.get("/history/{thread_id}")
async def get_thread_history(
    thread_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get conversation history for a thread.
    
    Args:
        thread_id: Thread ID to fetch history for.
        
    Returns:
        List of message responses.
    """
    history = await fetch_thread_history(thread_id)
    return {"messages": history, "total": len(history)}

