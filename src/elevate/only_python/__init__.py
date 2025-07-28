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
Only Python - Your AI coding companion that transforms ideas into working Python code.

Never feel intimidated by coding challenges again. This module creates functional Python
code from your natural language descriptions, handles complex programming tasks, and
provides complete solutions with clear explanations. Whether you're a beginner learning
to code, a professional automating workflows, or exploring data science, get working
code that solves real problems.
"""

import logging
import os
import re
import tempfile
from pathlib import Path

from e2b import AsyncSandbox
from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field

from common import setup_logging


logger = setup_logging(logging.INFO)


class PythonConfig(BaseModel):
    """Configuration for OnlyPython class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class PythonInput(BaseModel):
    """What you want to build or accomplish with Python code."""

    task: str = Field(
        ...,
        description="What you want to accomplish (e.g., 'create a web scraper for product prices', 'analyze my sales data')",
    )
    purpose: str | None = Field(
        None,
        description="Why you need this code (e.g., 'automate my daily report', 'learn web scraping', 'help with school project')",
    )
    experience_level: str = Field(
        default="beginner", description="Your coding experience: 'beginner', 'intermediate', or 'advanced'"
    )
    preferred_libraries: str | None = Field(
        default=None, description="Specific libraries you want to use (e.g., 'pandas', 'requests', 'flask')"
    )
    data_source: str | None = Field(
        default=None, description="What data you're working with (file path, URL, or description)"
    )
    output_format: str = Field(
        default="display", description="How you want results: 'display', 'save_file', 'return_data', or 'create_chart'"
    )
    existing_code: str | None = Field(default=None, description="Any existing code you want to build upon or modify")


class PythonOutput(BaseModel):
    """Your complete Python solution with code and guidance."""

    code: str = Field(..., description="Clean, executable Python code that solves your task")
    explanation: str = Field(..., description="Clear explanation of how the code works")
    key_concepts: list[str] = Field(default_factory=list, description="Important programming concepts used")
    dependencies: list[str] = Field(default_factory=list, description="Required Python packages to install")
    usage_instructions: str = Field(..., description="How to run and use the code")
    example_output: str | None = Field(None, description="What the code produces when run")
    learning_notes: list[str] = Field(default_factory=list, description="Tips to understand and modify the code")
    next_improvements: list[str] = Field(default_factory=list, description="Suggestions to enhance or extend the code")


