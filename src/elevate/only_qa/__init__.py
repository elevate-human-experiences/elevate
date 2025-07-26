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
Only QA module for the Elevate app.

This module provides the OnlyQA class, which is responsible for
answering questions based on product documentation using
the litellm library and the large language model.
"""

from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class QAConfig(BaseModel):
    """Configuration for OnlyQA class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class QAInput(BaseModel):
    """Input model for Q&A generation."""

    input_text: str = Field(..., description="Input text to generate answers from")


class QAOutput(BaseModel):
    """Output model for Q&A generation."""

    answers: str = Field(..., description="Generated answers")


class OnlyQA:
    """Class that only returns answers based on product documentation."""

    def __init__(self, config: QAConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyQA class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = QAConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Makes the LLM call using litellm, extracting the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        # Fix: Use response.content if choices/message is not available
        return str(response.choices[0].message.content)

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_qa_system_prompt(self) -> str:
        """Return a system prompt to generate answers from the input text."""
        template = self._load_prompt_template()
        return str(template.render())

    async def generate_answers(self, input_data: QAInput) -> QAOutput:
        """Generate answers from the given input."""
        system_prompt = self.get_qa_system_prompt()
        answers = await self.make_llm_call(system_prompt, input_data.input_text)
        return QAOutput(answers=answers)
