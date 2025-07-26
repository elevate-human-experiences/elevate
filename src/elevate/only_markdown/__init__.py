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
"""
OnlyMarkdown class for converting text to Markdown format using litellm.

This module provides the OnlyMarkdown class, which is designed to convert
plain text into GitHub Flavored Markdown (GFM) using the litellm library.
The conversion process is guided by a set of predefined scenarios and a
system prompt that instructs the model on the desired Markdown output.
"""

import logging
import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field

from common import setup_logging


logger = setup_logging(logging.INFO)


class MarkdownConfig(BaseModel):
    """Configuration for OnlyMarkdown class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class MarkdownInput(BaseModel):
    """User-friendly input for markdown conversion."""

    content: str = Field(..., description="The text content you want to convert to Markdown")
    context: str | None = Field(
        default=None,
        description="Optional context about where you'll use this (e.g., 'for my team presentation', 'in documentation')",
    )
    purpose: str | None = Field(
        default=None, description="Optional purpose or goal (e.g., 'make it more readable', 'format for GitHub')"
    )


class MarkdownOutput(BaseModel):
    """Enhanced output with user-valuable insights."""

    markdown: str = Field(..., description="Your content converted to clean Markdown format")
    formatting_improvements: list[str] = Field(
        default_factory=list, description="Key formatting improvements made to enhance readability"
    )
    summary: str | None = Field(default=None, description="Brief summary of the content structure")
    next_steps: list[str] = Field(default_factory=list, description="Suggested next steps for using this markdown")


class OnlyMarkdown:
    """
    Transform messy text into beautiful, professional Markdown formatting.

    Perfect for:
    • Converting copy-pasted content from websites, Word docs, or emails
    • Cleaning up unformatted text for GitHub documentation
    • Preparing content for team wikis, README files, or blog posts
    • Transforming database outputs or reports into readable formats
    • Making presentation notes more structured and visually appealing
    """

    def __init__(self, config: MarkdownConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyMarkdown class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = MarkdownConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, user_message: str) -> dict[str, str | list[str] | None]:
        """Make the LLM call and extract both markdown and metadata."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        output = str(getattr(response, "content", response))

        # Extract markdown content
        markdown_pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        markdown_match = re.search(markdown_pattern, output, re.DOTALL)
        markdown = markdown_match.group(1).strip() if markdown_match else output

        # Extract formatting improvements
        improvements_pattern = r"IMPROVEMENTS:(.*?)(?=SUMMARY:|NEXT_STEPS:|$)"
        improvements_match = re.search(improvements_pattern, output, re.DOTALL)
        improvements = []
        if improvements_match:
            improvements = [
                imp.strip()
                for imp in improvements_match.group(1).strip().split("\n")
                if imp.strip() and not imp.strip().startswith("-")
            ]

        # Extract summary
        summary_pattern = r"SUMMARY:(.*?)(?=NEXT_STEPS:|$)"
        summary_match = re.search(summary_pattern, output, re.DOTALL)
        summary = summary_match.group(1).strip() if summary_match else None

        # Extract next steps
        next_steps_pattern = r"NEXT_STEPS:(.*?)$"
        next_steps_match = re.search(next_steps_pattern, output, re.DOTALL)
        next_steps = []
        if next_steps_match:
            next_steps = [
                step.strip()
                for step in next_steps_match.group(1).strip().split("\n")
                if step.strip() and not step.strip().startswith("-")
            ]

        return {"markdown": markdown, "improvements": improvements, "summary": summary, "next_steps": next_steps}

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_conversion_system_prompt(self, context: str | None = None, purpose: str | None = None) -> str:
        """Return a user-focused system prompt for markdown conversion."""
        template = self._load_prompt_template()
        return str(template.render(context=context, purpose=purpose))

    async def convert_to_markdown(self, input_data: MarkdownInput) -> MarkdownOutput:
        """Transform your content into beautiful, professional Markdown."""
        system_prompt = self.get_conversion_system_prompt(input_data.context, input_data.purpose)

        # Create user message with context
        user_message = input_data.content
        if input_data.context or input_data.purpose:
            context_info = []
            if input_data.context:
                context_info.append(f"Context: {input_data.context}")
            if input_data.purpose:
                context_info.append(f"Purpose: {input_data.purpose}")
            user_message = f"{' | '.join(context_info)}\n\nContent to convert:\n{input_data.content}"

        result = await self.make_llm_call(system_prompt, user_message)

        # Ensure correct types for MarkdownOutput
        markdown = result["markdown"] if isinstance(result["markdown"], str) else ""
        improvements = result["improvements"] if isinstance(result["improvements"], list) else []
        summary = result["summary"] if isinstance(result["summary"], str) else None
        next_steps = result["next_steps"] if isinstance(result["next_steps"], list) else []

        return MarkdownOutput(
            markdown=markdown,
            formatting_improvements=improvements,
            summary=summary,
            next_steps=next_steps,
        )

    async def summarize_and_convert_to_markdown(self, input_data: MarkdownInput) -> MarkdownOutput:
        """Create a concise, well-formatted summary in Markdown."""
        # Add summarization context to the purpose
        enhanced_purpose = "create a concise summary"
        if input_data.purpose:
            enhanced_purpose = f"{input_data.purpose} with a concise summary"

        enhanced_input = MarkdownInput(content=input_data.content, context=input_data.context, purpose=enhanced_purpose)

        return await self.convert_to_markdown(enhanced_input)

    def print_section_header(self, title: str) -> None:
        """Print a formatted section header."""
        logger.debug("%s", f"\n{'*' * 20} {title} {'*' * 20}\n")
