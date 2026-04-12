"""
ChronoMind Backend - FastAPI application
Personal Learning Journal with AI-powered semantic memory retrieval
"""
from __future__ import annotations

import os
import uuid
import asyncio
from datetime import datetime, timezone
from typing import Optional, List

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# Config

ENDEE_BASE_URL    = os.getenv("ENDEE_BASE_URL",    "http://localhost:8001/api/v1")
ENDEE_AUTH_TOKEN  = os.getenv("ENDEE_AUTH_TOKEN",  "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY",    "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

INDEX_NAME = "chronomind_notes"
EMBED_DIM  = 384

# FastAPI app

app = FastAPI(
    title="ChronoMind API",
    version="1.0.0",
    responses={
        500: {"description": "Internal server error"},
        502: {"description": "Endee vector database error"},
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Embedder (loaded once)

embedder: Optional[SentenceTransformer] = None

def get_embedder() -> SentenceTransformer:
    global embedder
    if embedder is None:
        print("Loading sentence-transformers model …")
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
        print("Model loaded ✓")
    return embedder

def embed(text: str) -> List[float]:
    return get_embedder().encode(text, normalize_embeddings=True).tolist()

# Endee helpers

def endee_headers() -> dict:
    h: dict = {"Content-Type": "application/json"}
    if ENDEE_AUTH_TOKEN:
        h["Authorization"] = ENDEE_AUTH_TOKEN
    return h

async def endee_get(path: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{ENDEE_BASE_URL}{path}", headers=endee_headers())
        r.raise_for_status()
        return r.json()

async def endee_post(path: str, body: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{ENDEE_BASE_URL}{path}",
            json=body,
            headers=endee_headers(),
        )
        r.raise_for_status()
        return r.json()

# Startup — ensure index exists

@app.on_event("startup")
async def startup() -> None:
    get_embedder()
    max_retries = 10

    for i in range(max_retries):
        try:
            indexes = await endee_get("/index/list")
            existing = [idx.get("name") for idx in (indexes if isinstance(indexes, list) else indexes.get("indexes", []))]

            if INDEX_NAME not in existing:
                await endee_post("/index/create", {
                    "index_name": INDEX_NAME,
                    "dim": EMBED_DIM,
                    "space_type": "cosine",
                    "precision": "int8"
                })
                print(f"Index '{INDEX_NAME}' created ✓")
            else:
                print(f"Index '{INDEX_NAME}' already exists ✓")

            # Successfully connected and ensured index exists, breakout of retry loop
            return
        except Exception as e:
            print(f"Waiting for Endee to start (attempt {i+1}/{max_retries}). Error: {e}")
            await asyncio.sleep(3)

    print("Warning: Could not connect to Endee gracefully on startup. Saving might fail until it comes online.")

# Pydantic schemas

class NoteCreate(BaseModel):
    title:   str
    content: str
    tags:    List[str] = []
    topic:   str = "general"

class NoteResponse(BaseModel):
    id:         str
    title:      str
    content:    str
    tags:       List[str]
    topic:      str
    created_at: str
    similarity: Optional[float] = None

class SearchRequest(BaseModel):
    query:        str
    top_k:        int = 5
    topic_filter: Optional[str]       = None
    tags_filter:  Optional[List[str]] = None

class RAGRequest(BaseModel):
    question:     str
    top_k:        int = 5
    topic_filter: Optional[str] = None

class RAGResponse(BaseModel):
    answer:      str
    sources:     List[NoteResponse]
    tokens_used: int = 0

# Health check

@app.get("/health")
@app.get("/api/health")
async def health() -> dict:
    try:
        await endee_get("/index/list")
        endee_status = "connected"
    except Exception:
        endee_status = "disconnected"
    return {"status": "ok", "endee": endee_status}

# Create note

@app.post(
    "/notes",
    status_code=201,
    responses={502: {"description": "Endee upsert failed"}, 500: {"description": "Unexpected error"}},
)
@app.post(
    "/api/notes",
    status_code=201,
    responses={502: {"description": "Endee upsert failed"}, 500: {"description": "Unexpected error"}},
)
async def create_note(note: NoteCreate) -> NoteResponse:
    note_id    = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    vector     = embed(f"{note.title}\n\n{note.content}")
    tags_str   = ",".join(note.tags) if note.tags else ""

    try:
        await endee_post(f"/index/{INDEX_NAME}/vector/insert", {
            "id":     note_id,
            "vector": vector,
            "meta":   import_json.dumps({
                "title":      note.title,
                "content":    note.content,
                "tags":       tags_str,
                "created_at": created_at,
            }),
            "filter": import_json.dumps({"topic": note.topic})
        })
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Endee upsert failed: {exc.response.status_code} — {exc.response.text}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save note: {exc}",
        ) from exc

    return NoteResponse(
        id=note_id,
        title=note.title,
        content=note.content,
        tags=note.tags,
        topic=note.topic,
        created_at=created_at,
    )

# Search notes

@app.post(
    "/notes/search",
    response_model=List[NoteResponse],
    responses={502: {"description": "Endee query failed"}},
)
@app.post(
    "/api/notes/search",
    response_model=List[NoteResponse],
    responses={502: {"description": "Endee query failed"}},
)
async def search_notes(req: SearchRequest) -> List[NoteResponse]:
    payload: dict = {
        "vector":          embed(req.query),
        "k":               req.top_k,
        "ef":              128,
        "include_vectors": False,
    }
    if req.topic_filter:
        payload["filter"] = f'[{"topic":{"$eq":{req.topic_filter}}}]'

    try:
        results = await endee_post(f"/index/{INDEX_NAME}/query", payload)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Endee query failed: {exc.response.status_code} — {exc.response.text}",
        ) from exc

    raw   = results if isinstance(results, list) else results.get("results", [])
    notes: List[NoteResponse] = []

    for item in raw:
        meta_str = item.get("meta", "{}")
        try:
            meta = import_json.loads(meta_str)
        except:
            meta = {}
        tags_raw = meta.get("tags", "")
        tags     = [t for t in tags_raw.split(",") if t] if tags_raw else []

        if req.tags_filter and not any(tag in tags for tag in req.tags_filter):
            continue

        notes.append(NoteResponse(
            id=item["id"],
            title=meta.get("title", ""),
            content=meta.get("content", ""),
            tags=tags,
            topic=item.get("filter", {}).get("topic", "general"),
            created_at=meta.get("created_at", ""),
            similarity=round(item.get("similarity", 0), 4),
        ))
    return notes

# Delete note

@app.delete(
    "/notes/{note_id}",
    responses={500: {"description": "Delete failed"}},
)
@app.delete(
    "/api/notes/{note_id}",
    responses={500: {"description": "Delete failed"}},
)
async def delete_note(note_id: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.delete(
                f"{ENDEE_BASE_URL}/index/{INDEX_NAME}/vector/{note_id}/delete",
                headers=endee_headers(),
            )
            r.raise_for_status()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {exc}",
        ) from exc
    return {"deleted": note_id}

# RAG Q&A

@app.post(
    "/ask",
    responses={502: {"description": "Endee query failed"}},
)
@app.post(
    "/api/ask",
    responses={502: {"description": "Endee query failed"}},
)
async def ask(req: RAGRequest) -> RAGResponse:
    payload: dict = {
        "vector":          embed(req.question),
        "k":               req.top_k,
        "ef":              200,
        "include_vectors": False,
    }
    if req.topic_filter:
        payload["filter"] = f'[{"topic":{"$eq":{req.topic_filter}}}]'

    try:
        results = await endee_post(f"/index/{INDEX_NAME}/query", payload)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Endee query failed: {exc}",
        ) from exc

    raw     = results if isinstance(results, list) else results.get("results", [])
    sources: List[NoteResponse] = []
    context_parts: List[str]   = []

    for item in raw:
        meta_str = item.get("meta", "{}")
        try:
            meta = import_json.loads(meta_str)
        except:
            meta = {}
        tags_raw = meta.get("tags", "")
        note     = NoteResponse(
            id=item["id"],
            title=meta.get("title", ""),
            content=meta.get("content", ""),
            tags=tags,
            topic=import_json.loads(item.get("filter", '{"topic":"general"}')).get("topic", "general"),
            created_at=meta.get("created_at", ""),
            similarity=round(item.get("similarity", 0), 4),
        )
        sources.append(note)
        context_parts.append(f"[{note.title}] ({note.created_at[:10]})\n{note.content}")

    if not sources:
        return RAGResponse(
            answer="I couldn't find any relevant notes. Try adding some notes first!",
            sources=[],
        )

    answer, tokens = await synthesize_answer(req.question, "\n\n---\n\n".join(context_parts))
    return RAGResponse(answer=answer, sources=sources, tokens_used=tokens)

async def synthesize_answer(question: str, context: str) -> tuple[str, int]:
    system_prompt = (
        "You are ChronoMind, an intelligent assistant that helps users recall and "
        "synthesize their personal learning notes. Answer the user's question using "
        "ONLY the provided notes as context. Be concise, specific, and reference "
        "which notes you drew from. If the notes don't contain enough info, say so."
    )
    user_prompt = f"My notes:\n{context}\n\nQuestion: {question}"

    if ANTHROPIC_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key":         ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "Content-Type":      "application/json",
                    },
                    json={
                        "model":    "claude-haiku-4-5-20251001",
                        "max_tokens": 512,
                        "system":   system_prompt,
                        "messages": [{"role": "user", "content": user_prompt}],
                    },
                )
                data = r.json()
                return data["content"][0]["text"], data.get("usage", {}).get("output_tokens", 0)
        except Exception as exc:
            print(f"Anthropic error: {exc}")

    if OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                    json={
                        "model":      "gpt-4o-mini",
                        "max_tokens": 512,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user",   "content": user_prompt},
                        ],
                    },
                )
                data = r.json()
                return (
                    data["choices"][0]["message"]["content"],
                    data.get("usage", {}).get("completion_tokens", 0),
                )
        except Exception as exc:
            print(f"OpenAI error: {exc}")

    # Extractive fallback — no LLM key needed
    lines = [f"• {src.split(chr(10))[0]}" for src in context.split("---")[:3]]
    return (
        f"Based on your notes, here are the most relevant entries for '{question}':\n\n"
        + "\n".join(lines)
        + "\n\n(Tip: Set ANTHROPIC_API_KEY or OPENAI_API_KEY for full AI synthesis.)",
        0,
    )

# Serve frontend (if built)

_frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(_frontend_dist):
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(_frontend_dist, "assets")),
        name="assets",
    )

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str) -> FileResponse:
        return FileResponse(os.path.join(_frontend_dist, "index.html"))