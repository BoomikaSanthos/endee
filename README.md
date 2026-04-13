<p align="center">
  <picture>
      <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="docs/assets/logo-light.svg">
      <img height="100" alt="Endee" src="docs/assets/logo-dark.svg">
  </picture>
</p>

<p align="center">
    <b>High-performance open-source vector database for AI search, RAG, semantic search, and hybrid retrieval.</b>
</p>

<p align="center">
    <a href="./docs/getting-started.md"><img src="https://img.shields.io/badge/Quick_Start-Local_Setup-success?style=flat-square" alt="Quick Start"></a>
    <a href="https://docs.endee.io/quick-start"><img src="https://img.shields.io/badge/Docs-Quick_Start-success?style=flat-square" alt="Docs"></a>
    <a href="https://github.com/endee-io/endee/blob/master/LICENSE"><img src="https://img.shields.io/github/license/endee-io/endee?style=flat-square" alt="License"></a>
    <a href="https://discord.gg/5HFGqDZQE3"><img src="https://img.shields.io/badge/Discord-Join_Chat-5865F2?logo=discord&style=flat-square" alt="Discord"></a>
    <a href="https://endee.io/"><img src="https://img.shields.io/badge/Website-Endee-111111?style=flat-square" alt="Website"></a>
    <!-- <a href="https://endee.io/benchmarks"><img src="https://img.shields.io/badge/Benchmarks-Coming_Soon-1F8B4C?style=flat-square" alt="Benchmarks"></a> -->
    <!-- <a href="https://endee.io/cloud"><img src="https://img.shields.io/badge/Cloud-Coming_Soon-2496ED?style=flat-square" alt="Cloud"></a> -->
</p>

<p align="center">
<strong><a href="./docs/getting-started.md">Quick Start</a> • <a href="#why-endee">Why Endee</a> • <a href="#use-cases">Use Cases</a> • <a href="#features">Features</a> • <a href="#api-and-clients">API and Clients</a> • <a href="#docs-and-links">Docs</a> • <a href="#community-and-contact">Contact</a></strong>
</p>

# Endee: Open-Source Vector Database for AI Search

**Endee** is a high-performance open-source vector database built for AI search and retrieval workloads. It is designed for teams building **RAG pipelines**, **semantic search**, **hybrid search**, recommendation systems, and filtered vector retrieval APIs that need production-oriented performance and control.

Endee combines vector search with filtering, sparse retrieval support, backup workflows, and deployment flexibility across local builds and Docker-based environments. The project is implemented in C++ and optimized for modern CPU targets, including AVX2, AVX512, NEON, and SVE2.

