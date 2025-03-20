# Elevate GenAI Snippets
Contains common snippets of code with GenAI, like:
- Text to JSON
- Text to Markdown
- Text to SQL
- And more ...

## Approach
This project aims to provide fast, cheap, accurate, and deterministic outcomes to common code in GenAI.
If you're planning to perform one of the tasks that this code helps with, you should be guaranteed gold standard model and tool to perform that task. For example, in Text-to-JSON, you could use different models, but you can also use `lite-llm` or `instructor`. What's the best one for you?

Here's how we will achieve this:
- We'll be using a Test-Driven Development approach to building this toolset.
- Each helper class can be run `with_tool` and `with_model`.
- The default values for them should be the "gold standard".
- Pytests should enforce the speed, cost, accuracy and determinism constraints.
- Precommits should run pytest, and also test before merge to main.
- A comparison chart should suggest what tools and models work well (TODO). Users will typically know the models they are allowed to use. The code should choose the right tools for it.

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
