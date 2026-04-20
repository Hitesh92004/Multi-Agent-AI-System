"""
orchestrator.py — Pipeline Orchestrator for the Multi-Agent AI System.

Coordinates the Research, Writer, and Reviewer agents in sequence
to produce polished, reviewed content on any topic.
"""

from agents.research_agent import research
from agents.writer_agent import write_content
from agents.reviewer_agent import review_content


def run_pipeline(topic: str, content_type: str = "blog post") -> dict:
    """Run the full multi-agent pipeline: Research → Write → Review.

    Orchestrates three specialized agents in sequence:
    1. Research Agent gathers information on the topic.
    2. Writer Agent produces a draft based on the research.
    3. Reviewer Agent evaluates and improves the draft.

    Args:
        topic: The topic to create content about.
        content_type: The type of content to produce (e.g. 'blog post', 'report').

    Returns:
        A dict containing topic, content_type, research_summary, draft,
        review, score, approved status, and final_content.
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting Multi-Agent Pipeline | Topic: {topic}")
    print(f"{'='*60}\n")

    # Step 1 — Research
    print("🔬 Research Agent working...")
    research_data = research(topic)
    print("✅ Research complete!\n")

    # Step 2 — Write
    print("✍️  Writer Agent working...")
    draft = write_content(topic, research_data, content_type)
    print("✅ Draft complete!\n")

    # Step 3 — Review
    print("🔍 Reviewer Agent working...")
    review_result = review_content(topic, draft)
    print("✅ Review complete!\n")

    # Final output
    final_content = review_result.get("revised_content") or draft

    result = {
        "topic": topic,
        "content_type": content_type,
        "research_summary": research_data,
        "draft": draft,
        "review": review_result.get("raw_review", ""),
        "score": review_result.get("score", "N/A"),
        "approved": review_result.get("approved", False),
        "final_content": final_content,
    }

    print(f"\n{'='*60}")
    print(f"🎉 Pipeline complete! Score: {result['score']}")
    print(f"{'='*60}\n")

    return result
