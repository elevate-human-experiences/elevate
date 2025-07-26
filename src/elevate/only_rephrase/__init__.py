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
from pydantic import BaseModel, Field


class RephraseConfig(BaseModel):
    """Configuration for OnlyRephrase class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class RephraseInput(BaseModel):
    """Input model for text rephrasing."""

    message: str = Field(..., description="Message to rephrase")
    tone: str = Field(..., description="Desired tone for the rephrased message")
    length: str = Field(..., description="Desired length for the rephrased message")


class RephraseOutput(BaseModel):
    """Output model for text rephrasing."""

    rephrased_text: str = Field(..., description="Rephrased message")


class OnlyRephrase:
    """Class that returns rephrased text."""

    def __init__(self, config: RephraseConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyRephrase class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = RephraseConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(
            api_key="", model=self.config.model, messages=messages, temperature=self.config.temperature
        )
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

    async def rephrase_text(self, input_data: RephraseInput) -> RephraseOutput:
        """
        Rephrases the given message with the specified tone and length.

        Args:
        ----
            input_data: Input containing message, tone, and length parameters.

        Returns:
        -------
            RephraseOutput: The rephrased message.
        """
        system_prompt = self.get_rephrase_system_prompt()

        message = "\n<Message>" + input_data.message + "</Message>\n\n"
        message += "<Tone> " + input_data.tone + " </Tone>\n\n"
        message += "<Length> " + input_data.length + " </Length>"

        rephrased_text = await self.make_llm_call(system_prompt, message)
        return RephraseOutput(rephrased_text=rephrased_text)
