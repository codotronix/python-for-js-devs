"""SQLite Database Connection and Schema Initialization Module."""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

DB_DIR = Path(__file__).resolve().parent / "data"
DB_FILE = DB_DIR / "tasks.db"


def get_db_connection() -> sqlite3.Connection:
    """Creates a connection to the SQLite database with dictionary-like row factory."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables column access by name: row["title"]
    return conn


def init_db() -> None:
    """Initializes the database tables and seeds sample data if empty."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Create tasks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Normal',
            completed INTEGER DEFAULT 0,
            tags TEXT DEFAULT '[]',
            created_at TEXT NOT NULL
        );
        """)
        
        # 2. Seed initial data if table is brand new
        cursor.execute("SELECT COUNT(*) FROM tasks;")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_tasks = [
                (
                    "Setup SQLite database schema",
                    "Create tables with parameterized queries and row_factory",
                    "High",
                    1,
                    json.dumps(["database", "sqlite"]),
                    datetime.now(timezone.utc).isoformat()
                ),
                (
                    "Connect FastAPI service to SQLite",
                    "Wire CRUD repository methods into TaskManagerService",
                    "High",
                    0,
                    json.dumps(["api", "backend"]),
                    datetime.now(timezone.utc).isoformat()
                ),
                (
                    "Write pytest test suite",
                    "Test endpoints with TestClient and parameterized inputs",
                    "Normal",
                    0,
                    json.dumps(["testing", "qa"]),
                    datetime.now(timezone.utc).isoformat()
                )
            ]
            
            cursor.executemany("""
            INSERT INTO tasks (title, description, priority, completed, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?);
            """, sample_tasks)
            conn.commit()
