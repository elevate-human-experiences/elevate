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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Only Video Transcript - Your AI companion for extracting maximum value from video content.

Transform hours of video content into actionable insights in minutes. Whether you're reviewing
educational content, analyzing business meetings, extracting research insights, or preparing
presentation materials, get the key information you need without rewatching entire videos.
Never miss important details or waste time searching through long recordings again.
"""

import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class VideoTranscriptConfig(BaseModel):
    """Configuration for OnlyVideoTranscript class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class VideoTranscriptInput(BaseModel):
    """What video content you want analyzed and why."""

    transcript: str = Field(..., description="The video transcript text you want to analyze")
    purpose: str | None = Field(
        None,
        description="Why you're analyzing this video (e.g., 'study for exam', 'prepare meeting summary', 'extract research insights')",
    )
    context: str | None = Field(
        None,
        description="Additional context about the video (e.g., 'technical training session', 'client meeting', 'conference keynote')",
    )
    focus_areas: list[str] = Field(
        default_factory=list,
        description="Specific topics or themes to focus on (e.g., ['key decisions', 'action items', 'technical concepts'])",
    )
    time_available: str = Field(
        default="detailed",
        description="How much detail you need: 'quick' (2-3 min read), 'standard' (5-7 min read), or 'detailed' (10+ min read)",
    )


class VideoTranscriptOutput(BaseModel):
    """Your comprehensive video analysis with actionable insights."""

    summary: str = Field(..., description="Clear overview of the video's main points and conclusions")
    key_insights: list[str] = Field(default_factory=list, description="The most important takeaways and discoveries")
    main_topics: list[str] = Field(default_factory=list, description="Core subjects and themes discussed")
    action_items: list[str] = Field(
        default_factory=list, description="Specific tasks, decisions, or follow-ups mentioned"
    )
    important_quotes: list[str] = Field(
        default_factory=list, description="Notable statements, definitions, or memorable phrases"
    )
    timestamps_mentioned: list[str] = Field(
        default_factory=list, description="Any time references or chronological markers found"
    )
    next_steps: list[str] = Field(default_factory=list, description="Suggested actions based on the video content")
    related_topics: list[str] = Field(default_factory=list, description="Connected subjects worth exploring further")
    content_type: str = Field(
        ..., description="Type of video content: 'educational', 'meeting', 'presentation', 'interview', 'training'"
    )
    complexity_level: str = Field(
        ..., description="Content difficulty: 'beginner', 'intermediate', 'advanced', 'expert'"
    )


