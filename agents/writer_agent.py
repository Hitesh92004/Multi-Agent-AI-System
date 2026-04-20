"""
writer_agent.py — Writer Agent for the Multi-Agent AI System.

Takes research data and produces polished content (blog post, report, etc.)
using Google Gemini 2.5 Flash for natural writing and creative output.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


def create_writer_agent():
    """Create and return a Gemini 2.5 Flash instance configured for creative writing.

    Uses Google Gemini 2.5 Flash with temperature=0.7 for varied,
    natural, and engaging content output.

    Returns:
        A ChatGoogleGenerativeAI LLM instance.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-preview-04-17",
        temperature=0.7,
    )
    return llm


def write_content(topic: str, research_data: str, content_type: str = "blog post") -> str:
    """Write content based on the provided topic and research data.

    Builds a system + human message pair and invokes Gemini 2.5 Flash to
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
                f"You are an expert content writer powered by Gemini 2.5 Flash.\n"
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
