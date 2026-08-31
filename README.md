# 🦜 LangChain Doc Assistant

A Retrieval-Augmented Generation (RAG) system that answers questions about LangChain by searching its official documentation and generating grounded answers with an LLM.

🔗 **[Live Demo](https://langchain-doc-assistant.onrender.com)** *(first load may take 30-60s to wake up)*

![Python](https://img.shields.io/badge/Python-3.9-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Docker-teal)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF)

---

## What it does

Ask a question about LangChain in plain English (or Turkish) and get an answer grounded in the actual documentation — not the model's memory. The system retrieves the most relevant documentation chunks first, then asks the LLM to answer using only that context.

## Features

- 📄 Automated ingestion of LangChain's official docs
- 🔍 Semantic search via embeddings (retrieval, not keyword matching)
- ⚡ Fast, free inference via Groq API
- 🌐 REST API built with FastAPI + a minimal chat UI
- 🐳 Fully containerized with Docker
- ✅ CI pipeline via GitHub Actions
- 📊 Request logging: latency, token usage, estimated cost per query
- 🔄 Prompt versioning (track which prompt version produced which answer)

## Architecture

```
User question
     │
     ▼
FastAPI  (/ask)
     │
     ▼
Retrieval  →  Chroma vector DB returns top-3 relevant chunks
     │
     ▼
Generation  →  chunks + question sent to Groq LLM
     │
     ▼
Answer  +  Logging (logs.jsonl: latency, tokens, cost, prompt version)
```

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9 |
| Doc processing | LangChain |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM inference | Groq API (openai/gpt-oss-120b) |
| API | FastAPI |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Deployment | Render |

## Getting Started

### Local setup (venv)

```bash
git clone https://github.com/cgozde/langchain-doc-assistant.git
cd langchain-doc-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# create .env with your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

uvicorn src.api.main:app --reload
```

### With Docker

```bash
docker build -t langchain-doc-assistant .
docker run -p 8000:8000 --env-file .env -v $(pwd)/chroma_db:/app/chroma_db langchain-doc-assistant
```

## Usage

Once running, visit `http://localhost:8000` for the chat UI, or call the API directly:

```
GET http://localhost:8000/ask?soru=How do I create an agent?
```

**Example response:**
```json
{
  "cevap": "To create an agent in LangChain, you can use the create_agent function..."
}
```

Interactive API docs: `http://localhost:8000/docs`

## Project Structure

```
├── src/
│   ├── api/          # FastAPI endpoints + chat UI
│   ├── generation/   # LLM calls, prompt management
│   ├── ingestion/    # Document loading and chunking
│   └── retrieval/    # Embedding and vector search
├── Dockerfile
├── .github/workflows/  # CI pipeline
└── requirements.txt
```

## Development Notes

This project was built end-to-end as a hands-on way to learn RAG systems and MLOps/LLMOps practices — from data ingestion to deployment. Detailed build notes, including mistakes made along the way, are in [LEARNING_LOG.md](./LEARNING_LOG.md).