# AI-Powered HRMS — Face Recognition, RAG & Agentic AI

A full-stack Human Resource Management System combining computer vision (face-recognition attendance), a role-based FastAPI + MySQL backend, a React dashboard, and three GenAI features: a RAG-based HR policy chatbot, a tool-calling AI agent for admins, and a Redis/Valkey caching layer for cost optimization.

Built as a personal project to bridge computer vision engineering experience with production GenAI patterns (RAG, agentic tool use, LLM cost tracking).

---

## Demo

### 🤖 AI Admin Agent — Natural-Language Database Queries

https://github.com/Sriram121212/ai-hrms-face-attendance/assets/admin-chatbot-demo.mp4

> Admin asks questions like *"Who was absent this week?"* or *"Show me pending leaves"* — the agent calls safe, pre-written Python tools (no raw SQL) and returns a natural-language answer.

---

### 💬 Employee HR Policy Chat (RAG)

https://github.com/Sriram121212/ai-hrms-face-attendance/assets/employee-hr-policy-demo.mp4

> Employees ask policy questions (leave rules, working hours, benefits) — answers are grounded exclusively in the uploaded HR policy PDF via RAG (ChromaDB + Groq), with Valkey caching for repeated queries.

---

## Features

### Admin Dashboard
- Employee management (CRUD, soft delete)
- Attendance monitoring (manual + face-recognition check-in/checkout)
- Leave approval workflow
- Salary calculation (attendance-based deduction)
- **AI Admin Agent** — ask natural-language questions about attendance, leave, and salary; the agent calls safe, pre-written database tools instead of generating raw SQL
- **HR Policy Management** — upload a PDF once; it's chunked, embedded, and stored permanently
- **GenAI Cost Tracker** — token/cost breakdown by feature, with a live chart and query log

### Employee Dashboard
- Face-recognition or manual check-in/checkout
- Leave application
- Salary slip viewer
- **HR Policy Chat** — ask questions about leave rules, working hours, and benefits; answers are sourced only from uploaded policy documents (RAG)
- Profile view

---

## System Architecture

```mermaid
flowchart TB
    subgraph Clients
        A[React frontend<br/>Admin & employee UI]
        B[Face recognition script<br/>Webcam check-in client]
    end

    subgraph Backend[FastAPI backend — role-based REST API]
        C[Auth & CRUD]
        D[RAG engine]
        E[AI agent]
    end

    F[(MySQL<br/>core data)]
    G[(ChromaDB<br/>policy vectors)]
    H[(Valkey cache<br/>cached answers)]
    I[Groq API<br/>LLM inference]

    A --> Backend
    B --> Backend
    C --> F
    D --> F
    D --> G
    D --> H
    D --> I
    E --> F
    E --> I
```

**Why this split:**
- **Auth & CRUD** handles JWT authentication and standard employee/attendance/leave/salary operations
- **RAG engine** owns the HR policy chatbot — chunking, embedding, retrieval, and cache lookups
- **AI agent** owns natural-language database queries via controlled tool-calling (never raw LLM-generated SQL)

---

## Workflow: HR Policy Chat (RAG)

```mermaid
sequenceDiagram
    participant E as Employee
    participant API as FastAPI
    participant Cache as Valkey
    participant Vec as ChromaDB
    participant LLM as Groq

    E->>API: Ask a question
    API->>Cache: Check exact-match cache
    alt Cache hit
        Cache-->>API: Cached answer
        API-->>E: Return answer (cost: $0)
    else Cache miss
        API->>Vec: Retrieve relevant policy chunks
        Vec-->>API: Top-k chunks
        API->>LLM: Generate answer from context
        LLM-->>API: Answer + token usage
        API->>Cache: Store answer (1hr TTL)
        API->>API: Log tokens/cost to MySQL
        API-->>E: Return answer
    end
```

## Workflow: AI Admin Agent

The admin agent follows the same shape, except retrieval is replaced by a **tool-calling loop**:

1. Admin asks a question (e.g. "Who was absent today?")
2. Groq decides which of 4 named tools to call: `get_attendance_summary`, `get_employee_attendance`, `get_pending_leaves`, `get_salary_info`
3. The backend executes that Python function directly against MySQL (no LLM-generated SQL — safer and predictable)
4. The tool's result is fed back to Groq, which writes the final natural-language answer
5. Usage is logged to `chat_logs` with `chat_type = "admin_agent"`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), Tailwind CSS, Recharts |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | MySQL |
| Face Recognition | Dlib, OpenCV (DNN face detector) |
| Vector Store | ChromaDB (persistent, local) |
| Embeddings | sentence-transformers (local, free) |
| LLM | Groq API (`openai/gpt-oss-120b`) |
| Cache | Redis / Valkey |
| Auth | JWT (python-jose), bcrypt |

---

## Project Structure

```
attendance-backend/
├── app/
│   ├── main.py                  # FastAPI entrypoint, router registration
│   ├── config.py                # Environment variable loading
│   ├── database.py              # SQLAlchemy engine & session
│   ├── models.py                # ORM models
│   ├── schemas.py                # Pydantic request/response schemas
│   ├── auth.py                   # JWT, password hashing, role guards
│   ├── rag_utils.py              # PDF chunking, ChromaDB storage/retrieval
│   ├── groq_client.py            # RAG answer generation via Groq
│   ├── admin_agent.py             # Tool-calling agent loop
│   ├── admin_agent_tools.py       # The 4 database query tools
│   ├── cache.py                   # Valkey caching helpers
│   └── routers/
│       ├── auth_routes.py
│       ├── admin_routes.py
│       ├── attendance_routes.py
│       ├── face_attendance_routes.py
│       ├── leave_routes.py
│       ├── salary_routes.py
│       ├── rag_routes.py
│       ├── admin_agent_routes.py
│       └── cost_tracker_routes.py
├── schema.sql
└── requirements.txt

attendance-frontend/
├── src/
│   ├── api/                      # Axios client + endpoint functions
│   ├── context/                  # Auth & theme context
│   ├── components/                # Sidebar, Topbar, PresenceRibbon, StatCard, etc.
│   ├── layouts/                   # AdminLayout, EmployeeLayout
│   └── pages/
│       ├── admin/
│       └── employee/
└── package.json

face-recognition-client/
└── main_attendance.py            # Webcam capture + Dlib recognition + API calls
```

---

## Setup

### Backend

```bash
cd attendance-backend
python -m venv venv
venv\Scripts\activate            # Windows
pip install -r requirements.txt
cp .env.example .env             # fill in DATABASE_URL, SECRET_KEY, GROQ_API_KEY, DEVICE_API_KEY
mysql -u root -p < schema.sql
uvicorn app.main:app --reload
```

### Frontend

```bash
cd attendance-frontend
npm install
npm run dev
```

### Face Recognition Client

```bash
cd face-recognition-client
# ensure dlib model files are present under data/data_dlib/
python main_attendance.py
```

### Valkey (for caching)

```bash
docker run -d --name valkey-cache -p 6379:6379 valkey/valkey
```

---

## Environment Variables (`.env`)

```
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/attendance_system
SECRET_KEY=your_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
GROQ_API_KEY=your_groq_api_key
DEVICE_API_KEY=your_device_api_key
```

---

## Notes

- **Model:** uses `openai/gpt-oss-120b` on Groq (Llama 3.3 70B was deprecated by Groq on Aug 16, 2026)
- **Security:** the AI agent never generates raw SQL — it selects from a fixed set of parameterized Python functions
- **Persistence:** HR policy PDFs are chunked and embedded once; ChromaDB stores them on disk, so re-uploading is only needed when the policy document changes
