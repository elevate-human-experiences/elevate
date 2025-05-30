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
"""Only rephrase module for the Elevate app."""

from litellm import completion


class OnlyShell:
    """Class that returns a shell command based on users prompt."""

    def __init__(self, with_model: str = "gemini/gemini-2.0-flash-lite") -> None:
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

        response = completion(
            api_key="", model=self.model, messages=messages, temperature=0.1
        )
        output = str(response.choices[0].message.content)
        return output

    def get_shell_system_prompt(self) -> str:
        """Returns the shell system prompt.

        Returns:
            str: A string containing the shell system prompt.
        """
        rephrase_prompt = """
You are an expert shell command generator. Your task is to translate user requests into precise and efficient shell commands.

*   **Input:** User's description of a task (e.g., "List all files in the current directory").
*   **Output:** A single, executable shell command that accomplishes the task.  Do not include any introductory text, explanations, or apologies.  Focus solely on the command itself.  Assume a Linux/Unix environment.  Prioritize common and portable commands.  If the task is ambiguous, ask the user for clarification.
"""
        return rephrase_prompt

    def generate_shell_command(self, user_prompt: str) -> str:
        """
        Generates a shell command based on a user-provided natural language prompt.

        This function takes a user prompt describing the desired shell command, combines it with a
        predefined system prompt that guides the language model's response, and then invokes the
        language model to generate the actual shell command.

        Args:
            user_prompt: A string containing the natural language description of the desired
                shell command.  For example, "List all files in the current directory."

        Returns:
            A string containing the generated shell command. The command is the output of the
            language model, intended to fulfill the user's request.
        """
        system_prompt = self.get_shell_system_prompt()

        message = "\n<UserPrompt>" + user_prompt + "</UserPrompt>\n\n"

        return self.make_llm_call(system_prompt, message)
