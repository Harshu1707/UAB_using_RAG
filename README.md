# University Academic Advisor Bot (UAB)

UAB is a production-style full-stack AI academic advisor for university students. It combines a React/Vite chat UI, FastAPI APIs, SQLite analytics, Gemini-powered orchestration, SerpAPI web search, and LangChain + FAISS RAG over uploaded PDFs.

## Features

- JWT authentication with student/admin roles.
- ChatGPT-style multi-turn chat UI with markdown, typing loader, responsive layout, dark/light mode, and voice-input button UI.
- Intent routing to RAG, SQL analytics, web search, or general Gemini chat.
- Admin PDF upload with PyPDF/LangChain parsing, chunking, sentence-transformer embeddings, and FAISS indexing.
- Student analytics APIs and Recharts dashboard for CGPA, pass rate, risk analysis, and distributions.
- Local development setup with environment examples.

## Tech Stack

> This project is intentionally configured for local execution without Docker.


- Frontend: React, Vite, TailwindCSS, React Router, Axios, Context API, Framer Motion, React Markdown, Recharts.
- Backend: FastAPI, SQLAlchemy ORM, SQLite, JWT, dotenv, UploadFile.
- AI/RAG: Gemini API, LangChain, FAISS, sentence-transformers, PyPDFLoader.
- Search: SerpAPI.

## Project Structure

```text
backend/app/
  api/ auth/ core/ db/ models/ rag/ schemas/ services/ utils/ main.py
frontend/src/
  components/ pages/ services/ hooks/ context/ layouts/ routes/ assets/ App.jsx
```

## Environment Setup

Backend:

```bash
cp backend/.env.example backend/.env
# edit backend/.env and provide GEMINI_API_KEY, SERPAPI_API_KEY, JWT_SECRET
```

Frontend:

```bash
cp frontend/.env.example frontend/.env
```

## Run Locally

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

Demo users seeded on startup:

- Admin: `admin@uab.edu` / `admin123`
- Student: `student@uab.edu` / `student123`

## Main API Endpoints

- `POST /auth/register`
- `POST /auth/login`
- `POST /chat`
- `POST /upload-pdf`
- `GET /student/{id}`
- `GET /topper/{department}`
- `GET /analytics/pass-rate`
- `GET /analytics/at-risk`
- `GET /analytics/cgpa-distribution`
- `POST /search/web`

## Sample Questions

- "What are semester 5 electives?"
- "Who is topper in CSE?"
- "Show at-risk students"
- "Find average CGPA of ECE"
- "Latest AI internships for students"
