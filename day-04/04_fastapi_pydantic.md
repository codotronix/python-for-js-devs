# Chapter 4: FastAPI & Pydantic (Building Strongly-Typed REST APIs)

> *"In the previous chapters, we mastered Python's core language syntax, modular application design, and asynchronous web client libraries. Now, we step into the backend realm to build high-performance, strongly typed REST APIs that seamlessly connect to modern JavaScript and TypeScript frontends."*

---

## 1. Introduction: The Full-Stack Web Boundary

If you build web applications using React, Vue, Svelte, or Next.js, you interact with REST and JSON APIs daily.

Traditionally in Node.js, you might use Express or Fastify combined with Zod or TypeScript to validate incoming JSON payloads and format responses.

**FastAPI** is Python's premier modern web framework. It unites three powerful technologies:
1. **Starlette:** The high-performance ASGI web toolkit handling routing, middleware, and WebSockets.
2. **Pydantic (v2):** The data validation engine that enforces types and constraints at runtime.
3. **Uvicorn:** The production ASGI server that executes asynchronous Python coroutines at near-C speed.

### Why FastAPI is Beloved by Frontend Developers

- **Zero-Config Swagger UI (`/docs`):** Automatically generates an interactive API documentation portal.
- **Runtime Validation:** Rejects malformed JSON with descriptive HTTP 422 errors automatically.
- **Native Async:** First-class `async def` and `await` support for non-blocking I/O.
- **OpenAPI Schema Generation:** Export `/openapi.json` to automatically generate TypeScript client types via tools like `openapi-typescript`.

---

## 2. Managing FastAPI with `uv`

Adding FastAPI and launching the development server using `uv` is seamless:

```bash
# 1. Install FastAPI standard bundle (includes Uvicorn and Pydantic)
uv add "fastapi[standard]"

# 2. Run the development server with live reload enabled
uv run fastapi dev app/main.py

# Or using the standard Uvicorn runner:
uv run uvicorn app.main:app --reload --port 8000
```

Once running, your API is live at `http://localhost:8000` and interactive docs are available at `http://localhost:8000/docs`.

---

## 3. Pydantic v2: Strongly-Typed Schemas & Runtime Validation

In TypeScript, types and interfaces only exist during compilation; at runtime, `JSON.parse()` can still introduce unexpected shapes.

In Python, **Pydantic** validates data at **runtime**:

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        description="The title of the task",
        examples=["Implement OAuth 2.0 flow"]
    )
    priority: str = Field(
        default="Normal",
        pattern="^(Low|Normal|High|Urgent)$",
        description="Task priority level"
    )
    completed: bool = False
    tags: list[str] = Field(default_factory=list)

# 1. Instantiation with Automatic Type Coercion
# If string "101" is passed to an integer field, Pydantic parses it safely!
task = TaskCreate(title="Setup Redis", priority="High")

# 2. Exporting to Dictionary or JSON String
raw_dict = task.model_dump()        # Python dict: {'title': 'Setup Redis', ...}
json_string = task.model_dump_json() # JSON string: '{"title": "Setup Redis", ...}'
```

### Automatic HTTP 422 Error Responses

If a frontend client sends an invalid payload (e.g. `{"title": "a", "priority": "Invalid"}`), FastAPI catches Pydantic's `ValidationError` and automatically responds with HTTP **422 Unprocessable Entity**:

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

---

## 4. Routing & Parameter Cheatsheet

FastAPI automatically parses path parameters, query strings, and JSON request bodies depending on where and how arguments are typed in your route function.

```python
from fastapi import FastAPI, HTTPException, status, Query, Path

app = FastAPI(title="Task API")

# 1. Path Parameters: Declared in the URL template {task_id}
@app.get("/tasks/{task_id}")
def get_task(task_id: int = Path(..., ge=1, description="ID of the task")):
    return {"task_id": task_id}

# 2. Query Parameters: Declared as primitive function arguments NOT in URL path
@app.get("/tasks")
def list_tasks(
    priority: str | None = Query(default=None),
    completed: bool | None = None,
    limit: int = Query(default=20, ge=1, le=100)
):
    return {"priority": priority, "completed": completed, "limit": limit}

# 3. Request Body: Declared as a Pydantic Model parameter
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    return {"id": 101, **payload.model_dump()}
```

---

## 5. Protecting Data with `response_model`

When sending data back to the client, you often want to omit private internal fields (such as hashed passwords or internal database keys).

Using `response_model` ensures FastAPI filters the outgoing JSON strictly through the designated response schema:

```python
class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    completed: bool
    created_at: str

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int):
    # Even if the underlying database record contains private fields,
    # FastAPI only serializes the fields defined in TaskResponse!
    return task_service.get_task(task_id)
