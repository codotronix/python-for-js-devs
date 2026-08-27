# Chapter 3: Python for Web & Async I/O

> *"Python truly shines when it starts communicating with the outside world. In this chapter, we bridge JavaScript's asynchronous patterns to Python coroutines, consume REST APIs with HTTPX, stream data efficiently with generators, and parse web documents using BeautifulSoup."*

---

## 1. The Web Toolchain & Modern Dependency Workflow

In traditional Python setups, engineers often relied on `requests` for synchronous HTTP and `urllib` for basic requests. In modern Python, the ecosystem has converged on **`HTTPX`**—a next-generation HTTP client designed for both synchronous and asynchronous workflows.

### Adding Web Dependencies with `uv`

Using our modern `uv` workflow:

```bash
# Add HTTPX and BeautifulSoup4 to your project
uv add httpx beautifulsoup4

# Run your script within the managed virtual environment
uv run python fetch_data.py
```

`uv` records these dependencies in `pyproject.toml` and locks deterministic binary versions in `uv.lock`.

---

## 2. Consuming REST APIs with Synchronous HTTPX

HTTPX provides an intuitive, high-level API that handles JSON serialization, headers, query parameters, and connection pooling automatically.

```python
import httpx

# 1. Simple GET Request with Query Parameters
response = httpx.get(
    "https://api.github.com/users/sumanbarick",
    params={"tab": "repositories"},
    headers={"Accept": "application/vnd.github.v3+json"},
    timeout=10.0
)

# 2. Inspecting the Response
print("HTTP Status:", response.status_code)  # 200
print("Encoding:", response.encoding)        # utf-8

# 3. Direct JSON Parsing (replaces response.json() Promise in JS)
user_data = response.json()  # Returns a Python dictionary directly!
print(f"User: {user_data.get('name')} | Public Repos: {user_data.get('public_repos')}")

# 4. POST Requests with JSON Payloads (use `json=` keyword)
payload = {"title": "Refactor auth middleware", "priority": "High"}
post_response = httpx.post("https://httpbin.org/post", json=payload)
print("Server echoed payload:", post_response.json().get("json"))
```

### Connection Reuse with `httpx.Client()`

If your application makes multiple requests to the same host, use `httpx.Client()` inside a `with` block to reuse underlying TCP connections:

```python
with httpx.Client(base_url="https://api.github.com", timeout=5.0) as client:
    user_info = client.get("/users/sumanbarick").json()
    repo_list = client.get("/users/sumanbarick/repos").json()
    print(f"Fetched profile and {len(repo_list)} repositories.")
```

---

## 3. HTTP Resilience: Error Handling and Status Verification

In JavaScript `fetch()`, an HTTP 404 or 500 error does not reject the Promise—you must check `res.ok`.

In Python HTTPX, you call **`response.raise_for_status()`** to convert any 4xx (client error) or 5xx (server error) into a catchable `httpx.HTTPStatusError` exception:

```python
import httpx

def fetch_user_avatar(username: str) -> str | None:
    url = f"https://api.github.com/users/{username}"
    try:
        res = httpx.get(url, timeout=5.0)
        res.raise_for_status()  # Throws HTTPStatusError if status != 200..299
        return res.json().get("avatar_url")
    except httpx.HTTPStatusError as err:
        print(f"[HTTP {err.response.status_code}] Failed to fetch user '{username}'")
        return None
    except httpx.TimeoutException:
        print(f"[TIMEOUT] Request to {url} exceeded timeout threshold")
        return None
    except httpx.RequestError as err:
        print(f"[NETWORK ERROR] Failed to connect: {err}")
        return None
```

---

## 4. The Asynchronous Mental Model: Coroutines vs. Promises

If you come from JavaScript/TypeScript, you already understand event loops and non-blocking I/O. However, Python's execution model has one critical distinction.

### JavaScript Promises (Hot / Eager)

In JavaScript, calling an `async` function **immediately starts execution** in the background:

```javascript
// JavaScript: Executes immediately upon invocation!
const taskPromise = fetchUser(101);
// ...do other work...
const user = await taskPromise;
```

### Python Coroutines (Cold / Lazy)

In Python, calling an `async def` function creates a **coroutine object** that does **nothing** until it is explicitly awaited or scheduled on an active event loop:

```python
# Python: Creates a paused coroutine object (does NOT start network call yet!)
coro = fetch_user(101)

# Execution only begins when awaited
user = await coro
```

