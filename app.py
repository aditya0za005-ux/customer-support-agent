# app.py

from graph import build_graph
from langgraph.types import Command

import streamlit as st
import uuid

st.set_page_config(
    page_title="Customer Support"
)

st.title("Customer Support")

st.caption(
    "Ask about your orders, billing, refunds, or anything else."
)

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

graph = build_graph()

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }

    with st.chat_message("assistant"):

        placeholder = st.empty()

        final_response = ""

        try:

            events = graph.stream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                },
                config=config,
                stream_mode="values"
            )

            for event in events:

                # human interrupt
                if "__interrupt__" in event:

                    question = event["__interrupt__"][0].value

                    human_reply = st.chat_input(question)

                    if human_reply:

                        result = graph.invoke(
                            Command(resume=human_reply),
                            config=config
                        )

                        final_response = result["messages"][-1].content

                    break

                messages = event.get("messages", [])

                if messages:

                    last_message = messages[-1]

                    if hasattr(last_message, "content"):

                        final_response = last_message.content

            placeholder.markdown(final_response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": final_response
            })

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")