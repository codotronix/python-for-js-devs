"""Pydantic Models and Schemas for Task Management API."""

from pydantic import BaseModel, Field
from datetime import datetime, timezone


class TaskNotFoundError(Exception):
    """Raised when a task ID is not found in the repository."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found.")


class TaskBase(BaseModel):
    """Shared attributes for Task schemas."""
    title: str = Field(
        min_length=3,
        max_length=100,
        description="The title of the task",
        examples=["Implement JWT authentication"]
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Optional detailed description"
    )
    priority: str = Field(
        default="Normal",
        pattern="^(Low|Normal|High|Urgent)$",
        description="Priority level (Low, Normal, High, Urgent)"
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Categorization tags"
    )


class TaskCreate(TaskBase):
    """Schema for creating a new Task."""
    completed: bool = False


class TaskUpdate(BaseModel):
    """Schema for updating an existing Task (all fields optional)."""
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    priority: str | None = Field(default=None, pattern="^(Low|Normal|High|Urgent)$")
    completed: bool | None = None
    tags: list[str] | None = None


class TaskResponse(TaskBase):
    """Schema for returning Task data to the client."""
    id: int
    completed: bool
    created_at: str

    class Config:
        from_attributes = True
