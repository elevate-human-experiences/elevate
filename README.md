# Elevate GenAI Snippets
This project is designed to deliver fast, cost-effective, reliable, and deterministic solutions to common GenAI challenges like:
- Text to JSON
- Text to Markdown
- Text to SQL
- [And more](#snippets) ...

This is a task focused way to do GenAI - you care about particular tasks work, not which model or tool to use. Or if you do have a preference of the model, the choice of underlying tool doesn't matter as long as you get the right result. There may be nuances to the tools and the models, but choosing this lib, you choose gold standard.


### Only Snippets

| Implemented | Snippet          | Description                      | Uses      | # Tests |
|:-----------:|------------------|----------------------------------|-----------|---------|
| ✅          | Only JSON     | Converts text to JSON format     |           | 5       |
| ✅          | Only AudioCast | Converts text to podcast style format | Only JSON | 5       |
| ✅          | Only Markdown | Converts text to Markdown format |           | 5       |
|            | Only Python | Only generates python code, executes it and returns the response |           | -       |
|            | Only SQL      | Converts text to SQL query       |           | -       |
| ✅          | Only Rephrase      | Force grammar and rephrase for the conversation context (e.g. professional email) |           | 8       |
| ✅          | Only Summaries      | Write summaries        |           | -       |
|            | Only ELI5      | Write ELI5 summaries        |           | -       |
| ✅          | Only Email      | Write better emails        |           | 8       |
|            | Only Forms      | Conversations for form filling       |           | -       |
|            | Only Excel      | Understand and execute Financial Models to answer user questions        |           | -       |
|  ✅          | Only Judge LLMs      | Judge the outputs of LLMs        |           | 5       |

### Only Prompts

| Implemented | Snippet          | Description                      | Uses | # Tests |
|:-----------:|------------------|----------------------------------|------|---------|
|            | Only Prompt      | Write prompts based on seed, and list of feedback containing examples or with critiques |      | -       |
|            | Only Feedback      | Improve prompts with agent driven feedback. |      | -       |


### Only Plan

| Implemented | Snippet          | Description                      | Uses | # Tests |
|:-----------:|------------------|----------------------------------|------|---------|
|            | Only Plan      | Plan a tree of actions to be done to execute user task |      | -       |
|            | Only Writing      | Uses the DAG Planner to write a blog, etc. |      | -       |

### Only Swarm

| Implemented | Snippet          | Description                      | Uses | # Tests |
|:-----------:|------------------|----------------------------------|------|---------|
|            | Only Elves | Multi-agent system to do multiple small Only Tasks |      | -       |
|            | Only Data Hygene | Elves that clean up your data together |      | -       |

### Only Art

| Implemented | Snippet          | Description                      | Uses | # Tests |
|:-----------:|------------------|----------------------------------|------|---------|
|            | Only Fiction      | Uses the DAG Planner to write a fiction |      | -       |
|            | Only Art      | Generate images based on artistic params |      | -       |
|            | Only Hokusai      | Generate images inspired from "36 Views of Mount Fuji" |      | -       |


## Approach
We follow a Test-Driven Development methodology to ensure robust functionality and rapid feedback. Each helper class is configured to use a "gold standard" model and tool by default, with tests enforcing high performance, accuracy, and reproducibility. A forthcoming comparison chart will guide users to the best models and tools for their specific needs.

## Setup

```bash
uv sync
source .venv/bin/activate
```

Also create a `.env` file with the following:
```
OPENAI_API_KEY=
```
The .env file is loaded automatically using `python-dotenv`'s `load_env` method.

## Usage

### ClI Agent
You can use a CLI Agent to use the snippets to do work.

You can run the agent with:
```bash
uv run agent/cli.py
```

### Tests

- Run the helper classes using the default "gold standard" tool and model.
- Execute tests with `pytest` to ensure speed, cost, accuracy, and determinism.
    - `uv run pytest` or `uv run pytest -s tests/test_file.py `.
- Refer to individual module documentation for task-specific instructions.

## Contributing

Contributions are welcome! Please ensure all changes pass tests and adhere to our TDD guidelines.

## Developer Instructions

- Follow the "Setting it up" section to configure your development environment.
- We also use precommit to make sure commited files work well. After installing pre-commit, run:
```bash
pre-commit install
```
While pre-commit runs on commits, you can manually run the tests with `pre-commit run --all-files`.
- Use `uv sync` and activate the virtual environment before making changes.
- Run tests with `uv run pytest` to ensure functionality and performance.
- Adhere to TDD practices and ensure pre-commit hooks pass before merging.
- Use descriptive branch names for feature development and submit pull requests for review.
