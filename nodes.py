# nodes.py

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langchain_core.messages import AIMessage

from tools import get_order_status
from tools import process_refund
from tools import get_billing_info

from rag import search_docs

from state import AgentState

from langgraph.types import interrupt

from dotenv import load_dotenv

import re
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

SYSTEM_PROMPT = """
You are a helpful customer support agent.

You are friendly, concise, and professional.

You have access to:
- Order status lookups
- Refund processing
- Billing information
- FAQ knowledge base

If extra context is provided, use it to answer accurately.

Never invent order details or billing info.

If the user is extremely frustrated, threatening legal action,
or needs complex support, respond with exactly:

ESCALATE

and nothing else.

Keep answers short and conversational.
"""


def call_llm(state: AgentState) -> AgentState:

    print("LLM NODE")

    messages = state["messages"]

    context_parts = []

    if state.get("rag_context"):

        context_parts.append(
            f"[FAQ CONTEXT]\n{state['rag_context']}"
        )

    if state.get("tool_result"):

        context_parts.append(
            f"[TOOL RESULT]\n{state['tool_result']}"
        )

    system_content = SYSTEM_PROMPT

    if context_parts:

        system_content += "\n\n" + "\n\n".join(context_parts)

    full_messages = [
        SystemMessage(content=system_content)
    ] + messages

    response = llm.invoke(full_messages)

    return {
        "messages": [response]
    }


def call_tools(state: AgentState) -> AgentState:

    print("TOOLS NODE")

    last_message = state["messages"][-1].content.lower()

    result = ""

    # order status
    if (
        "order" in last_message
        or "status" in last_message
        or "track" in last_message
    ):

        match = re.search(
            r"\b([A-Z]{2,3}-?\d{4,8}|\d{6,10})\b",
            state["messages"][-1].content
        )

        order_id = match.group(0) if match else "ORD12345"

        result = get_order_status(order_id)

    # refund
    elif (
        "refund" in last_message
        or "return" in last_message
        or "money back" in last_message
    ):

        match = re.search(
            r"\b([A-Z]{2,3}-?\d{4,8}|\d{6,10})\b",
            state["messages"][-1].content
        )

        order_id = match.group(0) if match else "ORD12345"

        result = process_refund(order_id)

    # billing
    elif (
        "billing" in last_message
        or "invoice" in last_message
        or "charge" in last_message
        or "payment" in last_message
    ):

        result = get_billing_info()

    else:

        result = "No matching tool found."

    return {
        "tool_result": result
    }


def call_rag(state: AgentState) -> AgentState:

    print("RAG NODE")

    query = state["messages"][-1].content

    docs = search_docs(query)

    context = "\n\n".join(docs)

    return {
        "rag_context": context
    }


def escalate_to_human(state: AgentState) -> AgentState:

    print("HUMAN NODE")

    human_input = interrupt(
        "This conversation needs human review."
    )

    return {
        "messages": [
            AIMessage(
                content=f"Human agent response: {human_input}"
            )
        ]
    }