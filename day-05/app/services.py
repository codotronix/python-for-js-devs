"""SQLite-backed Task Service Layer executing safe parameterized SQL queries."""

import json
import sqlite3
from datetime import datetime, timezone
from app.database import get_db_connection
from app.models import TaskCreate, TaskUpdate, TaskNotFoundError


class SqliteTaskService:
    """Service layer communicating with SQLite database."""

    def _row_to_dict(self, row: sqlite3.Row) -> dict:
        """Helper to convert sqlite3.Row to serializable dictionary."""
        tags_raw = row["tags"]
        try:
            tags_list = json.loads(tags_raw) if tags_raw else []
        except (json.JSONDecodeError, TypeError):
            tags_list = []

        return {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "priority": row["priority"],
            "completed": bool(row["completed"]),
            "tags": tags_list,
            "created_at": row["created_at"]
        }

    def list_tasks(
        self,
        priority: str | None = None,
        completed: bool | None = None,
        tag: str | None = None,
        limit: int = 50
    ) -> list[dict]:
        """Query tasks with dynamic parameterized filters."""
        query = "SELECT * FROM tasks WHERE 1=1"
        params: list[object] = []

        if priority is not None:
            query += " AND LOWER(priority) = LOWER(?)"
            params.append(priority)

        if completed is not None:
            query += " AND completed = ?"
            params.append(1 if completed else 0)

        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            results = [self._row_to_dict(r) for r in rows]

            # In-memory tag filter if requested
            if tag is not None:
                results = [t for t in results if tag.lower() in [tg.lower() for tg in t["tags"]]]

            return results

    def get_task(self, task_id: int) -> dict:
        """Retrieve a single task by ID using parameterized query."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row is None:
                raise TaskNotFoundError(task_id)
            return self._row_to_dict(row)

    def create_task(self, task_in: TaskCreate) -> dict:
        """Insert a new task record into SQLite."""
        created_at = datetime.now(timezone.utc).isoformat()
        tags_json = json.dumps(task_in.tags)

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO tasks (title, description, priority, completed, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (
                task_in.title,
                task_in.description,
                task_in.priority,
                1 if task_in.completed else 0,
                tags_json,
                created_at
            ))
            conn.commit()
            new_id = cursor.lastrowid

        return self.get_task(new_id)

    def update_task(self, task_id: int, update_data: TaskUpdate) -> dict:
        """Update an existing task in SQLite."""
        # Ensure task exists first
        self.get_task(task_id)

        dump = update_data.model_dump(exclude_unset=True)
        if not dump:
            return self.get_task(task_id)

        set_clauses = []
        params = []

        for key, value in dump.items():
            if key == "tags":
                set_clauses.append("tags = ?")
                params.append(json.dumps(value))
            elif key == "completed":
                set_clauses.append("completed = ?")
                params.append(1 if value else 0)
            else:
                set_clauses.append(f"{key} = ?")
                params.append(value)

        params.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = ?"

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            conn.commit()

        return self.get_task(task_id)

    def delete_task(self, task_id: int) -> None:
        """Delete a task record from SQLite."""
        # Ensure exists
        self.get_task(task_id)

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()


# Singleton service instance
task_service = SqliteTaskService()
