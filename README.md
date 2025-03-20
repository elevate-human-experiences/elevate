# Elevate GenAI Snippets
Contains common snippets of code with GenAI like:
- Text to JSON
- Text to Markdown
- Text to SQL
- And more ...
  
This project aims to provide fast, cheap, accurate, and deterministic outcomes to common code in GenAI. 
We'll be using a Test-Driven Development approach to building this toolset.

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
