# Day 4: Task Management REST API (FastAPI + Pydantic)

A modern, strongly typed REST API built with **FastAPI** and **Pydantic v2**, designed for clean integration with frontend web frameworks (React, Next.js, Vue, Svelte).

---

## 1. Project Architecture

This application follows the decoupled **3-Layer Architecture** (Thin Controllers + Domain Services):

```text
day-04/app/
├── __init__.py      # Package indicator
├── models.py        # Pydantic validation schemas (TaskCreate, TaskUpdate, TaskResponse)
├── services.py      # Business logic & TaskManagerService layer
├── main.py          # FastAPI application, route controllers, and CORS configuration
└── README.md        # Setup and execution instructions
```

---

## 2. Prerequisites & Installation

Ensure you have **Python 3.10+** and **`uv`** installed.

### Option A: Using `uv` (Recommended)

From the project root directory:

```bash
# Add FastAPI with standard dependencies (includes Uvicorn, Pydantic, and starlette)
uv add "fastapi[standard]"
```

---

## 3. Running the Development Server

### Command 1: Fast CLI Runner

```bash
# From the workspace root:
uv run fastapi dev day-04/app/main.py
```

### Command 2: Standard Uvicorn Runner

```bash
# From inside the day-04 directory:
cd day-04
uv run uvicorn app.main:app --reload --port 8000
```

Once started, the server will be available at:
- **API Base URL:** `http://localhost:8000`
- **Interactive Swagger UI:** `http://localhost:8000/docs`
- **Alternative ReDoc UI:** `http://localhost:8000/redoc`
- **OpenAPI JSON Spec:** `http://localhost:8000/openapi.json`

---

## 4. API Endpoints Reference

| Method | Endpoint | Description | Request Body | Response Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API Health & Info | None | `200 OK` |
| `GET` | `/tasks` | List tasks (supports `?priority=`, `?completed=`, `?tag=`, `?limit=`) | None | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve single task by ID | None | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create a new task | `TaskCreate` JSON | `201 Created` / `422 Error` |
| `PUT` | `/tasks/{id}` | Update existing task fields | `TaskUpdate` JSON | `200 OK` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Remove a task | None | `204 No Content` / `404` |

---

## 5. Example API Requests (`curl`)

### 1. Create a Task (`POST /tasks`)

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Connect React Frontend to FastAPI",
    "description": "Integrate useQuery hooks with /tasks endpoint",
    "priority": "High",
    "tags": ["frontend", "api"]
  }'
```

### 2. List Tasks with Filters (`GET /tasks`)

```bash
curl "http://localhost:8000/tasks?priority=High&completed=false"
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

## 6. Testing Validation Behavior (HTTP 422)

FastAPI and Pydantic automatically reject malformed payloads. Try sending an invalid priority or a title shorter than 3 characters:

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "ab", "priority": "InvalidPriority"}'
```

**Response (`HTTP 422 Unprocessable Entity`):**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "String should have at least 3 characters",
      "type": "string_too_short"
    },
    {
      "loc": ["body", "priority"],
      "msg": "String should match pattern '^(Low|Normal|High|Urgent)$'",
      "type": "string_pattern_mismatch"
    }
  ]
}
```
