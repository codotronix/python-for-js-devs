# Python Training — Day-wise Production Plan

## 1. Purpose

Master plan for **Learn Python in 5 Days**, a five-day, one-hour-per-day training program for experienced JavaScript/TypeScript web and hybrid-mobile developers.

For each day, this plan will later be used to create:

1. Professional-grade slides, preferably HTML or presentation-ready assets.
2. A Jupyter Notebook (`.ipynb`) with explanations, examples, exercises, and runnable code.
3. Optionally, a standalone Markdown chapter for the book **Learn Python in 5 Days**.

The live training is intentionally lean. The objective is not to cover Python comprehensively, but to give experienced developers practical Python knowledge and a foundation for continuing independently.

---

# 2. Audience

The trainees are experienced frontend/web developers, predominantly JavaScript/TypeScript developers.

Assume they already understand:

- Variables, functions, and control flow
- Objects and arrays
- OOP fundamentals
- HTTP and REST
- JSON
- Async/await and promises
- Frontend/backend interaction
- Git and normal software-development workflows

Use JavaScript/TypeScript comparisons whenever they accelerate understanding.

---

# 3. Overall Course Goal

By the end of the five days, trainees should be able to:

- Read and write basic Python confidently.
- Understand common Python idioms.
- Work with Python collections and functions.
- Structure code into modules and classes.
- Handle files, JSON, and exceptions.
- Use external Python libraries.
- Consume HTTP APIs.
- Understand practical async Python.
- Build a basic FastAPI application.
- Validate API data using Pydantic.
- Persist application data using SQLite.
- Understand the basic shape of a real Python application.
- Continue independently into larger Python, backend, automation, data, or AI projects.

The course should **not** promise advanced Python mastery or AI engineering expertise.

---

# 4. Course Progression

```text
Day 1
Python language fundamentals
        ↓
Day 2
Practical Python application code
        ↓
Day 3
HTTP + async + useful Python libraries
        ↓
Day 4
FastAPI + Pydantic
        ↓
Day 5
SQLite + complete application
```

AI should **not** be a formal Day 5 module. It can be mentioned as an important area where Python is widely used, and may be offered as an optional capstone extension.

---

# 5. Training Format

Each day is exactly **60 minutes**.

Recommended rhythm:

```text
00–05   Context / motivation
05–15   Concept introduction
15–30   Live coding / notebook demonstration
30–40   Additional examples + gotchas
40–53   Guided exercise
53–58   Review / solution
58–60   Recap
```

Do not attempt to cover every planned subtopic if the live session is running behind.

**Depth is more important than checklist completion.**

---

# 6. Day 1 — Python Foundations

## Objective

Give experienced JavaScript/TypeScript developers enough Python language knowledge to start writing small programs comfortably.

## Topics

### Python mental model

- What Python is.
- Where Python is commonly used.
- Python vs JavaScript/TypeScript.
- Running Python.
- Jupyter notebooks.
- Basic `uv` workflow.

### Variables and basic types

- Strings
- Integers
- Floats
- Booleans
- `None`
- Dynamic typing
- Basic type hints

### Core collections

- Lists
- Dictionaries
- Tuples
- Sets
- Indexing and slicing
- Mutation

### Control flow

- `if / elif / else`
- `for`
- `while`
- `break`
- `continue`

### Functions

- Defining functions
- Parameters
- Return values
- Default arguments
- Keyword arguments
- Type hints
- f-strings

### Pythonic basics

- List comprehensions
- Dictionary comprehensions
- Unpacking
- `enumerate`
- `zip`
- `range`

## Key gotchas

Introduce only those naturally associated with the day's topics:

- `==` vs `is`
- `None`
- Truthiness
- Mutable lists vs immutable strings/tuples
- Notebook cells can be executed out of order
- Python uses indentation as syntax

## Notebook

`01_python_fundamentals.ipynb`

Include:

