import streamlit as st
import asyncio
from agent import research_agent

async def main():
    st.title('Pydantic AI Agent')

    question = st.text_input("Ask a question", "What is the true range of Tesla Model Y Long Range?")

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            result = await research_agent.run(question)
            st.write(result.data)

if __name__ == "__main__":
    asyncio.run(main())