> [!WARNING]
> **Forgetting `await` in Python:**  
> If you call an async function without `await` (e.g. `data = fetch_user(101)`), Python will NOT throw a compile error. Instead, `data` will hold a `<coroutine object>` and Python will print a runtime warning: `RuntimeWarning: coroutine 'fetch_user' was never awaited`.

---

## 5. Non-Blocking Async HTTP with `httpx.AsyncClient`

When building scalable APIs or querying multiple services, use **`httpx.AsyncClient`** with `async with` and `await`:

```python
import httpx
import asyncio

async def get_github_stats(username: str) -> dict:
    url = f"https://api.github.com/users/{username}"
    # async with guarantees the underlying HTTP/2 socket pool is closed asynchronously
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(url)
        res.raise_for_status()
        return res.json()

# In standalone scripts, bootstrap the event loop with asyncio.run():
if __name__ == "__main__":
    profile = asyncio.run(get_github_stats("sumanbarick"))
    print("User Bio:", profile.get("bio"))
```

---

## 6. Concurrent Network Requests with `asyncio.gather`

`asyncio.gather(*coros)` is Python's direct equivalent to JavaScript's **`Promise.all()`**. It schedules multiple coroutines concurrently on the event loop:

```python
import asyncio
import httpx
import time

async def fetch_repo_stars(client: httpx.AsyncClient, repo_name: str) -> tuple[str, int]:
    url = f"https://api.github.com/repos/{repo_name}"
    try:
        res = await client.get(url)
        stars = res.json().get("stargazers_count", 0)
        return repo_name, stars
    except httpx.HTTPError:
        return repo_name, 0

async def fetch_all_libraries():
    target_repos = [
        "tiangolo/fastapi",
        "encode/httpx",
        "pydantic/pydantic",
        "astral-sh/uv",
        "pallets/flask"
    ]
    
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Build list of coroutines
        tasks = [fetch_repo_stars(client, repo) for repo in target_repos]
        # Run all 5 requests concurrently on a single thread!
        results = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start
    print(f"Fetched {len(results)} repositories in {elapsed:.2f}s total:")
    for repo, stars in results:
        print(f" - {repo:<25} : {stars:,} stars")

if __name__ == "__main__":
    asyncio.run(fetch_all_libraries())
```

---

## 7. Understanding the Iteration Protocol: Iterables vs. Iterators

Under the hood, Python's `for` loops, list comprehensions, and sequence unpackers rely on the **Iteration Protocol**:

1. **Iterable:** An object that produces an iterator when passed to `iter(obj)`. Examples: `list`, `dict`, `set`, `tuple`, `str`.
2. **Iterator:** A stateful object with a `__next__()` method. Calling `next(it)` advances the stream by one element. When no items remain, it raises `StopIteration`.

```python
colors = ["red", "green", "blue"]  # Iterable

# Manually driving the iterator:
iterator = iter(colors)
print(next(iterator))  # "red"
print(next(iterator))  # "green"
print(next(iterator))  # "blue"

# Next call raises StopIteration:
try:
    next(iterator)
except StopIteration:
    print("Iterator has been completely exhausted.")
```

---

## 8. Memory-Efficient Streaming with Generators (`yield`)

When dealing with large files, database result sets, or paginated API responses, loading millions of records into memory at once can crash your server with an Out-Of-Memory (OOM) error.

A **Generator function** uses the **`yield`** keyword. Instead of returning a full list, it pauses execution and yields values to the caller one by one on demand:

```python
def stream_large_dataset(chunk_size: int = 1000, total_records: int = 10000):
    """Simulates streaming records from a database or remote API."""
    for offset in range(0, total_records, chunk_size):
        # In a real app, this would query DB with LIMIT/OFFSET
        chunk = [f"Record #{i}" for i in range(offset, offset + chunk_size)]
        for record in chunk:
            yield record  # Pauses execution and yields single record to caller

# The caller consumes records one by one without holding 10,000 strings in RAM:
for idx, record in enumerate(stream_large_dataset(chunk_size=100, total_records=500), start=1):
    if idx % 100 == 0:
        print(f"Processed up to: {record}")
```

> [!NOTE]
> **List Comprehension vs. Generator Expression:**  
> - `[x ** 2 for x in range(1_000_000)]` creates a list in RAM immediately (~8 MB).  
> - `(x ** 2 for x in range(1_000_000))` creates a generator expression (~100 bytes of memory!).

---

