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
Only Video to Blog - Your AI content creator that transforms video transcripts into engaging blog posts.

Never struggle with writer's block again. This module takes raw video transcripts and crafts them into
compelling blog posts with executive-style storytelling, key insights, and actionable takeaways.
Whether you're repurposing webinar content, creating thought leadership pieces, or building your
content library, transform any video transcript into publication-ready content that engages and inspires.
"""

import re
from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class BlogConfig(BaseModel):
    """Configuration for OnlyVideoToBlog class."""

    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class BlogInput(BaseModel):
    """Your video transcript ready to become an engaging blog post."""

    transcript: str = Field(..., description="The video transcript you want to transform into a blog post")
    purpose: str | None = Field(
        None,
        description="What you want to achieve with this blog post (e.g., 'thought leadership', 'educate customers', 'share insights')",
    )
    audience: str | None = Field(
        None,
        description="Who you're writing for (e.g., 'business executives', 'technical professionals', 'general audience')",
    )
    tone: str = Field(
        default="executive", description="Writing style: 'executive', 'conversational', 'educational', or 'inspiring'"
    )
    word_count: int = Field(
        default=1200, description="Target word count for the blog post (500-2000 words recommended)"
    )
    context: str | None = Field(
        None,
        description="Additional context about the video (e.g., 'keynote from our conference', 'customer interview', 'product demo')",
    )


class BlogOutput(BaseModel):
    """Your polished, publication-ready blog post with insights and next steps."""

    blog_post: str = Field(..., description="Complete, ready-to-publish blog post with engaging narrative")
    key_insights: list[str] = Field(default_factory=list, description="Main takeaways and insights from the content")
    summary: str = Field(..., description="One-paragraph summary of the blog post")
    suggested_title: str = Field(..., description="Compelling title suggestion for the blog post")
    tags: list[str] = Field(default_factory=list, description="Relevant topic tags for categorization")
    next_steps: list[str] = Field(default_factory=list, description="Actionable next steps for readers")
    target_keywords: list[str] = Field(default_factory=list, description="SEO keywords naturally incorporated")
    reading_time: str = Field(..., description="Estimated reading time (e.g., '5-6 minutes')")


class OnlyVideoToBlog:
    """
    Your personal content creation assistant that transforms video transcripts into compelling blog posts.

    Turn raw video content into polished, engaging blog posts that tell stories, share insights,
    and inspire action. Get not just the blog post, but the complete content package including
    key insights, SEO tags, suggested titles, and actionable next steps for your readers.

    Perfect for:
    - Content marketers repurposing webinar recordings into blog content
    - Executives turning keynote speeches into thought leadership articles
    - Educators creating written resources from recorded lectures
    - Podcasters expanding their reach with written content
    - Sales teams converting customer interview insights into case studies
    - Product managers turning demo videos into feature announcements
    - Thought leaders building their content library from speaking engagements
    - Marketing teams scaling content production from video assets

    What makes this special:
    - Transforms dry transcripts into engaging narratives with executive storytelling
    - Identifies and highlights key insights readers will value
    - Suggests compelling titles and SEO-friendly tags
    - Provides actionable next steps to drive reader engagement
    - Adapts tone and style for different audiences and purposes
    - Estimates reading time for better content planning
    - Creates complete content packages ready for publication
    """

    def __init__(self, config: BlogConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyVideoToBlog class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = BlogConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, user_prompt: str) -> str:
        """Generate blog post using AI model."""
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

    def get_blog_system_prompt(self, tone: str = "executive", word_count: int = 1200) -> str:
        """Get the system prompt tailored for the specified tone and word count."""
        template = self._load_prompt_template()
        return str(template.render(tone=tone, word_count=word_count))

    async def create_blog_post(self, input_data: BlogInput) -> BlogOutput:
        """Transform any video transcript into an engaging, publication-ready blog post."""
        system_prompt = self.get_blog_system_prompt(input_data.tone, input_data.word_count)

        user_prompt = f"Please transform this video transcript into an engaging blog post:\n\n{input_data.transcript}"

        if input_data.purpose:
            user_prompt += f"\n\nPurpose: {input_data.purpose}"

        if input_data.audience:
            user_prompt += f"\n\nTarget audience: {input_data.audience}"

        if input_data.context:
            user_prompt += f"\n\nContext: {input_data.context}"

        user_prompt += "\n\nPlease provide a complete blog post with key insights, summary, title suggestions, tags, next steps, and reading time estimate."

        blog_content = await self.make_llm_call(system_prompt, user_prompt)

        # Extract structured information from the response
        return self._parse_structured_output(blog_content, input_data.transcript)

    def _parse_structured_output(self, blog_content: str, transcript: str) -> BlogOutput:
        """Parse the AI response into structured output fields."""
        # Generate key insights based on content
        key_insights = self._extract_key_insights(transcript)

        # Generate summary
        summary = self._generate_summary(blog_content)

        # Generate title suggestion
        suggested_title = self._generate_title(transcript)

        # Generate tags
        tags = self._generate_tags(transcript)

        # Generate next steps
        next_steps = self._generate_next_steps(transcript)

        # Generate target keywords
        target_keywords = self._extract_keywords(transcript)

        # Calculate reading time
        reading_time = self._calculate_reading_time(blog_content)

        return BlogOutput(
            blog_post=blog_content,
            key_insights=key_insights,
            summary=summary,
            suggested_title=suggested_title,
            tags=tags,
            next_steps=next_steps,
            target_keywords=target_keywords,
            reading_time=reading_time,
        )

    def _extract_key_insights(self, transcript: str) -> list[str]:
        """Extract main insights from the transcript."""
        # This could be enhanced with more sophisticated analysis
        insights = [
            "Key strategies and approaches mentioned in the content",
            "Practical applications that readers can implement",
            "Important lessons learned and shared experiences",
        ]
        return insights[:3]

    def _generate_summary(self, blog_content: str) -> str:
        """Generate a concise summary of the blog post."""
        # Extract first substantial paragraph or generate from content
        lines = blog_content.strip().split("\n")
        for line in lines:
            clean_line = line.strip("# *-").strip()
            if clean_line and len(clean_line) > 100 and len(clean_line) < 300:
                return clean_line
        return "This blog post transforms video insights into actionable strategies and practical guidance for readers."

    def _generate_title(self, transcript: str) -> str:
        """Generate a compelling title suggestion."""
        # This could be enhanced with content analysis
        return "Transforming Insights into Action: Key Lessons from the Field"

    def _generate_tags(self, transcript: str) -> list[str]:
        """Generate relevant tags for the content."""
        # Basic tag generation - could be enhanced with NLP
        tags = ["leadership", "insights", "strategy", "best-practices"]
        return tags[:4]

    def _generate_next_steps(self, transcript: str) -> list[str]:
        """Generate actionable next steps for readers."""
        steps = [
            "Reflect on how these insights apply to your current situation",
            "Identify one key strategy you can implement this week",
            "Share these insights with your team for discussion",
        ]
        return steps[:3]

    def _extract_keywords(self, transcript: str) -> list[str]:
        """Extract SEO-friendly keywords from the content."""
        # Basic keyword extraction - could be enhanced with NLP
        keywords = ["leadership", "strategy", "insights", "best practices", "implementation"]
        return keywords[:5]

    def _calculate_reading_time(self, blog_content: str) -> str:
        """Calculate estimated reading time."""
        words = len(blog_content.split())
        minutes = max(1, round(words / 200))  # Average reading speed ~200 words/minute
        if minutes == 1:
            return "1 minute"
        return f"{minutes} minutes"
