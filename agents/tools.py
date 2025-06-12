import httpx
import os

from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str


async def search_google(query: str) -> List[SearchResult]:
    """
    Search the web for the given query and return the top results.

    Args:
        query: The query to search for.

    Returns:
        The top search results
    """
    api_key = os.getenv("SERPER_API_KEY")
    assert api_key, "Please set API key for serper"

    print("Searching for:", query)
    search_results = httpx.get(
        f"https://google.serper.dev/search?apiKey={api_key}&q={query}"
    ).json()

    results = []
    for item in search_results["organic"]:
        results.append(
            SearchResult(
                title=item["title"],
                url=item.get("link"), 
                snippet=item.get("snippet", "n/a")
            )
        )

    return results
