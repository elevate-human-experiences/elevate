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
Only demo script module for the Elevate app.

This module provides the OnlyDemoScript class, which is responsible for
generating prodcut demo script it to Markdown
using the litellm library and the large language model.
"""

import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class DemoScriptConfig(BaseModel):
    """Configuration for OnlyDemoScript class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class DemoScriptInput(BaseModel):
    """Input model for demo script generation."""

    input_text: str = Field(..., description="Input text to generate demo script from")
    presentation_type: str = Field(..., description="Type of presentation")
    demo_length_in_minutes: int = Field(..., description="Length of demo in minutes")


class DemoScriptOutput(BaseModel):
    """Output model for demo script generation."""

    demo_script: str = Field(..., description="Generated demo script in Markdown format")


class OnlyDemoScript:
    """Class that only returns demo script in Markdown syntax."""

    def __init__(self, config: DemoScriptConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyDemoScript class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = DemoScriptConfig(model=with_model)

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

    def get_demo_script_generation_system_prompt(self, presentation_type: str, demo_length_in_minutes: int) -> str:
        """Return a system prompt to generate demo script content from the input text into Markdown syntax."""
        template = self._load_prompt_template()
        return str(template.render(presentation_type=presentation_type, demo_length_in_minutes=demo_length_in_minutes))

    async def generate_demo_script(self, input_data: DemoScriptInput) -> DemoScriptOutput:
        """Generate demo script from the given input."""
        system_prompt = self.get_demo_script_generation_system_prompt(
            input_data.presentation_type, input_data.demo_length_in_minutes
        )
        demo_script = await self.make_llm_call(system_prompt, input_data.input_text)
        return DemoScriptOutput(demo_script=demo_script)
