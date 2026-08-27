# Chapter 2: Practical Python & Modular Application Architecture

> *"In the first chapter, we explored Python's core syntax and primitive types. In this chapter, we take the crucial step from writing one-off scripts to architecting clean, maintainable, production-ready Python applications."*

---

## 1. Organizing Code: Modules, Imports & Packages

In Python, every single `.py` file is a **module**. When you group related modules inside a directory, you create a **package**.

### The Import Model: JavaScript vs. Python

In the JavaScript/TypeScript ecosystem (ESM), you explicitly `export` functions or objects before importing them elsewhere:

```typescript
// JavaScript (ESM)
import { Task } from "./models.js";
import * as path from "path";
export const maxRetries = 3;
```

In Python, **every top-level function, class, and variable in a file is automatically exportable**. There is no `export` keyword:

```python
# Python 3.12+
from app.models import Task
from pathlib import Path
MAX_RETRIES = 3  # Automatically accessible when imported
```

### Standard Project Architecture

A clean, standard Python application layout looks like this:

```text
task_app/
├── pyproject.toml         # Dependencies and project metadata (like package.json)
├── uv.lock                # Locked exact dependency tree
└── app/
    ├── __init__.py        # Marks the directory as a Python package
    ├── models.py          # Domain entities & Dataclasses
    ├── services.py        # Business logic & file persistence
    └── main.py            # CLI entrypoint or driver script
```

### The `if __name__ == "__main__":` Entrypoint Safeguard

When you run `python app/main.py`, Python sets the special built-in variable `__name__` to `"__main__"`. If that file is imported by another module (e.g. `import app.main`), `__name__` is set to `"app.main"`.

We use this pattern so a file can act as both an importable library and a runnable script:

```python
# app/main.py

def run_cli():
    print("Launching Task Manager CLI...")

if __name__ == "__main__":
    # This block ONLY executes when running `python app/main.py` directly.
    # It will NOT run if another file imports app.main!
    run_cli()
```

---

## 2. Object-Oriented Basics: Classes, `__init__`, and `self`

Python supports full object-oriented programming. If you are familiar with TypeScript or ES6 classes, Python classes will feel intuitive—with one major difference: **explicit `self`**.

```python
class TaskManager:
    # Constructor method in Python is named __init__
    def __init__(self, project_name: str):
        # Instance attributes are attached directly to self
        self.project_name = project_name
        self.tasks: list[str] = []

    # All instance methods must accept `self` as their first parameter
    def add_task(self, title: str) -> None:
        self.tasks.append(title)

    def total_count(self) -> int:
        return len(self.tasks)

# Instantiation (Note: Python does NOT use the `new` keyword!)
manager = TaskManager("Platform Modernization")
manager.add_task("Migrate to uv")
print(f"Total tasks: {manager.total_count()}")
```

### The `self` vs `this` Mental Model

In JavaScript, `this` is dynamically bound at runtime depending on *how* a function is called, leading to well-known callback binding issues (`this.handleClick.bind(this)` or arrow functions).

In Python:
1. `self` is explicitly declared as the first argument in method definitions: `def method(self, arg):`.
2. Python automatically passes the instance when you call `manager.add_task("...")`.
3. Method references retain their bound instance permanently when passed around as callbacks.

---

## 3. Dataclasses: The Modern Way to Model Data

Writing traditional classes for pure data containers involves tedious boilerplate: writing `__init__`, assigning every parameter, writing `__repr__` for debugging, and implementing `__eq__` for equality checks.

Python 3.7 introduced **`@dataclass`** (in the standard library module `dataclasses`), which generates all of this boilerplate automatically from type hints!

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    priority: str = "Normal"
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# 1. Clean Instantiation with positional or keyword arguments
task_1 = Task(id=1, title="Configure CI/CD", priority="High", tags=["devops"])
task_2 = Task(id=1, title="Configure CI/CD", priority="High", tags=["devops"])

# 2. Readable string representation out of the box:
print(task_1)
# Output: Task(id=1, title='Configure CI/CD', completed=False, priority='High', tags=['devops'], ...)

# 3. Automatic Value Equality (__eq__):
print(task_1 == task_2)  # True! (Compares field values, not memory addresses)
```

> [!TIP]
> **Why `field(default_factory=list)`?**  
> Just like default arguments in functions, mutable defaults in dataclasses must not be instantiated once. Using `default_factory=list` guarantees that every new `Task` instance gets its own fresh list.

---

## 4. Modern Filesystem Operations with `pathlib`

Legacy Python code often used `os.path.join` and raw strings for file paths. Modern Python uses the object-oriented **`pathlib.Path`** standard library.

### The Slash `/` Operator

`pathlib` overloads the division operator `/` to join path components cleanly across Windows, macOS, and Linux:

```python
from pathlib import Path

