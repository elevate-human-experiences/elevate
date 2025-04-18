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

import re

from litellm import completion
from e2b_code_interpreter import Sandbox

from elevate.only_python_prompt import PYTHON_CODE_GENRATION_PROMPT


class OnlyPython:
    """Class that returns rephrased text."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyMarkdown class"""
        self.model = with_model

    def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """
        Makes the LLM call using litellm, extracting the markdown content.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]

        response = completion(model=self.model, messages=messages, temperature=0.1)
        output = str(response.choices[0].message.content)
        pattern = r"```python\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            return match.group(1).strip()
        return output

    def print_sandbox_status(self, message: str, use_existing: bool = True) -> None:
        """Prints a status message inside a formatted box."""
        padding = 4
        message_with_color = f"\033[91m*\033[0m {message}"  # Add color consistently
        box_width = len(message) + padding
        border_top_bottom = "┌" + "─" * (box_width + 2) + "┐"
        border_middle = "│  " + message_with_color + "  │"

        print(border_top_bottom)
        print(border_middle)
        print(border_top_bottom)

    def execute_code_using_e2b_sandbox(self, python_code: str) -> str:
        """
        Executes the given Python code in an E2B sandbox environment.
        Reuses an existing sandbox if available, otherwise creates a new one.
        """
        # Attempt to get a running sandbox
        running_sandboxes = Sandbox.list()
        sandbox = None
        print()
        if running_sandboxes:
            self.print_sandbox_status("Sandbox found. Running code in it")
            sandbox = Sandbox.connect(running_sandboxes[0].sandbox_id)
        else:
            self.print_sandbox_status("No running sandboxes found. Creating a new one")
            sandbox = Sandbox()  # Default lifetime is 5 minutes

        try:
            print()
            execution = sandbox.run_code(python_code)
            return str(execution.logs)
        except Exception as e:
            return f"Error during code execution: {e}"

    def get_python_code_generation_system_prompt(self) -> str:
        """Returns the code generation system prompt.

        Returns:
            str: A string containing the code generation system prompt.
        """
        return PYTHON_CODE_GENRATION_PROMPT

    def generate_code(self, message: str, framework: str) -> str:
        """Generate code for user given prompt with the specified field and framework.

        Args:
            message (str): The message to rephrase.

        Returns:
            str: The generated python code.
        """
        system_prompt = self.get_python_code_generation_system_prompt()

        message = "\n<Prompt>" + message + "</Prompt>\n\n"
        message += "<Framework> " + framework + " </Framework>"

        python_code = self.make_llm_call(system_prompt, message)
        print("\nPython code:\n", python_code)
        return self.execute_code_using_e2b_sandbox(python_code)
