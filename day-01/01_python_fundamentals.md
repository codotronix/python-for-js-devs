# Chapter 1: Python Foundations for JavaScript & TypeScript Developers

> *"The fastest way to learn Python as an experienced developer is not to start from scratch, but to map the intuitions and patterns you already use daily in JavaScript/TypeScript directly into Pythonic equivalents."*

---

## 1. Introduction: The Python Mental Model

If you have spent years building frontend applications, React components, Node.js microservices, or TypeScript libraries, you already understand 90% of software engineering fundamentals: variables, control flow, functions, scope, asynchronous I/O, and data structures.

Python will feel remarkably familiar—yet deliberately disciplined. Python's design philosophy is famously summarized by *The Zen of Python* (which you can inspect anytime by typing `import this` in a Python REPL). The core tenets most relevant to JavaScript developers are:

1. **Readability counts:** Indentation is grammar, not optional formatting.
2. **Explicit is better than implicit:** Python avoids silent type coercions.
3. **There should be one—and preferably only one—obvious way to do it:** Python favors clear, standardized idioms over multiple competing syntaxes.

### Python vs. JavaScript: A Quick Architectural Comparison

| Dimension | JavaScript / TypeScript | Python 3.12+ |
| :--- | :--- | :--- |
| **Typing Discipline** | Dynamic, Weak (coercive in JS); Static via TypeScript | Dynamic, Strong (no implicit coercion); Optional Type Hints via PEP 484 |
| **Block Syntax** | Curly braces `{ ... }` | Significant Whitespace (4 spaces indentation) |
| **Null/Absence** | `null` and `undefined` | `None` (singleton object) |
| **Variable Declaration** | `let`, `const`, `var` | Direct assignment (`x = 10`) |
| **Modern Tooling** | `pnpm` / `bun` / `npm` | `uv` / `pyproject.toml` |
| **Collections** | `Array`, `Object`, `Map`, `Set` | `list`, `dict`, `tuple`, `set` |
| **Asynchronous Model** | Event Loop with Promises | Event Loop with Coroutines (`asyncio`) |

---

## 2. Modern Python Environment: The `uv` Workflow

Forget the legacy confusion of multiple global `pip` versions, conflicting virtual environments, and slow installs. Modern Python development revolves around **`uv`**—a blistering-fast package and environment manager written in Rust (developed by Astral).

Think of `uv` as the Python world's combination of `pnpm`, `nvm`, and `npm`.

### Core Workflow Commands

```bash
# 1. Initialize a new project with a standard pyproject.toml
uv init python-learning-lab
cd python-learning-lab

# 2. Add dependencies (automatically creates .venv and updates uv.lock)
uv add httpx fastapi pydantic

# 3. Run any command or script inside the isolated project environment
uv run python main.py

# 4. Launch Jupyter Notebook within the virtual environment
uv run jupyter notebook
```

Your project dependencies and environment metadata live in `pyproject.toml` (comparable to `package.json`), with locked exact versions recorded in `uv.lock`.

---

## 3. Variables, Primitive Types & Type Hints

In Python, variables are not "storage containers with fixed types"; they are **names bound to objects**.

### Primitives & Variable Binding

```python
# Direct variable assignment (no let / const keywords)
user_name: str = "Alex Rivera"     # String (str)
login_attempts: int = 3            # Integer (arbitrary precision)
hourly_rate: float = 85.50         # Floating-point number
is_active: bool = True             # Boolean (Capitalized True/False)
session_token: str | None = None   # NoneType (representing absence of a value)
```

> [!NOTE]
> **No `const` Keyword in Python:**
> Python does not provide runtime-enforced constants. By PEP 8 convention, constants are written in `ALL_CAPS` (e.g., `MAX_RETRY_LIMIT = 5`) to signal to other developers that the value must not be mutated.

### Strong Typing vs JavaScript Coercion

In JavaScript, expressions like `"4" + 2` produce `"42"` while `"4" - 2` produces `2`. 

Python is strictly **strongly typed**:

```python
# JavaScript: "Invoice #" + 1042 -> "Invoice #1042"
# Python:
try:
    message = "Invoice #" + 1042
except TypeError as err:
    print(f"Python rejected coercion: {err}")

# Pythonic way: f-strings
message = f"Invoice #{1042}"
print(message)  # "Invoice #1042"
```

---

## 4. Strings & Text Manipulation

Python strings are **immutable** ordered sequences of Unicode characters. Any method called on a string returns a new string.

### String Methods Cheatsheet

