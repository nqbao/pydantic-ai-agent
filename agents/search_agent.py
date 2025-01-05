from typing import List
import httpx
import os
import trafilatura

from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel

from agents.qa_agent import qa_agent, NoAnswer, Answer

model = OpenAIModel(
    "gpt-4o",
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL")
)

research_agent = Agent(
    model,
    model_settings=ModelSettings(max_tokens=1024, temperature=0),
    result_type=str,
    system_prompt=(
        "Be a helpful a research agent and do your best to answer the given question, be precise."
        "Today year is 2025.",
        "To answer a question you can use the search tool to look up information on the web then use ask website tool to ask a question to a website.",
        "If you don't know the answer, say \"I don't know\" instead of making things up."
    ),
)

@research_agent.tool_plain
async def search_google(query: str) -> List[str]:
    """
    Search the web for the given query and return the top results.

    Args:
        query: The query to search for.

    Returns:
        The top search results
    """
    api_key = os.getenv("SERPER_API_KEY")
    assert api_key, "Please set API key for serper"
    search_results = httpx.get(
        f"https://google.serper.dev/search?apiKey={api_key}&q={query}"
    ).json()

    results = []
    for item in search_results["organic"]:
        results.append(f"Title: {item['title']}\nURL: {item.get('link')}\nSnippet: {item.get('snippet', 'n/a')}")

    return results

@research_agent.tool
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
        resp = httpx.get(url, follow_redirects=True)
        if resp.status_code != 200:
            print(f"Failed to get response {url}, status code: {resp.status_code}")
            return NoAnswer()
    except Exception:
        return NoAnswer()

    html_content = trafilatura.extract(resp.text)

    return await qa_agent.run("Question: " + question + "\n\nContext:\n" + html_content, usage=ctx.usage)
