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
Only slides module for the Elevate app.

This module provides the OnlySlides class, which is responsible for
generating presentation slides converting them into Markdown
using the litellm library and the large language model.
"""

import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class SlidesConfig(BaseModel):
    """Configuration for OnlySlides class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class SlidesInput(BaseModel):
    """Input model for slides generation."""

    input_text: str = Field(..., description="Input text to generate slides from")
    type_of_slides: str = Field(..., description="Type of slides to generate")
    number_of_slides: int = Field(..., description="Number of slides to generate")


class SlidesOutput(BaseModel):
    """Output model for slides generation."""

    slides: str = Field(..., description="Generated slides in Markdown format")


class OnlySlides:
    """Class that only returns slides in Markdown syntax."""

    def __init__(self, config: SlidesConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlySlides class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = SlidesConfig(model=with_model)

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

    def get_slide_generation_system_prompt(self, type_of_slides: str, number_of_slides: int) -> str:
        """Return a system prompt to generate slide content from the input text into Markdown syntax."""
        template = self._load_prompt_template()
        return str(template.render(type_of_slides=type_of_slides, number_of_slides=number_of_slides))

    async def generate_slides(self, input_data: SlidesInput) -> SlidesOutput:
        """Generate slides from the given input."""
        system_prompt = self.get_slide_generation_system_prompt(input_data.type_of_slides, input_data.number_of_slides)
        slides = await self.make_llm_call(system_prompt, input_data.input_text)
        return SlidesOutput(slides=slides)
