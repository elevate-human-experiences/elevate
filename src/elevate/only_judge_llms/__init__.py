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
from typing import Any

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)


class JudgeLLMsConfig(BaseModel):
    """Configuration for OnlyJudgeLLMs class."""

    model: str = Field(default="o3-mini", description="LLM model to use")


class JudgeLLMsInput(BaseModel):
    """Input for evaluating content quality and performance."""

    content: str = Field(..., description="The text, message, or document you want to evaluate")
    context: str | None = Field(
        default=None,
        description="What you're using this content for (e.g., 'presentation to my team', 'blog post', 'customer email')",
    )
    purpose: str | None = Field(
        default=None,
        description="Your specific goal or situation (e.g., 'need to sound professional', 'explaining to beginners', 'marketing copy')",
    )
    criteria: type[BaseModel] = Field(..., description="Evaluation criteria model")
    custom_instructions: str | None = Field(
        default=None, description="Any specific evaluation guidance or requirements"
    )


class JudgeLLMsOutput(BaseModel):
    """Enhanced output with user-valuable insights beyond basic scoring."""

    scores: BaseModel = Field(..., description="Detailed scoring results based on your criteria")
    summary: str = Field(..., description="Overall assessment of your content's strengths and areas for improvement")
    key_insights: list[str] = Field(..., description="Most important takeaways about your content's performance")
    recommendations: list[str] = Field(..., description="Specific suggestions to improve your content")
    next_steps: list[str] = Field(
        default_factory=list, description="Actionable steps you can take to enhance your content"
    )


class OnlyJudgeLLMs:
    """
    AI-powered content evaluator to help you improve your writing and communication.

    Perfect for:
    • Reviewing emails, presentations, and documents before sending
    • Getting objective feedback on your writing quality and effectiveness
    • Evaluating content against specific criteria (clarity, professionalism, engagement)
    • Improving team communications and marketing materials
    • Quality assurance for customer-facing content
    • Getting actionable suggestions to enhance your messaging
    """

    def __init__(self, config: JudgeLLMsConfig) -> None:
        """
        Initialize the OnlyJudgeLLMs class with Pydantic config.

        Args:
        ----
            config: Configuration object containing model settings.
        """
        self.config = config

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

    def _extract_response_content(self, response: dict[str, Any] | object) -> str | None:
        """Extract content from LLM response, handling both dict and object formats."""
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

        return content

    def _build_insights_prompt(self, input_data: JudgeLLMsInput, scores: BaseModel) -> str:
        """Build prompt for generating user-focused insights and recommendations."""
        context_info = ""
        if input_data.context:
            context_info += f"Context: {input_data.context}\n"
        if input_data.purpose:
            context_info += f"Purpose: {input_data.purpose}\n"

        return f"""You are a helpful writing coach providing actionable feedback to help someone improve their content.

{context_info}
Based on the detailed scoring results, provide practical insights and recommendations.

Focus on:
- What's working well and what needs improvement
- Specific actionable suggestions they can implement
- Next steps to enhance their content's effectiveness

Be supportive, constructive, and specific in your feedback. Remember they want to use this content for: {input_data.context or "general purposes"}.

Scoring results: {scores.model_dump_json(indent=2)}"""

    async def evaluate(self, input_data: JudgeLLMsInput) -> JudgeLLMsOutput:
        """
        Get comprehensive feedback on your content to help you improve it.

        Analyzes your text against the criteria you care about and provides actionable insights
        including detailed scores, key takeaways, and specific recommendations for improvement.

        Args:
        ----
            input_data: Your content with context about how you plan to use it.

        Returns:
        -------
            Detailed evaluation with scores, insights, and actionable recommendations.

        Raises:
        ------
            ValueError: If evaluation fails or content cannot be analyzed.
        """
        system_prompt = input_data.custom_instructions or self.get_judgment_prompt()

        # Build user message with context and purpose
        user_message = f"Content to evaluate: {input_data.content}"
        if input_data.context:
            user_message += f"\n\nContext: {input_data.context}"
        if input_data.purpose:
            user_message += f"\n\nPurpose: {input_data.purpose}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        # Get basic criteria scoring
        criteria_response = await acompletion(
            model=self.config.model,
            messages=messages,
            response_format=input_data.criteria,
        )

        # Parse criteria response
        criteria_content = self._extract_response_content(criteria_response)
        scores = input_data.criteria.model_validate_json(str(criteria_content))

        # Generate enhanced insights
        insights_prompt = self._build_insights_prompt(input_data, scores)
        insights_messages = [
            {"role": "system", "content": insights_prompt},
            {"role": "user", "content": user_message},
        ]

        class InsightsModel(BaseModel):
            summary: str = Field(..., description="Overall assessment")
            key_insights: list[str] = Field(..., description="Key takeaways")
            recommendations: list[str] = Field(..., description="Improvement suggestions")
            next_steps: list[str] = Field(..., description="Actionable steps")

        insights_response = await acompletion(
            model=self.config.model,
            messages=insights_messages,
            response_format=InsightsModel,
        )

        insights_content = self._extract_response_content(insights_response)
        insights = InsightsModel.model_validate_json(str(insights_content))

        return JudgeLLMsOutput(
            scores=scores,
            summary=insights.summary,
            key_insights=insights.key_insights,
            recommendations=insights.recommendations,
            next_steps=insights.next_steps,
        )
