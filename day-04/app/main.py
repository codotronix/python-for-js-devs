"""FastAPI Application Entrypoint for Task Management REST API."""

from fastapi import FastAPI, HTTPException, status, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from app.models import TaskCreate, TaskUpdate, TaskResponse, TaskNotFoundError
from app.services import task_service

app = FastAPI(
    title="Task Management API",
    description="High-performance REST API built with FastAPI & Pydantic for frontend developers.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend clients (React, Vue, Svelte, Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["System"])
def root():
    """Health check and API information root."""
    return {
        "service": "Task Management API",
        "status": "online",
        "docs_url": "/docs",
        "version": "1.0.0"
    }


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    tags=["Tasks"],
    summary="List all tasks with optional filters"
)
def list_tasks(
    priority: str | None = Query(default=None, description="Filter by priority (Low, Normal, High, Urgent)"),
    completed: bool | None = Query(default=None, description="Filter by completion status"),
    tag: str | None = Query(default=None, description="Filter by tag"),
    limit: int = Query(default=50, ge=1, le=100, description="Max number of items to return")
):
    """Retrieve tasks matching the optional filter criteria."""
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
    """Retrieve a single task record by ID. Returns 404 if not found."""
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
    summary="Create a new task"
)
def create_task(payload: TaskCreate):
    """Validate incoming JSON body and create a new task record."""
    return task_service.create_task(payload)


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Update an existing task"
)
def update_task(
    task_id: int = Path(..., ge=1, description="ID of task to update"),
    payload: TaskUpdate = ...
):
    """Update fields of an existing task. Returns 404 if task does not exist."""
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
    summary="Delete a task"
)
def delete_task(
    task_id: int = Path(..., ge=1, description="ID of task to delete")
):
    """Remove a task from the system. Returns 204 No Content upon success."""
    try:
        task_service.delete_task(task_id)
        return None
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