- Short explanations
- Small runnable examples
- JavaScript comparisons
- "Try it" cells
- One or two small exercises
- Solutions after exercises

## Slides

The Day 1 deck is both a presentation and a **post-training learning reference**. It must therefore be substantially richer than a normal executive presentation.

The target is approximately **14–18 content-rich slides**. The live session remains one hour because the instructor will selectively teach from the deck and use the Jupyter notebook for live coding.

### Critical sequencing rule

Do **not** introduce concepts before their scheduled day merely because they make a slide more interesting.

For Day 1:

- Comprehensions are allowed because they are explicitly part of Day 1.
- Strings must be taught explicitly; they are not merely examples used while teaching another topic.
- Functions must include parameters, return values, default arguments, keyword arguments, and type hints.
- Lists, dictionaries, tuples, and sets each deserve explicit practical treatment.
- Control flow must cover `if / elif / else`, `for`, `while`, `break`, and `continue`.
- `enumerate`, `zip`, `range`, and unpacking are Day 1 material.
- Do not introduce classes, dataclasses, modules, exceptions, decorators, HTTPX, async, BeautifulSoup, FastAPI, Pydantic, SQLite, or pytest on Day 1.

### Cheatsheet principle

**Each topic slide should work as a visually impressive Python cheatsheet.**

A learner should be able to return to the slide after training and use it as a quick reference.

Examples:

- A **String** slide should be a String cheatsheet.
- A **List** slide should be a List cheatsheet.
- A **Dictionary** slide should be a Dictionary cheatsheet.
- A **Function** slide should be a Function cheatsheet.
- A **Control Flow** slide should be a Control Flow cheatsheet.

A cheatsheet slide should contain:

- Core syntax.
- Common operations.
- Small examples.
- Output or behavior where useful.
- One or two important gotchas.
- JavaScript/TypeScript comparison where it genuinely helps.

Do not turn slides into dense documentation. Use visual grouping, code cards, callouts, comparison panels, and diagrams to make the density feel intentional.

### Proposed Day 1 deck structure

1. **Opening — Python is familiar, but deliberately different**
2. **Python vs JavaScript — the mental-model bridge**
3. **Variables and types — Python names values without `let`/`const`**
4. **Strings — the Python string cheatsheet**
5. **Numbers, booleans and `None` — the basic value types**
6. **Lists — the everyday ordered collection**
7. **Tuples — grouped, immutable values**
8. **Sets — uniqueness and membership**
9. **Dictionaries — Python's everyday key/value structure**
10. **Indexing and slicing — getting pieces of sequences**
11. **Conditions — `if`, `elif`, `else` and truthiness**
12. **Loops — `for`, `while`, `break` and `continue`**
13. **Functions — definition, parameters and return values**
14. **Function parameters — defaults and keyword arguments**
15. **Type hints and f-strings — making intent clearer**
16. **Pythonic basics — comprehensions, unpacking, `enumerate`, `zip`, `range`**
17. **Python gotchas — the few things JavaScript developers trip over**
18. **Guided challenge + Day 1 recap**

Some slides can be combined during final production if the visual treatment becomes repetitive, but **content should not be removed merely to keep the deck short**. The deck is learning material; the live instructor controls the pace.

### Live-session rule

The instructor should not read every cheatsheet item aloud.

Use the deck as a reference surface:

- Explain the core idea.
- Demonstrate the most important examples in Jupyter.
- Point learners to the remaining cheatsheet material for later reference.
- Use the guided challenge to reinforce the highest-value concepts.

### Content-depth rule

For every Day 1 topic, the final deck should answer:

1. What is it?
2. What does the basic syntax look like?
3. What are the most common operations?
4. What is the Pythonic way to use it?
5. What is the JavaScript/TypeScript equivalent when useful?
6. What is one important gotcha?
7. Can I recognize and write a small example?

## Capstone connection

Start with a simple domain such as **Tasks**:

```text
Task
├── title
├── description
├── completed
└── priority
```

No API or database yet.

