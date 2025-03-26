"""Class that only supports JSON schema validation."""

import litellm
from litellm import completion
from pydantic import BaseModel
from typing import Type


class OnlyJson:
    """Class that only supports JSON schema validation."""

    def __init__(
        self, with_model: str = "gpt-4o-mini", with_tool: str = "lite-llm"
    ) -> None:
        """Initialize the OnlyJson class"""
        self.model_id = with_model
        self.tool_id = with_tool
        # Not all models support JSON schema validation,
        # so we need to do it on the client side.
        litellm.enable_json_schema_validation = True

    def parse(
        self, content: str, schema: Type[BaseModel], system_prompt: str | None = None
    ) -> BaseModel:
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
            resp = completion(
                model=self.model_id, messages=messages, response_format=json_schema
            )
            return schema.model_validate_json(resp.choices[0].message.content)
        else:
            raise ValueError(f"Tool {self.tool_id} is not supported for Text to JSON.")