## 9. Web Scraping & HTML Parsing with BeautifulSoup4

HTML is semi-structured document data. **BeautifulSoup4** parses HTML trees and provides intuitive CSS selector navigation.

```python
from bs4 import BeautifulSoup

html_doc = """
<div id="project-board">
  <div class="card" data-priority="high">
    <h2 class="title">Deploy Gateway API</h2>
    <span class="status">In Progress</span>
    <a href="/tasks/101" class="btn">View</a>
  </div>
  <div class="card" data-priority="low">
    <h2 class="title">Update Documentation</h2>
    <span class="status">Done</span>
    <a href="/tasks/102" class="btn">View</a>
  </div>
</div>
"""

soup = BeautifulSoup(html_doc, "html.parser")

# 1. Querying with CSS Selectors: select() returns a list, select_one() returns first match
cards = soup.select("div.card")

for card in cards:
    priority = card.get("data-priority")
    title = card.select_one("h2.title").get_text(strip=True)
    status = card.select_one("span.status").get_text(strip=True)
    link = card.select_one("a.btn")["href"]
    
    print(f"[{priority.upper()}] {title} ({status}) -> {link}")
```

---

## 10. Critical Gotchas in Async & Web Python

### Gotcha 1: Blocking the Event Loop with Synchronous Calls

Never call `time.sleep()` or synchronous `httpx.get()` inside an `async def` function! It halts the entire event loop, freezing all concurrent requests. Always use `await asyncio.sleep()` and `await async_client.get()`.

### Gotcha 2: Generators are Single-Pass

Once a generator yields all its items, it is **exhausted**. Iterating over it a second time will yield 0 items. If you need to re-use the dataset multiple times, convert it explicitly using `items = list(my_generator)`.

---

## 11. Practice Challenge: Async Service Health Aggregator

### The Goal

Build an asynchronous service health monitor that queries multiple HTTP endpoints concurrently, records latency, and formats the output.

### Challenge Solution

```python
import asyncio
import httpx
import time
from dataclasses import dataclass

@dataclass
class ServiceHealth:
    name: str
    url: str
    status_code: int
    latency_ms: float
    is_up: bool

async def check_endpoint(client: httpx.AsyncClient, name: str, url: str) -> ServiceHealth:
    start = time.perf_counter()
    try:
        res = await client.get(url, timeout=5.0)
        latency = (time.perf_counter() - start) * 1000
        return ServiceHealth(
            name=name,
            url=url,
            status_code=res.status_code,
            latency_ms=latency,
            is_up=res.status_code < 400
        )
    except (httpx.RequestError, httpx.TimeoutException):
        latency = (time.perf_counter() - start) * 1000
        return ServiceHealth(
            name=name,
            url=url,
            status_code=0,
            latency_ms=latency,
            is_up=False
        )

async def monitor_all_services():
    services = [
        ("HTTPBin API", "https://httpbin.org/get"),
        ("GitHub Status", "https://httpbin.org/status/200"),
        ("Degraded Service", "https://httpbin.org/status/503"),
        ("Delayed Service", "https://httpbin.org/delay/1"),
    ]

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [check_endpoint(client, name, url) for name, url in services]
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    report = asyncio.run(monitor_all_services())
    print("\n" + "=" * 70)
    print(f"{'SERVICE NAME':<20} | {'STATUS':<6} | {'LATENCY':<10} | {'HEALTH'}")
    print("=" * 70)
    for s in report:
        tag = "ONLINE" if s.is_up else "OFFLINE/DEGRADED"
        print(f"{s.name:<20} | {s.status_code:<6} | {s.latency_ms:6.1f}ms   | {tag}")
```

---

## 12. Chapter Summary & What's Next

### What We Mastered
- Modern REST API consumption with `httpx.get()`, `httpx.post()`, and session reuse.
- The lazy nature of Python coroutines and parallel execution with `asyncio.gather()`.
- The difference between iterables and single-pass iterators.
- Memory-efficient streaming with generator functions (`yield`).
- Parsing and structuring semi-structured web HTML with `BeautifulSoup4`.

### Looking Ahead to Day 4: FastAPI + Pydantic
Now that we understand asynchronous Python and web communication from the client side, tomorrow we start **building our own modern REST API backend**:
- Creating web applications with **FastAPI**
- Strongly-typed request/response validation with **Pydantic** (`BaseModel`)
- Building asynchronous endpoints that connect to services
- Automatic interactive documentation with Swagger / OpenAPI
