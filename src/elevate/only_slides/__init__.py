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
AI-Powered Presentation Creator for the Elevate app.

Transform any topic into professional presentation slides with AI assistance.
Just describe what you want to present, who you're presenting to, and your goal -
the AI handles the rest. Get slides, insights, presentation tips, and next steps
all in one package.
"""

import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class SlidesConfig(BaseModel):
    """Configuration for OnlySlides class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class SlidesInput(BaseModel):
    """User-friendly input for creating presentation slides."""

    topic: str = Field(..., description="What you want to present about")
    audience: str = Field(..., description="Who you're presenting to (e.g., 'investors', 'my team', 'customers')")
    purpose: str = Field(
        ..., description="Goal of your presentation (e.g., 'get funding', 'explain our product', 'train employees')"
    )
    context: str | None = Field(default=None, description="Additional background or specific situation")
    slide_count: int = Field(default=5, description="How many slides you need", ge=3, le=20)
    style: str = Field(
        default="professional", description="Presentation style (professional, casual, creative, technical)"
    )


class SlidesOutput(BaseModel):
    """Complete presentation package with slides and helpful insights."""

    slides: str = Field(..., description="Your presentation slides in Markdown format")
    key_insights: list[str] = Field(..., description="Main takeaways from your presentation")
    presentation_tips: list[str] = Field(..., description="Tips for delivering this presentation effectively")
    estimated_duration: str = Field(..., description="Estimated presentation time")
    next_steps: list[str] = Field(..., description="Suggested follow-up actions for your audience")


class OnlySlides:
    """
    AI-powered presentation creator that transforms your ideas into professional slides.

    Perfect for:
    • Entrepreneurs creating pitch decks for investors
    • Sales teams preparing client presentations
    • Managers explaining new projects to their team
    • Trainers developing educational content
    • Students presenting research or project ideas
    • Anyone who needs slides fast without design hassle
    """

    def __init__(self, config: SlidesConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlySlides class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = SlidesConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, user_message: str) -> str:
        """Makes the LLM call using litellm, returning the complete response."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        return str(response.choices[0].message.content)

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_slide_generation_system_prompt(self, audience: str, purpose: str, slide_count: int, style: str) -> str:
        """Create a user-focused system prompt for generating presentation slides."""
        template = self._load_prompt_template()
        return str(
            template.render(
                audience=audience,
                purpose=purpose,
                slide_count=slide_count,
                style=style,
            )
        )

    async def generate_slides(self, input_data: SlidesInput) -> SlidesOutput:
        """Transform your ideas into a complete presentation package."""
        system_prompt = self.get_slide_generation_system_prompt(
            input_data.audience, input_data.purpose, input_data.slide_count, input_data.style
        )

        # Create user message from input data
        user_message = f"Topic: {input_data.topic}\n"
        user_message += f"Audience: {input_data.audience}\n"
        user_message += f"Purpose: {input_data.purpose}\n"
        if input_data.context:
            user_message += f"Additional context: {input_data.context}\n"

        # Get the complete response from LLM
        llm_response = await self.make_llm_call(system_prompt, user_message)

        # Parse the response to extract different sections
        return self._parse_llm_response(llm_response)

    def _parse_llm_response(self, response: str) -> SlidesOutput:
        """Parse the LLM response into structured output."""
        # Extract markdown slides
        slides_pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        slides_match = re.search(slides_pattern, response, re.DOTALL)
        slides = slides_match.group(1).strip() if slides_match else response

        # Extract other sections or provide defaults
        key_insights = self._extract_list_section(response, "KEY INSIGHTS", ["Main presentation content covered"])
        presentation_tips = self._extract_list_section(
            response,
            "PRESENTATION TIPS",
            ["Speak clearly and maintain eye contact", "Use slides as talking points, not scripts"],
        )
        next_steps = self._extract_list_section(
            response, "NEXT STEPS", ["Follow up with audience questions", "Provide additional resources if requested"]
        )

        # Estimate duration (roughly 1-2 minutes per slide)
        slide_count = len([line for line in slides.split("\n") if line.startswith("# ")])
        estimated_duration = f"{slide_count * 1.5:.0f}-{slide_count * 2:.0f} minutes"

        return SlidesOutput(
            slides=slides,
            key_insights=key_insights,
            presentation_tips=presentation_tips,
            estimated_duration=estimated_duration,
            next_steps=next_steps,
        )

    def _extract_list_section(self, text: str, section_name: str, default: list[str]) -> list[str]:
        """Extract a list section from the LLM response."""
        pattern = rf"{section_name}:\s*\n((?:[-•*]\s*.+\n?)*)"
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            items = []
            for line in match.group(1).strip().split("\n"):
                item = re.sub(r"^[-•*]\s*", "", line.strip())
                if item:
                    items.append(item)
            return items if items else default
        return default