# Always anchor paths relative to the current file (__file__)
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TASKS_FILE = DATA_DIR / "tasks.json"

# Create directory hierarchy safely (like `mkdir -p`)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Inspect path properties
print("Filename:", TASKS_FILE.name)        # "tasks.json"
print("Stem (no ext):", TASKS_FILE.stem)   # "tasks"
print("Extension:", TASKS_FILE.suffix)     # ".json"
print("Exists?", TASKS_FILE.exists())      # True or False
```

### Quick Reads & Writes for Small Files

For simple text files, `Path` provides convenient one-line helpers:

```python
notes_file = DATA_DIR / "release_notes.txt"

# Write directly with encoding
notes_file.write_text("Release v1.0.0 ready for staging.", encoding="utf-8")

# Read entire content
content = notes_file.read_text(encoding="utf-8")
print(content)
```

---

## 5. Context Managers & The `with` Statement

When working with files, network sockets, or database transactions, resource leaks occur if you forget to close handles.

The **`with`** statement creates a **Context Manager** that guarantees resources are closed deterministically when the code block exits—even if an unhandled exception is raised:

```python
from pathlib import Path

log_path = Path(__file__).parent / "application.log"

# Writing lines safely
with open(log_path, mode="a", encoding="utf-8") as file:
    file.write("2026-08-27 12:00:00 [INFO] System health check passed\n")
# The file handle is 100% closed immediately at this line!

# Reading line-by-line efficiently without loading entire file into RAM
with open(log_path, mode="r", encoding="utf-8") as file:
    for line in file:
        print("LOG:", line.strip())
```

> [!IMPORTANT]
> **Never use manual `file.close()` in production Python.** Always wrap file operations in a `with open(...)` context manager.

---

## 6. JSON Serialization & Persistence

Python includes the built-in `json` module. Knowing the difference between the 4 core functions is essential:

| Function | Input / Target | Equivalent in JS | Use Case |
| :--- | :--- | :--- | :--- |
| `json.dump(obj, file)` | Directly writes to a **file object** | — | Saving data directly to disk |
| `json.load(file)` | Directly reads from a **file object** | — | Loading data directly from disk |
| `json.dumps(obj)` | Converts object to **JSON string** | `JSON.stringify(obj)` | Formatting API payloads or logging |
| `json.loads(str)` | Parses **JSON string** into dict/list | `JSON.parse(str)` | Parsing in-memory JSON text |

### Combining Dataclasses and JSON

```python
import json
from dataclasses import asdict
from pathlib import Path

# Converting dataclasses to dictionary list
task_records = [
    asdict(Task(id=1, title="Refactor Auth", completed=True)),
    asdict(Task(id=2, title="Implement Rate Limiting", completed=False))
]

file_target = Path(__file__).parent / "data" / "tasks.json"

# 1. Persisting to disk
with open(file_target, mode="w", encoding="utf-8") as f:
    json.dump(task_records, f, indent=2)