---

# 7. Day 2 — Practical Python

## Objective

Move from isolated snippets to code that can form a small maintainable application.

## Topics

### Modules and imports

- Python modules
- Standard-library imports
- Local modules
- Basic package structure

### Classes and objects

- Classes
- `__init__`
- `self`
- Instance attributes
- Methods
- Basic inheritance
- Composition

Do not spend time on advanced OOP.

### Dataclasses

Introduce:

```python
@dataclass
class Task:
    title: str
    completed: bool = False
```

Explain why dataclasses are useful.

### Files and JSON

- `pathlib`
- Reading/writing files
- JSON
- `with`
- Context managers

### Exceptions

- `try`
- `except`
- `finally`
- `raise`
- Common exception types
- Basic custom exceptions
- Why not to catch everything

### Useful function features

- `*args`
- `**kwargs`
- Unpacking

### Introductory decorators

Use one simple example.

Explain what:

```python
@decorator
```

means conceptually.

Do not go into advanced decorator patterns.

## Key gotchas

- Mutable default arguments.
- Mutable class attributes.
- `is` vs `==` where relevant.
- File paths and current working directory.
- Broad `except Exception`.
- Notebook state hiding import/runtime problems.

## Notebook

`02_practical_python.ipynb`

Include:

- Classes
- Dataclasses
- File/JSON example
- Exception example
- Small decorator example
- Refactoring exercise

## Slides

Suggested story:

1. **Python becomes useful when code becomes reusable**
2. Modules turn scripts into applications
3. Classes and dataclasses
4. Files and JSON
5. Exceptions as part of application design
6. A quick look at decorators
7. Python gotchas worth remembering
8. Refactoring challenge
9. Day 2 recap

## Capstone connection

Move the Task application into a basic project structure:

```text
app/
├── models.py
├── services.py
└── main.py
```

Persist/read simple task data from a JSON file initially.

---

# 8. Day 3 — Python for Web & Async

## Objective

Teach the subset of Python that makes it particularly useful for web integration, automation, and I/O-heavy applications.

## Topics

### HTTP APIs

- HTTP basics in Python
- HTTPX
- GET/POST
- Query parameters
- Headers
- JSON responses
- Status codes
- Basic timeouts/error handling

### Async Python

- `async def`
- `await`
- Coroutine concept
- Async I/O
- Basic concurrent requests
- `asyncio.gather`

Use JavaScript promises/async-await as the comparison point.

### Iterables and generators

- Iterable concept
- Iterator concept
- `yield`
- Why generators can be useful

Keep this practical and brief.

### Web scraping introduction

- HTML as input data
- BeautifulSoup
- Extracting simple information
- Converting HTML into structured data

Do not turn the course into a scraping course.

### `uv` workflow

- Adding dependencies
- Running commands
- Project environment
- `pyproject.toml`
- `uv.lock`

Typical examples:

```bash
uv add httpx
uv add beautifulsoup4
uv run python ...
```

## Key gotchas

- Forgetting `await`.
- `async def` does not execute immediately.
- Async does not automatically make CPU-heavy work faster.
- Blocking calls inside async code.
- Missing HTTP timeouts.
- Uncontrolled concurrency.
- Generators can be consumed.
- Notebook async behavior can differ from a normal application.

## Notebook

`03_web_and_async.ipynb`

Include:

- Calling a public HTTP API.
- Inspecting JSON.
- Async request example.
- Concurrent request example.
- Small generator example.
- Simple BeautifulSoup example.

## Slides

Suggested story:

1. **Python becomes powerful when it starts talking to the outside world**
2. Calling APIs with HTTPX
3. From JavaScript promises to Python coroutines
4. Async: waiting efficiently
5. Concurrent I/O
6. Generators: produce data when needed
7. A small web-scraping example
8. Practical gotchas
9. Day 3 recap

## Capstone connection

Add a useful external-data feature or use HTTPX/BeautifulSoup as preparation for a later capstone.

