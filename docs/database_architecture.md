# Database Architecture: Video Comparison RAG

## Overview
This document outlines the database design for the AI-Powered Video Comparison RAG application, which stores metadata for YouTube/Instagram videos, generates transcript chunks with embeddings, and maintains chat session history.

## Schema Design
The schema leverages Supabase (PostgreSQL) with the `pgvector` extension.

### Tables
1. **`videos`**: Stores raw metadata for YouTube/Instagram videos (URL, creator info, view counts, duration, and the full transcript).
2. **`transcript_chunks`**: Stores segmented chunks of the transcript. Each chunk has an `embedding` column of type `vector(768)` for semantic similarity search.
3. **`chat_sessions`**: Maintains the high-level grouping of interactions between the user and the system.
4. **`chat_messages`**: Stores individual messages mapped to a specific session.
5. **`citations`**: Maps a `chat_message` to the exact `transcript_chunks` used by the LangGraph RAG chain to generate the answer.

## Scalability
This schema is designed to scale effortlessly for thousands of analyses:
- **HNSW Indexing**: We use Hierarchical Navigable Small World (`hnsw`) indexing on the vector embeddings, allowing incredibly fast Approximate Nearest Neighbor (ANN) search as the database grows, rather than scanning the entire table.
- **In-Database Similarity Search**: The similarity matching runs directly inside PostgreSQL via the `match_transcript_chunks` RPC function using cosine distance (`<=>`). This eliminates the need to fetch large arrays of vectors into the Python application layer, preventing memory and network bottlenecks.
- **Normalization & Constraints**: Separating chat sessions, messages, and citations keeps queries highly optimized and payload sizes small. `ON DELETE CASCADE` ensures that cleaning up old video records effortlessly reclaims space from thousands of chunk vectors without dangling references.

## Example Usage
The Python implementation uses the Repository Pattern and Pydantic models for data validation.

```python
from app.db.repositories.chunk_repository import ChunkRepository

repo = ChunkRepository()

# Search for relevant transcript chunks using pgvector RPC
matches = repo.match_transcript_chunks(
    query_embedding=[0.02, -0.01, ...], # 768-dim vector from Groq API
    match_threshold=0.7,
    match_count=5,
    filter_video_id="550e8400-e29b-41d4-a716-446655440000"
)

for match in matches:
    print(f"Similarity: {match['similarity']}, Text: {match['chunk_text']}")
```
