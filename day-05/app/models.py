"""Pydantic Schemas for Day 5 Task Management REST API."""

from pydantic import BaseModel, Field


class TaskNotFoundError(Exception):
    """Raised when a task ID is not found in the SQLite database."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found.")


class TaskBase(BaseModel):
    """Base Task attributes."""
    title: str = Field(
        min_length=3,
        max_length=100,
        description="The title of the task",
        examples=["Complete Day 5 Capstone"]
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Detailed description"
    )
    priority: str = Field(
        default="Normal",
        pattern="^(Low|Normal|High|Urgent)$",
        description="Priority (Low, Normal, High, Urgent)"
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Associated category tags"
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
