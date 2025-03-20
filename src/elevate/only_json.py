"""Class that only supports JSON schema validation."""

import litellm
from litellm import completion
from pydantic import BaseModel
from typing import Type


class OnlyJson:
    """Class that only supports JSON schema validation."""

    def __init__(self, with_model: str) -> None:
        """Initialize the OnlyJson class"""
        self.model_id = with_model
        # Not all models support JSON schema validation,
        # so we need to do it on the client side.
        litellm.enable_json_schema_validation = True

    def parse(self, content: str, schema: Type[BaseModel]) -> BaseModel:
        """Parse the content using the specified schema."""
        messages = [{"role": "user", "content": content}]
        resp = completion(
            model=self.model_id, messages=messages, response_format=schema
        )
        return schema.model_validate_json(resp.choices[0].message.content)
