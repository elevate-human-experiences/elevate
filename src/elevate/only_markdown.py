import re

from dotenv import load_dotenv
from litellm import completion

# Load environment variables
load_dotenv()


class OnlyMarkdown:
    """Class that only supports Markdown syntax."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyMarkdown class"""
        self.model = with_model

    def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """
        Makes the LLM call using litellm, extracting the markdown content.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]

        response = completion(model=self.model, messages=messages, temperature=0.1)
        output = response.choices[0].message.content  # type: str
        pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            return match.group(1).strip()
        return output

    def get_conversion_system_prompt(self) -> str:
        """
        Return a system prompt to convert input text into Markdown syntax.
        """
        prompt_content = r"""ROLE:
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
        return prompt_content

    def convert_to_markdown(self, input_text: str) -> str:
        """
        Converts the given input text to GitHub Flavored Markdown (GFM) format.

        This method retrieves the system prompt specifically designed for markdown conversion,
        then uses it to make an LLM call to convert the input text.

        Args:
            input_text: The plain text to be converted to Markdown (string).

        Returns:
            The converted Markdown text (string).
        """
        system_prompt = self.get_conversion_system_prompt()  # Get the system prompt
        return self.make_llm_call(system_prompt, input_text)