```python
raw_query = "   SELECT * FROM users WHERE active = 1;   "

# 1. Trimming & Case Conversion
clean_query = raw_query.strip()             # Removes leading/trailing whitespace (JS: .trim())
lower_query = clean_query.lower()           # Lowercase
title_text = "python fundamentals".title()  # "Python Fundamentals"

# 2. Splitting and Joining
tags_str = "backend, api, authentication, security"
tags_list = [t.strip() for t in tags_str.split(",")]  # ['backend', 'api', 'authentication', 'security']

# Notice: In Python, join is called ON the delimiter string!
formatted_tags = " | ".join(tags_list)                 # "backend | api | authentication | security"

# 3. Substring Verification (replaces .includes())
has_select = "SELECT" in clean_query                   # True
starts_with_sel = clean_query.startswith("SELECT")     # True
```

### f-Strings: Modern String Interpolation

Introduced in Python 3.6 and refined in recent releases, **f-strings** (`f"..."`) offer clean expression interpolation and rich formatting options:

```python
service = "FastAPI Gateway"
latency_ms = 14.8291
status_code = 200

# Formatting floats, currency, and padding
log_entry = (
    f"[{service}] Status: {status_code} | "
    f"Latency: {latency_ms:.2f}ms | "
    f"Pass: {status_code == 200}"
)
print(log_entry)
# Output: [FastAPI Gateway] Status: 200 | Latency: 14.83ms | Pass: True
```

---

## 5. Core Collections: The Four Pillars

Python provides four essential built-in collections. Knowing when to use each is the hallmark of an effective Python engineer.

### 1. Lists (`list`) — Dynamic Arrays

Lists are mutable, ordered sequences. They are the exact equivalent of JavaScript arrays.

```python
tasks = ["Setup DB", "Write tests"]

# Adding elements
tasks.append("Deploy API")       # JS: tasks.push("Deploy API")
tasks.insert(0, "Code review")   # JS: tasks.unshift("Code review")

# Removing elements
last = tasks.pop()               # Removes and returns last element
tasks.remove("Write tests")      # Removes first occurrence by value

# Checking length & membership
count = len(tasks)               # JS: tasks.length
is_pending = "Setup DB" in tasks # JS: tasks.includes("Setup DB")
```

### 2. Tuples (`tuple`) — Immutable Records

Tuples are fixed-length, immutable sequences defined using parentheses `(...)`.

Use tuples when a collection represents a fixed schema or record (e.g., coordinates, HTTP status tuples, or returning multiple values from a function).

```python
# Defining a tuple
http_status = (404, "Not Found")

# Destructuring / Unpacking (identical to JS destructuring)
code, reason = http_status
print(f"Error {code}: {reason}")

# Multi-value function returns
def get_user_coordinates(user_id: int) -> tuple[float, float]:
    # Returns latitude, longitude
    return 37.7749, -122.4194

lat, lng = get_user_coordinates(101)
```

> [!TIP]
> **Why Tuples Matter:** Because tuples are immutable, Python can hash them. This means a tuple can be used as a key in a Dictionary or an element in a Set—Lists cannot!

### 3. Sets (`set`) — Fast Uniqueness & Math Operations

A `set` is an unordered collection of unique, hashable items. Checking if an element exists in a set is an **$O(1)$ average-time operation**.

```python
admin_roles = {"admin", "superadmin", "billing"}
user_roles = {"developer", "billing"}

# Fast Set Algebra
common_roles = admin_roles & user_roles    # Intersection -> {"billing"}
all_roles = admin_roles | user_roles       # Union -> {"admin", "superadmin", "billing", "developer"}
missing_roles = admin_roles - user_roles   # Difference -> {"admin", "superadmin"}

# Deduplicating a list
raw_tags = ["ui", "backend", "ui", "docker", "docker"]
unique_tags = list(set(raw_tags))          # ['ui', 'backend', 'docker']
```

> [!WARNING]
> **Empty Set Gotcha:** Writing `empty_dict = {}` creates an empty **dictionary**. To create an empty set, you must call `empty_set = set()`.

### 4. Dictionaries (`dict`) — Key-Value Hash Maps

Dictionaries represent key-value mappings (counterparts to JavaScript objects / Maps). Keys must be immutable (strings, numbers, tuples).

```python
user_profile = {
    "id": 101,
    "username": "alex",
    "email": "alex@company.io",
    "role": "Engineer"
}

# 1. Safe Access with .get()
# CRITICAL: user_profile["department"] raises KeyError if missing!
department = user_profile.get("department", "Engineering")

# 2. Updating and Merging
user_profile["last_login"] = "2026-08-27"
user_profile.update({"country": "US", "tier": "Gold"})

# Python 3.9+ dictionary union operator (|)
updated_profile = user_profile | {"theme": "dark"}

# 3. Iterating over keys and values
for key, value in updated_profile.items():
    print(f"{key:>12} : {value}")
```

