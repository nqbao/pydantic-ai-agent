import streamlit as st
import asyncio
import dotenv
import json

dotenv.load_dotenv()

from agents.search_agent import research_agent


@st.dialog("Message JSON", width="large")
def show_message(messages):
    st.write(messages)


async def main():
    st.title('Pydantic AI Agent')

    question = st.text_input("Ask a question", "What is Pydantic AI?")

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            result = await research_agent.run(question)
            st.session_state['chat_result'] = result

    if 'chat_result' in st.session_state:
        result = st.session_state['chat_result']
        st.write(result.output)

        if st.button("Show Message JSON"):
            show_message(json.loads(result.all_messages_json()))


if __name__ == "__main__":
    asyncio.run(main())
