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
Only summary module for the Elevate app.

This module provides the OnlySummary class, which is responsible for
generating TL;DR summaries and converting them into GitHub Flavored Markdown
(GFM) using the litellm library and the GPT-4o language model. The class
offers a method to summarize input text and return the summary in a
Markdown format, suitable for GitHub rendering.
"""

import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class SummaryConfig(BaseModel):
    """Configuration for OnlySummary class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class SummaryInput(BaseModel):
    """Input model for summary generation."""

    input_text: str = Field(..., description="Input text to summarize")
    summary_type: str = Field(default="generic", description="Type of summary to generate")


class SummaryOutput(BaseModel):
    """Output model for summary generation."""

    summary: str = Field(..., description="Generated summary in Markdown format")


class OnlySummary:
    """Class that only returns summary in Markdown syntax."""

    def __init__(self, config: SummaryConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlySummary class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = SummaryConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Makes the LLM call using litellm, extracting the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        # Fix: Use response.content if choices/message is not available
        output = str(response.choices[0].message.content)
        pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            return match.group(1).strip()
        return output

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_summarization_system_prompt(self, summary_type: str) -> str:
        """Return a system prompt to summarize and convert input text into Markdown syntax."""
        template = self._load_prompt_template()
        return str(template.render(summary_type=summary_type))

    async def summarize_and_convert_to_markdown(self, input_data: SummaryInput) -> SummaryOutput:
        """Summarizes and Converts the given input text to GitHub Flavored Markdown (GFM) format."""
        system_prompt = self.get_summarization_system_prompt(input_data.summary_type)
        summary = await self.make_llm_call(system_prompt, input_data.input_text)
        return SummaryOutput(summary=summary)
