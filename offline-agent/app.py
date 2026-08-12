import streamlit as st
from agent import run_agent


st.set_page_config(
    page_title="Offline AI Agent",
    page_icon="🤖"
)


st.title("Offline AI Agent")


st.write(
    "Local LLM + Python Tool Calling using LM Studio"
)


user_input = st.text_input(
    "Ask your question:",
    placeholder="What is 25 multiplied by 40?"
)


if st.button("Ask Agent"):

    if user_input:

        with st.spinner("Thinking..."):

            try:

                answer = run_agent(user_input)

                st.write(answer)

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

    else:

        st.warning(
            "Please enter a question."
        )