---

# 9. Day 4 — FastAPI + Pydantic

## Objective

Give frontend developers enough knowledge to build a Python backend that their existing frontend skills can consume.

## Important teaching decision

Use Jupyter for:

- Explaining
- Experimenting
- Inspecting Pydantic behavior
- Demonstrating API concepts

Use actual Python files for the FastAPI application.

Example:

```text
day-04/
    04_fastapi_pydantic.ipynb
    app/
        main.py
        models.py
        services.py
```

## Topics

### FastAPI fundamentals

- What FastAPI is
- Application object
- Routes
- HTTP methods
- Running the application
- Automatic API documentation

### Request parameters

- Path parameters
- Query parameters
- Request bodies

### Pydantic

- `BaseModel`
- Request models
- Response models
- Validation
- Serialization
- Relationship between type hints and runtime validation

### Async endpoints

- `async def`
- Using async service calls
- Avoiding blocking work in async endpoints

### Error handling

- HTTP status codes
- `HTTPException`
- Basic application error handling

### Basic application structure

Introduce a lightweight structure:

```text
app/
├── main.py
├── api/
├── models/
└── services/
```

Do not over-engineer the project structure.

## Key gotchas

- Decorators register FastAPI routes.
- Type hints are not the same as runtime validation.
- `async` does not make blocking code non-blocking.
- Avoid putting all business logic inside route functions.
- Avoid exposing internal exceptions or secrets.

## Notebook

`04_fastapi_pydantic.ipynb`

Use the notebook to explain and experiment.

Include:

- First FastAPI endpoint.
- Parameters.
- Pydantic request model.
- Pydantic response model.
- Basic validation.
- Error handling.
- Calling a service.

## Slides

Suggested story:

1. **FastAPI gives Python developers a familiar web boundary**
2. Request → route → service → response
3. Building the first endpoint
4. Parameters and request bodies
5. Pydantic: making data trustworthy
6. Async endpoints
7. Keeping routes thin
8. API gotchas
9. Day 4 recap

## Capstone connection

Turn the application into an API:

```text
GET    /tasks
GET    /tasks/{id}
POST   /tasks
PUT    /tasks/{id}
DELETE /tasks/{id}
```

Initially, data can remain in memory.

---

# 10. Day 5 — SQLite + Putting It Together

## Objective

Complete the transition from Python examples to a small end-to-end application with persistent data.

## Topics

### Database fundamentals

- What a relational database is.
- Tables and rows.
- Primary keys.
- Basic SQL.
- SQLite and why it is useful for small applications.

### Python + SQLite

- Connecting to SQLite.
- Creating a table.
- Insert.
- Select.
- Update.
- Delete.

Keep SQL deliberately simple.

### Connecting SQLite to FastAPI

Demonstrate:

```text
HTTP request
    ↓
FastAPI
    ↓
Pydantic
    ↓
Python service
    ↓
SQLite
    ↓
Response
```

### Basic project structure

Bring together:

```text
app/
├── main.py
├── api/
├── models/
├── services/
└── database.py
```

Do not introduce a large ORM framework unless there is significant spare time.

### Basic testing

Introduce the idea of automated testing with pytest.

Primary focus:

- Unit test concept.
- A simple Python function test.
- One basic API test if time permits.

Do not teach a complete testing framework.

### Final walkthrough

Show the complete application from frontend/API client to database.

## Key gotchas

- SQL injection and parameterized queries.
- Database connections/resources need proper handling.
- SQLite is excellent for small applications but not a universal production database.
- Don't put database logic directly into every route.
- Keep secrets/configuration out of source code.
- Don't confuse a working demo with production readiness.

## Notebook

`05_sqlite_and_capstone.ipynb`

Include:

- Basic SQL examples.
- Python SQLite example.
- CRUD example.
- Connecting the concepts to FastAPI.
- Final architecture walkthrough.
- Optional testing example.

## Slides

Suggested story:

