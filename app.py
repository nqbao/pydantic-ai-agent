import streamlit as st
import asyncio
import dotenv
import json
from agents.search_agent import research_agent

async def main():
    st.title('Pydantic AI Agent')

    question = st.text_input("Ask a question", "What is Pydantic AI?")

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            result = await research_agent.run(question)
            st.write(result.data)
            
            st.write(json.loads(result.all_messages_json()))
            st.write(result.usage())

if __name__ == "__main__":
    dotenv.load_dotenv()
    asyncio.run(main())