---

## 6. Indexing & Slicing: `[start:stop:step]`

Python provides universal slicing mechanics that work identically across strings, lists, and tuples:

$$\text{sequence}[\text{start} : \text{stop} : \text{step}]$$

- `start`: The starting index (inclusive, defaults to 0).
- `stop`: The end index (**exclusive**, defaults to length).
- `step`: The stride/stride interval (can be negative).

```python
items = ["A", "B", "C", "D", "E", "F"]

print(items[0])       # "A" (First element)
print(items[-1])      # "F" (Last element — no arr.length - 1 needed!)
print(items[1:4])     # ['B', 'C', 'D'] (Items from index 1 up to 4)
print(items[:3])      # ['A', 'B', 'C'] (First 3 elements)
print(items[-2:])     # ['E', 'F'] (Last 2 elements)
print(items[::2])     # ['A', 'C', 'E'] (Every 2nd item)
print(items[::-1])    # ['F', 'E', 'D', 'C', 'B', 'A'] (Reversed shallow copy)
```

---

## 7. Control Flow, Truthiness & Conditionals

Python conditions eliminate parentheses around tests and use `:` with 4-space indentation.

```python
score = 88

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# Python Ternary Conditional Expression
# (JavaScript: const status = score >= 50 ? "Pass" : "Fail";)
status_label = "Pass" if score >= 50 else "Fail"
```

### Truthiness Table

In JavaScript, `[]` and `{}` are truthy. In Python, **all empty containers are falsy**.

| Falsy in Python | Truthy in Python |
| :--- | :--- |
| `False`, `None` | `True` |
| `0`, `0.0` | Any non-zero number (`1`, `-5`, `0.1`) |
| `""` (empty string) | Any non-empty string (`"hello"`, `" "`) |
| `[]`, `{}`, `set()`, `()` | Any non-empty container (`[1]`, `{"a": 1}`) |

```python
# The Pythonic way to test if a collection has items:
active_connections = ["ws://1", "ws://2"]

# DO NOT write: if len(active_connections) > 0:
if active_connections:
    print(f"Broadcasting to {len(active_connections)} sockets")
```

---

## 8. Functions, Arguments & The Mutable Default Trap

Functions are declared with `def`. They support positional arguments, keyword arguments, and default parameter values.

```python
def create_endpoint(
    path: str,
    method: str = "GET",
    authenticated: bool = True
) -> dict:
    """Constructs endpoint route configuration metadata."""
    return {
        "path": path,
        "method": method.upper(),
        "auth_required": authenticated
    }

# Positional call
ep1 = create_endpoint("/users", "GET")

# Keyword call (self-documenting at call sites)
ep2 = create_endpoint(path="/auth/login", method="POST", authenticated=False)
```

### The #1 Python Trap: Mutable Default Arguments

> [!CAUTION]
> **Never use a mutable object (`[]` or `{}`) as a default argument in Python.**
> In Python, default parameter expressions are evaluated **once when the function is defined**, not on each invocation. Every subsequent call will mutate the exact same shared object in memory!

```python
# ❌ THE DANGEROUS BUG:
def add_to_queue(item: str, queue: list = []):
    queue.append(item)
    return queue

print(add_to_queue("Email 1"))  # ['Email 1']
print(add_to_queue("Email 2"))  # ['Email 1', 'Email 2'] (BUG! Shared state!)

# ✅ THE PYTHONIC SOLUTION: Default to None
def add_to_queue_safe(item: str, queue: list[str] | None = None) -> list[str]:
    if queue is None:
        queue = []
    queue.append(item)
    return queue

print(add_to_queue_safe("Email 1"))  # ['Email 1']
print(add_to_queue_safe("Email 2"))  # ['Email 2'] (Isolated & clean)
```

---

## 9. Pythonic Idioms: Comprehensions, Enumerate & Zip

### List & Dictionary Comprehensions

Comprehensions replace imperative `for` loops and `.map()` / `.filter()` chains:

```python
raw_scores = [45, 88, 92, 53, 76, 95]

# List comprehension: [expression for item in iterable if condition]
# (JS: raw_scores.filter(s => s >= 75).map(s => s + 5))
adjusted_passing_scores = [s + 5 for s in raw_scores if s >= 75]
print("Adjusted scores:", adjusted_passing_scores)  # [93, 97, 81, 100]

# Dictionary comprehension
users = ["alex", "beth", "carlos"]
user_id_lookup = {user: 1000 + idx for idx, user in enumerate(users, 1)}
print(user_id_lookup)  # {'alex': 1001, 'beth': 1002, 'carlos': 1003}
```

