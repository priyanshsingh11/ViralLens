-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Videos table
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform VARCHAR(50) NOT NULL,
    url TEXT NOT NULL UNIQUE,
    creator_name TEXT,
    creator_followers INTEGER,
    views INTEGER,
    likes INTEGER,
    comments INTEGER,
    engagement_rate NUMERIC(5, 4),
    upload_date TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    transcript TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Transcript Chunks table
CREATE TABLE transcript_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create HNSW index for fast similarity search using cosine distance
CREATE INDEX idx_transcript_chunks_embedding ON transcript_chunks USING hnsw (embedding vector_cosine_ops);

-- 3. Chat Sessions table
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Chat Messages table
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Citations table
CREATE TABLE citations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES chat_messages(id) ON DELETE CASCADE,
    video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    chunk_id UUID NOT NULL REFERENCES transcript_chunks(id) ON DELETE CASCADE
);

-- 6. Similarity search function (RPC)
CREATE OR REPLACE FUNCTION match_transcript_chunks(
    query_embedding vector(1536),
    match_threshold float,
    match_count int,
    filter_video_ids uuid[] DEFAULT NULL
)
RETURNS TABLE (
    id uuid,
    video_id uuid,
    chunk_index int,
    chunk_text text,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        transcript_chunks.id,
        transcript_chunks.video_id,
        transcript_chunks.chunk_index,
        transcript_chunks.chunk_text,
        1 - (transcript_chunks.embedding <=> query_embedding) AS similarity
    FROM transcript_chunks
    WHERE 
        (filter_video_ids IS NULL OR transcript_chunks.video_id = ANY(filter_video_ids))
        AND 1 - (transcript_chunks.embedding <=> query_embedding) > match_threshold
    ORDER BY transcript_chunks.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
