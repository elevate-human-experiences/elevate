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
    """Input model for JSON parsing."""

    model_config = {"arbitrary_types_allowed": True}

    content: str = Field(..., description="Content to parse")
    schema: Any = Field(..., description="Pydantic schema to use for parsing")
    system_prompt: str | None = Field(None, description="Optional system prompt override")


class OnlyJson:
    """Class that only supports JSON schema validation."""

    def __init__(self, config: JsonConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyJson class"""
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

    def get_system_prompt(self, schema_name: str = "default") -> str:
        """Return the appropriate system prompt based on the schema type."""
        template = self._load_prompt_template()
        return str(template.render(schema_name=schema_name))

    async def parse(self, input_data: JsonInput) -> Any:
        """Parse the content using the specified schema."""
        # If no system prompt provided, use the template system
        system_prompt = input_data.system_prompt or self.get_system_prompt(input_data.schema.__name__)

        # Updated messages with a system prompt for JSON schema validation
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_data.content},
        ]

        # Rebuild the model and get the JSON schema
        input_data.schema.model_rebuild()
        s = input_data.schema.model_json_schema()
        s["type"] = "object"
        json_schema = {
            "type": "json_schema",
            "json_schema": {"name": input_data.schema.__name__, "schema": s},
        }
        resp = await acompletion(
            model=self.config.model, messages=messages, response_format=json_schema, temperature=self.config.temperature
        )
        return input_data.schema.model_validate_json(resp.choices[0].message.content)