If you want the fastest path to evaluate Endee locally, start with the [Getting Started guide](./docs/getting-started.md) or the hosted docs at [docs.endee.io](https://docs.endee.io/quick-start).

## Why Endee

- Built as a dedicated vector database for AI applications, search systems, and retrieval-heavy workloads.
- Supports dense vector retrieval plus sparse search capabilities for hybrid search use cases.
- Includes payload filtering for metadata-aware retrieval and application-specific query logic.
- Ships with operational features already documented in this repo, including backup flows and runtime observability.
- Offers flexible deployment paths: local scripts, manual builds, Docker images, and prebuilt registry images.

## Getting Started

The full installation, build, Docker, runtime, and authentication instructions are in [docs/getting-started.md](./docs/getting-started.md).

Fastest local path:

```bash
chmod +x ./install.sh ./run.sh
./install.sh --release --avx2
./run.sh
```

The server listens on port `8080`. For detailed setup paths, supported operating systems, CPU optimization flags, Docker usage, and authentication examples, use:

- [Getting Started](./docs/getting-started.md)
- [Hosted Quick Start Docs](https://docs.endee.io/quick-start)

## Use Cases

### RAG and AI Retrieval

Use Endee as the retrieval layer for question answering, chat assistants, copilots, and other RAG applications that need fast vector search with metadata-aware filtering.

### Agentic AI and AI Agent Memory

Use Endee as the long-term memory and context retrieval layer for AI agents built with frameworks like LangChain, CrewAI, AutoGen, and LlamaIndex. Store and retrieve past observations, tool outputs, conversation history, and domain knowledge mid-execution with low-latency filtered vector search, so your autonomous agents get the right context without stalling their reasoning loop.

### Semantic Search

Build semantic search experiences for documents, products, support content, and knowledge bases using vector similarity search instead of exact keyword-only matching.

### Hybrid Search

Combine dense retrieval, sparse vectors, and filtering to improve relevance for search workflows where both semantic understanding and term-level precision matter.

### Recommendations and Matching

Support recommendation, similarity matching, and nearest-neighbor retrieval workflows across text, embeddings, and other high-dimensional representations.

## Features

- **Vector search** for AI retrieval and semantic similarity workloads.
- **Hybrid retrieval support** with sparse vector capabilities documented in [docs/sparse.md](./docs/sparse.md).
- **Payload filtering** for structured retrieval logic documented in [docs/filter.md](./docs/filter.md).
- **Backup APIs and flows** documented in [docs/backup-system.md](./docs/backup-system.md).
- **Operational logging and instrumentation** documented in [docs/logs.md](./docs/logs.md) and [docs/mdbx-instrumentation.md](./docs/mdbx-instrumentation.md).
- **CPU-targeted builds** for AVX2, AVX512, NEON, and SVE2 deployments.
- **Docker deployment options** for local and server environments.

## API and Clients

Endee exposes an HTTP API for managing indexes and serving retrieval workloads. The current repo documentation and examples focus on running the server directly and calling its API endpoints.

Current developer entry points:

- [Getting Started](./docs/getting-started.md) for local build and run flows
- [Hosted Docs](https://docs.endee.io/quick-start) for product documentation
- [Release Notes 1.0.0](https://github.com/endee-io/endee/releases/tag/1.0.0) for recent platform changes

## Docs and Links

- [Getting Started](./docs/getting-started.md)
- [Hosted Documentation](https://docs.endee.io/quick-start)
- [Release Notes](https://github.com/endee-io/endee/releases/tag/1.0.0)
- [Sparse Search](./docs/sparse.md)
- [Filtering](./docs/filter.md)
- [Backups](./docs/backup-system.md)

## Community and Contact

- Join the community on [Discord](https://discord.gg/5HFGqDZQE3)
- Visit the website at [endee.io](https://endee.io/)
- For trademark or branding permissions, contact [enterprise@endee.io](mailto:enterprise@endee.io)

## Contributing

We welcome contributions from the community to help make vector search faster and more accessible for everyone.

- Submit pull requests for fixes, features, and improvements
- Report bugs or performance issues through GitHub issues
- Propose enhancements for search quality, performance, and deployment workflows

## License

Endee is open source software licensed under the **Apache License 2.0**. See the [LICENSE](./LICENSE) file for full terms.

## Trademark and Branding

“Endee” and the Endee logo are trademarks of Endee Labs.

The Apache License 2.0 does not grant permission to use the Endee name, logos, or branding in a way that suggests endorsement or affiliation.

If you offer a hosted or managed service based on this software, you must use your own branding and avoid implying it is an official Endee service.

## Third-Party Software

This project includes or depends on third-party software components licensed under their respective open-source licenses. Use of those components is governed by their own license terms.
# 🧠 ChronoMind — AI-Powered Personal Learning Journal

> Capture what you learn. Ask questions about it. Never forget.

ChronoMind is a personal knowledge base and RAG (Retrieval-Augmented Generation) system built on top of [Endee](https://github.com/endee-io/endee), a high-performance open-source vector database. Write learning notes, then search them by meaning — or ask an AI that synthesizes answers grounded entirely in your own notes.

---

## 📋 Mandatory Steps Before Starting

> These are required by the internship evaluation criteria.

1. ⭐ **Star** the official Endee repo → [github.com/endee-io/endee](https://github.com/endee-io/endee)
2. 🍴 **Fork** it to your GitHub account (click Fork button on that page)
3. 📁 **Clone your fork** and place this `chronomind/` folder inside it

```
github.com/YOUR_USERNAME/endee/         ← your forked repo
└── chronomind/                         ← this project lives here
    ├── backend/
    ├── frontend/
    ├── scripts/
    └── README.md
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 Note Capture | Write learning notes with title, content, topic, and tags |
| 🔍 Semantic Search | Find notes by meaning, not just keywords — powered by Endee ANN search |
| 🤖 RAG Q&A | Ask questions and get AI answers grounded in your personal notes |
| 🏷️ Topic Filtering | Filter searches by topic (ai, programming, devops) using Endee filters |
| 📊 Similarity Scores | See how closely each result matches your query as a percentage |
| 🗑️ Note Management | Add and delete notes with live updates |

---

## 🏗️ How the Project Works — Architecture

```
┌─────────────────────────────────────┐
│         Your Browser                │
│      React UI (port 3000)           │
│  [ Search Tab ]  [ Ask AI Tab ]     │
└────────────┬────────────────────────┘
             │  HTTP requests (/api/...)
             ▼
┌─────────────────────────────────────┐
│       FastAPI Backend               │
│         (port 8000)                 │
│                                     │
│  1. Receives your text              │
│  2. Converts it to a 384-dim        │
│     vector using AI model           │
│  3. Sends vector to Endee           │
│  4. Gets similar notes back         │
│  5. (For RAG) sends to LLM          │
│  6. Returns answer to browser       │
└────────────┬────────────────────────┘
             │  REST API calls
             ▼
┌─────────────────────────────────────┐
│       Endee Vector Database         │
│    (cloud at api.endee.io OR        │
│     local Docker at port 8080)      │
│                                     │
│  Stores notes as vectors            │
│  HNSW index — cosine similarity     │
│  Returns top-K nearest matches      │
└─────────────────────────────────────┘
```

### What each part does in plain English

**Frontend (React)** — The web page you open in your browser at `localhost:3000`. Has two tabs: Semantic Search and Ask AI (RAG). It talks to the backend to save and retrieve notes.

**Backend (FastAPI)** — A Python server running at `localhost:8000`. When you search or ask a question, it converts your text into a mathematical vector using the AI model `all-MiniLM-L6-v2`, then sends that vector to Endee to find the most similar notes. For RAG, it also calls an LLM to write a synthesized answer.

**Endee** — The vector database. Stores all your notes as vectors and can search them in milliseconds using the HNSW algorithm. This is the core technology the whole project is built around.

---

## ⚙️ Do You Need to Start Docker Every Time?

**Yes — Docker Desktop must be open before running any `docker` command.** Here is what you need to know:

| Situation | What to do |
|---|---|
| First time ever | Install Docker Desktop → run `docker compose up --build` (slow, ~30 min) |
| Every time after | Open Docker Desktop → run `docker compose up` (fast, ~30 sec) |
| After PC restart | Open Docker Desktop first → then `docker compose up` |
| Want to stop | Run `docker compose down` or press Ctrl+C |

You do NOT need `--build` every time. Only use `--build` the very first time, or if you edit the code files. After that, just `docker compose up` is enough.

---

## 🚀 Setup and Run — Step by Step

### What you need installed

| Tool | Purpose | Download |
|---|---|---|
| Docker Desktop | Runs backend + frontend containers | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) |
| Python 3.8+ | Only for running the seed script | [python.org/downloads](https://www.python.org/downloads/) |
| Git | To clone the repo | [git-scm.com](https://git-scm.com/downloads) |

Node.js is NOT needed separately — it runs inside Docker automatically.

---

### Step 1 — Clone your forked Endee repo

```bash
git clone https://github.com/YOUR_USERNAME/endee.git
cd endee
mkdir chronomind
```

Copy all files from `chronomind.zip` into the `chronomind/` folder, then:

```bash
cd chronomind
```

---

### Step 2 — Set up Endee Cloud (required if you have less than 4GB free RAM)

> If Endee crashes with "Insufficient memory" error, use the free cloud version instead.

**2a.** Go to [app.endee.io](https://app.endee.io) → sign up → create an API token → copy it.

**2b.** Open `docker-compose.yml` and replace the entire content with:

```yaml
services:

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: chronomind-backend
    ports:
      - "8000:8000"
    environment:
      ENDEE_BASE_URL: "https://api.endee.io/api/v1"
      ENDEE_AUTH_TOKEN: "paste-your-endee-token-here"
      ANTHROPIC_API_KEY: ""
      OPENAI_API_KEY: ""
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: chronomind-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

---

### Step 3 — Open Docker Desktop

Open the Docker Desktop application. Wait until you see the green "Docker Desktop is running" indicator at the bottom left of the app.

---

### Step 4 — First time build and start (~10–30 min)

```bash
docker compose up --build
```

Wait until you see this in the terminal:

```
chronomind-backend  | Model loaded ✓
chronomind-backend  | Index 'chronomind_notes' created ✓
chronomind-backend  | INFO: Uvicorn running on http://0.0.0.0:8000
chronomind-frontend | nginx: the child process is ready
```

---

### Step 5 — Add sample notes (open a new terminal tab)

```bash
pip install httpx
python scripts/seed_data.py
```

Expected output:

```
Seeding ChronoMind with sample notes…
  ✓ Understanding Python Decorators
  ✓ Vector Databases Explained
  ✓ RAG Pipeline Architecture
  ✓ Git Branching Strategy (GitFlow)
  ✓ Attention Mechanism in Transformers
  ✓ Docker vs Kubernetes
  ✓ Cosine Similarity vs Dot Product
  ✓ Python asyncio Basics
  ✓ System Design: Rate Limiting
  ✓ HNSW Index — How It Works

Done: 10/10 notes inserted.
```

---

### Step 6 — Open the app

| What | URL |
|---|---|
| 🌐 The App | http://localhost:3000 |
| 🔧 Backend API docs | http://localhost:8000/docs |
| ❤️ Health check | http://localhost:8000/api/health |

---

### Every time after the first run (30 seconds)

```bash
# 1. Open Docker Desktop (just open the app — wait for green status)

# 2. Start containers — no --build needed
docker compose up
```

### To stop the app

```bash
docker compose down
```

Your notes are saved in Endee Cloud and will be there next time.

---

## 🔄 How the Backend Runs (Explained Simply)

The backend is a **Python FastAPI server** running inside a Docker container. Here is the exact sequence of what happens:

```
docker compose up
       │
       ▼
Docker reads backend/Dockerfile
       │
       ▼
Starts Python 3.11 environment inside a container
       │
       ▼
Loads all packages (FastAPI, sentence-transformers, httpx, torch...)
       │
       ▼
Downloads AI model: all-MiniLM-L6-v2  (~90MB, only first time)
       │
       ▼
Starts uvicorn web server → runs main.py
       │
       ▼
main.py connects to Endee → creates chronomind_notes index if missing
       │
       ▼
Server is ready at http://localhost:8000  ✓
```

Every time you type something and search:
- Backend receives the text
- Runs it through the AI model → 384 numbers (a vector)
- Sends the vector to Endee
- Endee returns the most similar stored notes
- Backend sends them back to the browser

## 🔄 How the Frontend Runs (Explained Simply)

The frontend is a **React app** served by nginx inside a Docker container:

```
docker compose up
       │
       ▼
Docker reads frontend/Dockerfile
       │
       ▼
Node.js runs: npm run build
(converts App.jsx + CSS → plain HTML/CSS/JS files)
       │
       ▼
Built files copied into nginx container
       │
       ▼
nginx starts at http://localhost:3000  ✓
       │
       ├── Requests to /         → serves React app files
       │
       └── Requests to /api/...  → forwarded to backend:8000
```

This is why you only open `localhost:3000` — nginx handles routing both the UI and API calls behind the scenes.

---

## 📡 API Endpoints Reference

| Method | Endpoint | What it does |
|---|---|---|
| `GET` | `/api/health` | Check if backend + Endee are connected |
| `POST` | `/api/notes` | Save a new note to Endee |
| `POST` | `/api/notes/search` | Semantic search by query string |
| `POST` | `/api/ask` | RAG — ask question, get AI answer |
| `DELETE` | `/api/notes/{id}` | Delete a note by ID |

You can test all these at `http://localhost:8000/docs` — a built-in interactive API explorer.

---

## 🧩 How Endee Is Used in the Code

**Creating the index (once on startup):**
```python
await endee_post("/index/create", {
    "name": "chronomind_notes",
    "dimension": 384,         # all-MiniLM-L6-v2 output size
    "space_type": "cosine",   # best for text embeddings
    "precision": "INT8"       # 4x memory savings
})
```

**Storing a note:**
```python
vector = embedder.encode(title + "\n\n" + content).tolist()
await endee_post("/index/chronomind_notes/upsert", {
    "vectors": [{
        "id": note_id,
        "vector": vector,                              # 384 numbers
        "meta": { "title": ..., "content": ..., "tags": ..., "created_at": ... },
        "filter": { "topic": "ai" }                    # for filtered search
    }]
})
```

**Searching notes:**
```python
query_vector = embedder.encode(user_question).tolist()
results = await endee_post("/index/chronomind_notes/query", {
    "vector": query_vector,
    "top_k": 5,
    "ef": 128,
    "filter": [{ "topic": { "$eq": "ai" } }]          # Endee filter operator
})
# Returns notes ranked by cosine similarity — most relevant first
```

---

## 🧠 RAG Pipeline

```
User asks: "What do I know about vector search?"
       │
       ▼
Backend embeds the question → 384-dim vector
       │
       ▼
Endee ANN search → top 5 most relevant notes retrieved
       │
       ▼
Notes assembled into context:
  [HNSW Index Note] ...
  [Vector Databases Note] ...
  [Cosine Similarity Note] ...
       │
       ▼
LLM prompt: "Using only these notes, answer: What do I know about vector search?"
       │
       ▼
LLM generates grounded answer ← only from your notes, not from training data
       │
       ▼
Browser shows: answer + source note cards
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Vector DB | Endee (HNSW, cosine, INT8) | Store and search note vectors |
| Embeddings | all-MiniLM-L6-v2 (384 dims) | Convert text to vectors |
| Backend | Python + FastAPI + uvicorn | API server + RAG pipeline |
| HTTP client | httpx (async) | Talk to Endee REST API |
| Frontend | React 18 + Vite + Axios | Web UI |
| Web server | nginx | Serve React + proxy API |
| LLM optional | Anthropic Claude / OpenAI GPT | AI answer synthesis |
| Containers | Docker + Docker Compose | One-command startup |

---

## ❗ Troubleshooting

| Problem | Fix |
|---|---|
| `Cannot connect to Docker` | Open Docker Desktop and wait for green status |
| Endee RAM error (need 4096 MB) | Use Endee Cloud — see Step 2 in this README |
| `Port 3000 already in use` | Change `"3000:80"` to `"3001:80"` in docker-compose.yml |
| `Port 8000 already in use` | Change `"8000:8000"` to `"8001:8000"` |
| Seed script: connection refused | Backend not fully started yet — wait 30 more seconds |
| Endee shows disconnected in UI | Check ENDEE_AUTH_TOKEN value in docker-compose.yml |
| Need to apply code changes | Run `docker compose up --build` to rebuild |

---

## 📄 License

MIT — see [LICENSE](./LICENSE)

---

*Built using [Endee](https://github.com/endee-io/endee) — the high-performance open-source vector database.*
