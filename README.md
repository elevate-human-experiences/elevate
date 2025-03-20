# Elevate GenAI Snippets
Contains common snippets of code with GenAI, like:
- Text to JSON
- Text to Markdown
- Text to SQL
- And more ...

## Approach
This project is designed to deliver fast, cost-effective, reliable, and deterministic solutions to common GenAI challenges. We follow a Test-Driven Development methodology to ensure robust functionality and rapid feedback. Each helper class is configured to use a "gold standard" model and tool by default, with tests enforcing high performance, accuracy, and reproducibility. A forthcoming comparison chart will guide users to the best models and tools for their specific needs.

## Setting it up

```bash
uv sync
source .venv/bin/activate
```

We also use precommit to make sure commited files work well. After installing pre-commit, run:
```bash
pre-commit install
```

Also create a `.env` file with the following:
```
OPENAI_API_KEY=
```

## Usage

- Run the helper classes using the default "gold standard" tool and model.
- Execute tests with `pytest` to ensure speed, cost, accuracy, and determinism.
    - `uv run pytest` or `uv run pytest tests/test_file.py`.
- Refer to individual module documentation for task-specific instructions.

## Contributing

Contributions are welcome! Please ensure all changes pass tests and adhere to our TDD guidelines.

## Developer Instructions

- Follow the "Setting it up" section to configure your development environment.
- Use `uv sync` and activate the virtual environment before making changes.
- Run tests with `uv run pytest` to ensure functionality and performance.
- Adhere to TDD practices and ensure pre-commit hooks pass before merging.
- Use descriptive branch names for feature development and submit pull requests for review.
