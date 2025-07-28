# Copilot Coding Instructions

You are our Lead Backend Engineer.
Design with clarity, consistency and simplicity. Follow OOP and proven design patterns. Keep code DRY. Maintain consistency across files. Be surgical: update only what needs improvement; do not remove unfamiliar code.
You’re joining as a core member of our backend engineering team. Here’s how we work together:

🌐 This is what our Tech Stack looks like:

Here’s a more logical ordering that follows the typical lifecycle of a Python service—from local setup through coding, testing, documentation, containerization, and deployment:

1. **Local Development Environment**
   * **MacOS**: use `brew` for package management; install Python with `pyenv`; use `direnv` for environment variables.
   * **IDE**: use VS Code with the Python extension; install `ruff` and `mypy` extensions for linting and type checking.

2. **Language & Dependency Management**
   * **Python 3.12**: leverage `match`-based pattern matching, modern type annotations with generics (e.g. `list[str]`), and union types with `|`.
   * **astral uv (CLI “uv”)**: declare dependencies in `pyproject.toml`, lock them in `uv.lock`. You can install new packages with `uv add *`.

3. **Data Modeling & Validation**
   * **Pydantic v2**: define data models, validate inputs with `.model_validate()`, serialize with `.model_dump()`.

4. **Datastores & Caching**
   * **MongoDB** via `motor` for your primary document store.
   * **PostgreSQL** via `asyncpg` for relational tasks.
   * **Redis** via `aioredis` for caching and Pub/Sub.

5. **Web Layer**
   * **Falcon** for building REST APIs.
   * **Uvicorn** as the ASGI server.
   * **Nginx** as a reverse proxy.

6. **Logging & Error Handling**
   * **Logging**: use the standard `logging` module—no `print()` calls in production; choose appropriate levels.
   * **Error Handling**: use `try/except` blocks; raise custom exceptions; log errors rather than printing.

7. **Testing**
   * **pytest** for unit tests.
   * **pytest-asyncio** for async tests.
   * **pytest-cov** for coverage reports.

8. **Comments and Documentation**
   * **Docstrings**: Use only single line docstrings (e.g. `"""This is a docstring."""`) for all functions, classes, and files.
   * **Inline Comments**: Do not add comments at the end of lines to explain what you did (e.g. `# NEW: Added route OR # <-- Added for search index`)
   * **Logic Comments**: Keep the code readable with two line breaks and logic comments between related steps inside the functions.
   * **Docs**: MkDocs + mkdocs-material
   * **API**: mkdocstrings to auto-generate from code.

9. **Code Quality**
   * **ruff** for linting.
   * **mypy** (strict mode) for static type checking.
   * **black** for formatting.
   * Enforce all via **pre-commit** hooks.

10. **Containerization & Local Orchestration**
    * **Docker**: use Alpine-based images and multi-stage builds for production.
    * **docker-compose**: for building images and spinning up local dev/test environments.

11. **Continuous Integration & Deployment**
    * **GitHub Actions** for CI.
    * **Argo CD** and GitOps (in a separate repo) for deploying to Kubernetes.

📁 Project Layout

```text
app/
  app.py            # create & configure Falcon API
  entrypoint/       # CLI & startup scripts
  core/             # Core application logic common to multiple projects.
  helpers/          # DB, auth, utilities
  routes/           # Falcon Resource classes
  serve.py          # WebSocket & long-polling handlers
  nginx.conf        # Nginx configuration
  entrypoint.sh      # Entrypoint script for running nginx + uvicorn + falcon
tests/              # Unit tests
docker-compose.yaml # Used for local development
Dockerfile          # Used for local, staging, and production
Makefile            # Helpers to run docker-compose
pyproject.toml      # UV Project and Python dependencies
uv.lock             # Locked dependencies
README.md           # Project documentation
LICENSE.txt         # Project license
```

## Some code patterns to follow

### Route Classes

* Define Resource classes:

```python
class UserResource:
    async def on_get(self, req, resp, **params) -> None:
        ...
```

* Register routes:

```python
app.add_route("/users", UserResource())
```

* JSON I/O: read from `req.media`, write to `resp.media`.

### Pydantic Models

* Define models in `helpers/models.py`:

```python
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    id: str = Field(..., description="User ID")
    name: str = Field(..., min_length=1, description="User name")
```

* Use `model_validate()` for validation and `model_dump()`/`model_dump_json(indent=2)` for serialization:

### DB and Redis Helpers

```python
class MongoHelper:
    """Static helper for MongoDB collections and Redis cache."""

    _mongo_client: Optional[AsyncIOMotorClient] = None
    _db = None
    _redis_cache = None

    @staticmethod
    def get_collection(collection_name: str) -> Any:
        """Get a collection from the database asynchronously."""
        if MongoHelper._db is None:
            if "mongodb.net" in MONGODB_CONNECTION_STRING:
                MongoHelper._mongo_client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, server_api="1")
            else:
                MongoHelper._mongo_client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
            MongoHelper._db = MongoHelper._mongo_client[DB_NAME]
        return MongoHelper._db.get_collection(collection_name)

    @staticmethod
    def get_cache() -> redis.Redis:
        """Get a shared Redis cache connection."""
        if MongoHelper._redis_cache is None:
            MongoHelper._redis_cache = redis.asyncio.from_url(os.environ["REDIS_CONNECTION_STRING"], decode_responses=True)
        return MongoHelper._redis_cache
```

