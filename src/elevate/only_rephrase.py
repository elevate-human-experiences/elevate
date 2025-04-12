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

from elevate.only_rephrase_prompt import REPHRASE_PROMPT


class OnlyRephrase:
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
        return output

    def get_rephrase_system_prompt(self) -> str:
        """Returns the rephrase system prompt.

        Returns:
            str: A string containing the rephrase system prompt.
        """
        return REPHRASE_PROMPT

    def rephrase_text(self, message: str, tone: str, length: str) -> str:
        """Rephrases the given message with the specified tone and length.

        Args:
            message (str): The message to rephrase.
            tone (str): The desired tone for the rephrased message.
            length (str): The desired length for the rephrased message.

        Returns:
            str: The rephrased message.
        """
        system_prompt = self.get_rephrase_system_prompt()

        message = "\n<Message>" + message + "</Message>\n\n"
        message += "<Tone> " + tone + " </Tone>\n\n"
        message += "<Length> " + length + " </Length>"

        return self.make_llm_call(system_prompt, message)
