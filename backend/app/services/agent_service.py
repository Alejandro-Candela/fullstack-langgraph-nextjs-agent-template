"""Agent service for streaming responses and managing agent state."""

import logging
from typing import AsyncGenerator, Optional, List

from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, AIMessageChunk
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command

from app.agent.builder import AgentBuilder
from app.agent.memory import get_checkpointer, get_history
from app.agent.mcp import get_mcp_tools
from app.config import settings
from app.schemas.message import MessageResponse, MessageOptions, AIMessageData, ToolCall
from app.database import AsyncSessionLocal
from app.services.thread_service import ensure_thread

logger = logging.getLogger(__name__)

# Global agent instance cache
_agent_cache = {}


def _get_llm_instance(model: Optional[str] = None):
    """
    Get language model instance based on model name.
    
    Args:
        model: Model name (e.g., "gpt-4", "gemini-pro")
        
    Returns:
        Language model instance.
    """
    model = model or "gpt-4o-mini"
    
    if model.startswith("gpt") or model.startswith("o1"):
        return ChatOpenAI(
            model=model,
            api_key=settings.openai_api_key,
            streaming=True,
        )
    elif model.startswith("gemini"):
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.google_api_key,
        )
    else:
        # Default to OpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.openai_api_key,
            streaming=True,
        )


async def _ensure_agent(
    model: Optional[str] = None,
    tools: Optional[List[str]] = None,
    approve_all_tools: bool = False,
):
    """
    Ensure agent is created and cached.
    
    Args:
        model: Model name to use.
        tools: List of specific tools to enable.
        approve_all_tools: Auto-approve all tool calls.
        
    Returns:
        Compiled agent graph.
    """
    cache_key = f"{model}_{tools}_{approve_all_tools}"
    
    if cache_key in _agent_cache:
        return _agent_cache[cache_key]
    
    # Get LLM
    llm = _get_llm_instance(model)
    
    # Get tools from MCP
    mcp_tools = await get_mcp_tools()
    
    # Filter tools if specific list provided
    if tools and len(tools) > 0:
        mcp_tools = [t for t in mcp_tools if t.name in tools]
    
    # Get checkpointer
    checkpointer = get_checkpointer()
    
    # Build agent
    builder = AgentBuilder(
        tools=mcp_tools,
        llm=llm,
        prompt="",
        checkpointer=checkpointer,
        approve_all_tools=approve_all_tools,
    )
    
    agent = builder.build()
    _agent_cache[cache_key] = agent
    
    logger.info(f"Agent created with model={model}, tools={len(mcp_tools)}")
    return agent


def _process_ai_message(message: BaseMessage) -> Optional[MessageResponse]:
    """
    Process an AI message and convert to MessageResponse.
    
    Args:
        message: AI message to process.
        
    Returns:
        MessageResponse or None if message should be skipped.
    """
    if not isinstance(message, (AIMessage, AIMessageChunk)):
        return None
    
    # Check if this is a tool call
    has_tool_call = (
        hasattr(message, "tool_calls")
        and message.tool_calls
        and len(message.tool_calls) > 0
    )
    
    if has_tool_call:
        # Return full AI message data for tool calls
        tool_calls = [
            ToolCall(
                id=tc["id"],
                name=tc["name"],
                args=tc["args"],
                type=tc.get("type", "function"),
            )
            for tc in message.tool_calls
        ]
        
        return MessageResponse(
            type="ai",
            data=AIMessageData(
                id=message.id or str(id(message)),
                content=message.content if isinstance(message.content, str) else "",
                tool_calls=tool_calls,
                additional_kwargs=getattr(message, "additional_kwargs", None),
                response_metadata=getattr(message, "response_metadata", None),
            ),
        )
    else:
        # Handle regular text content
        if isinstance(message.content, str):
            text = message.content
        elif isinstance(message.content, list):
            # Extract text from content blocks
            text = "".join(
                c if isinstance(c, str) else c.get("text", "")
                for c in message.content
            )
        else:
            text = str(message.content) if message.content else ""
        
        # Only return if we have actual text
        if text.strip():
            return MessageResponse(
                type="ai",
                data=AIMessageData(
                    id=message.id or str(id(message)),
                    content=text,
                ),
            )
    
    return None


async def stream_response(
    thread_id: str,
    user_text: str,
    opts: Optional[MessageOptions] = None,
) -> AsyncGenerator[MessageResponse, None]:
    """
    Stream agent responses for a user message.
    
    Args:
        thread_id: Thread ID for the conversation.
        user_text: User's message text.
        opts: Optional message options (model, tools, approval settings).
        
    Yields:
        MessageResponse objects as they are generated.
    """
    opts = opts or MessageOptions()
    
    # Ensure thread exists in database
    async with AsyncSessionLocal() as session:
        await ensure_thread(session, thread_id, user_text)
    
    # Determine inputs based on options
    if opts.allow_tool:
        # This is a tool approval response
        inputs = Command(
            resume={
                "action": "continue" if opts.allow_tool == "allow" else "update",
                "data": {},
            }
        )
    else:
        # Regular user message
        inputs = {"messages": [HumanMessage(content=user_text)]}
    
    # Get or create agent
    agent = await _ensure_agent(
        model=opts.model,
        tools=opts.tools,
        approve_all_tools=opts.approve_all_tools,
    )
    
    # Stream agent responses
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        async for chunk in agent.astream(inputs, config, stream_mode="updates"):
            if not chunk:
                continue
            
            # Handle different chunk formats
            # LangGraph can return: dict with node updates
            if isinstance(chunk, dict):
                # Look for agent node updates
                if "agent" in chunk:
                    agent_data = chunk["agent"]
                    if "messages" in agent_data:
                        messages = agent_data["messages"]
                        if not isinstance(messages, list):
                            messages = [messages]
                        
                        for msg in messages:
                            processed = _process_ai_message(msg)
                            if processed:
                                yield processed
    
    except Exception as e:
        logger.error(f"Error streaming response: {e}", exc_info=True)
        raise


async def fetch_thread_history(thread_id: str) -> List[MessageResponse]:
    """
    Fetch conversation history for a thread.
    
    Args:
        thread_id: Thread ID to fetch history for.
        
    Returns:
        List of message responses.
    """
    try:
        history = await get_history(thread_id)
        
        # Convert messages to MessageResponse format
        responses: List[MessageResponse] = []
        
        for msg in history:
            msg_dict = msg.dict() if hasattr(msg, "dict") else {}
            
            # This is a simplified conversion - adjust based on actual message types
            if msg_dict.get("type") == "human":
                responses.append(MessageResponse(
                    type="human",
                    data={"id": msg.id or str(id(msg)), "content": msg.content}
                ))
            elif msg_dict.get("type") == "ai":
                processed = _process_ai_message(msg)
                if processed:
                    responses.append(processed)
        
        return responses
        
    except Exception as e:
        logger.error(f"Failed to fetch thread history: {e}")
        return []

