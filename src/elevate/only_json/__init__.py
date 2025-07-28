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

"""OnlyJson class for JSON schema validation using litellm."""

from pathlib import Path
from typing import Any

import litellm
from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class JsonConfig(BaseModel):
    """Configuration for OnlyJson class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class JsonInput(BaseModel):
    """User-friendly input for extracting structured data."""

    model_config = {"arbitrary_types_allowed": True}

    text: str = Field(..., description="The text, message, or content you want to analyze")
    purpose: str | None = Field(
        default=None,
        description="Why are you extracting this data? (e.g., 'for a presentation', 'to organize my notes')",
    )
    context: str | None = Field(
        default=None, description="Additional context about your situation or the source of this text"
    )
    schema: Any = Field(..., description="The data structure you want to extract (Pydantic model)")
    custom_instructions: str | None = Field(
        default=None, description="Any special instructions for how to process your text"
    )


class JsonOutput(BaseModel):
    """Enhanced output with user-valuable insights beyond just the extracted data."""

    model_config = {"arbitrary_types_allowed": True}

    data: Any = Field(..., description="The extracted structured data matching your requested schema")
    key_insights: list[str] = Field(
        default_factory=list, description="Important patterns or insights discovered in your text"
    )
    summary: str | None = Field(None, description="Brief summary of what was found and extracted")
    next_steps: list[str] = Field(
        default_factory=list, description="Suggested actions you might take with this extracted data"
    )
    confidence_notes: str | None = Field(None, description="Any notes about the extraction quality or potential issues")


class OnlyJson:
    """
    Transform unstructured text into organized, actionable data with insights.

    Perfect for:
    • Extracting contact information from emails or business cards
    • Organizing meeting notes into structured action items
    • Converting research notes into categorized insights
    • Structuring customer feedback into analyzable data
    • Parsing invoices or receipts into expense tracking format
    • Transforming social media posts into sentiment analysis data
    """

    def __init__(self, config: JsonConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize your data extraction assistant."""
        if config:
            self.config = config
        else:
            self.config = JsonConfig(model=with_model)
        # Not all models support JSON schema validation,
        # so we need to do it on the client side.
        litellm.enable_json_schema_validation = True

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        template_content = template_path.read_text(encoding="utf-8")
        return Template(template_content)

    def get_system_prompt(
        self, schema_name: str = "default", purpose: str | None = None, context: str | None = None
    ) -> str:
        """Generate a user-focused system prompt with context."""
        template = self._load_prompt_template()
        return str(
            template.render(
                schema_name=schema_name,
                purpose=purpose or "organizing and understanding your data",
                context=context or "general text processing",
            )
        )

    async def parse(self, input_data: JsonInput) -> JsonOutput:
        """Extract structured data with valuable insights from your text."""
        # Generate context-aware system prompt
        system_prompt = input_data.custom_instructions or self.get_system_prompt(
            input_data.schema.__name__, input_data.purpose, input_data.context
        )

        # Prepare user message with context
        user_message = input_data.text
        if input_data.purpose:
            user_message = f"Purpose: {input_data.purpose}\n\n{user_message}"
        if input_data.context:
            user_message = f"Context: {input_data.context}\n\n{user_message}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        # Create enhanced output schema that includes the user's data schema
        class DynamicJsonOutput(JsonOutput):
            data: Any = Field(..., description="The extracted structured data matching your requested schema")

        # Rebuild the enhanced model and get the JSON schema
        DynamicJsonOutput.model_rebuild()
        s = DynamicJsonOutput.model_json_schema()
        s["type"] = "object"
        json_schema = {
            "type": "json_schema",
            "json_schema": {"name": "EnhancedOutput", "schema": s},
        }

        resp = await acompletion(
            model=self.config.model, messages=messages, response_format=json_schema, temperature=self.config.temperature
        )
        return DynamicJsonOutput.model_validate_json(resp.choices[0].message.content)
