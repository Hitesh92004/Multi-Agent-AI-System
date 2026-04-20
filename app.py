"""
app.py — Streamlit Frontend for the Multi-Agent AI System.

Provides an interactive UI where users enter a topic and content type,
then displays research, draft, review, and final content in tabs.
"""

import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide",
)

# ─── API URL ────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ─── Header ─────────────────────────────────────────────────
st.title("🤖 Multi-Agent AI System")
st.caption("Research Agent → Writer Agent → Reviewer Agent")
st.divider()

# ─── Input Section ──────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "📌 Enter Topic",
        placeholder="e.g. Future of AI in Healthcare 2026",
    )

with col2:
    content_type = st.selectbox(
        "📄 Content Type",
        ["blog post", "report", "summary", "LinkedIn post", "email"],
    )

# ─── Run Button ─────────────────────────────────────────────
run_button = st.button("🚀 Run All Agents", type="primary")

if run_button:
    if not topic.strip():
        st.warning("⚠️ Please enter a topic first!")
    else:
        st.info(
            "**Pipeline Steps:**\n"
            "1. 🔬 Research Agent → searches the web\n"
            "2. ✍️ Writer Agent → writes content\n"
            "3. 🔍 Reviewer Agent → reviews & improves"
        )

        try:
            with st.spinner("⚙️ Agents working... this takes ~30 seconds"):
                response = requests.post(
                    f"{API_URL}/run",
                    json={"topic": topic, "content_type": content_type},
                    timeout=120,
                )

            if response.status_code == 200:
                data = response.json()

                tab1, tab2, tab3, tab4 = st.tabs(
                    ["🔬 Research", "✍️ Draft", "🔍 Review", "✅ Final Content"]
                )

                with tab1:
                    st.subheader("Research Summary")
                    st.write(data.get("research_summary", "No research data."))

                with tab2:
                    st.subheader("Draft Content")
                    st.write(data.get("draft", "No draft available."))

                with tab3:
                    st.subheader("Review Results")
                    r_col1, r_col2 = st.columns(2)
                    with r_col1:
                        st.metric("Quality Score", data.get("score", "N/A"))
                    with r_col2:
                        if data.get("approved"):
                            st.success("✅ Approved!")
                        else:
                            st.warning("⚠️ Needs Revision")
                    st.divider()
                    st.write(data.get("review", "No review data."))

                with tab4:
                    st.subheader("Final Polished Content")
                    final = data.get("final_content", "No final content.")
                    st.write(final)
                    st.download_button(
                        label="📥 Download as .txt",
                        data=final,
                        file_name=f"{topic[:30].replace(' ', '_')}.txt",
                        mime="text/plain",
                    )
            else:
                st.error(f"❌ API returned status {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info(f"Make sure the backend is running at {API_URL}")