# 2. Loading back from disk
with open(file_target, mode="r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Reconstitute into typed dataclass objects using dictionary unpacking (**item)
restored_tasks = [Task(**item) for item in raw_data]
print(f"Restored {len(restored_tasks)} typed tasks from disk.")
```

---

## 7. Robust Exception Architecture

Error handling in Python uses `try`, `except`, `else`, and `finally` blocks.

```python
def load_application_settings(config_path: Path) -> dict:
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {config_path} not found. Loading fallback settings.")
        return {"environment": "development", "debug": True}
    except json.JSONDecodeError as err:
        print(f"Error: Malformed JSON syntax on line {err.lineno}: {err.msg}")
        raise ValueError("Invalid configuration file") from err
    finally:
        print("Configuration load sequence completed.")
```

### Designing Custom Domain Exceptions

In large applications, create domain-specific exceptions by subclassing `Exception`. This creates clear error boundaries:

```python
class TaskAppError(Exception):
    """Base exception for all domain errors in the Task application."""
    pass

class TaskNotFoundError(TaskAppError):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task #{task_id} does not exist.")

class DuplicateTaskTitleError(TaskAppError):
    pass
```

---

## 8. Function Features: `*args`, `**kwargs`, and Decorators

### Variadic Positional and Keyword Arguments

- `*args` captures any number of additional positional arguments as a `tuple` (equivalent to JS `...args`).
- `**kwargs` captures any number of additional keyword arguments as a `dict`.

```python
def emit_telemetry(event: str, *args, **kwargs):
    print(f"Event Name: {event}")
    print(f"Positional details: {args}")
    print(f"Keyword tags: {kwargs}")

emit_telemetry("USER_LOGIN", "browser_auth", user_id=42, ip="192.168.1.1")
```

### Understanding Decorators

A decorator is simply a function that takes a function, wraps it with additional behavior, and returns the wrapped function.

Writing:
```python
@my_decorator
def calculate():
    pass
```
is identical to:
```python
calculate = my_decorator(calculate)
```

### Writing a Production Timing Decorator

```python
import functools
import time

def log_execution_time(func):
    @functools.wraps(func)  # Keeps original func.__name__ and docstring intact
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration_ms = (time.perf_counter() - start) * 1000
        print(f"[METRIC] '{func.__name__}' executed in {duration_ms:.2f}ms")
        return result
    return wrapper

@log_execution_time
def heavy_data_transformation(records: list[dict]):
    time.sleep(0.05)  # Simulate processing
    return [r for r in records if r.get("active")]
```

---

## 9. Critical Gotchas for Practical Python

### Gotcha 1: The Mutable Class Attribute Trap

```python
# ❌ INCORRECT (Class attribute shared across ALL instances)
class BuggyCart:
    items = []  # Shared across all BuggyCart() objects!

# ✅ CORRECT (Instance attribute isolated per instance)
class SafeCart:
    def __init__(self):
        self.items = []
```

### Gotcha 2: Broad `except Exception:`

Never write a bare `except Exception:` unless you are logging and re-raising. Catching everything indiscriminately will swallow typos (`NameError`), missing imports, and logic bugs, making debugging extremely difficult.

---

## 10. Capstone Practice Challenge: 3-Layer Task Service

### The Challenge

Refactor the Task system into a clean 3-layer architecture:
1. **`models.py`**: Define `Task` (`@dataclass`) and `TaskNotFoundError` (`Exception`).
2. **`services.py`**: Build `TaskManagerService` with `add_task()`, `get_task()`, `mark_completed()`, `list_tasks()`, and JSON file persistence using `pathlib`.
3. **`main.py`**: Driver script verifying the end-to-end functionality.

### Challenge Solution

```python
# ==========================================
# 1. models.py
# ==========================================
from dataclasses import dataclass, field
from datetime import datetime, timezone

class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found.")

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    priority: str = "Normal"
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ==========================================
# 2. services.py
# ==========================================
import json
from pathlib import Path
from dataclasses import asdict

class TaskManagerService:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.tasks: list[Task] = []
        self._next_id = 1
        self._load()

    def add_task(self, title: str, priority: str = "Normal", tags: list[str] | None = None) -> Task:
        task = Task(
            id=self._next_id,
            title=title,
            priority=priority,
            tags=tags if tags is not None else []
        )
        self.tasks.append(task)
        self._next_id += 1
        self._save()
        return task

    def get_task(self, task_id: int) -> Task:
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise TaskNotFoundError(task_id)

    def mark_completed(self, task_id: int) -> Task:
        task = self.get_task(task_id)
        task.completed = True
        self._save()
        return task

    def _save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            raw_list = [asdict(t) for t in self.tasks]
            json.dump(raw_list, f, indent=2)

    def _load(self) -> None:
        if not self.storage_path.exists():
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                self.tasks = [Task(**item) for item in raw_list]
                if self.tasks:
                    self._next_id = max(t.id for t in self.tasks) + 1
        except (json.JSONDecodeError, KeyError):
            self.tasks = []


# ==========================================
# 3. main.py (Verification)
# ==========================================
if __name__ == "__main__":
    db_file = Path(__file__).resolve().parent / "data" / "tasks.json"
    service = TaskManagerService(db_file)

    # Add tasks
    t1 = service.add_task("Implement FastAPI endpoints", priority="High", tags=["backend"])
    t2 = service.add_task("Write unit tests with pytest", priority="Medium", tags=["testing"])
    print(f"Created tasks #{t1.id} and #{t2.id}")

    # Complete task
    service.mark_completed(t1.id)
    print(f"Task #{t1.id} status: completed={service.get_task(t1.id).completed}")

    # Query urgent
    urgent = [t for t in service.tasks if t.priority == "High"]
    print(f"Urgent tasks count: {len(urgent)}")
```

---

## 11. Chapter Summary & Bridge to Day 3

### What We Learned
- Python modules and packages organize code without explicit `export` keywords.
- Dataclasses (`@dataclass`) provide clean, type-hinted domain models with automatic constructors and equality checks.
- `pathlib.Path` and `with open(...)` provide safe, cross-platform, deterministic file persistence.
- Custom exceptions establish clear domain failure boundaries.
- Decorators wrap and augment functions with reusable behavior.

### Preview of Day 3: Python for Web & Async
In the next chapter, we connect Python to the outside world:
- Making asynchronous HTTP requests using **`HTTPX`**
- The mechanics of Python coroutines (`async def` and `await`)
- Efficient concurrency with `asyncio.gather`
- Data streaming with **Generators (`yield`)**
- Parsing and scraping web data with **BeautifulSoup4**
