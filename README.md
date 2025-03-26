# Elevate GenAI Snippets
This project is designed to deliver fast, cost-effective, reliable, and deterministic solutions to common GenAI challenges like:
- Text to JSON
- Text to Markdown
- Text to SQL
- [And more](#snippets) ... 

This is a task focused way to do GenAI - you care about particular tasks work, not which model or tool to use. Or if you do have a preference of the model, the choice of underlying tool doesn't matter as long as you get the right result. There may be nuances to the tools and the models, but choosing this lib, you choose gold standard. 

## Approach
We follow a Test-Driven Development methodology to ensure robust functionality and rapid feedback. Each helper class is configured to use a "gold standard" model and tool by default, with tests enforcing high performance, accuracy, and reproducibility. A forthcoming comparison chart will guide users to the best models and tools for their specific needs.

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

## Snippets

| Implemented | Snippet          | Description                      | # Tests |
|:-----------:|------------------|----------------------------------|---------|
| ✅          | Only JSON     | Converts text to JSON format     | 5       |
| ✅          | Only AudioCast | Converts text to podcast style format | 2       |
|            | Only Prompt      | Write prompts based on seed, and list of ffeedback containing examples or with critiques        | -       |
|            | Only Markdown | Converts text to Markdown format | -       |
|            | Only Python | Only generates python code, executes it and returns the response | -       |
|            | Only SQL      | Converts text to SQL query       | -       |
|            | Only Rephrase      | Force grammar and rephrase for the conversation context (e.g. professional email)       | -       |
|            | Only Summaries      | Write summaries        | -       |
|            | Only ELI5      | Write ELI5 summaries        | -       |
|            | Only Email      | Write better emails        | -       |
|            | Only Forms      | Conversations for form filling       | -       |
|            | Only Plan      | Plan a tree of actions to be done to execute user task       | -       |
|            | Only Writing      | Uses the DAG Planner to write a blog, etc.        | -       |
|            | Only Excel      | Understand and execute Financial Models to answer user questions        | -       |
|            | Only Fiction      | Uses the DAG Planner to write a fiction        | -       |
|            | Only Art      | Generate images based on artistic params        | -       |
|:-----------:|------------------|----------------------------------|---------|

## Contributing

Contributions are welcome! Please ensure all changes pass tests and adhere to our TDD guidelines.

## Developer Instructions

- Follow the "Setting it up" section to configure your development environment.
- Use `uv sync` and activate the virtual environment before making changes.
- Run tests with `uv run pytest` to ensure functionality and performance.
- Adhere to TDD practices and ensure pre-commit hooks pass before merging.
- Use descriptive branch names for feature development and submit pull requests for review.
