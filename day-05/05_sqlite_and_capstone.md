# Chapter 5: SQLite, Full-Stack Architecture & Capstone Project

> *"In this final chapter, we bring all the pieces together. We replace temporary in-memory collections with persistent relational storage using SQLite, write secure parameterized SQL queries, wire the full end-to-end stack into FastAPI, verify the system with automated pytest suites, and launch your capstone project."*

---

## 1. Introduction: The Need for Persistent Relational Storage

Over the past four chapters, we evolved our Python code from basic syntax snippets into structured dataclasses, async web clients, and FastAPI route controllers. However, whenever the web server restarted, all state disappeared.

A production-ready application requires **persistent, structured, ACID-compliant storage**.

### Why SQLite is the Ideal Database for Modern Python Services

- **Zero-Configuration:** No external database servers (like PostgreSQL or MySQL) to install, configure, or authenticate with.
- **Single-File Portability:** The entire relational database lives in a single `.db` file on your filesystem.
- **Built into Python:** Python includes the `sqlite3` C-binding directly in the standard library.
- **Standard SQL:** Writing clean SQL queries in SQLite makes transitioning to PostgreSQL in the cloud seamless when your app scales.

---

## 2. Relational SQL Fundamentals & `sqlite3`

Relational databases organize structured data into **Tables** containing **Columns** and **Rows**.

### Essential Table Schema

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'Normal',
    completed INTEGER DEFAULT 0,  -- SQLite stores booleans as 0 or 1
    tags TEXT DEFAULT '[]',        -- Stored as JSON text
    created_at TEXT NOT NULL
);
```

### Python `sqlite3` Connection & Row Factory

By default, `sqlite3` returns query results as plain tuples (`(1, "Deploy API", ...)`). Setting `conn.row_factory = sqlite3.Row` allows you to access columns by name like a Python dictionary (`row["title"]`):

```python
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "data" / "tasks.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    # Enable dictionary-style column access
    conn.row_factory = sqlite3.Row
    return conn
```

---

## 3. The #1 Security Trap: SQL Injection vs. Parameterized Queries

> [!CAUTION]
> **NEVER concatenate or format user variables directly into SQL queries using f-strings.**  
> String interpolation in SQL opens catastrophic **SQL Injection** vulnerabilities (OWASP Top 10).

```python
# ❌ VULNERABLE TO SQL INJECTION:
user_input = "'; DROP TABLE tasks; --"
cursor.execute(f"SELECT * FROM tasks WHERE title = '{user_input}'")
# Destroys the database table!

# ✅ SECURE: PARAMETERIZED PLACEHOLDERS
# Pass variables as a tuple in the second argument:
cursor.execute(
    "SELECT * FROM tasks WHERE title = ?",
    (user_input,)  # Passed as tuple
)
# The database engine treats user_input strictly as literal string data.
```

---

## 4. End-to-End Architecture: The 6-Stage Request Flow

Here is how data flows through a clean, decoupled 3-layer FastAPI application:

```text
1. Client (Browser / React / Mobile)
   ↓ HTTP POST /tasks {"title": "Deploy API", "priority": "High"}
2. FastAPI Router (app/main.py)
   ↓ Thin controller extracts payload and routes to service
3. Pydantic Runtime Validation (app/models.py)
   ↓ Validates constraints (TaskCreate) -> Returns 422 if invalid
4. Service Layer (app/services.py)
   ↓ Executes business logic and database queries
5. SQLite Database (app/database.py -> tasks.db)
   ↓ Executes parameterized SQL INSERT, commits to disk
6. JSON Response Model (app/models.py -> TaskResponse)
   ↓ Serializes safe JSON back to client (HTTP 201 Created)
```

---

## 5. Automated Testing with `pytest` and `TestClient`

In Python, writing automated test suites is remarkably straightforward with **`pytest`**.

### Adding `pytest` to your Project

```bash
uv add --dev pytest
uv run pytest
```

### Writing Integration Tests (`tests/test_api.py`)

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_task():
    # 1. POST /tasks
    create_res = client.post(
        "/tasks",
        json={"title": "Automated Testing Task", "priority": "High"}
    )
    assert create_res.status_code == 201
    task_id = create_res.json()["id"]

    # 2. GET /tasks/{id}
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Automated Testing Task"

    # 3. DELETE /tasks/{id}
    del_res = client.delete(f"/tasks/{task_id}")
    assert del_res.status_code == 204

    # 4. Verify 404
    missing_res = client.get(f"/tasks/{task_id}")
    assert missing_res.status_code == 404
```

---

## 6. The 5-Day Journey Retrospective

Congratulations! Over 5 days, you have progressed from Python syntax fundamentals to a complete, production-ready full-stack architecture:

```text
Day 1: "I can write idiomatic Python syntax and collections."
  ↓
Day 2: "I can organize Python into modular classes, dataclasses, and packages."
  ↓
Day 3: "I can make Python communicate asynchronously with web APIs and scrape data."
  ↓
Day 4: "I can expose strongly typed REST APIs with FastAPI and Pydantic."
  ↓
Day 5: "I can persist relational data with SQLite, write tests, and build full applications."
```

---

## 7. Capstone Project Guidelines

Your final course outcome is to build a practical capstone project combining your existing frontend/web skills with Python.

### Suggested Capstone Tracks

1. **Expense Tracker & Financial Dashboard:**
   - **Backend:** FastAPI + Pydantic + SQLite spending aggregations (`SUM()`, `GROUP BY`).
   - **Frontend:** React / Chart.js spending breakdown graphs.

2. **Automated Bookmark Manager & Metadata Harvester:**
   - **Backend:** HTTPX + BeautifulSoup4 OpenGraph tag extractor + SQLite store.
   - **Frontend:** Visual card preview grid with tag filtering.

3. **Real-Time Website & API Uptime Monitor:**
   - **Backend:** Async ping scheduler tracking latency history in SQLite.
   - **Frontend:** Status sparklines and incident timelines.

4. **GitHub Developer Analytics Dashboard:**
   - **Backend:** GitHub REST API consumer + SQLite cache.
   - **Frontend:** Repository search and comparison metrics.

### Capstone Evaluation Rubric

- **Architecture (25%):** Decoupled 3-layer layout (`models.py`, `services.py`, `main.py`).
- **Persistence (25%):** Safe parameterized SQLite queries (`?` placeholders).
- **Usability (25%):** Functional user interface (Web UI or CLI) and interactive Swagger docs at `/docs`.
- **Testing & Docs (25%):** Comprehensive `README.md` setup guide and passing `pytest` suite.

---

## 8. Where to Go Next: Expanding Your Python Journey

Now that you have a rock-solid Python foundation, here are the three major specialized pathways you can pursue:

1. **Enterprise Cloud & Backend:**
   - Deploying FastAPI on Docker and Kubernetes
   - Advanced ORMs (SQLAlchemy 2.0 / SQLModel) and PostgreSQL
   - Asynchronous background task queues (Celery / Redis / ARQ)

2. **AI & LLM Application Engineering:**
   - Building Retrieval-Augmented Generation (RAG) pipelines with LangChain & LlamaIndex
   - Vector databases (ChromaDB, Qdrant, Pinecone)
   - Function calling & structured LLM outputs using Pydantic
   - Building autonomous multi-agent systems with Antigravity

3. **Data Engineering & Automation:**
   - Data analysis with Pandas and Polars
   - Interactive data apps with Streamlit
   - Headless browser automation with Playwright
