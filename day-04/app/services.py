"""Task Manager Service Layer handling domain logic and in-memory/JSON persistence."""

import json
from pathlib import Path
from datetime import datetime, timezone
from app.models import TaskCreate, TaskUpdate, TaskResponse, TaskNotFoundError


class TaskManagerService:
    """Service layer managing task entities."""
    
    def __init__(self, storage_file: Path | None = None):
        self.storage_file = storage_file
        self.tasks: list[dict] = []
        self._next_id: int = 1
        self._seed_sample_data()

    def _seed_sample_data(self) -> None:
        """Seed initial dataset for immediate testing."""
        initial = [
            {
                "id": 1,
                "title": "Configure project with uv",
                "description": "Initialize pyproject.toml and virtual environment",
                "priority": "High",
                "completed": True,
                "tags": ["devops", "tooling"],
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": 2,
                "title": "Build Pydantic request models",
                "description": "Create TaskCreate and TaskResponse schemas",
                "priority": "High",
                "completed": False,
                "tags": ["backend", "validation"],
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": 3,
                "title": "Design frontend task board",
                "description": "React / Next.js dark mode UI consuming FastAPI",
                "priority": "Normal",
                "completed": False,
                "tags": ["frontend", "ui"],
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
        self.tasks = initial
        self._next_id = 4

    def list_tasks(
        self,
        priority: str | None = None,
        completed: bool | None = None,
        tag: str | None = None,
        limit: int = 50
    ) -> list[dict]:
        """List tasks with optional filtering."""
        results = self.tasks
        if priority is not None:
            results = [t for t in results if t["priority"].lower() == priority.lower()]
        if completed is not None:
            results = [t for t in results if t["completed"] == completed]
        if tag is not None:
            results = [t for t in results if tag.lower() in [tg.lower() for tg in t.get("tags", [])]]
        return results[:limit]

    def get_task(self, task_id: int) -> dict:
        """Retrieve a single task by ID or raise TaskNotFoundError."""
        for t in self.tasks:
            if t["id"] == task_id:
                return t
        raise TaskNotFoundError(task_id)

    def create_task(self, task_in: TaskCreate) -> dict:
        """Create a new task and append to store."""
        new_task = {
            "id": self._next_id,
            "title": task_in.title,
            "description": task_in.description,
            "priority": task_in.priority,
            "completed": task_in.completed,
            "tags": task_in.tags,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.tasks.append(new_task)
        self._next_id += 1
        return new_task

    def update_task(self, task_id: int, update_data: TaskUpdate) -> dict:
        """Update fields on an existing task."""
        task = self.get_task(task_id)
        dump = update_data.model_dump(exclude_unset=True)
        for key, value in dump.items():
            task[key] = value
        return task

    def delete_task(self, task_id: int) -> None:
        """Remove a task from the store or raise TaskNotFoundError."""
        task = self.get_task(task_id)
        self.tasks.remove(task)


# Global singleton instance for the FastAPI application
task_service = TaskManagerService()
