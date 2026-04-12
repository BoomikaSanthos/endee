"""
seed_data.py — Populate ChronoMind with sample notes for demo purposes.
Run: python scripts/seed_data.py
"""
import httpx, json, sys, time

BASE = "http://localhost:8000/api"

SAMPLE_NOTES = [
    {
        "title": "Understanding Python Decorators",
        "content": (
            "Decorators in Python are a way to modify or enhance functions without changing their "
            "source code. They use the @syntax sugar. A decorator is essentially a function that "
            "takes another function as input, wraps it in some logic, and returns the result. "
            "Key use cases: logging, authentication guards, caching (functools.lru_cache), "
            "timing, and input validation. The order of decorators matters — they apply bottom-up."
        ),
        "tags": ["python", "functions", "advanced"],
        "topic": "programming",
    },
    {
        "title": "Vector Databases Explained",
        "content": (
            "Vector databases store high-dimensional numerical vectors and enable fast approximate "
            "nearest-neighbor (ANN) search. Unlike traditional SQL databases, they excel at "
            "semantic similarity lookups. Core concepts: embedding models convert text/images to "
            "vectors, HNSW is the most popular indexing algorithm, cosine similarity measures "
            "direction, L2 measures distance. Popular choices: Endee, Pinecone, Weaviate, Qdrant, Milvus."
        ),
        "tags": ["ai", "databases", "vectors"],
        "topic": "ai",
    },
    {
        "title": "RAG Pipeline Architecture",
        "content": (
            "Retrieval-Augmented Generation (RAG) combines vector search with LLM generation. "
            "Steps: 1) Chunk and embed documents into a vector DB. 2) At query time, embed the "
            "user question and do semantic search to retrieve top-K relevant chunks. 3) Stuff the "
            "chunks into an LLM prompt as context. 4) LLM generates a grounded answer. "
            "Key metrics to tune: chunk size, overlap, top_k, embedding model quality. "
            "Advanced variants: HyDE, multi-query retrieval, re-ranking."
        ),
        "tags": ["ai", "rag", "llm"],
        "topic": "ai",
    },
    {
        "title": "Git Branching Strategy (GitFlow)",
        "content": (
            "GitFlow defines a strict branching model: main (production), develop (integration), "
            "feature/* (new features branched off develop), release/* (stabilization before merge to main), "
            "hotfix/* (emergency patches off main). Benefits: clean history, parallel development. "
            "Downsides: overhead for small teams. Trunk-based development is a simpler alternative "
            "where everyone branches off and merges back to main frequently with feature flags."
        ),
        "tags": ["git", "devops", "workflow"],
        "topic": "programming",
    },
    {
        "title": "Attention Mechanism in Transformers",
        "content": (
            "Self-attention allows each token to attend to all other tokens in the sequence. "
            "Query, Key, Value matrices are learned projections. Score = softmax(QK^T / sqrt(d_k)) * V. "
            "Multi-head attention runs attention in parallel across H heads, then concatenates. "
            "The 'All You Need Is Attention' paper (Vaswani 2017) introduced the Transformer. "
            "Key insight: attention captures long-range dependencies that RNNs struggle with."
        ),
        "tags": ["ml", "transformers", "nlp"],
        "topic": "ai",
    },
    {
        "title": "Docker vs Kubernetes",
        "content": (
            "Docker packages an application and its dependencies into a container image. "
            "It's great for single-machine local development. Kubernetes (K8s) is a container "
            "orchestration platform for running containers at scale across a cluster. K8s handles: "
            "auto-scaling, self-healing (restarting crashed pods), rolling deployments, service "
            "discovery, and load balancing. Docker Compose is the simpler multi-container local dev "
            "tool. In production, K8s or managed services like ECS/Cloud Run are preferred."
        ),
        "tags": ["devops", "docker", "kubernetes"],
        "topic": "devops",
    },
    {
        "title": "Cosine Similarity vs Dot Product",
        "content": (
            "Cosine similarity measures the angle between two vectors, ignoring magnitude: "
            "cos(θ) = (A·B) / (|A| * |B|). Range: [-1, 1]. Best for text embeddings where "
            "length shouldn't matter. Dot product (inner product) measures magnitude AND direction — "
            "longer vectors get higher scores. If vectors are already normalized (unit length), "
            "cosine and dot product are equivalent. L2 distance measures Euclidean distance and "
            "works best when exact spatial proximity matters."
        ),
        "tags": ["math", "vectors", "similarity"],
        "topic": "ai",
    },
    {
        "title": "Python asyncio Basics",
        "content": (
            "asyncio is Python's built-in async I/O framework. Key primitives: async def (coroutine), "
            "await (pause coroutine), asyncio.run() (entry point), asyncio.gather() (run tasks concurrently). "
            "Event loop processes one task at a time but switches during I/O waits — good for network-bound "
            "workloads, NOT for CPU-bound tasks (use multiprocessing instead). FastAPI, aiohttp, and "
            "httpx are popular async Python libraries. Use asyncio.create_task() for fire-and-forget tasks."
        ),
        "tags": ["python", "async", "concurrency"],
        "topic": "programming",
    },
    {
        "title": "System Design: Rate Limiting",
        "content": (
            "Rate limiting prevents API abuse and ensures fair usage. Common algorithms: "
            "Token Bucket (smooth bursts allowed), Leaky Bucket (constant output rate), "
            "Fixed Window Counter (simple but edge-case prone), Sliding Window Log (accurate, memory heavy). "
            "Redis is the standard backend for distributed rate limiting. Headers to return: "
            "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset. "
            "Apply at: API Gateway (global), per-user, per-IP, per-endpoint."
        ),
        "tags": ["system-design", "api", "scalability"],
        "topic": "devops",
    },
    {
        "title": "HNSW Index — How It Works",
        "content": (
            "Hierarchical Navigable Small World (HNSW) is the leading ANN algorithm for vector search. "
            "It builds a multi-layer graph where upper layers are sparse (long-range connections) and "
            "lower layers are dense (fine-grained neighbors). Search starts at the top and greedily "
            "navigates down, pruning the candidate set at each level. Key params: M (edges per node, "
            "controls graph connectivity), ef_construction (build quality), ef (search quality). "
            "Trade-off: higher M/ef = better recall, more RAM and slower inserts."
        ),
        "tags": ["algorithms", "ai", "vectors"],
        "topic": "ai",
    },
]


def seed():
    print("Seeding ChronoMind with sample notes…")
    ok = 0
    for note in SAMPLE_NOTES:
        try:
            r = httpx.post(f"{BASE}/notes", json=note, timeout=30)
            r.raise_for_status()
            print(f"  ✓ {note['title'][:60]}")
            ok += 1
            time.sleep(0.2)   # be gentle
        except Exception as e:
            print(f"  ✗ {note['title'][:60]}: {e}")
    print(f"\nDone: {ok}/{len(SAMPLE_NOTES)} notes inserted.")


if __name__ == "__main__":
    seed()
