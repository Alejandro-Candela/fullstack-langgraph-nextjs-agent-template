"""Agent builder for creating LangGraph StateGraph with tool approval workflow."""

import logging
from typing import List, Optional, Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.types import Command, interrupt

from app.agent.prompt import get_system_prompt

logger = logging.getLogger(__name__)


class AgentBuilder:
    """
    Builder for creating a LangGraph agent with human-in-the-loop tool approval.
    
    The agent follows this flow:
    START → agent → tool_approval (if tools needed) → tools → agent → END
    """
    
    def __init__(
        self,
        tools: List[BaseTool],
        llm: BaseChatModel,
        prompt: str = "",
        checkpointer: Optional[BaseCheckpointSaver] = None,
        approve_all_tools: bool = False,
    ):
        """
        Initialize the agent builder.
        
        Args:
            tools: List of tools available to the agent.
            llm: Language model to use for the agent.
            prompt: System prompt for the agent.
            checkpointer: Checkpointer for state persistence.
            approve_all_tools: If True, auto-approve all tool calls without human review.
        """
        if not llm:
            raise ValueError("Language model (llm) is required")
        
        self.tools = tools or []
        self.tool_node = ToolNode(self.tools)
        self.system_prompt = get_system_prompt(prompt)
        self.model = llm
        self.checkpointer = checkpointer
        self.approve_all_tools = approve_all_tools
    
    def _should_approve_tool(self, state: MessagesState) -> Literal["tool_approval", "__end__"]:
        """
        Conditional edge: determine if we need tool approval or can end.
        
        Args:
            state: Current graph state.
            
        Returns:
            Next node name: "tool_approval" if tools detected, END otherwise.
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        if (
            isinstance(last_message, AIMessage)
            and hasattr(last_message, "tool_calls")
            and last_message.tool_calls
            and len(last_message.tool_calls) > 0
        ):
            return "tool_approval"
        
        return END
    
    def _approve_tool_call(self, state: MessagesState) -> Command:
        """
        Tool approval node: pause for human review unless auto-approval enabled.
        
        Args:
            state: Current graph state.
            
        Returns:
            Command to continue to tools, update and continue, or return to agent.
        """
        # If auto-approve is enabled, skip human review
        if self.approve_all_tools:
            return Command(goto="tools")
        
        messages = state["messages"]
        last_message = messages[-1]
        
        if (
            isinstance(last_message, AIMessage)
            and hasattr(last_message, "tool_calls")
            and last_message.tool_calls
            and len(last_message.tool_calls) > 0
        ):
            tool_call = last_message.tool_calls[-1]
            
            # Interrupt for human review
            human_review = interrupt(
                {
                    "question": "Is this correct?",
                    "toolCall": {
                        "id": tool_call["id"],
                        "name": tool_call["name"],
                        "args": tool_call["args"],
                    },
                }
            )
            
            review_action = human_review.get("action", "continue")
            review_data = human_review.get("data", {})
            
            if review_action == "continue":
                # Approve and continue to tools
                return Command(goto="tools")
            
            elif review_action == "update":
                # Update tool call arguments and continue
                updated_message = AIMessage(
                    content=last_message.content,
                    tool_calls=[
                        {
                            "id": tool_call["id"],
                            "name": tool_call["name"],
                            "args": review_data,
                        }
                    ],
                    id=last_message.id,
                )
                return Command(
                    goto="tools",
                    update={"messages": [updated_message]},
                )
            
            elif review_action == "feedback":
                # Send feedback and return to agent
                tool_message = ToolMessage(
                    name=tool_call["name"],
                    content=str(review_data),
                    tool_call_id=tool_call["id"],
                )
                return Command(
                    goto="agent",
                    update={"messages": [tool_message]},
                )
            
            raise ValueError(f"Invalid review action: {review_action}")
        
        # No tool calls found, return to agent
        return Command(goto="agent")
    
    def _call_model(self, state: MessagesState) -> dict:
        """
        Agent node: call the language model with tools bound.
        
        Args:
            state: Current graph state.
            
        Returns:
            Updated state with AI response.
        """
        if not self.model or not hasattr(self.model, "bind_tools"):
            raise ValueError("Invalid or missing language model (llm)")
        
        # Add system prompt (not duplicated in messages)
        messages = [SystemMessage(content=self.system_prompt), *state["messages"]]
        
        # Bind tools and invoke model
        model_with_tools = self.model.bind_tools(self.tools)
        response = model_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    def build(self):
        """
        Build and compile the StateGraph.
        
        Returns:
            Compiled graph ready for execution.
        """
        # Create state graph
        state_graph = StateGraph(MessagesState)
        
        # Add nodes
        state_graph.add_node("agent", self._call_model)
        state_graph.add_node("tools", self.tool_node)
        state_graph.add_node("tool_approval", self._approve_tool_call)
        
        # Add edges
        state_graph.add_edge(START, "agent")
        state_graph.add_conditional_edges(
            "agent",
            self._should_approve_tool,
            {
                "tool_approval": "tool_approval",
                END: END,
            },
        )
        state_graph.add_edge("tools", "agent")
        
        # Compile with checkpointer
        compiled_graph = state_graph.compile(checkpointer=self.checkpointer)
        
        logger.info(f"Agent built with {len(self.tools)} tools, approve_all={self.approve_all_tools}")
        return compiled_graph

