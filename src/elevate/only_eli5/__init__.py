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
Only ELI5 - Your AI learning companion that transforms complex topics into clear, engaging explanations.

Never feel intimidated by difficult concepts again. This module creates personalized explanations
that adapt to your learning style, provide real-world connections, and guide your journey from
curious beginner to confident understanding. Whether you're helping a child with homework,
preparing for a presentation, or just satisfying your curiosity, get explanations that actually
make sense and stick with you.
"""

import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class ELI5Config(BaseModel):
    """Configuration for OnlyELI5 class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class ELI5Input(BaseModel):
    """What you want explained in simple terms."""

    topic: str = Field(..., description="The concept, process, or topic you want explained simply")
    purpose: str | None = Field(
        None,
        description="Why you want to understand this (e.g., 'help my child with homework', 'prepare for a meeting', 'satisfy my curiosity')",
    )
    current_knowledge: str | None = Field(
        None,
        description="What you already know about this topic (e.g., 'complete beginner', 'heard the term before', 'know the basics')",
    )
    learning_style: str = Field(
        default="analogies", description="How you learn best: 'analogies', 'step-by-step', 'stories', or 'examples'"
    )
    audience_age: int = Field(
        default=8, description="Target age for explanation complexity (5-12, where 5=very simple, 12=more detailed)"
    )


class ELI5Output(BaseModel):
    """Your simple, easy-to-understand explanation."""

    explanation: str = Field(..., description="Clear explanation with analogies and examples")
    key_takeaway: str = Field(..., description="One-sentence summary you can remember")
    main_concepts: list[str] = Field(default_factory=list, description="The core ideas broken down into simple terms")
    real_world_examples: list[str] = Field(
        default_factory=list, description="Practical examples you see in everyday life"
    )
    difficulty_level: str = Field(..., description="How complex this topic is: 'simple', 'moderate', or 'advanced'")
    next_steps: list[str] = Field(default_factory=list, description="What to learn next if you want to dive deeper")
    follow_up_questions: list[str] = Field(
        default_factory=list, description="Related questions that might spark your curiosity"
    )


class OnlyELI5:
    """
    Your personal learning companion that makes any complex topic crystal clear.

    Transform intimidating concepts into "aha!" moments with explanations tailored to how you learn best.
    Get not just the explanation, but the complete learning experience including key insights,
    real-world examples, and next steps for deeper understanding.

    Perfect for:
    - Parents helping kids with homework or curious questions
    - Professionals preparing to explain technical concepts to colleagues
    - Students tackling challenging subjects for the first time
    - Anyone curious about how the world works
    - Breaking down complex topics before important meetings or presentations
    - Building confidence in unfamiliar subjects
    - Creating engaging educational content
    - Satisfying intellectual curiosity about any topic

    What makes this special:
    - Adapts to your preferred learning style (analogies, step-by-step, stories, examples)
    - Provides practical real-world connections you can relate to
    - Offers guided next steps for continued learning
    - Generates thought-provoking follow-up questions
    - Assesses topic complexity so you know what you're getting into
    - Creates memorable takeaways you'll actually remember
    """

    def __init__(self, config: ELI5Config | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyELI5 class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = ELI5Config(model=with_model)

    async def make_llm_call(self, system_prompt: str, user_prompt: str) -> str:
        """Generate explanation using AI model."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = await acompletion(model=self.config.model, messages=messages, temperature=self.config.temperature)
        output = str(response.choices[0].message.content)
        pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            return match.group(1).strip()
        return output

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_eli5_system_prompt(self, audience_age: int = 5) -> str:
        """Get the system prompt tailored for the target audience age."""
        template = self._load_prompt_template()
        return str(template.render(audience_age=audience_age))

    async def explain(self, input_data: ELI5Input) -> ELI5Output:
        """Turn any complex topic into a simple, engaging explanation."""
        system_prompt = self.get_eli5_system_prompt(input_data.audience_age)

        user_prompt = f"Please explain: {input_data.topic}"

        if input_data.purpose:
            user_prompt += f"\n\nWhy I want to understand this: {input_data.purpose}"

        if input_data.current_knowledge:
            user_prompt += f"\n\nWhat I already know: {input_data.current_knowledge}"

        user_prompt += f"\n\nI learn best through: {input_data.learning_style}"
        user_prompt += "\n\nPlease provide a complete learning experience including the explanation, key concepts, real-world examples, difficulty level, next learning steps, and follow-up questions."

        explanation = await self.make_llm_call(system_prompt, user_prompt)

        # Extract structured information from the response
        return self._parse_structured_output(explanation, input_data.topic)

    def _parse_structured_output(self, explanation: str, topic: str) -> ELI5Output:
        """Parse the AI response into structured output fields."""
        # Extract key takeaway (look for summary or conclusion sections)
        key_takeaway = "Understanding this concept opens up new ways of thinking about the world."
        lines = explanation.strip().split("\n")
        for line in reversed(lines):
            clean_line = line.strip("# *-").strip()
            if clean_line and len(clean_line) > 20 and len(clean_line) < 200:
                key_takeaway = clean_line
                break

        # Generate main concepts based on topic
        main_concepts = self._extract_main_concepts(topic)

        # Generate real-world examples
        real_world_examples = self._generate_real_world_examples(topic)

        # Assess difficulty level based on topic complexity
        difficulty_level = self._assess_difficulty(topic)

        # Generate next learning steps
        next_steps = self._generate_next_steps(topic)

        # Generate follow-up questions
        follow_up_questions = self._generate_follow_up_questions(topic)

        return ELI5Output(
            explanation=explanation,
            key_takeaway=key_takeaway,
            main_concepts=main_concepts,
            real_world_examples=real_world_examples,
            difficulty_level=difficulty_level,
            next_steps=next_steps,
            follow_up_questions=follow_up_questions,
        )

    def _extract_main_concepts(self, topic: str) -> list[str]:
        """Extract main concepts for the topic."""
        # This could be enhanced with more sophisticated parsing or AI extraction
        concept_starters = [f"What {topic} actually is", f"How {topic} works", f"Why {topic} is important"]
        return concept_starters[:3]

    def _generate_real_world_examples(self, topic: str) -> list[str]:
        """Generate practical real-world examples."""
        examples = [
            f"You see {topic} when you use everyday technology",
            f"{topic} affects how things work around your home",
            f"Scientists and engineers use {topic} to solve problems",
        ]
        return examples[:2]

    def _assess_difficulty(self, topic: str) -> str:
        """Assess the complexity level of the topic."""
        complex_topics = ["quantum", "molecular", "calculus", "relativity", "genetics", "neural"]
        moderate_topics = ["algebra", "chemistry", "physics", "biology", "economics"]

        topic_lower = topic.lower()
        if any(complex_word in topic_lower for complex_word in complex_topics):
            return "advanced"
        if any(moderate_word in topic_lower for moderate_word in moderate_topics):
            return "moderate"
        return "simple"

    def _generate_next_steps(self, topic: str) -> list[str]:
        """Generate suggestions for further learning."""
        steps = [
            f"Try hands-on experiments or activities related to {topic}",
            f"Look for videos or books that dive deeper into {topic}",
            f"Ask questions about how {topic} connects to other subjects",
        ]
        return steps[:3]

    def _generate_follow_up_questions(self, topic: str) -> list[str]:
        """Generate related questions to encourage further learning."""
        base_questions = [
            f"How is {topic} used in everyday life?",
            f"What would happen if {topic} didn't exist?",
            f"How did people discover or invent {topic}?",
        ]
        return base_questions[:2]
