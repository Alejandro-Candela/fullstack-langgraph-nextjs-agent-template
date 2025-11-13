"""Message schemas for request/response validation."""

from typing import Optional, Dict, Any, List, Union, Literal
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Tool call information."""
    id: str
    name: str
    args: Dict[str, Any]
    type: Optional[str] = "function"


class HumanMessageData(BaseModel):
    """Human message data."""
    id: str
    content: str


class AIMessageData(BaseModel):
    """AI message data with optional tool calls."""
    id: str
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    additional_kwargs: Optional[Dict[str, Any]] = None
    response_metadata: Optional[Dict[str, Any]] = None


class ToolMessageData(BaseModel):
    """Tool execution result message data."""
    id: str
    content: str
    tool_call_id: str
    name: Optional[str] = None


class ErrorMessageData(BaseModel):
    """Error message data."""
    id: str
    content: str


class MessageResponse(BaseModel):
    """
    Union type for different message responses.
    
    Discriminated union based on 'type' field.
    """
    type: Literal["human", "ai", "tool", "error"]
    data: Union[HumanMessageData, AIMessageData, ToolMessageData, ErrorMessageData]
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "type": "human",
                    "data": {"id": "msg_123", "content": "Hello, how are you?"}
                },
                {
                    "type": "ai",
                    "data": {
                        "id": "msg_456",
                        "content": "I'm doing well, thank you!",
                        "tool_calls": None
                    }
                }
            ]
        }


class MessageOptions(BaseModel):
    """Options for sending messages."""
    model: Optional[str] = None
    tools: Optional[List[str]] = None
    allow_tool: Optional[Literal["allow", "deny"]] = Field(None, alias="allowTool")
    approve_all_tools: bool = Field(False, alias="approveAllTools")
    
    class Config:
        populate_by_name = True


class StreamRequest(BaseModel):
    """Request body for streaming endpoint."""
    content: str
    thread_id: str = Field(..., alias="threadId")
    options: Optional[MessageOptions] = None
    
    class Config:
        populate_by_name = True

