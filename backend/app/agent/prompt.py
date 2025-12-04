"""System prompts for the agent."""

DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant powered by LangGraph. 

Current time: {current_time}

You have access to various tools that you can use to help users with their tasks. 
When you need to use a tool, explain what you're going to do and why it's helpful.

Always be clear, concise, and helpful in your responses. If you're unsure about something, 
it's better to acknowledge it than to make assumptions.

If a tool requires approval from the user, wait for their confirmation before proceeding."""


def get_system_prompt(custom_prompt: str = "") -> str:
    """
    Get the system prompt for the agent.
    
    Args:
        custom_prompt: Optional custom prompt to use instead of default.
        
    Returns:
        System prompt string.
    """
    from datetime import datetime
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt = custom_prompt if custom_prompt else DEFAULT_SYSTEM_PROMPT
    
    # Format with current time if placeholder exists
    if "{current_time}" in prompt:
        return prompt.format(current_time=current_time)
        
    return f"{prompt}\n\nCurrent time: {current_time}"