### `enumerate()`: Index and Element in Harmony

```python
frameworks = ["FastAPI", "React", "TailwindCSS"]

# enumerate gives (index, item) cleanly
for rank, name in enumerate(frameworks, start=1):
    print(f"Rank #{rank}: {name}")
```

### `zip()`: Parallel Sequence Iteration

```python
service_names = ["auth-service", "order-service", "payment-service"]
ports = [8001, 8002, 8003]

# Pair up corresponding elements across lists
for name, port in zip(service_names, ports):
    print(f"Service '{name}' running on localhost:{port}")
```

---

## 10. Capstone Domain: Modeling the Task Management System

Throughout this 5-day course, we will build an end-to-end Task Management System, starting today with raw Python data structures and advancing to FastAPI and SQLite by Day 5.

```python
# Task Domain Data Structure (Day 1 representation using lists & dicts)
task_repository = [
    {
        "id": 1,
        "title": "Configure project with uv",
        "completed": True,
        "priority": "High",
        "tags": ["tooling", "devops"]
    },
    {
        "id": 2,
        "title": "Build Pydantic schemas",
        "completed": False,
        "priority": "High",
        "tags": ["backend", "validation"]
    },
    {
        "id": 3,
        "title": "Design dark-mode dashboard UI",
        "completed": False,
        "priority": "Low",
        "tags": ["frontend", "design"]
    }
]

# Querying with list comprehensions:
urgent_pending_tasks = [
    t["title"] for t in task_repository
    if t["priority"] == "High" and not t["completed"]
]

print("Urgent Tasks to Execute:", urgent_pending_tasks)
# Output: ['Build Pydantic schemas']
```

---

## 11. Hands-On Practice Exercises

### Exercise 1: URL Query String Parser
Write a function `parse_query_params(url: str) -> dict[str, str]` that extracts the query parameters from a URL into a Python dictionary.

*Example Input:* `"https://api.internal/v1/tasks?status=active&priority=high&limit=20"`  
*Expected Output:* `{"status": "active", "priority": "high", "limit": "20"}`

### Exercise 2: Deduplicating and Tag Frequency Counter
Given a list of task records, write a Python function to:
1. Extract all unique tags across all tasks using a `set`.
2. Produce a dictionary counting how many tasks use each tag.

---

## 12. Exercise Solutions

```python
# Solution 1: URL Query String Parser
def parse_query_params(url: str) -> dict[str, str]:
    if "?" not in url:
        return {}
    _, query_string = url.split("?", 1)
    param_pairs = query_string.split("&")
    
    params = {}
    for pair in param_pairs:
        if "=" in pair:
            k, v = pair.split("=", 1)
            params[k] = v
    return params

# Verification:
test_url = "https://api.internal/v1/tasks?status=active&priority=high&limit=20"
print(parse_query_params(test_url))


# Solution 2: Tag Extraction & Frequency
tasks_dataset = [
    {"title": "Task A", "tags": ["python", "api"]},
    {"title": "Task B", "tags": ["frontend", "ui"]},
    {"title": "Task C", "tags": ["python", "docker", "api"]}
]

def analyze_tags(tasks: list[dict]) -> tuple[set[str], dict[str, int]]:
    unique_tags = set()
    tag_counts = {}
    
    for t in tasks:
        for tag in t.get("tags", []):
            unique_tags.add(tag)
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
    return unique_tags, tag_counts

unique, counts = analyze_tags(tasks_dataset)
print("Unique Tags:", unique)
print("Tag Frequency:", counts)
```

---

## 13. Summary & What's Next

### Key Takeaways
- Python variables are dynamically typed labels pointing to memory objects without declaration keywords.
- `uv` is the modern, high-speed toolchain for packages, environments, and locks.
- Lists are dynamic arrays; Tuples are immutable records; Sets are fast unique hashes; Dictionaries are key-value mappings with explicit `.get()` safety.
- Comprehensions, `enumerate()`, and `zip()` replace verbose imperative loops with clean declarative expressions.
- Always default optional mutable arguments to `None`.

### Coming Up in Day 2: Practical Python Application Code
In the next session, we transition from individual scripts to modular application architectures:
- Multi-file code organization with **Modules and Packages**
- Clean data modeling with Python classes and **`@dataclass`**
- Safe file I/O and JSON persistence with **`pathlib`** and context managers (`with`)
- Robust application **Exception Handling** hierarchies
- Function flexibility with `*args`, `**kwargs`, and an introduction to **Decorators**
