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
"""OnlyEmail class for generating emails using LLMs."""

import logging
from pathlib import Path

import litellm
from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel

from common import setup_logging


logger = setup_logging(logging.INFO)


class Email(BaseModel):
    """Pydantic model representing a structured email."""

    subject: str
    salutation: str
    body: str
    closing: str
    signature: str


class OnlyEmail:
    """Class that returns well formatted emails."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyEmail class"""
        self.model = with_model
        # Enable JSON schema validation for structured output
        litellm.enable_json_schema_validation = True

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(api_key="", model=self.model, messages=messages, temperature=0.1)
        content = response.choices[0].message.content
        return str(content) if content else ""

    async def generate_structured_email(self, message: str, email_type: str) -> Email:
        """Generate a structured email using JSON schema validation."""
        system_prompt = self.get_email_prompt(email_type)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
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
            model=self.model,
            messages=messages,
            response_format=json_schema,
            temperature=0.1,
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("No content received from LLM response")

        return Email.model_validate_json(content)

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

    async def generate_email(self, message: str, email_type: str) -> str:
        """Generate an email of the specified type using an LLM."""
        try:
            system_prompt = self.get_email_prompt(email_type)
            return await self.make_llm_call(system_prompt, message)
        except ValueError as ve:
            logger.debug(f"ValueError: {ve}")
            return "Error: Invalid email type specified."
        except Exception as e:
            logger.debug(f"An error occurred: {e}")
            return "Error: An unexpected error occurred while generating the email."
