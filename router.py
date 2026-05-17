# router.py

from langchain_groq import ChatGroq

from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

from dotenv import load_dotenv

load_dotenv()

router_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

CLASSIFIER_PROMPT = """
You are an intent classifier for a customer support agent.

Classify the user query into EXACTLY ONE route.

Routes:

tools
- refunds
- billing
- invoices
- order tracking
- payments
- subscriptions

rag
- FAQs
- policies
- support information
- general questions

human
- angry customers
- legal threats
- manager requests
- escalation requests

end
- greetings
- thanks
- goodbye

Return ONLY one word:
tools
rag
human
end
"""


def route_intent(state):

    print("ROUTER NODE")

    # stop graph after tool execution
    if state.get("tool_result"):

        print("ENDING AFTER TOOL")

        return "end"

    # stop graph after rag execution
    if state.get("rag_context"):

        print("ENDING AFTER RAG")

        return "end"

    user_messages = [
        m for m in state["messages"]
        if hasattr(m, "type") and m.type == "human"
    ]

    if not user_messages:

        return "end"

    last_user_message = user_messages[-1].content

    response = router_llm.invoke([
        SystemMessage(content=CLASSIFIER_PROMPT),
        HumanMessage(content=last_user_message)
    ])

    intent = response.content.strip().lower()

    print("ROUTER:", intent)

    if intent not in ["tools", "rag", "human", "end"]:

        return "end"

    return intent