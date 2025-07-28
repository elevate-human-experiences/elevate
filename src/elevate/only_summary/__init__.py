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
Only summary module for the Elevate app.

This module provides the OnlySummary class, which is responsible for
generating TL;DR summaries and converting them into GitHub Flavored Markdown
(GFM) using the litellm library and the GPT-4o language model. The class
offers a method to summarize input text and return the summary in a
Markdown format, suitable for GitHub rendering.
"""

import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class SummaryConfig(BaseModel):
    """Configuration for OnlySummary class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class SummaryInput(BaseModel):
    """Input model for summary generation with user-friendly fields."""

    content: str = Field(..., description="The text, article, document, or content you want summarized")
    context: str = Field(
        default="", description="Optional context about why you need this summary or how you'll use it"
    )
    purpose: str = Field(
        default="general", description="What you need this for: presentation, email, meeting, study, etc."
    )
    audience: str = Field(
        default="general", description="Who will read this: team, executives, students, general audience, etc."
    )


class SummaryOutput(BaseModel):
    """Output model for summary generation with enhanced user value."""

    summary: str = Field(..., description="Main summary in clean Markdown format")
    key_insights: list[str] = Field(default=[], description="Most important takeaways from the content")
    word_count: int = Field(..., description="Word count of the original vs summary")
    reading_time: str = Field(..., description="Estimated reading time for the summary")


class OnlySummary:
    """
    Transform any content into clear, actionable summaries.

    Perfect for:
    • Condensing long articles, reports, or documents for quick consumption
    • Creating executive summaries for presentations and meetings
    • Extracting key insights from research papers or technical docs
    • Converting verbose content into digestible formats for your team
    • Preparing study notes or briefing materials
    • Making complex information accessible to different audiences
    """

    def __init__(self, config: SummaryConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlySummary class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = SummaryConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Makes the LLM call using litellm, extracting the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        # Fix: Use response.content if choices/message is not available
        output = str(response.choices[0].message.content)
        pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            return match.group(1).strip()
        return output

    def _extract_key_insights(self, summary: str) -> list[str]:
        """Extract key insights from the summary text."""
        insights = []
        lines = summary.split("\n")

        for line in lines:
            line = line.strip()
            # Look for bullet points, numbered lists, or strong statements
            if line.startswith(("- ", "* ", "• ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ")):
                clean_line = re.sub(r"^[-*•]\s*|^\d+\.\s*", "", line)
                if len(clean_line) > 10:  # Only meaningful insights
                    insights.append(clean_line)
            elif line.startswith("**") and line.endswith("**") and len(line) > 10:
                insights.append(line.strip("*"))

        # If no structured insights found, return first few sentences
        if not insights:
            sentences = summary.split(". ")
            insights = [s.strip() + "." for s in sentences[:3] if len(s.strip()) > 20]

        return insights[:5]  # Limit to top 5 insights

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_summarization_system_prompt(self, purpose: str, audience: str, context: str) -> str:
        """Generate a user-focused system prompt for summarization."""
        template = self._load_prompt_template()
        return str(template.render(purpose=purpose, audience=audience, context=context))

    async def summarize_and_convert_to_markdown(self, input_data: SummaryInput) -> SummaryOutput:
        """Transform your content into a clear, actionable summary with key insights."""
        system_prompt = self.get_summarization_system_prompt(
            input_data.purpose, input_data.audience, input_data.context
        )
        summary = await self.make_llm_call(system_prompt, input_data.content)

        # Extract key insights from the summary
        key_insights = self._extract_key_insights(summary)

        # Calculate metrics
        original_words = len(input_data.content.split())
        summary_words = len(summary.split())
        reading_time = f"{max(1, summary_words // 200)} min read"

        return SummaryOutput(
            summary=summary, key_insights=key_insights, word_count=original_words, reading_time=reading_time
        )
