"""FastAPI Application with SQLite Database Persistence."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.models import TaskCreate, TaskUpdate, TaskResponse, TaskNotFoundError
from app.services import task_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan Context Manager initializing the SQLite database on startup."""
    init_db()
    yield


app = FastAPI(
    title="Full-Stack Task API with SQLite",
    description="Production-ready REST API backed by SQLite persistence and Pydantic validation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for all frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["System"])
def root():
    return {
        "service": "Task Management API (SQLite)",
        "status": "online",
        "docs_url": "/docs",
        "version": "1.0.0"
    }


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    tags=["Tasks"],
    summary="List tasks from SQLite"
)
def list_tasks(
    priority: str | None = Query(default=None, description="Filter by priority (Low, Normal, High, Urgent)"),
    completed: bool | None = Query(default=None, description="Filter by completion status"),
    tag: str | None = Query(default=None, description="Filter by tag"),
    limit: int = Query(default=50, ge=1, le=100, description="Max records to return")
):
    return task_service.list_tasks(priority=priority, completed=completed, tag=tag, limit=limit)


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Get single task by ID"
)
def get_task(
    task_id: int = Path(..., ge=1, description="Unique integer ID of the task")
):
    try:
        return task_service.get_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task in SQLite"
)
def create_task(payload: TaskCreate):
    return task_service.create_task(payload)


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Update task in SQLite"
)
def update_task(
    task_id: int = Path(..., ge=1, description="ID of task to update"),
    payload: TaskUpdate = ...
):
    try:
        return task_service.update_task(task_id, payload)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete task from SQLite"
)
def delete_task(
    task_id: int = Path(..., ge=1, description="ID of task to delete")
):
    try:
        task_service.delete_task(task_id)
        return None
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
