"""
main.py — FastAPI Backend for the Multi-Agent AI System.

Exposes REST endpoints to run the multi-agent pipeline,
check system health, and view system status.
"""

import os
import asyncio
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from orchestrator import run_pipeline

load_dotenv()


async def keep_alive():
    """Periodically ping the app URL to prevent cold starts on hosted platforms.

    Sends a GET request every 14 minutes to the APP_URL environment variable.
    Silently ignores any errors.
    """
    while True:
        await asyncio.sleep(14 * 60)
        try:
            app_url = os.getenv("APP_URL", "")
            if app_url:
                async with httpx.AsyncClient() as client:
                    await client.get(app_url)
        except Exception:
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager — starts the keep-alive background task."""
    asyncio.create_task(keep_alive())
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Multi-Agent AI System",
    description="3 AI agents that research, write, and review content",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PipelineRequest(BaseModel):
    """Request body for the /run endpoint."""

    topic: str
    content_type: str = "blog post"


@app.get("/")
async def root():
    """Return system status, version, and list of available agents."""
    return {
        "status": "online",
        "version": "1.0.0",
        "agents": ["Research Agent", "Writer Agent", "Reviewer Agent"],
    }


@app.get("/health")
async def health():
    """Health check endpoint for deployment platforms (Koyeb, etc.)."""
    return {"status": "healthy"}


@app.post("/run")
async def run(request: PipelineRequest):
    """Run the full multi-agent pipeline.

    Validates the topic, executes the Research → Writer → Reviewer pipeline,
    and returns the aggregated results.

    Args:
        request: A PipelineRequest with topic and optional content_type.

    Returns:
        A dict with research_summary, draft, review, score, approved, and final_content.

    Raises:
        HTTPException 400: If topic is empty.
        HTTPException 500: If the pipeline encounters an error.
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    try:
        result = run_pipeline(request.topic, request.content_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")