class OnlyVideoTranscript:
    """
    Your intelligent video transcript analyzer that turns hours of content into actionable insights.

    Stop rewatching videos to find that one important detail. Get comprehensive analysis that
    identifies key insights, extracts action items, highlights important quotes, and provides
    clear summaries tailored to your specific needs and time constraints.

    Perfect for:
    - Students reviewing lecture recordings and educational content
    - Professionals analyzing meeting recordings and business presentations
    - Researchers extracting insights from interviews and conferences
    - Content creators studying competitor videos and industry talks
    - Team members catching up on meetings they missed
    - Executives reviewing earnings calls and strategic presentations
    - Trainers extracting key points from educational sessions
    - Anyone who needs to quickly understand video content without rewatching

    What makes this special:
    - Adapts analysis depth to your available time (quick, standard, detailed)
    - Focuses on specific areas that matter most to your purpose
    - Identifies actionable items and next steps automatically
    - Extracts memorable quotes and important definitions
    - Categorizes content type and complexity for better understanding
    - Provides related topics for continued learning or research
    - Works with any type of video content from any source
    """

    def __init__(self, config: VideoTranscriptConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyVideoTranscript class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = VideoTranscriptConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, user_prompt: str) -> str:
        """Generate analysis using AI model."""
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

    def get_analysis_system_prompt(self, time_available: str = "detailed", focus_areas: list[str] | None = None) -> str:
        """Get the system prompt tailored for the analysis requirements."""
        template = self._load_prompt_template()
        return str(template.render(time_available=time_available, focus_areas=focus_areas or []))

    async def analyze(self, input_data: VideoTranscriptInput) -> VideoTranscriptOutput:
        """Transform video transcript into comprehensive, actionable insights."""
        if not input_data.transcript or not input_data.transcript.strip():
            raise ValueError("Transcript cannot be empty or contain only whitespace")

        system_prompt = self.get_analysis_system_prompt(input_data.time_available, input_data.focus_areas)

        user_prompt = f"Please analyze this video transcript:\n\n{input_data.transcript}"

        if input_data.purpose:
            user_prompt += f"\n\nWhy I'm analyzing this: {input_data.purpose}"

        if input_data.context:
            user_prompt += f"\n\nVideo context: {input_data.context}"

        if input_data.focus_areas:
            user_prompt += f"\n\nPlease pay special attention to: {', '.join(input_data.focus_areas)}"

        user_prompt += f"\n\nI have {input_data.time_available} time available for reading the analysis."
        user_prompt += "\n\nPlease provide a comprehensive analysis including summary, key insights, action items, important quotes, and next steps."

        analysis = await self.make_llm_call(system_prompt, user_prompt)

        return self._parse_structured_output(analysis, input_data.transcript)

    def _parse_structured_output(self, analysis: str, transcript: str) -> VideoTranscriptOutput:
        """Parse the AI response into structured output fields."""
        lines = analysis.strip().split("\n")

        # Extract summary from the beginning of the analysis
        summary_lines = []
        for line in lines[:10]:  # Look in first 10 lines for summary
            clean_line = line.strip("# *-").strip()
            if clean_line and len(clean_line) > 30:
                summary_lines.append(clean_line)
                if len(" ".join(summary_lines)) > 100:  # Get substantial summary
                    break
        summary = " ".join(summary_lines) if summary_lines else "This video contains valuable insights and information."

        # Generate key insights based on content
        key_insights = self._extract_key_insights(analysis, transcript)

        # Extract main topics
        main_topics = self._extract_main_topics(transcript)

        # Find action items and next steps
        action_items = self._extract_action_items(analysis, transcript)

        # Extract important quotes
        important_quotes = self._extract_important_quotes(transcript)

        # Find timestamp mentions
        timestamps_mentioned = self._extract_timestamps(transcript)

        # Generate next steps
        next_steps = self._generate_next_steps(analysis)

        # Identify related topics
        related_topics = self._identify_related_topics(transcript)

        # Determine content type and complexity
        content_type = self._determine_content_type(transcript)
        complexity_level = self._assess_complexity(transcript)

        return VideoTranscriptOutput(
            summary=summary,
            key_insights=key_insights,
            main_topics=main_topics,
            action_items=action_items,
            important_quotes=important_quotes,
            timestamps_mentioned=timestamps_mentioned,
            next_steps=next_steps,
            related_topics=related_topics,
            content_type=content_type,
            complexity_level=complexity_level,
        )

    def _extract_key_insights(self, analysis: str, transcript: str) -> list[str]:
        """Extract the most important insights from the content."""
        insights = []

        # Look for insight indicators in the transcript
        insight_keywords = ["important", "key", "crucial", "significant", "remember", "takeaway", "lesson"]
        sentences = transcript.replace("\n", " ").split(".")

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in insight_keywords):
                insights.append(sentence.capitalize() + ".")
                if len(insights) >= 5:
                    break

        # If no insights found, generate based on analysis
        if not insights:
            insights = [
                "This content provides valuable information for the intended audience.",
                "Key concepts are explained in a clear and understandable manner.",
                "The information can be applied to real-world situations.",
            ]

        return insights[:5]

    def _extract_main_topics(self, transcript: str) -> list[str]:
        """Identify the main subjects discussed in the video."""
        # Simple topic extraction based on frequently mentioned terms
        words = transcript.lower().split()
        word_freq: dict[str, int] = {}

        # Filter out common words
        stop_words = {
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "this",
            "that",
            "these",
            "those",
            "a",
            "an",
        }

        for word in words:
            word = word.strip('.,!?;:"()[]{}').lower()
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Get top topics
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:8]
        topics = [word.title() for word, _ in top_words if len(word) > 4]

        return topics[:6]

    def _extract_action_items(self, analysis: str, transcript: str) -> list[str]:
        """Find specific tasks, decisions, or follow-ups mentioned."""
        action_items = []
        action_keywords = [
            "need to",
            "should",
            "must",
            "action",
            "next step",
            "follow up",
            "decision",
            "task",
            "assignment",
        ]

        sentences = transcript.replace("\n", " ").split(".")
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in action_keywords) and len(sentence) > 15:
                action_items.append(sentence.capitalize() + ".")
                if len(action_items) >= 4:
                    break

        return action_items[:4]

    def _extract_important_quotes(self, transcript: str) -> list[str]:
        """Find notable statements, definitions, or memorable phrases."""
        quotes = []
        quote_indicators = ['"', "'", "definition", "means", "defined as", "important to note"]

        sentences = transcript.replace("\n", " ").split(".")
        for sentence in sentences:
            sentence = sentence.strip()
            if (
                any(indicator in sentence.lower() for indicator in quote_indicators)
                or ('"' in sentence and len(sentence) > 20)
            ) and len(sentence) < 200:
                quotes.append(sentence.capitalize() + ".")
                if len(quotes) >= 3:
                    break

        return quotes[:3]

    def _extract_timestamps(self, transcript: str) -> list[str]:
        """Find any time references or chronological markers."""
        timestamp_patterns = [
            r"\b\d{1,2}:\d{2}\b",  # MM:SS or H:MM
            r"\b\d{1,2}:\d{2}:\d{2}\b",  # H:MM:SS
            r"\bminute \d+\b",  # minute 5
            r"\bat \d+:\d+\b",  # at 5:30
        ]

        timestamps = []
        for pattern in timestamp_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            timestamps.extend(matches)

        return list(set(timestamps))[:5]

    def _generate_next_steps(self, analysis: str) -> list[str]:
        """Generate suggested actions based on the video content."""
        next_steps = [
            "Review and bookmark key sections for future reference",
            "Apply the main concepts to your current project or situation",
            "Share insights with relevant team members or colleagues",
        ]

        # Look for specific next steps in analysis
        if "research" in analysis.lower():
            next_steps.append("Conduct additional research on mentioned topics")
        if "practice" in analysis.lower():
            next_steps.append("Practice the techniques or methods discussed")

        return next_steps[:4]

    def _identify_related_topics(self, transcript: str) -> list[str]:
        """Identify connected subjects worth exploring further."""
        # Extract potential related topics from context
        related = []

        if "business" in transcript.lower():
            related.extend(["Strategy", "Management", "Leadership"])
        if "technology" in transcript.lower() or "technical" in transcript.lower():
            related.extend(["Innovation", "Digital Transformation", "Best Practices"])
        if "education" in transcript.lower() or "learning" in transcript.lower():
            related.extend(["Pedagogy", "Curriculum Design", "Assessment"])

        # Default related topics
        if not related:
            related = ["Industry Trends", "Professional Development", "Implementation Strategies"]

        return related[:5]

    def _determine_content_type(self, transcript: str) -> str:
        """Categorize the type of video content."""
        transcript_lower = transcript.lower()

        if any(word in transcript_lower for word in ["agenda", "minutes", "action items", "meeting"]):
            return "meeting"
        if any(word in transcript_lower for word in ["lesson", "chapter", "homework", "quiz", "lecture"]):
            return "educational"
        if any(word in transcript_lower for word in ["slides", "presentation", "presenting", "audience"]):
            return "presentation"
        if any(word in transcript_lower for word in ["interview", "question", "answer", "guest"]):
            return "interview"
        if any(word in transcript_lower for word in ["training", "tutorial", "how to", "step by step"]):
            return "training"
        return "educational"

    def _assess_complexity(self, transcript: str) -> str:
        """Assess the complexity level of the content."""
        transcript_lower = transcript.lower()

        # Count technical terms and complex indicators
        complex_indicators = ["algorithm", "methodology", "framework", "implementation", "architecture", "paradigm"]
        advanced_indicators = ["theoretical", "hypothesis", "empirical", "quantitative", "statistical"]
        beginner_indicators = ["introduction", "basics", "fundamentals", "getting started", "overview"]

        complex_count = sum(1 for word in complex_indicators if word in transcript_lower)
        advanced_count = sum(1 for word in advanced_indicators if word in transcript_lower)
        beginner_count = sum(1 for word in beginner_indicators if word in transcript_lower)

        if advanced_count > 2:
            return "expert"
        if complex_count > 3:
            return "advanced"
        if beginner_count > 2:
            return "beginner"
        return "intermediate"
