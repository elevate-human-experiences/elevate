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
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field

from common import setup_logging


logger = setup_logging(logging.INFO)


class MarkdownConfig(BaseModel):
    """Configuration for OnlyMarkdown class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class MarkdownInput(BaseModel):
    """Input model for markdown conversion."""

    input_text: str = Field(..., description="Input text to convert to Markdown")


class MarkdownOutput(BaseModel):
    """Output model for markdown conversion."""

    markdown: str = Field(..., description="Converted text in Markdown format")


class OnlyMarkdown:
    """Class that only supports Markdown syntax."""

    def __init__(self, config: MarkdownConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyMarkdown class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = MarkdownConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]

        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        # Fix: Use response.content if choices/message is not available
        output = str(getattr(response, "content", response))
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

    def get_conversion_system_prompt(self) -> str:
        """Return a system prompt to convert input text into Markdown syntax."""
        template = self._load_prompt_template()
        return str(template.render())

    async def convert_to_markdown(self, input_data: MarkdownInput) -> MarkdownOutput:
        """Convert the given input text to GitHub Flavored Markdown (GFM) format."""
        system_prompt = self.get_conversion_system_prompt()
        markdown = await self.make_llm_call(system_prompt, input_data.input_text)
        return MarkdownOutput(markdown=markdown)

    async def summarize_and_convert_to_markdown(self, input_data: MarkdownInput) -> MarkdownOutput:
        """Summarize and convert the given input text to GitHub Flavored Markdown (GFM) format."""
        system_prompt = self.get_conversion_system_prompt()
        markdown = await self.make_llm_call(system_prompt, input_data.input_text)
        return MarkdownOutput(markdown=markdown)

    def print_section_header(self, title: str) -> None:
        """Print a formatted section header."""
        logger.debug("%s", f"\n{'*' * 20} {title} {'*' * 20}\n")
