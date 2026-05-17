# graph.py

from langgraph.graph import StateGraph
from langgraph.graph import END
from langgraph.checkpoint.postgres import PostgresSaver

from state import AgentState

from nodes import call_llm
from nodes import call_tools
from nodes import call_rag
from nodes import escalate_to_human

from router import route_intent

from dotenv import load_dotenv

import psycopg
import os

load_dotenv()

DB_URI = os.getenv("DATABASE_URL")


def build_graph():

    conn = psycopg.connect(DB_URI)

    checkpointer = PostgresSaver(conn)

    builder = StateGraph(AgentState)

    # nodes
    builder.add_node("llm", call_llm)
    builder.add_node("tools", call_tools)
    builder.add_node("rag", call_rag)
    builder.add_node("human", escalate_to_human)

    # entry point
    builder.set_entry_point("llm")

    # routing
    builder.add_conditional_edges(
        "llm",
        route_intent,
        {
            "tools": "tools",
            "rag": "rag",
            "human": "human",
            "end": END
        }
    )

    # after tool execution -> generate final response
    builder.add_edge("tools", "llm")

    # after rag retrieval -> generate final response
    builder.add_edge("rag", "llm")

    # human escalation ends conversation
    builder.add_edge("human", END)

    graph = builder.compile(
        checkpointer=checkpointer
    )

    return graph