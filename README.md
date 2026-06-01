# AI-Powered Video Comparison RAG

A production-ready monorepo for an AI-powered Video Comparison RAG application.

## Project Architecture

This application consists of two main parts:
- **Frontend**: A Next.js 15 (App Router) application with Tailwind CSS, Shadcn/UI, and React Query.
- **Backend**: A FastAPI (Python) service integrating with Supabase, pgvector, and LangGraph for RAG capabilities.

## Prerequisites

- Node.js (v18+ recommended)
- Python (v3.10+ recommended)
- Supabase project (for PostgreSQL and pgvector)
- OpenAI API Key

## Setup Instructions

### 1. Environment Setup

Copy `.env.example` to `.env` in both the `frontend` and `backend` directories, or configure them according to your needs.

```bash
cp .env.example .env
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv

# Activate on Windows:
venv\Scripts\activate
# Activate on Unix/MacOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Development Workflow

- The frontend runs on `http://localhost:3000`
- The backend API runs on `http://localhost:8000`
- The backend API documentation (Swagger UI) is available at `http://localhost:8000/docs`
