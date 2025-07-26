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
"""OnlyJudgeLLMs: Class to evaluate LLM outputs based on defined scoring criteria."""

import logging
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class OnlyJudgeLLMs:
    """
    Class to evaluate LLM outputs based on defined scoring criteria.

    This evaluation uses an LLM call to transform the provided text into a structured JSON
    evaluation that strictly conforms to a given Pydantic schema (which defines the scoring criteria).
    """

    def __init__(self, with_model: str = "o3-mini") -> None:
        """
        Initialize the OnlyJudgeLLMs class with the specified LLM model.

        Args:
        ----
            with_model: Identifier for the LLM model.
        """
        self.model = with_model

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_judgment_prompt(self) -> str:
        """Construct a system prompt for LLM evaluation."""
        template = self._load_prompt_template()
        return str(template.render())

    async def evaluate(self, text: str, criteria: type[BaseModel], system_prompt: str | None = None) -> BaseModel:
        """
        Evaluates the given text against the scoring criteria defined in the Pydantic model.

        This method builds an evaluation prompt (unless one is provided), makes an LLM call, and then parses
        the resulting JSON into an instance of the scoring criteria model.

        Args:
        ----
            text: The LLM output text to be evaluated.
            criteria: A Pydantic model representing the scoring criteria.
            system_prompt: An optional custom system prompt to override the default evaluation prompt.

        Returns:
        -------
            An instance of the criteria model populated with the evaluation metrics.

        Raises:
        ------
            ValueError: If the output cannot be parsed according to the criteria schema.
        """
        if system_prompt is None:
            system_prompt = self.get_judgment_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
        response = await acompletion(
            model=self.model,
            messages=messages,
            response_format=criteria,
        )
        content = None
        # Try dict-like access
        try:
            if isinstance(response, dict):
                choices = response.get("choices")
                if choices and isinstance(choices, list) and len(choices) > 0:
                    message = choices[0].get("message")
                    if message and isinstance(message, dict):
                        content = message.get("content")
        except Exception as ex_dict:
            logger.debug(f"Dict-like response parsing failed: {ex_dict}")
        # Try object-like access
        if content is None:
            try:
                choices = getattr(response, "choices", None)
                if choices and isinstance(choices, list) and len(choices) > 0:
                    message = getattr(choices[0], "message", None)
                    if message:
                        content = getattr(message, "content", None)
            except Exception as ex_obj:
                logger.debug(f"Object-like response parsing failed: {ex_obj}")

        return criteria.model_validate_json(str(content))
