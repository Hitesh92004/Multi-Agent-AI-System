"""
research_agent.py — Research Agent for the Multi-Agent AI System.

Uses DuckDuckGo web search via a LangGraph ReAct agent to gather
information on a given topic and return a structured bullet-point summary.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import search_tool

load_dotenv()


def create_research_agent():
    """Create and return a LangGraph ReAct agent configured for research.

    The agent uses GPT-3.5-turbo with temperature=0 for factual responses
    and the DuckDuckGo search tool for web lookups.

    Returns:
        A LangGraph CompiledGraph agent ready for research tasks.
    """
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    agent = create_react_agent(
        model=llm,
        tools=[search_tool],
    )

    return agent


def research(topic: str) -> str:
    """Research a topic using the research agent.

    Creates a research agent, sends it a structured prompt, and returns
    the agent's findings as a bullet-point summary.

    Args:
        topic: The topic to research.

    Returns:
        A structured summary of research findings, or an error message on failure.
    """
    try:
        agent = create_research_agent()
        prompt = (
            f"Research the following topic thoroughly: {topic}\n"
            f"Search for the latest information.\n"
            f"Find 3-5 key facts or points.\n"
            f"Return a structured bullet-point summary.\n"
            f"Be factual and concise."
        )
        result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        # Extract the final AI message content
        messages = result.get("messages", [])
        if messages:
            return messages[-1].content
        return "No research results found."
    except Exception as e:
        return f"Research Agent error: {str(e)}"
