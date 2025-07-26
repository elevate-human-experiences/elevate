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
"""Only video to blog module for the Elevate app."""

from pathlib import Path

from jinja2 import Template
from litellm import acompletion
from pydantic import BaseModel, Field


class VideoToBlogConfig(BaseModel):
    """Configuration for OnlyVideoToBlog class."""

    model: str = Field(default="gemini/gemini-2.0-flash-lite", description="LLM model to use")
    temperature: float = Field(default=0.1, description="Temperature for LLM calls")


class VideoToBlogInput(BaseModel):
    """Input model for video to blog conversion."""

    transcript: str = Field(..., description="Video transcript to convert to blog")
    number_of_words: int = Field(default=1200, description="Target number of words for the blog")


class VideoToBlogOutput(BaseModel):
    """Output model for video to blog conversion."""

    blog_post: str = Field(..., description="Generated blog post")


class OnlyVideoToBlog:
    """Class that returns blog posts generated from video transcripts."""

    def __init__(self, config: VideoToBlogConfig | None = None, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyVideoToBlog class with Pydantic config."""
        if config:
            self.config = config
        else:
            self.config = VideoToBlogConfig(model=with_model)

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]

        response = await acompletion(
            api_key="", model=self.config.model, messages=messages, temperature=self.config.temperature
        )
        return str(response.choices[0].message.content)

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_blog_generation_system_prompt(self, number_of_words: int) -> str:
        """Return the system prompt for blog generation."""
        template = self._load_prompt_template()
        return str(template.render(number_of_words=number_of_words))

    async def generate_blog(self, input_data: VideoToBlogInput) -> VideoToBlogOutput:
        """Generate a blog post from a given video transcript."""
        # Validate input transcript
        if not input_data.transcript or not input_data.transcript.strip():
            raise ValueError("Transcript cannot be empty or contain only whitespace")

        system_prompt = self.get_blog_generation_system_prompt(input_data.number_of_words)
        blog_post = await self.make_llm_call(system_prompt, input_data.transcript)
        return VideoToBlogOutput(blog_post=blog_post)
