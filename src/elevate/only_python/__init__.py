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

"""Only Python module for the Elevate app."""

import json
import logging
import os
import re
import tempfile
from pathlib import Path

import aiofiles  # type: ignore
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
    """Input model for Python code generation."""

    message: str = Field(..., description="Message/prompt for code generation")
    framework: str = Field(default="", description="Framework to use")
    jsonify: bool = Field(default=True, description="Whether to return JSON output")
    plot_graph: bool = Field(default=False, description="Whether to generate graphs")
    genai_snippet_code: str = Field(default="", description="Existing code snippet")


class PythonOutput(BaseModel):
    """Output model for Python code generation."""

    result: str = Field(..., description="Generated code execution result")


class OnlyPython:
    """Class that returns rephrased text."""

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

    def get_python_code_generation_system_prompt(self) -> str:
        """
        Returns the code generation system prompt.

        Returns
        -------
            str: A string containing the code generation system prompt.
        """
        template = self._load_prompt_template()
        return str(template.render(prompt_type="code_generation"))

    def get_json_conversion_prompt(self) -> str:
        """
        Returns the JSON conversion system prompt.

        Returns
        -------
            str: A string containing the JSON conversion system prompt.
        """
        template = self._load_prompt_template()
        return str(template.render(prompt_type="json_conversion"))

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm, extracting the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        output = str(response.choices[0].message.content)
        pattern = r"```python\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)
        if match:
            return match.group(1).strip()
        pattern = r"```json\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)
        if match:
            return match.group(1).strip()
        return output

    def print_sandbox_status(self, message: str, use_existing: bool = True) -> None:
        """Print a status message inside a formatted box."""
        padding = 4
        message_with_color = f"\033[91m*\033[0m {message}"
        box_width = len(message) + padding
        border_top_bottom = "┌" + "─" * (box_width + 2) + "┐"
        border_middle = f"│  {message_with_color}  │"
        logger.debug(border_top_bottom)
        logger.debug(border_middle)
        logger.debug(border_top_bottom)

    async def execute_code_using_e2b_sandbox(self, python_code: str, pip_installs: str, plot_graph: bool) -> str:
        """Execute the given Python code in an E2B async sandbox environment."""
        sandbox = None
        temp_file_path = None
        try:
            sandbox = await AsyncSandbox.create(envs=dict(os.environ))
            if pip_installs:
                # Handle case where pip_installs already contains "pip install"
                if pip_installs.strip().startswith("pip install"):
                    pip_command = pip_installs.strip()
                else:
                    pip_command = f"pip install {pip_installs}"
                pip_result = await sandbox.commands.run(pip_command)
                pip_stderr = pip_result.stderr if hasattr(pip_result, "stderr") and pip_result.stderr else ""
                pip_exit_code = pip_result.exit_code if hasattr(pip_result, "exit_code") else 0
                # Only treat stderr as error if the command actually failed (non-zero exit code)
                if pip_stderr and pip_exit_code != 0:
                    return f"Error during pip install: {pip_stderr}"
            # Use a secure temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
                temp_file_path = tmp_file.name
                tmp_file.write(python_code.encode())
            await sandbox.files.write(temp_file_path, python_code)
            exec_result = await sandbox.commands.run(f"python {temp_file_path}")
            stderr = exec_result.stderr if hasattr(exec_result, "stderr") and exec_result.stderr else ""
            stdout = exec_result.stdout if hasattr(exec_result, "stdout") and exec_result.stdout else ""
            if stderr:
                return f"Error during code execution: {stderr}"
            if plot_graph:
                try:
                    chart_bytes = await sandbox.files.read("chart.png")
                    async with aiofiles.open(Path("chart.png"), "wb") as f:
                        if isinstance(chart_bytes, str):
                            await f.write(chart_bytes.encode())
                        else:
                            await f.write(chart_bytes)
                except Exception:
                    logger.exception("Error saving chart.png")
                else:
                    return "Chart saved as chart.png"
            if stdout:
                return str(stdout)
            return str(exec_result)
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

    async def create_json_reponse(self, generated_output: str) -> str:
        system_prompt = self.get_json_conversion_prompt()
        return await self.make_llm_call(system_prompt, generated_output)

    def print_section_header(self, title: str) -> None:
        """Print a formatted section header."""
        logger.debug("%s", f"\n{'*' * 20} {title} {'*' * 20}\n")

    async def generate_code(self, input_data: PythonInput) -> PythonOutput:
        """
        Generate code for user given prompt with the specified field and framework.

        Args:
        ----
            input_data: Input containing code generation parameters.

        Returns:
        -------
            PythonOutput: The generated python code execution result.
        """
        system_prompt = self.get_python_code_generation_system_prompt()

        message = "\n<Prompt>" + input_data.message + "</Prompt>\n\n"
        if input_data.framework:
            message += "<Framework> " + input_data.framework + " </Framework>"
        if input_data.genai_snippet_code:
            message += "<Code>" + input_data.genai_snippet_code + " </Code>"
        if input_data.jsonify:
            message += "\n<OutputFormat>json</OutputFormat>"
        else:
            message += "\n<OutputFormat>str</OutputFormat>"

        self.print_section_header("Generating Python Code")
        logger.debug("Generating the python code...")
        code = await self.make_llm_call(system_prompt, message)
        logger.debug("\nGenerated Code + Installs:\n\n%s", code)
        if "<PipInstalls>" in code:
            pip_installs = code[code.index("<PipInstalls>") + len("<PipInstalls>") : code.index("</PipInstalls>")]
        else:
            pip_installs = ""
        python_code = code[code.index("<CodeCompletion>") + len("<CodeCompletion>") : code.index("</CodeCompletion>")]
        python_imports = code[code.index("<Imports>") + len("<Imports>") : code.index("</Imports>")]
        pip_installs = pip_installs.strip()
        python_code = python_code.strip()
        python_imports = python_imports.strip()
        self.print_section_header("End of Generated Code")

        self.print_section_header("Generated Code")
        full_code = "\n\n".join(
            [
                "# -" * 40,
                "# Generated imports",
                python_imports,
                "# -" * 40,
                "# Original code.",
                input_data.genai_snippet_code,
                "# -" * 40,
                "# Generated Completion",
                python_code,
            ]
        )
        logger.debug("%s", "-" * 40)
        logger.debug("Full code with imports and pip installs:\n")
        logger.debug("%s", "-" * 40)
        logger.debug(pip_installs)
        logger.debug("%s", "-" * 40)
        logger.debug(full_code)
        logger.debug("%s", "-" * 40)

        self.print_section_header("Executing Generated Code")
        generated_code_output = await self.execute_code_using_e2b_sandbox(
            full_code, pip_installs, input_data.plot_graph
        )
        generated_code_output = generated_code_output.strip()
        logger.debug("\nOutput of Execution:\n")
        logger.debug(generated_code_output)

        self.print_section_header("End of Execution")
        if input_data.jsonify:
            generated_code_output = json.loads(generated_code_output)

        return PythonOutput(result=str(generated_code_output))
