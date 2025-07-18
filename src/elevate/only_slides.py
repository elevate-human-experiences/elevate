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
Only sldies module for the Elevate app.

This module provides the OnlySlides class, which is responsible for
generating presentation slides converting them into Markdown
using the litellm library and the large language model.
"""

import re

from litellm import acompletion


class OnlySlides:
    """Class that only returns slides in Markdown syntax."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlySlides class"""
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

    def get_slide_generation_system_prompt(self, type_of_slides: str, number_of_slides: int) -> str:
        """Return a system prompt to generate slide content from the input text into Markdown syntax."""
        return f"""ROLE:
Create a compelling product pitch deck from provided technical documentation. As an AI presentation specialist, you will receive:

Product Technical Documentation
Slide Type: {type_of_slides}
Number of Slides: {number_of_slides}
Based on this input, generate a {number_of_slides}-slide product pitch deck in Markdown format. The deck should be tailored to the {type_of_slides}. Prioritize clear communication and a visually appealing structure (considering Markdown limitations). Focus on delivering concise and well-organized slide content.
"""

    async def generate_slides(self, input_text: str, type_of_slides: str, number_of_slides: int) -> str:
        """Generate slides from the given input."""
        system_prompt = self.get_slide_generation_system_prompt(
            type_of_slides, number_of_slides
        )  # Get the system prompt
        return await self.make_llm_call(system_prompt, input_text)
