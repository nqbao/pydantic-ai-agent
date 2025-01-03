from typing import List
import httpx
import os
import dotenv
import asyncio

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel

dotenv.load_dotenv()

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
        "Use the provided tools to answer the question if needed."
        "If you don't know the answer, say \"I don't know\" instead of making things up."
    ),
)


@research_agent.tool_plain
def search_google(query: str) -> List[str]:
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
        results.append(f"Title: {item['title']}\nSnippet: {item.get('snippet', 'n/a')}")

    return results

if __name__ == "__main__":
    result = research_agent.run_sync("What is Pydantic AI?")
    print(result.data)
