"""
research_agent.py — Research Agent for the Multi-Agent AI System.

Uses DuckDuckGo for web search and DeepSeek R1 (via Groq) for
chain-of-thought reasoning and deep analysis of the results.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


def create_research_agent():
    """Create and return a ChatGroq instance with DeepSeek R1.

    Uses DeepSeek R1 (distilled 70B) with temperature=0 for
    deep chain-of-thought reasoning and factual analysis.

    Returns:
        A ChatGroq LLM instance configured with DeepSeek R1.
    """
    llm = ChatGroq(temperature=0, model="deepseek-r1-distill-llama-70b")
    return llm


def research(topic: str) -> str:
    """Research a topic using DuckDuckGo search + DeepSeek R1 analysis.

    Step 1: Searches the web using DuckDuckGo for raw data.
    Step 2: Passes raw results to DeepSeek R1 for deep reasoning
            and structured analysis.

    Args:
        topic: The topic to research.

    Returns:
        A structured summary of research findings, or an error message on failure.
    """
    try:
        # Step 1: Web search with DuckDuckGo
        print("    🌐 Searching the web...")
        ddg = DuckDuckGoSearchRun()
        raw_results = ddg.run(f"{topic} latest information")
        print("    📄 Raw results collected, analyzing with DeepSeek R1...")

        # Step 2: Deep analysis with DeepSeek R1
        llm = create_research_agent()

        system_msg = SystemMessage(
            content=(
                "You are a world-class research analyst powered by DeepSeek R1.\n"
                "Analyze the provided search results using deep reasoning.\n"
                "Extract the most important and factual information.\n"
                "Always structure your output as clear bullet points.\n"
                "Be factual, concise, and cite specific details from the data."
            )
        )

        human_msg = HumanMessage(
            content=(
                f"Research topic: {topic}\n\n"
                f"Here are the raw web search results:\n{raw_results}\n\n"
                f"Instructions:\n"
                f"- Identify 3-5 key facts or insights\n"
                f"- Organize them as a structured bullet-point summary\n"
                f"- Note any recent trends or developments\n"
                f"- Be factual and concise"
            )
        )

        response = llm.invoke([system_msg, human_msg])
        return response.content
    except Exception as e:
        return f"Research Agent error: {str(e)}"
