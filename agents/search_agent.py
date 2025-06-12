from typing import List
import httpx
import os
import trafilatura

from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.settings import ModelSettings

from agents.qa_agent import agent as qa_agent, NoAnswer, Answer
from agents.models import main_model
from agents.tools import search_google

agent = Agent(
    main_model,
    model_settings=ModelSettings(max_tokens=1024, temperature=0),
    tools=[
        Tool(search_google, takes_ctx=False),
    ],
    output_type=str,
    system_prompt=
        "Be a helpful a research agent and do your best to answer the given question, be precise."
        "Today year is 2025."
        "To answer a question you can use the search tool to look up information on the web, then use ask website tool to visit the website to extract additional information."
        "If you don't know the answer, say \"I don't know\" instead of making things up."
    ,
)


@agent.tool
async def ask_website(ctx: RunContext, url: str, question: str) -> NoAnswer | Answer:
    """
    Ask a question about a website to get the answer.

    Args:
        url: The URL of the website to ask the question.
        question: The question to ask.

    Returns:
        The answer from the website.
    """
    try:
        print("Visiting:", url)
        resp = httpx.get(url, follow_redirects=True)
        if resp.status_code != 200:
            print(f"Failed to get response {url}, status code: {resp.status_code}")
            return NoAnswer()
    except Exception:
        return NoAnswer()

    html_content = trafilatura.extract(resp.text)
    return await qa_agent.run("Question: " + question + "\n\nContext:\n" + html_content, usage=ctx.usage)


if __name__ == "__main__":
    result = agent.run_sync("Which teams are in the NFL playoffs 2025?")
    print("Answer:", result.output)
