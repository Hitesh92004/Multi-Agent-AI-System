"""
reviewer_agent.py — Reviewer Agent for the Multi-Agent AI System.

Reviews content for quality, scores it, and produces an improved version.
Returns a structured dict with score, approval status, and revised content.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


def create_reviewer_agent():
    """Create and return a ChatOpenAI instance configured for content review.

    Uses GPT-3.5-turbo with temperature=0.2 for consistent, critical output.

    Returns:
        A ChatOpenAI LLM instance.
    """
    llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")
    return llm


def extract_score(text: str) -> str:
    """Extract the quality score from the review text.

    Looks for a line containing 'SCORE:' and returns its value.

    Args:
        text: The full review response text.

    Returns:
        The score string (e.g. '8/10'), or 'N/A' if not found.
    """
    for line in text.split("\n"):
        if "SCORE:" in line.upper():
            return line.split(":", 1)[1].strip()
    return "N/A"


def extract_revised(text: str) -> str:
    """Extract the revised content section from the review text.

    Splits on 'REVISED_CONTENT:' and returns everything after it.

    Args:
        text: The full review response text.

    Returns:
        The revised content string, or empty string if not found.
    """
    upper_text = text.upper()
    if "REVISED_CONTENT:" in upper_text:
        idx = upper_text.index("REVISED_CONTENT:")
        after = text[idx + len("REVISED_CONTENT:"):]
        return after.strip()
    return ""


def review_content(original_topic: str, content: str) -> dict:
    """Review content and return a structured evaluation.

    Sends the content to the reviewer LLM with instructions to score,
    list strengths/improvements, give a verdict, and produce a revised version.

    Args:
        original_topic: The original topic the content was written about.
        content: The draft content to review.

    Returns:
        A dict with keys: raw_review, approved, score, revised_content.
        On failure, returns a dict with error message and approved=False.
    """
    try:
        llm = create_reviewer_agent()

        system_msg = SystemMessage(
            content=(
                "You are a senior content editor and reviewer.\n"
                "You MUST respond in this EXACT format:\n\n"
                "SCORE: [X/10]\n"
                "STRENGTHS:\n- [bullet list]\n"
                "IMPROVEMENTS:\n- [bullet list]\n"
                "VERDICT: APPROVED or NEEDS_REVISION\n"
                "REVISED_CONTENT:\n[full improved version of the content]"
            )
        )

        human_msg = HumanMessage(
            content=(
                f"Review the following content written about '{original_topic}'.\n"
                f"Evaluate quality, accuracy, engagement, and structure.\n\n"
                f"Content to review:\n{content}"
            )
        )

        response = llm.invoke([system_msg, human_msg])
        raw_review = response.content

        return {
            "raw_review": raw_review,
            "approved": "APPROVED" in raw_review.upper(),
            "score": extract_score(raw_review),
            "revised_content": extract_revised(raw_review),
        }
    except Exception as e:
        return {
            "error": str(e),
            "approved": False,
            "raw_review": "",
            "score": "N/A",
            "revised_content": "",
        }
