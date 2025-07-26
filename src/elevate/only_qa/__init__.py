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
Knowledge Assistant for making information accessible and actionable.

This module provides the OnlyQA class - a user-friendly tool that transforms
complex documentation into clear answers, insights, and actionable guidance.
Perfect for team explanations, presentations, and decision-making support.
"""

from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class QAConfig(BaseModel):
    """Configuration for OnlyQA class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class QAInput(BaseModel):
    """User-friendly input for getting answers and insights."""

    topic: str = Field(..., description="What you want to learn about or get help with")
    context: str = Field(default="", description="Your situation, background, or why you need this information")
    purpose: str = Field(default="", description="What you plan to do with this information")
    specific_questions: str = Field(default="", description="Any specific questions you have")


class QAOutput(BaseModel):
    """Comprehensive output with answers and valuable insights."""

    main_answer: str = Field(..., description="Primary answer to your question")
    key_insights: list[str] = Field(default_factory=list, description="Important takeaways and insights")
    summary: str = Field(default="", description="Brief summary of the key points")
    next_steps: list[str] = Field(default_factory=list, description="Suggested actions you can take")
    related_topics: list[str] = Field(default_factory=list, description="Related topics you might want to explore")


class OnlyQA:
    """
    Transform complex information into clear, actionable insights.

    Perfect for:
    • Explaining concepts to team members or stakeholders
    • Preparing presentations and training materials
    • Getting quick insights from documentation before meetings
    • Understanding complex topics with practical next steps
    • Making information accessible for decision-making
    """

    def __init__(self, config: QAConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize your knowledge assistant."""
        if config:
            self.config = config
        else:
            self.config = QAConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, user_input: str) -> str:
        """Generate response using the configured language model."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]
        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        return str(response.choices[0].message.content)

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_qa_system_prompt(self) -> str:
        """Get the user-focused system prompt for generating helpful responses."""
        template = self._load_prompt_template()
        return str(template.render())

    async def generate_answers(self, input_data: QAInput) -> QAOutput:
        """Generate comprehensive insights and answers from user input."""
        system_prompt = self.get_qa_system_prompt()

        # Create user-friendly input message
        user_input_parts = [f"Topic: {input_data.topic}"]
        if input_data.context:
            user_input_parts.append(f"Context: {input_data.context}")
        if input_data.purpose:
            user_input_parts.append(f"Purpose: {input_data.purpose}")
        if input_data.specific_questions:
            user_input_parts.append(f"Specific Questions: {input_data.specific_questions}")

        user_input = "\n".join(user_input_parts)
        response = await self.make_llm_call(system_prompt, user_input)

        # For now, return the response as main_answer
        # In a production system, you might parse the structured response
        return QAOutput(main_answer=response, key_insights=[], summary="", next_steps=[], related_topics=[])
