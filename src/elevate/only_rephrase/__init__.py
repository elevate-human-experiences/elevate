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

from pathlib import Path

from jinja2 import Template
from litellm import acompletion


class OnlyRephrase:
    """Class that returns rephrased text."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyRephrase class"""
        self.model = with_model

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(api_key="", model=self.model, messages=messages, temperature=0.1)
        # Fix: Use response.content if choices/message is not available
        return str(getattr(response, "content", response))

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_rephrase_system_prompt(self) -> str:
        """Return the rephrase system prompt."""
        template = self._load_prompt_template()
        return str(template.render())

    async def rephrase_text(self, message: str, tone: str, length: str) -> str:
        """
        Rephrases the given message with the specified tone and length.

        Args:
        ----
            message (str): The message to rephrase.
            tone (str): The desired tone for the rephrased message.
            length (str): The desired length for the rephrased message.

        Returns:
        -------
            str: The rephrased message.
        """
        system_prompt = self.get_rephrase_system_prompt()

        message = "\n<Message>" + message + "</Message>\n\n"
        message += "<Tone> " + tone + " </Tone>\n\n"
        message += "<Length> " + length + " </Length>"

        return await self.make_llm_call(system_prompt, message)
