# state.py

from typing import TypedDict
from typing import Annotated
from typing import Optional

from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    # full conversation history
    messages: Annotated[list, add_messages]

    # classified route
    intent: Optional[str]

    # retrieved FAQ context
    rag_context: Optional[str]

    # tool outputs
    tool_result: Optional[str]

    # human escalation response
    human_response: Optional[str]