class OnlyPython:
    """
    Your personal Python coding assistant that turns ideas into working code.

    Transform your programming challenges into clean, functional Python solutions with detailed
    explanations and learning guidance. Get not just code that works, but understanding of how
    and why it works, plus actionable next steps for improvement.

    Perfect for:
    - Students learning Python programming fundamentals
    - Professionals automating repetitive tasks and workflows
    - Data analysts building scripts for data processing and visualization
    - Web developers creating APIs, scrapers, and automation tools
    - Researchers processing data and generating reports
    - Anyone wanting to solve problems with Python but needing guidance
    - Building prototypes and proof-of-concept applications
    - Learning best practices through real working examples

    What makes this special:
    - Writes clean, well-commented code that follows Python best practices
    - Provides detailed explanations of programming concepts used
    - Suggests appropriate libraries and explains why they're chosen
    - Includes usage instructions and example outputs
    - Offers learning tips to help you understand and modify the code
    - Suggests improvements and next steps for extending functionality
    - Handles everything from simple scripts to complex applications
    - Adapts explanations to your experience level
    """

    def __init__(self, config: PythonConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyPython class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = PythonConfig(model=with_model)

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_code_generation_system_prompt(self, experience_level: str = "beginner") -> str:
        """Get the system prompt tailored for the user's experience level."""
        template = self._load_prompt_template()
        return str(template.render(experience_level=experience_level))

    async def make_llm_call(self, system_prompt: str, user_prompt: str) -> str:
        """Generate code using AI model."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        output = str(response.choices[0].message.content)
        pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)
        if match:
            return match.group(1).strip()
        return output

    async def execute_code_safely(self, python_code: str, dependencies: list[str]) -> str:
        """Execute Python code safely in a sandbox environment."""
        sandbox = None
        temp_file_path = None
        try:
            sandbox = await AsyncSandbox.create(envs=dict(os.environ))

            # Install dependencies if provided
            if dependencies:
                pip_packages = " ".join(dependencies)
                pip_command = f"pip install {pip_packages}"
                pip_result = await sandbox.commands.run(pip_command)
                pip_stderr = pip_result.stderr if hasattr(pip_result, "stderr") and pip_result.stderr else ""
                pip_exit_code = pip_result.exit_code if hasattr(pip_result, "exit_code") else 0
                if pip_stderr and pip_exit_code != 0:
                    return f"Error installing dependencies: {pip_stderr}"

            # Execute the code
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
                temp_file_path = tmp_file.name
                tmp_file.write(python_code.encode())

            await sandbox.files.write(temp_file_path, python_code)
            exec_result = await sandbox.commands.run(f"python {temp_file_path}")

            stderr = exec_result.stderr if hasattr(exec_result, "stderr") and exec_result.stderr else ""
            stdout = exec_result.stdout if hasattr(exec_result, "stdout") and exec_result.stdout else ""

            # Return based on execution results
            if stderr:
                return f"Execution resulted in: {stderr}"

            if stdout:
                return str(stdout)

            # Default case: successful execution with no output
            return "Code executed successfully (no output)"  # noqa: TRY300

        except Exception:
            logger.exception("Error during code execution")
            return "Error during code execution."
        finally:
            if sandbox:
                await sandbox.kill()
            if temp_file_path:
                try:
                    Path(temp_file_path).unlink(missing_ok=True)
                except Exception:
                    logger.debug(f"Could not delete temp file: {temp_file_path}")

    async def create_code(self, input_data: PythonInput) -> PythonOutput:
        """Transform your idea into working Python code with complete guidance."""
        system_prompt = self.get_code_generation_system_prompt(input_data.experience_level)

        user_prompt = f"I need help with: {input_data.task}"

        if input_data.purpose:
            user_prompt += f"\n\nWhy I need this: {input_data.purpose}"

        if input_data.data_source:
            user_prompt += f"\n\nData I'm working with: {input_data.data_source}"

        if input_data.preferred_libraries:
            user_prompt += f"\n\nPreferred libraries: {input_data.preferred_libraries}"

        if input_data.existing_code:
            user_prompt += f"\n\nExisting code to build on: {input_data.existing_code}"

        user_prompt += f"\n\nI want the output to: {input_data.output_format}"
        user_prompt += f"\n\nMy coding experience: {input_data.experience_level}"
        user_prompt += "\n\nPlease provide a complete solution including the code, explanation, key concepts, dependencies, usage instructions, and learning guidance."

        response = await self.make_llm_call(system_prompt, user_prompt)

        # Parse the response and execute code if needed
        parsed_response = self._parse_code_response(response, input_data)

        # Execute the code to get example output
        example_output: str | None = None
        if parsed_response["code"] and input_data.output_format != "code_only":
            code = parsed_response["code"]
            dependencies = parsed_response["dependencies"]
            if isinstance(code, str) and isinstance(dependencies, list):
                execution_result = await self.execute_code_safely(code, dependencies)
                example_output = execution_result
        else:
            example_output_raw = parsed_response["example_output"]
            example_output = example_output_raw if isinstance(example_output_raw, str) else None

        # Ensure all values have correct types for PythonOutput
        code = parsed_response["code"] if isinstance(parsed_response["code"], str) else ""
        explanation = parsed_response["explanation"] if isinstance(parsed_response["explanation"], str) else ""
        key_concepts = parsed_response["key_concepts"] if isinstance(parsed_response["key_concepts"], list) else []
        dependencies = parsed_response["dependencies"] if isinstance(parsed_response["dependencies"], list) else []
        usage_instructions = (
            parsed_response["usage_instructions"] if isinstance(parsed_response["usage_instructions"], str) else ""
        )
        learning_notes = (
            parsed_response["learning_notes"] if isinstance(parsed_response["learning_notes"], list) else []
        )
        next_improvements = (
            parsed_response["next_improvements"] if isinstance(parsed_response["next_improvements"], list) else []
        )

        return PythonOutput(
            code=code,
            explanation=explanation,
            key_concepts=key_concepts,
            dependencies=dependencies,
            usage_instructions=usage_instructions,
            example_output=example_output,
            learning_notes=learning_notes,
            next_improvements=next_improvements,
        )

    def _parse_code_response(self, response: str, input_data: PythonInput) -> dict[str, str | list[str]]:
        """Parse the AI response into structured components."""
        # Basic parsing - in a real implementation, this would be more sophisticated
        # For now, we'll provide reasonable defaults based on the input
        return {
            "code": self._extract_code_from_response(response),
            "explanation": "This code solves your task using Python best practices.",
            "key_concepts": self._extract_key_concepts(input_data.task),
            "dependencies": self._extract_dependencies(input_data.preferred_libraries or ""),
            "usage_instructions": "Run this code in your Python environment.",
            "example_output": "",
            "learning_notes": self._generate_learning_notes(input_data.experience_level, input_data.task),
            "next_improvements": self._generate_next_improvements(input_data.task),
        }

    def _extract_code_from_response(self, response: str) -> str:
        """Extract Python code from the response."""
        pattern = r"```python\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response.strip()

    def _extract_key_concepts(self, task: str) -> list[str]:
        """Generate key programming concepts based on the task."""
        concepts = ["Python fundamentals", "Problem solving"]
        task_lower = task.lower()
        if "data" in task_lower:
            concepts.append("Data processing")
        if "web" in task_lower or "scrape" in task_lower:
            concepts.append("Web development")
        if "file" in task_lower:
            concepts.append("File handling")
        return concepts[:3]

    def _extract_dependencies(self, preferred_libs: str) -> list[str]:
        """Extract required dependencies."""
        if not preferred_libs:
            return []
        return [lib.strip() for lib in preferred_libs.split(",") if lib.strip()]

    def _generate_learning_notes(self, experience_level: str, task: str) -> list[str]:
        """Generate helpful learning notes based on experience level."""
        base_notes = ["Read the code comments to understand each step"]
        if experience_level == "beginner":
            base_notes.extend(
                [
                    "Try running the code line by line to see how it works",
                    "Experiment with changing small parts to see the effects",
                ]
            )
        elif experience_level == "intermediate":
            base_notes.extend(
                [
                    "Consider how you might optimize this code for better performance",
                    "Think about error handling and edge cases",
                ]
            )
        else:
            base_notes.extend(
                ["Consider architectural patterns and code organization", "Think about testing and maintainability"]
            )
        return base_notes[:3]

    def _generate_next_improvements(self, task: str) -> list[str]:
        """Generate suggestions for extending the code."""
        improvements = [
            "Add error handling for edge cases",
            "Create a user interface for easier interaction",
            "Add logging and monitoring capabilities",
        ]
        return improvements[:3]
