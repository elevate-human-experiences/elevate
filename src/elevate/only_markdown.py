# MIT License
#
# Copyright (c) 2025 elevate-human-experiences
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
OnlyMarkdown class for converting text to Markdown format using litellm.

This module provides the OnlyMarkdown class, which is designed to convert
plain text into GitHub Flavored Markdown (GFM) using the litellm library.
The conversion process is guided by a set of predefined scenarios and a
system prompt that instructs the model on the desired Markdown output.
"""

import logging
import re

from litellm import acompletion

from common import setup_logging


logger = setup_logging(logging.INFO)


class OnlyMarkdown:
    """Class that only supports Markdown syntax."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyMarkdown class"""
        self.model = with_model

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]

        response = await acompletion(model=self.model, messages=messages, temperature=0.1)
        # Fix: Use response.content if choices/message is not available
        output = str(getattr(response, "content", response))
        pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            return match.group(1).strip()
        return output

    def get_conversion_system_prompt(self) -> str:
        """Return a system prompt to convert input text into Markdown syntax."""
        return r"""ROLE:
You are a highly skilled Markdown converter, specializing in transforming plain text into clean and accurate GitHub Flavored Markdown (GFM). Your sole purpose is to convert the provided input text into its equivalent Markdown representation.

**Task:**

Convert the given input text into GitHub Flavored Markdown.

**Instructions:**

1.  **Input:** You will receive a string of plain text as input.
2.  **Conversion:** Carefully analyze the input and apply the appropriate Markdown syntax to represent the text's structure, formatting, and content. This includes, but is not limited to:
    *   Headings (using `#`, `##`, `###`, etc.)
    *   Emphasis (using `*`, `_`, `**`, `__`)
    *   Lists (ordered and unordered)
    *   Links (using `[text](url)`)
    *   Images (using `![alt text](url)`)
    *   Code blocks (using backticks ``` or indentation)
    *   Inline code (using backticks ``)
    *   Blockquotes (using `>`)
    *   Tables (using pipes `|` and hyphens `-`)
    *   Horizontal rules (using `---` or `***`)

3.  **GitHub Flavored Markdown (GFM) Specifics:** Adhere to GFM conventions. This includes, but is not limited to:
    *   Using fenced code blocks with syntax highlighting (e.g., ```python)
    *   Using task lists (e.g., `- [x] Completed task`)
    *   Using tables with proper alignment.

4.  **Accuracy & Scenarios:** Ensure the Markdown syntax is correct and renders as intended in a GitHub environment. Demonstrate accuracy by correctly converting the following scenarios.

    *   **Scenario 1: Simple Paragraph with Emphasis**
        *   **Input:** `This is a simple paragraph. It contains *italicized* text and **bold** text. There's also some \`inline code\`.`
        *   **Expected Output:** `This is a simple paragraph. It contains *italicized* text and **bold** text. There's also some \`inline code\`.`

    *   **Scenario 2: Headings (Levels 1-3)**
        *   **Input:**
            ```
            Heading Level 1
            Heading Level 2
            Heading Level 3
            ```
        *   **Expected Output:**
            # Heading Level 1
            ## Heading Level 2
            ### Heading Level 3

    *   **Scenario 3: Unordered List with Nested Ordered List**
        *   **Input:**
            Item 1
                Sub-item A
                Sub-item B
            Item 2
        *   **Expected Output:**
            * Item 1
                1. Sub-item A
                2. Sub-item B
            * Item 2

    *   **Scenario 4: Link and Image**
        *   **Input:** See [Google](https://www.google.com) and ![My Image](https://example.com/image.png).
        *   **Expected Output:** See [Google](https://www.google.com) and ![My Image](https://example.com/image.png).

    *   **Scenario 5: Fenced Code Block with Language**
        *   **Input:**
            ```
            def hello_world():
                print("Hello, world!")
            ```
        *   **Expected Output:**
            ```<detected language>
            def hello_world():
                print("Hello, world!")
            ```

    *   **Scenario 6: Block Quote**
        *   **Input:**
            ```
            > This is a block quote.
            > It can span multiple lines.
            ```
        *   **Expected Output:**
            > This is a block quote.
            > It can span multiple lines.

    *   **Scenario 7: Simple Table**
        *   **Input:**
            ```
            Header 1 | Header 2 |
            Cell 1  |  Cell 2 |
            ```
        *   **Expected Output:**
            | Header 1 | Header 2 |
            | -------- | -------- |
            | Cell 1   | Cell 2   |

    *   **Scenario 8: Complex Document**
        *   **Input:**
            ```
            # My Document

            This is a paragraph with *emphasis*.

            ## Section 1

            * Item 1
            * Item 2

            See [example](https://example.com).

            ```python
            print("Hello")
            ```
            ```
        *   **Expected Output:**
            # My Document

            This is a paragraph with *emphasis*.

            ## Section 1

            * Item 1
            * Item 2

            See [example](https://example.com).

            ```python
            print("Hello")
            ```

5.  **Conciseness:** Strive for the most concise and efficient Markdown representation possible.
6.  **No Additional Information:** Do NOT add any extra text, comments, or explanations. Only return the Markdown output. The output should be a single string.
7.  **Output Format:** Important!!! Return ONLY the Markdown code, without any surrounding ```markdown blocks or other delimiters.
"""

    async def convert_to_markdown(self, input_text: str) -> str:
        """Convert the given input text to GitHub Flavored Markdown (GFM) format."""
        system_prompt = self.get_conversion_system_prompt()
        return await self.make_llm_call(system_prompt, input_text)

    async def summarize_and_convert_to_markdown(self, input_text: str) -> str:
        """Summarize and convert the given input text to GitHub Flavored Markdown (GFM) format."""
        system_prompt = self.get_conversion_system_prompt()
        return await self.make_llm_call(system_prompt, input_text)

    def print_section_header(self, title: str) -> None:
        """Print a formatted section header."""
        logger.debug("%s", f"\n{'*' * 20} {title} {'*' * 20}\n")