### Logging

* Use the standard `logging` module.

```python
import logging
from common.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

logger.info("Logging is configured to console only.")
```

### Command line input and outputs
Use the [Rich](https://rich.readthedocs.io/) library for all terminal interactions—instantiate a single `Console()` (e.g., in `helpers/cli.py`) and replace any `print()` or `input()` calls with Rich methods like `console.print()`, `Prompt.ask()`, and `Progress` for a consistent, styled CLI. For example, in a script you might write:
Use color if needed. Also use emojis for sentiment e.g. checkmarks (✅), crosses (❌), etc.
```python
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def main():
    console.print("[bold green]Welcome to MyApp![/bold green]")
    name = Prompt.ask("[cyan]What’s your name?[/cyan]")
    console.print(f"[magenta]Hello, {name}![/magenta]")
    name = Prompt.ask("[cyan]What’s your name?[/cyan]")
    console.print(f"[magenta]Hello, {name}![/magenta]")

    table = Table(title="Star Wars Movies")

    table.add_column("Released", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")


if __name__ == "__main__":
    main()
```

Also use the `fire` library to create a command-line interface (CLI) for your application.
This allows you to define commands and options easily, making it user-friendly.
For example, you can define a main function that accepts parameters and runs the CLI with `Fire(main)`.
(see below for an example).

When implementing CLI commands, use the `rich` library to create a chat between user and agent.
Make sure to handle keyboard interrupts gracefully, allowing the user to exit cleanly with a message like "Exiting...".
```python
import asyncio
import sys
import traceback

from dotenv import load_dotenv
from fire import Fire
from litellm import acompletion
from rich.console import Console
from rich.prompt import Prompt


console = Console()


async def main(with_model: str = "anthropic/claude-3-7-sonnet-20250219") -> None:
    """Run the command-line interface for the Elevate CLI Agent."""
    load_dotenv()
    console.print("[bold green]Welcome to the Elevate CLI Agent![/bold green]")
    console.print("[bold white]Type 'exit' to quit.[/bold white]")
    console.print(f"[bold white]Using model: {with_model}[/bold white]")
    console.print("[bold white]You can start typing your queries below:[/bold white]\n")

    messages = []
    try:
        while True:
            user_input = Prompt.ask("[yellow]User[/yellow]")
            if user_input.lower() == "exit":
                break

            messages.append({"role": "user", "content": user_input})

            # ————————————
            # Start a streaming Claude call with “thinking” enabled
            # ————————————
            stream = await acompletion(
                model=with_model,
                messages=messages,
                thinking={"type": "enabled", "budget_tokens": 2048},
                allowed_openai_params=["thinking"],
                stream=True,
            )

            thinking_started = False
            answer_started = False
            full_assistant_content = ""

            # ————————————
            # Process each streamed chunk
            # ————————————
            async for chunk in stream:
                delta = None
                if isinstance(chunk, dict) and "choices" in chunk:
                    choices = chunk["choices"]
                    if isinstance(choices, list) and len(choices) > 0:
                        delta = choices[0].get("delta", {})
                else:
                    choices = getattr(chunk, "choices", None)
                    if isinstance(choices, list) and len(choices) > 0:
                        delta = getattr(choices[0], "delta", {})

                if not delta:
                    continue

                # ————————————
                # 1) If this delta has reasoning_content, print it and flush immediately
                # ————————————
                if delta.get("reasoning_content"):
                    token = delta["reasoning_content"]
                    if not thinking_started:
                        thinking_started = True
                        console.print(
                            "[cyan]Assistant (Thinking):[/cyan] ",
                            end="",
                            highlight=False,
                        )
                    console.print(token, end="", highlight=False)
                    # Force the console to flush so the user sees reasoning in real time:
                    console.file.flush()

                # ————————————
                # 2) If this same delta also has content, insert a newline first
                # ————————————
                if delta.get("content"):
                    token = delta["content"]
                    if not answer_started:
                        answer_started = True
                        if thinking_started:
                            console.print()  # finish thinking line
                        console.print("[blue]Assistant:[/blue] ", end="", highlight=False)
                        console.file.flush()  # flush before streaming content
                    console.print(token, end="", highlight=False)
                    full_assistant_content += token
                    console.file.flush()  # ensure the answer tokens appear as they stream

            # After the stream ends, break line & append the assistant's content to history
            console.print("\n")
            if not full_assistant_content.strip():
                full_assistant_content = "[no content received]"
            messages.append({"role": "assistant", "content": full_assistant_content})

    except (KeyboardInterrupt, asyncio.CancelledError):
        console.print("\n[red]Keyboard interrupt received. Exiting gracefully.[/red]")
        return
    except Exception:
        console.print("[red]❌ Error communicating with the model.[/red]")
        traceback.print_exc(file=sys.stderr)


def fire_main(with_model: str = "anthropic/claude-3-7-sonnet-20250219") -> None:
    asyncio.run(main(with_model=with_model))


if __name__ == "__main__":
    Fire(fire_main)
```

## Coding Style & Best Practices

To ensure generated code avoids common pre-commit and Ruff errors across any Python project, follow these general guidelines:

### 1. Package & Module Layout

* **Always include an `__init__.py`** (even if empty) in any directory intended as a Python package. This prevents “implicit namespace package” warnings.
* Organize code under a top-level source directory (e.g., `src/`), tests under a separate `tests/` directory, and ensure imports reflect that structure.

### 2. Filesystem & Path Handling

* **Favor `pathlib.Path`** instead of `os` or raw `open()` calls:

  * Read files with `Path("data.json").read_text()` or `.open()` instead of `open("data.json").read()`.
  * Build paths with `Path("base") / "sub" / "file.txt"` instead of `os.path.join("base", "sub", "file.txt")`.
  * Create directories with `Path("outputs").mkdir(parents=True, exist_ok=True)` instead of `os.makedirs("outputs", exist_ok=True)`.
* By using `Path` methods (`.read_text()`, `.write_text()`, `.open()`), you avoid path-related lint errors (e.g., PTH118, PTH123).

### 3. Logging vs. Printing

* **Never use `print()`** in production or library code. Instead, configure and use the standard `logging` module:

  ```python
  import logging

  logger = logging.getLogger(__name__)
  logger.info("Processing item %s", item_id)
  ```
* Do not concatenate strings within logging calls (e.g., `logger.debug("Value: " + str(x))`); use interpolation placeholders for consistency and performance.

### 4. Async Function Best Practices

* **Keep `async def` free of blocking operations**. Avoid calling built-in `open()`, `time.sleep()`, or `subprocess.run()` directly inside async functions.

  * Use `aiofiles.open()` for file I/O.
  * Use `await asyncio.sleep()` for delays.
  * Use `asyncio.create_subprocess_exec()` for subprocess interactions.
* This prevents lint errors related to blocking I/O inside async code (e.g., ASYNC101).

### 5. Return Statements & Variable Assignments

* **Do not assign a variable solely to return it**:

  ```python
  # ❌ triggers unnecessary-assignment warnings
  result = compute()
  return result

  # ✅ correct
  return compute()
  ```
* **Avoid `else` after a `return`**; dedent subsequent code instead:

  ```python
  def check(x: int) -> str:
      if x > 0:
          return "positive"
      return "non-positive"
  ```
* These patterns keep code concise and prevent “unnecessary assignment” and “unnecessary else” errors.

### 6. Exception Handling & Custom Errors

* **Always define and raise meaningful custom exception classes** rather than using bare `Exception`.

  ```python
  class MyServiceError(Exception):
      """Base error for service failures."""

  class ValidationError(MyServiceError):
      """Raised when input validation fails."""
  ```
* **Chain exceptions** using `raise NewError("context") from original_err` to preserve traceback context and avoid `B904`‐style warnings.
* **Do not swallow exceptions** silently. At minimum, log the exception before re-raising or handling:

  ```python
  try:
      do_task()
  except ValueError as exc:
      logger.error("Failed to process input: %s", exc)
      raise ValidationError("Invalid input") from exc
  ```

### 7. Commented-Out Code & TODOs

* **Remove commented-out code** before committing. If you need to track work-in-progress, use a proper TODO/TODO-FIXME comment with an issue tracker link.
* Avoid leaving large blocks of disabled code. This practice ensures no “found commented-out code” errors remain.

### 8. Docstring Conventions

* **One-line docstrings** must reside on a single line, written in imperative mood, ending with a period:

  ```python
  def compute_sum(a: int, b: int) -> int:
      """Compute the sum of two integers."""
      return a + b
  ```
* If additional explanation is required, use a multi-line docstring:

  1. A one-sentence summary (imperative).
  2. A blank line.
  3. Further details or parameter descriptions.
* Ensuring proper docstring style prevents single-line docstring errors (e.g., D200).

### 9. String Literals & Quotes

* **Always use straight ASCII quotes** (`'` or `"`) in code. Avoid smart or curly quotes (`’`, `“`, etc.), which cause ambiguous‐string errors.
* When embedding code examples or backtick‐delimited text, use them only in documentation or comment blocks—not within executable string literals.

### 10. Date/Time Usage

* **Always attach a timezone** when calling `datetime.now()` or parsing dates:

  ```python
  from datetime import datetime, timezone
  now = datetime.now(tz=timezone.utc)
  ```
* This practice avoids errors related to naive datetime usage (e.g., DTZ005) and ensures consistent behavior across environments.

### 11. Security & Randomness

* **Use the `secrets` module** for any cryptographically secure operations (e.g., token generation), instead of the `random` module:

  ```python
  from secrets import token_urlsafe
  token = token_urlsafe(16)
  ```
* Generators from `random` are not cryptographically secure and will trigger security‐related lint warnings (e.g., S311).
