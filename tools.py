"""
tools.py — Shared tools for the Multi-Agent AI System.

Provides web search and word count utilities wrapped as LangChain Tool objects.
"""

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool


@tool
def search_tool(query: str) -> str:
    """Search the web for current information on any topic. Input should be a search query string."""
    try:
        ddg = DuckDuckGoSearchRun()
        results = ddg.run(query)
        return results
    except Exception as e:
        return f"Search error: {str(e)}"


@tool
def counter_tool(text: str) -> str:
    """Count the number of words in a given text. Input should be the text to count."""
    try:
        count = len(text.split())
        return f"Word count: {count}"
    except Exception as e:
        return f"Word count error: {str(e)}"
