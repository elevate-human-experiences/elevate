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
"""Only shell module for the Elevate app."""

from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class ShellConfig(BaseModel):
    """Configuration for OnlyShell class."""

    model: str = Field(default="gemini/gemini-2.0-flash-lite", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class ShellInput(BaseModel):
    """Input model for shell command generation."""

    user_prompt: str = Field(..., description="Natural language prompt for shell command")


class ShellOutput(BaseModel):
    """Output model for shell command generation."""

    command: str = Field(..., description="Generated shell command")


class OnlyShell:
    """Class that returns a shell command based on users prompt."""

    def __init__(self, config: ShellConfig) -> None:
        """Initialize the OnlyShell class with Pydantic config."""
        self.config = config

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the shell command."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(
            api_key="", model=self.config.model, messages=messages, temperature=self.config.temperature
        )
        return str(response.choices[0].message.content)

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_shell_system_prompt(self) -> str:
        """Return the shell system prompt."""
        template = self._load_prompt_template()
        return str(template.render())

    async def generate_shell_command(self, input_data: ShellInput) -> ShellOutput:
        """Generates a shell command based on a user-provided natural language prompt."""
        system_prompt = self.get_shell_system_prompt()
        message = "\n<UserPrompt>" + input_data.user_prompt + "</UserPrompt>\n\n"
        command = await self.make_llm_call(system_prompt, message)
        return ShellOutput(command=command)