1. **A useful application needs somewhere to remember things**
2. SQLite in one picture
3. Tables, rows, and simple SQL
4. Python talking to SQLite
5. FastAPI + SQLite request flow
6. Putting the project together
7. Basic testing
8. What would we improve for production?
9. Course recap / where to go next

## Capstone connection

Complete the Task application with persistent SQLite storage.

---

# 11. Capstone Philosophy

Capstones should not all be backend/API projects.

The trainees are already frontend developers, so they should combine their existing frontend skills with Python.

The question should be:

> **What useful thing can I build now using Python together with the skills I already have?**

A capstone may therefore be:

- Full-stack web application.
- Data-oriented application.
- Automation tool.
- Scraping/information-extraction application.
- Developer tool.
- External API integration.
- CLI utility.
- Dashboard.
- Optional AI-assisted application.

## Suggested capstone choices

### 1. Expense Tracker

Frontend:

- Dashboard
- Charts
- Filters
- Expense entry

Python:

- FastAPI
- Pydantic
- SQLite
- Aggregation

### 2. Bookmark Manager

Features:

- Save URLs.
- Tags.
- Search.
- Automatically retrieve page metadata.

Python can use:

```text
HTTPX
+
BeautifulSoup
+
SQLite
```

### 3. GitHub Dashboard

Features:

- Repository search.
- Stars.
- Issues.
- Languages.
- Basic repository statistics.

Python consumes the GitHub API and can optionally cache results.

### 4. JSON/CSV Data Explorer

Frontend:

- Upload file.
- Table view.
- Filtering.
- Sorting.
- Charts.

Python:

- Parse data.
- Validate data.
- Transform data.
- Aggregate results.

### 5. Website Monitor

Features:

- Track URLs.
- Check availability.
- Record response times.
- Show history.

Python handles periodic checking and persistence.

### 6. Price Tracker

Features:

- Track selected URLs.
- Extract a price.
- Store history.
- Display changes.

Python demonstrates automation and web parsing.

### 7. News Aggregator

Python:

- Consume RSS/API sources.
- Normalize articles.
- Deduplicate.
- Store data.

Frontend:

- Search.
- Categories.
- Bookmarks.
- Reading history.

### 8. AI Bookmark Assistant — optional extension

Start with the Bookmark Manager.

Optional enhancement:

```text
URL
 ↓
Python fetches page
 ↓
Extract content
 ↓
LLM
 ↓
Summary + tags
 ↓
SQLite
```

AI should remain an **optional extension**, not a required part of the five-day curriculum.

---

# 12. Common Capstone Requirements

To keep projects comparable and achievable:

## Minimum requirements

Every capstone should have:

- Python.
- `uv`.
- A meaningful Python component.
- A usable interface: web UI, CLI, or both.
- Basic error handling.
- README/setup instructions.
- Persistence where the project naturally needs it.

## Optional extensions

- FastAPI.
- SQLite.
- External APIs.
- Async.
- BeautifulSoup.
- Background processing.
- Charts.
- Automated tests.
- AI/LLM integration.

The objective is to demonstrate Python skills, not to build the largest application.

---

# 13. Slide Production Guidelines

The uploaded **EY Executive Presentation Visual Guide** is the source of truth for the visual direction of the slides. It describes an inferred design system rather than an official EY specification. fileciteturn2file0

## Visual tone

- Executive
- Premium
- Confident
- Minimal
- Structured
- Technology-oriented
- Consulting quality

Avoid:

- Busy layouts
- Academic lecture-slide appearance
- Startup-pitch aesthetics
- Excessive decoration
- Futuristic visuals without explanatory value

## Color direction

Use the visual guide's restrained palette:

- Very dark charcoal / near-black background.
- White primary text.
- EY Yellow as a restrained accent.
- Light grey supporting text.
- Medium grey borders/secondary lines.

Yellow should guide attention, not dominate.

## Typography

Headlines should be:

- Large.
- Bold.
- Short.
- Conclusion-oriented where possible.

Body copy should remain concise.

## Layout

Prefer:

- One dominant focal point.
- Strong hierarchy.
- Generous whitespace.
- One main diagram, framework, code example, or visual per slide.
- Clear visual reading order.

Preferred structures:

```text
Headline
↓
Main visual
↓
Supporting insight
```

or:

```text
Headline

Visual                  Key observations
```

or:

```text
Headline
Framework / diagram
Interpretation
```

Avoid multiple competing visuals.

## Visual diagrams

Prefer original conceptual diagrams rather than decorative graphics.

Useful diagrams for this course:

- Python ↔ JavaScript mental-model maps.
- Data structure maps.
- Notebook → project progression.
- HTTP request lifecycle.
- Async concurrency diagrams.
- FastAPI request flow.
- Pydantic validation boundary.
- Application architecture.
- Database request flow.
- Capstone architecture.

Do not use generic SmartArt.

## Code on slides

Code should explain the idea behind the code, not reproduce an entire notebook.

When code is necessary:

- Show only relevant lines.
- Use large readable typography.
- Annotate the important concept.
- Avoid full-screen source files.

## footer

**Every slide must include:**

> `Instructor: Suman Barick`
> `L&D POC: Rahul Bajaj / Aman Singh Kamboj`

The footer should be:

- Small but clearly visible.
- Consistent in position.
- Visually subordinate to the main content.
- Present on every slide, including title and closing slides.

## Self-sufficient slides

Every slide should be understandable without the instructor speaking.

Because the deck doubles as learning material, a learner should be able to revisit a slide weeks later and still use it.

A deck for a day must deeply cover all the topics of that day. It may reference topics from past. But it should never contain topics are are yet to be disucssed of a future day.

Let each slide be a (as much as possible) complete reference / cheatsheet of all the common usages of 1 particular topic, e.g. if a slide is on string, it should have everything on python strings, methods, usages, indexing etc.

There is no upper limit on how many slides a day can have.

For topic/cheatsheet slides, include enough information to:

- Identify the concept.
- Recall the syntax.
- See common usage.
- Recognize related operations.
- Understand important gotchas.
- Connect it to JavaScript/TypeScript where useful.

Do not create slides that contain only a topic title and depend entirely on narration.

### Cheatsheet slide anatomy

A strong topic slide will typically use:

```text
Title / takeaway

┌────────────────────┬────────────────────┐
│ Core syntax         │ Common operations  │
│                     │                    │
│ code example        │ code examples      │
├────────────────────┼────────────────────┤
│ Python mental model │ Gotcha / JS bridge │
└────────────────────┴────────────────────┘

Instructor footer
```

The exact layout should vary by topic; this is a content model, not a mandatory visual template.

## Slide quality test

Before finalizing each slide, ask:

1. Does the headline communicate a useful takeaway?
2. Is there one dominant idea?
3. Can the slide be understood quickly?
4. Does every visual element serve a purpose?
5. Is the text readable?
6. Is whitespace preserved?
7. Does the slide look appropriate for an experienced engineering audience?
8. Is `Instructor: Suman Barick` present?

---

# 14. Notebook Production Guidelines

The notebooks are the **hands-on learning material**.

Each notebook should be useful during the live class and after the class.

## Recommended structure

```text
# Day N — Title

## What you'll learn

Short list.

## Before we start

Environment/setup if necessary.

## 1. Concept

Short explanation.

### Example

Runnable code.

### What happened?

Explanation.

### JavaScript connection

Optional comparison.

### Python gotcha

Important pitfall.

### Try it

Small modification.

## 2. Next concept

...

## Practice challenge

A small exercise.

## Solution

Solution below the exercise.

## Day recap

Short summary.
```

## Notebook principles

