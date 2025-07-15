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
Only ELI5 module for the Elevate app.

This module provides the OnlyELI5 class, which is responsible for
generating simple explanations (Explain Like I'm 5) and converting them into
GitHub Flavored Markdown (GFM) using the litellm library and language models.
The class offers a method to simplify complex topics and return the explanation
in a Markdown format, suitable for easy understanding.
"""

import re

from litellm import acompletion


class OnlyELI5:
    """Class that only returns ELI5 explanations in Markdown syntax."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyELI5 class"""
        self.model = with_model

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Makes the LLM call using litellm, extracting the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(model=self.model, messages=messages, temperature=0.1)
        # Fix: Use response.content if choices/message is not available
        output = str(response.choices[0].message.content)
        pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            return match.group(1).strip()
        return output

    def get_eli5_system_prompt(self) -> str:
        """Return a system prompt to create ELI5 explanations in Markdown syntax."""
        return """ROLE:
You are an expert at explaining complex topics in simple terms that a 5-year-old could understand. You excel at using analogies, simple language, and relatable examples to make difficult concepts accessible.

**Task:**
Create an "Explain Like I'm 5" (ELI5) explanation of the given topic and format it in clean GitHub Flavored Markdown.

**Instructions:**
1. **Use Simple Language:** Use words and concepts that a young child would understand
2. **Use Analogies:** Compare complex concepts to familiar things (toys, animals, food, etc.)
3. **Be Visual:** Use descriptions that help create mental pictures
4. **Keep It Short:** Break down complex ideas into small, digestible pieces
5. **Make It Fun:** Use engaging examples and scenarios
6. **Markdown Format:** Structure your explanation using proper Markdown formatting

**Guidelines:**
- Start with "Imagine..." or "Think of it like..." to set up analogies
- Use simple sentences and avoid jargon
- Include bullet points or numbered lists for steps
- Use emojis sparingly to make it more engaging
- End with a simple summary that ties it all together

**Output Format:**
Return your response wrapped in markdown code blocks like this:
```markdown
# Your ELI5 Explanation Here
```
"""

    async def explain(self, input_text: str) -> str:
        """Generate an ELI5 explanation from the given input."""
        system_prompt = self.get_eli5_system_prompt()
        return await self.make_llm_call(system_prompt, input_text)
