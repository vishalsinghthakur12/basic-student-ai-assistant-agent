import streamlit as st
from graph import build_graph
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Acciojob AI Student Assistant")

st.title("Acciojob AI Student Assistant")

st.caption("Ask a question. The agent can answer directly or use a tool")

question = st.text_input(
    "Ask Anything",
    placeholder="Example: What is 523*532?"
)

ask_button = st.button("Ask")

if ask_button:
    if not question.strip():
        st.warning("Please type a question first")
    else:
        with st.spinner("Thinking..."):
            graph = build_graph()
            result = graph.invoke(
                {
                    "messages": [HumanMessage(content=question)]
                }
            )
            answer = result["messages"][-1].content

        st.markdown("### Response")
        st.write(answer)
