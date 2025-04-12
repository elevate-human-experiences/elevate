import re

from dotenv import load_dotenv
from litellm import completion

# Load environment variables
load_dotenv()


class OnlySummary:
    """Class that only returns summary in Markdown syntax."""

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

    def get_summarization_system_prompt(self) -> str:
        """
        Return a system prompt to summarize and convert input text into Markdown syntax.
        """
        prompt_content = """ROLE:
You are a highly skilled Markdown converter, specializing in transforming plain text into clean and accurate GitHub Flavored Markdown (GFM). You are also proficient at creating TL;DR summaries. Your task is to summarize the input text in TL;DR format *and* convert that summary into Markdown.

**Tasks:**

1.  **TL;DR Summary:** Create a concise "TL;DR" (Too Long; Didn't Read) summary of the input text.
2.  **Markdown Conversion (of the TL;DR):** Convert *only the TL;DR summary* into GitHub Flavored Markdown.

**Instructions:**

1.  **Input:** You will receive a string of plain text as input.
2.  **Process:**
    *   Generate the TL;DR summary of the input text.
    *   Convert the TL;DR summary *itself* into Markdown.
3.  **Output:** Return ONLY the converted Markdown of the TL;DR summary. Do NOT include the original text or any other content.
4.  **TL;DR Style:** The TL;DR should be concise, typically a few sentences, and convey the most important points of the original text.
5.  **GitHub Flavored Markdown (GFM) Specifics:** Adhere to GFM conventions:
    *   Using fenced code blocks with syntax highlighting (e.g., ```python) if appropriate for the summary.
    *   Using lists (ordered or unordered) if the summary benefits from them.
    *   Using emphasis (bold, italics) where needed.
6.  **Accuracy:** Ensure the TL;DR summary is accurate and the resulting Markdown is correct and renders as intended in a GitHub environment.
7.  **Conciseness:** Strive for the most concise and efficient representation.
8.  **No Additional Information:**  Do NOT add any extra text, comments, or explanations. Only return the Markdown output of the TL;DR summary."""
        return prompt_content

    def summarize_and_convert_to_markdown(self, input_text: str) -> str:
        """
        Summarizes and Converts the given input text to GitHub Flavored Markdown (GFM) format.

        This method retrieves the system prompt specifically designed to summarize and markdown conversion,
        then uses it to make an LLM call to convert the input text.

        Args:
            input_text: The plain text to be converted to Markdown (string).

        Returns:
            The converted Markdown text (string).
        """
        system_prompt = self.get_summarization_system_prompt()  # Get the system prompt
        return self.make_llm_call(system_prompt, input_text)
