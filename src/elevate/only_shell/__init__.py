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

    task_description: str = Field(..., description="What you want to accomplish (e.g., 'find all Python files')")
    context: str | None = Field(
        None, description="Your situation or purpose (e.g., 'preparing for deployment', 'debugging an issue')"
    )
    environment: str = Field(default="linux", description="Your operating system (linux, macos, windows)")
    skill_level: str = Field(
        default="intermediate", description="Your shell experience level (beginner, intermediate, advanced)"
    )


class ShellOutput(BaseModel):
    """Output model for shell command generation."""

    command: str = Field(..., description="The shell command to run")
    explanation: str = Field(..., description="Plain English explanation of what the command does")
    safety_notes: str | None = Field(None, description="Important warnings or precautions")
    example_output: str | None = Field(None, description="What you might expect to see when running this command")
    related_commands: list[str] = Field(default_factory=list, description="Other useful commands for similar tasks")
    next_steps: str | None = Field(None, description="What you might want to do after running this command")


class OnlyShell:
    """
    Your AI-powered shell command assistant that transforms everyday language into precise terminal commands.

    Perfect for:
    • System administrators managing servers and troubleshooting issues
    • Developers automating workflows and debugging build problems
    • Data scientists processing files and managing datasets
    • DevOps engineers handling deployments and monitoring systems
    • Anyone who knows what they want to do but needs the exact command syntax
    """

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
        """Generates a shell command with detailed explanation based on user's task description."""
        system_prompt = self.get_shell_system_prompt()

        # Build context-aware message
        message_parts = [f"<TaskDescription>{input_data.task_description}</TaskDescription>"]

        if input_data.context:
            message_parts.append(f"<Context>{input_data.context}</Context>")

        message_parts.extend(
            [
                f"<Environment>{input_data.environment}</Environment>",
                f"<SkillLevel>{input_data.skill_level}</SkillLevel>",
            ]
        )

        message = "\n".join(message_parts) + "\n\n"
        response = await self.make_llm_call(system_prompt, message)

        # Parse the structured response (assuming JSON format from the new prompt)
        import json

        try:
            # Handle JSON wrapped in code blocks
            if response.strip().startswith("```json"):
                # Extract JSON from code block
                start = response.find("{")
                end = response.rfind("}") + 1
                json_content = response[start:end]
            else:
                json_content = response

            parsed_response = json.loads(json_content)
            return ShellOutput(**parsed_response)
        except (json.JSONDecodeError, ValueError):
            # Fallback for backwards compatibility
            return ShellOutput(
                command=response,
                explanation="Generated shell command",
                safety_notes=None,
                example_output=None,
                related_commands=[],
                next_steps=None,
            )
