# Multi-Agent AI System 🤖

A production-ready multi-agent pipeline where **3 specialized AI agents** collaborate to research, write, and review content on any topic.

---

## What It Does

1. **Research Agent** — Searches the web using DuckDuckGo to gather the latest information on a given topic.
2. **Writer Agent** — Produces polished, structured content (blog post, report, summary, etc.) based on the research.
3. **Reviewer Agent** — Evaluates the draft, scores it out of 10, lists strengths and improvements, and produces a revised final version.

All three agents are orchestrated automatically — the user simply enters a topic and selects a content type.

---

## Architecture

```
User Input (Topic + Content Type)
        │
        ▼
  ┌─────────────┐
  │ Orchestrator │
  └─────┬───────┘
        │
        ▼
  ┌─────────────────┐
  │ Research Agent   │ ── DuckDuckGo + DeepSeek R1 ──▶ Bullet-point summary
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  Writer Agent    │ ── Gemini 2.5 Flash ──▶ Draft content
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ Reviewer Agent   │ ── Llama 3.3 70B (Groq) ──▶ Score + Revised content
  └────────┬────────┘
           │
           ▼
     Final Output
  (Score, Review, Polished Content)
```

---

## Tech Stack

| Layer       | Technology                              |
|-------------|-----------------------------------------|
| LLM         | DeepSeek R1 + Gemini 2.5 Flash + Llama 3.3 70B |
| Framework   | LangChain + langchain-groq + langchain-google-genai |
| Web Search  | DuckDuckGo (via langchain-community)    |
| Backend API | FastAPI + Uvicorn                       |
| Frontend UI | Streamlit                               |
| Deployment  | Docker (Render / Hugging Face Spaces)   |
| Environment | python-dotenv                           |

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/multi-agent-ai.git
cd multi-agent-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and add your free Groq API key (get one at [console.groq.com](https://console.groq.com/)):

```
GROQ_API_KEY=gsk_your-real-key-here
```

### 4. Start the backend (Terminal 1)

```bash
uvicorn main:app --reload --port 8000
```

### 5. Start the frontend (Terminal 2)

```bash
streamlit run app.py
```

### 6. Open in browser

Navigate to **http://localhost:8501** and start generating content!

---

## Deployment

### Backend — Docker (Hugging Face Spaces)

The included `Dockerfile` builds a slim Python 3.11 image and runs the FastAPI backend. Hugging Face Spaces expects port **7860** by default.

1. Create a "New Space" on Hugging Face.
2. Select **Docker** as the SDK.
3. Upload/Push your code.
4. Add `GROQ_API_KEY` in the Space's **Settings > Variables and Secrets**.

### Frontend — Streamlit Cloud

1. Push your code to a GitHub repository.
2. Connect the repository to [Streamlit Cloud](https://streamlit.io/cloud).
3. Set the `API_URL` environment variable to your Hugging Face Space URL (e.g., `https://username-space-name.hf.space`).
4. Set the `GROQ_API_KEY` in the Streamlit Cloud secrets if required.

### Required Environment Variables

| Variable        | Description                     | Required |
|-----------------|---------------------------------|----------|
| `GROQ_API_KEY`  | Groq API key (free)             | ✅       |
| `GOOGLE_API_KEY`| Google AI API key (free tier)    | ✅       |
| `API_URL`       | Backend URL (for Streamlit)     | For prod |
| `APP_URL`       | Self-URL for keep-alive pings   | Optional |

---

## Example Usage

Try these topics in the UI:

1. **"Future of AI in Healthcare 2026"** — blog post
2. **"Climate Change Impact on Global Agriculture"** — report
3. **"Top 5 Python Libraries for Data Science"** — LinkedIn post

---

## API Endpoints

| Method | Endpoint  | Description                                  |
|--------|-----------|----------------------------------------------|
| GET    | `/`       | System status, version, and agent list       |
| GET    | `/health` | Health check (returns `{"status": "healthy"}`)|
| POST   | `/run`    | Run the full pipeline with `topic` and `content_type` |

### Example `/run` request

```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"topic": "Quantum Computing Breakthroughs", "content_type": "blog post"}'
```

---

## License

MIT

---

Built with ❤️ using LangChain, Groq, FastAPI, and Streamlit.
