"""Module to test the text summarization functionality of the OnlySummary class."""

from elevate.only_markdown import OnlyMarkdown

# Sample input text
input_text = """
Repo for Learning - A Repository for Exploration

This repository is designed to be a learning resource. It covers a variety of topics to help you expand your knowledge. This is a *great* place to start, and it's also **useful** for more experienced learners. You might even find some `inline code` examples!

```
def greet(name):
    print(f"Hello, {name}!")

greet("Learner")
```
See [link](https://www.wikipedia.org/) for more information.

> This is a block quote.
> It's used to highlight important information.

Project Structure:

|File/Directory | Description |

| README.txt     | This file.  |
| /examples      | Code examples. |

This is the end of the README.
"""


def test_simple_text_markdown_conversion() -> None:
    """
    Tests the conversion of simple text to Markdown format using the OnlyMarkdown class.

    The test does *not* include assertions; it focuses on generating output
    for manual inspection of the Markdown conversion.
    """
    content = input_text
    only_markdown = OnlyMarkdown(with_model="gemini/gemini-2.0-flash-lite")
    markdown_output = only_markdown.convert_to_markdown(content)
    print(markdown_output)


# test_simple_text_markdown_conversion()
