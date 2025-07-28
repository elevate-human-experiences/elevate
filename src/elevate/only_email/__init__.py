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
"""AI-powered email assistant for crafting professional, personal, and marketing emails with insights."""

import logging
from pathlib import Path

import litellm
from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field

from common import setup_logging


logger = setup_logging(logging.INFO)


class EmailConfig(BaseModel):
    """Configuration for OnlyEmail class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class EmailInput(BaseModel):
    """User-friendly input for email generation."""

    purpose: str = Field(
        ...,
        description="What you want to communicate (e.g., 'Ask for time off', 'Thank a colleague', 'Invite friends to party')",
    )
    recipient: str = Field(..., description="Who you're writing to (e.g., 'my boss', 'my team', 'close friends')")
    email_type: str = Field(..., description="Type of email: personal, professional, or marketing")
    context: str | None = Field(
        None, description="Additional context about your situation or relationship with the recipient"
    )
    tone: str | None = Field(
        None, description="Desired tone (e.g., 'friendly', 'formal', 'enthusiastic', 'apologetic')"
    )
    key_details: str | None = Field(
        None, description="Important details to include (dates, names, specific requests, etc.)"
    )


class Email(BaseModel):
    """Enhanced email model with user-valuable insights."""

    subject: str
    salutation: str
    body: str
    closing: str
    signature: str
    key_insights: list[str] = Field(default_factory=list, description="Key points and insights about this email")
    tone_analysis: str | None = Field(None, description="Analysis of the email's tone and appropriateness")
    next_steps: list[str] = Field(default_factory=list, description="Suggested follow-up actions or considerations")
    alternative_approaches: list[str] = Field(
        default_factory=list, description="Other ways you could approach this communication"
    )


class OnlyEmail:
    """
    AI-powered email assistant that crafts professional, personal, and marketing emails.

    Perfect for:
    • Writing professional emails to colleagues, bosses, or clients
    • Crafting personal messages for friends, family, or invitations
    • Creating marketing emails that drive engagement and conversions
    • Getting unstuck when you know what to say but not how to say it
    • Ensuring your emails have the right tone for any situation
    • Learning better email communication through AI insights
    • Saving time while maintaining authenticity and professionalism
    """

    def __init__(self, config: EmailConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyEmail class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = EmailConfig(model=with_model)
        # Enable JSON schema validation for structured output
        litellm.enable_json_schema_validation = True

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(
            api_key="", model=self.config.model, messages=messages, temperature=self.config.temperature
        )
        content = response.choices[0].message.content
        return str(content) if content else ""

    async def generate_structured_email(self, input_data: EmailInput) -> Email:
        """Generate a structured email using JSON schema validation."""
        system_prompt = self.get_email_prompt(input_data.email_type)

        user_message = self._build_user_message(input_data)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        # Build the JSON schema for the Email model
        Email.model_rebuild()
        schema = Email.model_json_schema()
        schema["type"] = "object"
        json_schema = {
            "type": "json_schema",
            "json_schema": {"name": Email.__name__, "schema": schema},
        }

        response = await acompletion(
            model=self.config.model,
            messages=messages,
            response_format=json_schema,
            temperature=self.config.temperature,
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("No content received from LLM response")

        return Email.model_validate_json(content)

    def _build_user_message(self, input_data: EmailInput) -> str:
        """Build a comprehensive user message from the input data."""
        message_parts = [
            f"I need to write an email to {input_data.recipient}.",
            f"Purpose: {input_data.purpose}",
        ]

        if input_data.context:
            message_parts.append(f"Context: {input_data.context}")

        if input_data.tone:
            message_parts.append(f"Desired tone: {input_data.tone}")

        if input_data.key_details:
            message_parts.append(f"Important details to include: {input_data.key_details}")

        return "\n".join(message_parts)

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_email_prompt(self, email_type: str) -> str:
        """Return the appropriate email prompt based on the email type."""
        valid_types = ["personal", "professional", "marketing"]
        if email_type.lower() not in valid_types:
            raise ValueError("Invalid email type specified.")

        template = self._load_prompt_template()
        return str(template.render(email_type=email_type.lower()))

    async def generate_email(self, input_data: EmailInput) -> str:
        """Generate an email of the specified type using an LLM."""
        try:
            system_prompt = self.get_email_prompt(input_data.email_type)
            user_message = self._build_user_message(input_data)
            return await self.make_llm_call(system_prompt, user_message)
        except ValueError as ve:
            logger.debug(f"ValueError: {ve}")
            return "Error: Invalid email type specified."
        except Exception as e:
            logger.debug(f"An error occurred: {e}")
            return "Error: An unexpected error occurred while generating the email."
