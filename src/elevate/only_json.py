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

import litellm
from litellm import acompletion
from pydantic import BaseModel


class OnlyJson:
    """Class that only supports JSON schema validation."""

    def __init__(self, with_model: str = "gpt-4o-mini", with_tool: str = "lite-llm") -> None:
        """Initialize the OnlyJson class"""
        self.model_id = with_model
        self.tool_id = with_tool
        # Not all models support JSON schema validation,
        # so we need to do it on the client side.
        litellm.enable_json_schema_validation = True

    async def parse(self, content: str, schema: type[BaseModel], system_prompt: str | None = None) -> BaseModel:
        """Parse the content using the specified schema."""
        if self.tool_id == "lite-llm":
            # Use LiteLLM for conversion
            if self.model_id not in litellm.model_list:
                raise ValueError(f"Model {self.model_id} is not supported.")
            # Updated messages with a system prompt for podcast conversation generation
            messages = [
                {"role": "user", "content": content},
            ]
            if system_prompt:
                messages.insert(0, {"role": "system", "content": system_prompt})

            # Rebuild the model and get the JSON schema
            schema.model_rebuild()
            s = schema.model_json_schema()
            s["type"] = "object"
            json_schema = {
                "type": "json_schema",
                "json_schema": {"name": schema.__name__, "schema": s},
            }
            resp = await acompletion(model=self.model_id, messages=messages, response_format=json_schema)
            return schema.model_validate_json(resp.choices[0].message.content)
        raise ValueError(f"Tool {self.tool_id} is not supported for Text to JSON.")