```

---

## 6. Error Handling with `HTTPException`

In FastAPI, return standard HTTP error responses by raising **`HTTPException`**:

```python
from fastapi import HTTPException, status

@app.get("/tasks/{task_id}")
def get_task_or_fail(task_id: int):
    task = task_service.find_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
    return task
```

---

## 7. Decoupled 3-Layer Project Architecture

To build maintainable, enterprise-ready APIs, follow the **Thin Controller** pattern: keep routes small and delegate domain logic to services.

```text
app/
├── __init__.py
├── models.py        # Pydantic request and response schemas
├── services.py      # Business logic & repository access
└── main.py          # FastAPI application & route controllers
```

### Implementation Walkthrough

#### 1. `app/models.py`
```python
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    priority: str = Field(default="Normal", pattern="^(Low|Normal|High|Urgent)$")
    tags: list[str] = []

class TaskCreate(TaskBase):
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str | None = None
    priority: str | None = None
    completed: bool | None = None

class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: str
```

#### 2. `app/services.py`
```python
from datetime import datetime, timezone
from app.models import TaskCreate, TaskUpdate

class TaskManagerService:
    def __init__(self):
        self.tasks: list[dict] = []
        self._next_id = 1

    def create(self, task_in: TaskCreate) -> dict:
        record = {
            "id": self._next_id,
            **task_in.model_dump(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.tasks.append(record)
        self._next_id += 1
        return record

    def list_all(self) -> list[dict]:
        return self.tasks

    def get_by_id(self, task_id: int) -> dict | None:
        return next((t for t in self.tasks if t["id"] == task_id), None)

task_service = TaskManagerService()
```

#### 3. `app/main.py`
```python
from fastapi import FastAPI, HTTPException, status
from app.models import TaskCreate, TaskResponse
from app.services import task_service

app = FastAPI(title="Task REST API")

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks():
    return task_service.list_all()

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    return task_service.create(payload)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = task_service.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

---

## 8. Critical Gotchas in FastAPI Development

### Gotcha 1: Blocking Code in `async def` Routes
If you declare an endpoint with `async def`, **never call blocking synchronous functions** (such as `time.sleep()`, synchronous `open()`, or blocking DB drivers) inside it! That will block the single event loop. Either use non-blocking async libraries or declare the endpoint with regular `def` (which runs in FastAPI's external thread pool).

### Gotcha 2: Fat Routes Anti-Pattern
Never write SQL queries, file parsing, or complex data aggregation directly inside your route functions. Keep routes under 10 lines of code and delegate work to `services.py`.

---

## 9. Practice Challenge: Full CRUD Task API

### The Challenge

Complete the Task API by implementing:
1. `GET /tasks` with filtering by `?priority=` and `?completed=`.
2. `GET /tasks/{task_id}` returning 404 if missing.
3. `POST /tasks` validating incoming JSON.
4. `PUT /tasks/{task_id}` for partial updates.
5. `DELETE /tasks/{task_id}` returning `204 No Content`.

### Challenge Verification via TestClient

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_task_lifecycle():
    # 1. Create task
    res = client.post("/tasks", json={"title": "Test FastAPI", "priority": "High"})
    assert res.status_code == 201
    task_id = res.json()["id"]

    # 2. Get task
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Test FastAPI"

    # 3. Delete task
    del_res = client.delete(f"/tasks/{task_id}")
    assert del_res.status_code == 204

    # 4. Verify 404
    missing_res = client.get(f"/tasks/{task_id}")
    assert missing_res.status_code == 404

print("All API integration tests passed successfully!")
```

---

## 10. Chapter Summary & Bridge to Day 5

### What We Mastered
- Defining strongly typed Pydantic models with `Field(...)` constraints and type coercion.
- Building REST APIs with FastAPI route decorators and parameter extraction.
- Automatic interactive documentation with Swagger UI (`/docs`).
- Decoupling web applications into a 3-layer architecture (`models.py`, `services.py`, `main.py`).
- Testing API endpoints programmatically using `TestClient`.

### Looking Ahead to Day 5: SQLite & Capstone Integration
In our final session, we complete the full application stack:
- Connecting Python to a persistent relational database: **SQLite**
- Writing parameterized SQL queries to prevent SQL injection vulnerabilities
- Wiring SQLite persistence directly into our FastAPI service layer
- Writing automated test suites with **`pytest`**
- Guidance on building your final portfolio capstone project!
