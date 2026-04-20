"""
tools.py — Shared tools for the Multi-Agent AI System.

Provides web search and word count utilities wrapped as LangChain Tool objects.
"""

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool


def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return results.

    Args:
        query: The search query string.

    Returns:
        A string containing search results, or an error message on failure.
    """
    try:
        ddg = DuckDuckGoSearchRun()
        results = ddg.run(query)
        return results
    except Exception as e:
        return f"Search error: {str(e)}"


def word_count(text: str) -> str:
    """Count the number of words in the given text.

    Args:
        text: The text to count words in.

    Returns:
        A string stating the word count, or an error message on failure.
    """
    try:
        count = len(text.split())
        return f"Word count: {count}"
    except Exception as e:
        return f"Word count error: {str(e)}"


# LangChain Tool wrappers
search_tool = Tool(
    name="web_search",
    func=web_search,
    description="Search the web for current information on any topic. Input should be a search query string.",
)

counter_tool = Tool(
    name="word_count",
    func=word_count,
    description="Count the number of words in a given text. Input should be the text to count.",
)
