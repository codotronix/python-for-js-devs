# Day 5: Full-Stack Task REST API with SQLite Persistence

A production-ready REST API built with **FastAPI**, **Pydantic v2**, and persistent **SQLite** relational storage with SQL injection safeguards and automated testing.

---

## 1. Project Architecture

This application represents the complete end-to-end Python architecture from the 5-day curriculum:

```text
day-05/app/
├── __init__.py      # Package indicator
├── database.py      # SQLite connection manager, row_factory setup, and schema init
├── models.py        # Pydantic schemas (TaskCreate, TaskUpdate, TaskResponse)
├── services.py      # Parameterized SQL repository & business logic layer
├── main.py          # FastAPI application with lifespan database hook & CORS
├── data/            # Local directory containing the SQLite database file
│   └── tasks.db     # Single-file SQLite database (auto-generated on startup)
└── README.md        # Execution and testing guide
```

---

## 2. Prerequisites & Dependencies

Ensure you have **Python 3.10+** and **`uv`** installed.

```bash
# Add FastAPI and testing dependencies
uv add "fastapi[standard]"
uv add --dev pytest httpx
```

---

## 3. Running the Persistent API

### Command 1: Fast CLI Runner

```bash
# From the workspace root:
uv run fastapi dev day-05/app/main.py
```

### Command 2: Standard Uvicorn Runner

```bash
# From inside the day-05 directory:
cd day-05
uv run uvicorn app.main:app --reload --port 8000
```

### Database Initialization on Startup
When the server boots up, FastAPI's `lifespan` hook calls `init_db()` in `app/database.py`. It creates `app/data/tasks.db` and populates sample records automatically if the table does not exist.

Access the live services:
- **API Base:** `http://localhost:8000`
- **Interactive Swagger Docs:** `http://localhost:8000/docs`
- **ReDoc Documentation:** `http://localhost:8000/redoc`

---

## 4. API Endpoints Reference

| Method | Endpoint | Description | Request Body | Response Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API Health & Info | None | `200 OK` |
| `GET` | `/tasks` | List tasks (supports `?priority=`, `?completed=`, `?tag=`, `?limit=`) | None | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve single task by ID | None | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Insert a new task into SQLite | `TaskCreate` JSON | `201 Created` / `422 Error` |
| `PUT` | `/tasks/{id}` | Update existing task in SQLite | `TaskUpdate` JSON | `200 OK` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Remove a task from SQLite | None | `204 No Content` / `404` |

---

## 5. Running Automated Tests with `pytest`

The application includes automated integration tests using FastAPI's `TestClient`.

### Run the Test Suite

```bash
# Run pytest across the project
uv run pytest
```

---

## 6. Example API Requests (`curl`)

### 1. Insert a New Task (`POST /tasks`)

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Launch Capstone Project",
    "description": "Build full-stack financial dashboard consuming FastAPI",
    "priority": "Urgent",
    "tags": ["capstone", "react", "sqlite"]
  }'
```

### 2. Query High Priority Tasks (`GET /tasks`)

```bash
curl "http://localhost:8000/tasks?priority=Urgent"
```

### 3. Update Task Status (`PUT /tasks/1`)

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### 4. Delete a Task (`DELETE /tasks/1`)

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

---

## 7. Verifying Persistence

To verify that your data persists across server restarts:
1. Create a new task using the `POST /tasks` command above.
2. Stop the server (`Ctrl + C`).
3. Start the server again (`uv run fastapi dev day-05/app/main.py`).
4. Execute `GET /tasks`—your created task will remain intact in `app/data/tasks.db`!
