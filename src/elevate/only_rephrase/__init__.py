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

"""Communication coaching tool that helps people write better messages that connect with their audience and achieve their goals."""

from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class RephraseConfig(BaseModel):
    """Configuration for OnlyRephrase class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class RephraseInput(BaseModel):
    """Input model for text rephrasing with user-friendly fields."""

    original_text: str = Field(..., description="The text you want to rephrase")
    audience: str = Field(
        ..., description="Who you're writing for (e.g., 'my boss', 'team members', 'clients', 'friends')"
    )
    purpose: str = Field(
        ..., description="What you want to achieve (e.g., 'request time off', 'explain a delay', 'share good news')"
    )
    tone: str = Field(
        ..., description="How you want to sound (e.g., 'professional', 'friendly', 'apologetic', 'confident')"
    )
    format: str = Field(
        default="email", description="Type of communication (e.g., 'email', 'text message', 'presentation', 'letter')"
    )
    context: str = Field(default="", description="Any additional context about your situation (optional)")


class RephraseOutput(BaseModel):
    """Enhanced output model for text rephrasing with user-valuable insights."""

    rephrased_text: str = Field(..., description="Your improved message, ready to send")
    key_improvements: list[str] = Field(default_factory=list, description="What we improved in your message")
    tone_analysis: str = Field(default="", description="How your message comes across to the reader")
    alternative_versions: list[str] = Field(default_factory=list, description="Other ways to say the same thing")
    confidence_level: str = Field(default="high", description="How well this matches your intended purpose")


class OnlyRephrase:
    """
    Your personal communication coach - helps you write messages that get results.

    Perfect for:
    • Getting time off approved by your boss
    • Following up with clients without being pushy
    • Explaining delays or mistakes professionally
    • Making requests that people actually say yes to
    • Turning awkward messages into confident communication
    • Adapting your writing style for different audiences
    """

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
        Perfect for: Writing better emails, messages, and communications that connect with your audience.

        • Requesting time off from your boss
        • Following up with clients professionally
        • Apologizing for delays or mistakes
        • Sharing updates with your team
        • Making asks that get results

        Args:
        ----
            input_data: Your original text with context about audience and purpose.

        Returns:
        -------
            RephraseOutput: Enhanced message with improvements and alternatives.
        """
        system_prompt = self.get_rephrase_system_prompt()

        message = f"\n<OriginalText>{input_data.original_text}</OriginalText>\n\n"
        message += f"<Audience>{input_data.audience}</Audience>\n\n"
        message += f"<Purpose>{input_data.purpose}</Purpose>\n\n"
        message += f"<Tone>{input_data.tone}</Tone>\n\n"
        message += f"<Format>{input_data.format}</Format>\n\n"
        if input_data.context:
            message += f"<Context>{input_data.context}</Context>"

        rephrased_text = await self.make_llm_call(system_prompt, message)
        return RephraseOutput(rephrased_text=rephrased_text)
