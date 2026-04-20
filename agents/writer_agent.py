"""
writer_agent.py — Writer Agent for the Multi-Agent AI System.

Takes research data and produces polished content (blog post, report, etc.)
using Groq's Llama 3.3 70B with a creative temperature setting.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


def create_writer_agent():
    """Create and return a ChatGroq instance configured for creative writing.

    Uses Llama 3.3 70B with temperature=0.7 for varied, engaging output.

    Returns:
        A ChatGroq LLM instance.
    """
    llm = ChatGroq(temperature=0.7, model="llama-3.3-70b-versatile")
    return llm


def write_content(topic: str, research_data: str, content_type: str = "blog post") -> str:
    """Write content based on the provided topic and research data.

    Builds a system + human message pair and invokes the writer LLM to
    produce structured, engaging content of the requested type.

    Args:
        topic: The topic to write about.
        research_data: Research findings to use as source material.
        content_type: The type of content to produce (e.g. 'blog post', 'report').

    Returns:
        The generated content as a string, or an error message on failure.
    """
    try:
        llm = create_writer_agent()

        system_msg = SystemMessage(
            content=(
                f"You are an expert content writer.\n"
                f"Write engaging, clear, well-structured content.\n"
                f"Always use proper headings and paragraphs.\n"
                f"Content type: {content_type}"
            )
        )

        human_msg = HumanMessage(
            content=(
                f"Write a {content_type} about: {topic}\n\n"
                f"Use this research as your source:\n{research_data}\n\n"
                f"Requirements:\n"
                f"- Engaging introduction\n"
                f"- 3-4 main points with explanations\n"
                f"- Clear conclusion\n"
                f"- Professional but readable tone\n"
                f"- Around 300-400 words"
            )
        )

        response = llm.invoke([system_msg, human_msg])
        return response.content
    except Exception as e:
        return f"Writer Agent error: {str(e)}"