- Keep cells small.
- Prefer runnable examples.
- Avoid giant code cells.
- Explain output where useful.
- Include exercises achievable within the available time.
- Ensure examples work from a clean kernel.
- Avoid hidden state between unrelated sections.
- Clearly distinguish demonstration code from production code.
- Show when code should move from a notebook into `.py` modules.

---

# 15. Relationship Between Slides and Notebook

The two artifacts should complement each other.

### Slides answer:

> "What is this concept, why does it matter, and how does it fit into the bigger picture?"

### Notebook answers:

> "Show me how it works. Let me run it. Let me change it."

Example:

```text
SLIDE
FastAPI request lifecycle

Frontend
   ↓
HTTP
   ↓
Route
   ↓
Pydantic
   ↓
Service
   ↓
Response


NOTEBOOK
Actual FastAPI code
+
Run it
+
Change parameters
+
Observe validation
+
Try an invalid request
```

Do not duplicate the entire notebook on slides.

---

# 16. Future Markdown Chapter Guidelines

If a standalone Markdown chapter is created for a day, it should be written as a book chapter in:

# Learn Python in 5 Days

Tone:

- Friendly.
- Professional.
- Respectful.
- Clear.
- Like an experienced developer teaching a younger colleague.
- Never patronizing.
- Practical rather than academic.

The chapter should include:

- Conceptual explanations.
- A good amount of examples.
- JavaScript comparisons.
- Python gotchas.
- Practical engineering advice.
- Exercises.
- Capstone connection.
- Recap.

The chapter should be useful to someone who did not attend the live session.

---

# 17. Scope Guardrails

The following topics are intentionally outside the core five-day curriculum:

- Advanced decorators.
- Metaclasses.
- Descriptors.
- CPython internals.
- Advanced inheritance.
- Django.
- Full database/ORM training.
- Docker training.
- Cloud deployment training.
- Machine-learning mathematics.
- Model training.
- Advanced AI frameworks.
- Advanced RAG implementation.
- Production-grade distributed systems.

These can appear in "Where to go next" sections but should not consume live-session time.

---

# 18. Modern Tooling Principle

The course should use a modern Python workflow.

Primary tooling:

```text
Python
+
uv
+
Jupyter
+
pyproject.toml
+
FastAPI
+
Pydantic
+
HTTPX
+
SQLite
+
pytest
```

`pip` may be mentioned because learners will encounter it in existing projects, but `uv` should be the primary dependency/environment workflow.

The exact commands and library APIs should be checked against current documentation when final day materials are created.

---

# 19. Final Course Outcome

The five days should tell one simple story:

```text
"I can write Python."
        ↓
"I can structure Python."
        ↓
"I can make Python talk to the web."
        ↓
"I can expose Python as an API."
        ↓
"I can persist data and build a small application."
```

That is the core promise of the training.

AI, advanced Python, cloud deployment, sophisticated databases, and other ecosystem topics should be positioned as the **next step after the foundation**, not squeezed into the five-hour curriculum.

---

# 20. Day-wise Deliverables

For future content-generation work, produce the following for each day:

```text
day-01/
├── slides.html
├── 01_python_fundamentals.ipynb
└── 01_python_fundamentals.md

day-02/
├── slides.html
├── 02_practical_python.ipynb
└── 02_practical_python.md

day-03/
├── slides.html
├── 03_web_and_async.ipynb
└── 03_web_and_async.md

day-04/
├── slides.html
├── 04_fastapi_pydantic.ipynb
└── 04_fastapi_pydantic.md

day-05/
├── slides.html
├── 05_sqlite_and_capstone.ipynb
└── 05_sqlite_and_capstone.md
```

The Markdown chapter is optional if the immediate requirement is only slides and notebooks, but the content should be written with future book reuse in mind.

---

# 21. Final Production Rule

> **Do less, but teach it well.**

If there is a conflict between covering another topic and giving learners enough time to understand, run, modify, and practice the current topic, **drop the extra topic**.

The five-day course succeeds when learners leave confident enough to build something useful in Python—not when every Python feature has appeared in the slides.
