# ChronoMind — System Design

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        User's Browser                           │
│                   React SPA (Vite + Axios)                      │
│   ┌──────────────────┐    ┌──────────────────────────────────┐  │
│   │  Semantic Search │    │    Ask AI (RAG Q&A)              │  │
│   │  Tab             │    │    Tab                           │  │
│   └──────────────────┘    └──────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTP / REST
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Python)                       │
│                                                                  │
│  ┌─────────────────┐   ┌─────────────────┐  ┌───────────────┐  │
│  │  /api/notes     │   │  /api/notes/    │  │  /api/ask     │  │
│  │  POST — create  │   │  search         │  │  POST — RAG   │  │
│  │  DELETE — remove│   │  POST — query   │  │  Q&A pipeline │  │
│  └────────┬────────┘   └────────┬────────┘  └───────┬───────┘  │
│           │                     │                   │           │
│  ┌────────▼─────────────────────▼───────────────────▼────────┐ │
│  │        sentence-transformers (all-MiniLM-L6-v2)            │ │
│  │        Converts text → 384-dim embedding vectors           │ │
│  └────────────────────────────┬───────────────────────────────┘ │
└───────────────────────────────┼─────────────────────────────────┘
                                │ HTTP REST (Endee SDK protocol)
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Endee Vector Database                          │
│               (endeeio/endee-server:latest)                      │
│                                                                  │
│  Index: chronomind_notes                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Vector Record                                              │ │
│  │  ├── id:        UUID                                        │ │
│  │  ├── vector:    float[384]  (embedding)                     │ │
│  │  ├── meta:      { title, content, tags, created_at }        │ │
│  │  └── filter:    { topic }                                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Algorithm: HNSW (Hierarchical Navigable Small World)           │
│  Metric:    Cosine Similarity                                    │
│  Precision: INT8 quantized                                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                    (optional, for full RAG)
                                ▼
                  ┌─────────────────────────┐
                  │  LLM API (optional)     │
                  │  • Anthropic Claude     │
                  │  • OpenAI GPT-4o-mini   │
                  │  • Fallback: extractive │
                  └─────────────────────────┘
```

## Data Flow

### 1. Inserting a Note
```
User writes note
  → FastAPI receives title + content + tags + topic
  → SentenceTransformer encodes: embed(title + "\n\n" + content) → float[384]
  → Endee upsert: { id, vector, meta:{title,content,tags,created_at}, filter:{topic} }
  → Note persisted in Endee's HNSW index
```

### 2. Semantic Search
```
User enters query text
  → FastAPI encodes query → float[384]
  → Endee query: top_k ANN search with optional topic filter
  → Returns notes ranked by cosine similarity
  → Frontend displays results with similarity % scores
```

### 3. RAG Q&A
```
User asks a question
  → FastAPI encodes question → float[384]
  → Endee retrieves top-5 semantically relevant notes
  → Notes assembled into context string
  → LLM prompt: system_prompt + context + question
  → LLM generates grounded answer referencing source notes
  → Frontend shows answer + source cards
```

## Why Endee?

| Feature | Benefit in ChronoMind |
|---|---|
| HNSW indexing | Sub-millisecond ANN search even with thousands of notes |
| Cosine similarity | Works naturally with normalized sentence embeddings |
| Filter support | Narrow search by topic without scanning all vectors |
| Docker deploy | Zero-config vector DB, single `docker run` command |
| INT8 precision | 4× memory savings vs FP32 with negligible accuracy loss |
| REST API | Language-agnostic; works with any backend stack |
