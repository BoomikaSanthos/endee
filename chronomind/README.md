<div align="center">
  <img src="https://img.shields.io/badge/ChronoMind-Smart_Journal-6A0DAD?style=for-the-badge" alt="ChronoMind Logo" />

  <h1>🧠 ChronoMind</h1>
  <p><b>An AI-Powered Personal Learning Journal with Semantic Memory Retrieval.</b></p>
  
  <p>
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi" />
    <img alt="React" src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
    <img alt="Docker" src="https://img.shields.io/badge/Docker-2CA5E0?style=flat-square&logo=docker&logoColor=white" />
    <a href="https://github.com/endee-io/endee">
      <img alt="Powered by Endee" src="https://img.shields.io/badge/Powered_by-Endee_Vector_DB-FF5722?style=flat-square" />
    </a>
  </p>

  <p><em>Capture what you learn. Ask questions about it. Never forget.</em></p>
</div>

---

## 🌟 The Vision

How often do you read a great article, learn a new framework, or solve a tough programming bug—only to forget the details a few months later? 

**ChronoMind** is a personal knowledge base and RAG (Retrieval-Augmented Generation) system designed to solve that. Built on top of **Endee**, a high-performance open-source vector database, ChronoMind allows you to jot down daily learning notes. Instead of forcing you to remember exact keywords, the system uses AI to understand the *meaning* of your notes. 

When you ask, *"What did I learn about building graph databases last month?"*, ChronoMind acts as your personal tutor, instantly recalling and synthesizing the exact context from your past thoughts.

---

## ✨ Core Features

*   📝 **Smart Note Capture:** Quickly log notes with titles, rich content, tags, and topics.
*   🔍 **True Semantic Search:** Search by *intent and meaning*, powered by Endee's ANN engine (no more exact-match keyword frustration).
*   🤖 **Personalized RAG Q&A:** Ask conversational questions. ChronoMind analyzes your past notes and synthesizes a direct answer grounded *entirely* in what you've learned.
*   🏷️ **Topic & Time Filtering:** Use Endee's metadata filters to narrow down searches strictly to specific topics (e.g., "Programming", "Machine Learning").
*   📊 **Confidence Scores:** Instantly view structural similarity metrics to see exactly why the AI thought a note was relevant.
*   ⚡ **Extremely Fast:** Optimized with a C++ Endee backend and a seamless React frontend.

---

## 🚀 Quick Start Guide (Using Docker)

Getting ChronoMind up and running takes less than 3 minutes.

### Prerequisites
*   [Docker Desktop](https://docs.docker.com/get-docker/) installed running in the background.

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/chronomind.git
cd chronomind
```

**2. Configure your AI keys (Optional but highly recommended)**  
In the `docker-compose.yml` file, add your LLM API keys under the `backend` environment variables:
```yaml
environment:
  ANTHROPIC_API_KEY: "sk-ant-..."   # Preferable for Claude RAG
  OPENAI_API_KEY: "sk-proj-..."     # Alternative LLM
```
*(If you don't add keys, it will still use local Semantic Search and extractive summarization natively!)*

**3. Launch the Stack**
```bash
docker-compose up -d --build
```

**4. Open the App in your Browser!**
Navigate to: **[http://localhost:3000](http://localhost:3000)**

*(Note: The Endee Database will be successfully running on `http://localhost:8082` and the Backend API on `http://localhost:8000`)*

### Want some automated test data?
You can populate ChronoMind with excellent sample notes immediately so you can test the AI:
```bash
python scripts/seed_data.py
```

---

## 🏗️ System Architecture

ChronoMind integrates modern web apps with native AI vector databases seamlessly.

```mermaid
graph LR
    A[React \n Frontend] -->|REST API| B(FastAPI \n Backend)
    B -->|Text| C[sentence-transformers \n embeddings]
    C -->|Vector float[384]| B
    B -->|Similarity Search & Upserts| D[(Endee Vector \n Database DB)]
    D -->|Ranked Notes| B
    B -->|Optional: Claude/GPT-4| A
```

For an extremely comprehensive layout of data flows and architecture logic, see [SYSTEM_DESIGN.md](./SYSTEM_DESIGN.md).

---

## 📡 API Reference

ChronoMind's FastAPI backend comes fully documented out-of-the-box. Below are a few of the critical endpoints powering your journal:

| Method | Endpoint | Description | Example Payload |
|---|---|---|---|
| `POST` | `/api/notes` | Store a new note as a vector | `{"title": "HNSW", "content": "..."}` |
| `POST` | `/api/notes/search` | Performs native semantic search | `{"query": "algorithms", "top_k": 5}` |
| `POST` | `/api/ask` | Full AI Context Q&A (RAG) | `{"question": "How do vectors work?"}` |
| `DELETE` | `/api/notes/{id}` | Permanently delete a note | |

---

## 🧩 How It Works Under the Hood

ChronoMind relies strictly on [Endee](https://github.com/endee-io/endee) to handle the complex AI embedding workloads at lightspeed:

**1. Index Allocation:**
Upon startup, ChronoMind instructs Endee to create a vector space:
```python
await endee_post("/index/create", {
    "name": "chronomind_notes",
    "dimension": 384,           # Matches the all-MiniLM-L6-v2 transformer
    "space_type": "cosine",     # Best for textual semantic similarities
    "precision": "INT8"         # 4x Memory savings!
})
```

**2. Storing Thoughts (Upserts):**
Your typing is translated to vectors locally and shipped to Endee alongside your metadata filtering tags:
```python
await endee_post(f"/index/chronomind_notes/upsert", {
    "vectors": [{
        "id": note_id,
        "vector": embedded_vector,
        "meta": { "title": title, "content": content },
        "filter": { "topic": "ai" }
    }]
})
```

**3. RAG Retrieval Synthesis**
When you ask the AI a question, it queries Endee for the closest contextual matches. It then forces the AI to only construct answers based on the retrieved internal documents!

---

## ❤️ Mandatory Support & Credits

ChronoMind wouldn't be possible without Endee's extremely performant Vector handling protocols. 

**Before deploying this project into production, we heavily require you to:**
1. ⭐ **Star** the core Endee repository: [https://github.com/endee-io/endee](https://github.com/endee-io/endee)
2. 🍴 **Fork** the Endee repository to your GitHub account to support the Open Source algorithms!

---

## 📄 License
Released under the MIT License — see [LICENSE](./LICENSE)

*Always keep learning. Never forget a single thought.*
