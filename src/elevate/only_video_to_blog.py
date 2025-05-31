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
"""Only rephrase module for the Elevate app."""

from litellm import acompletion


class OnlyVideoToBlog:
    """Class that returns rephrased text."""

    def __init__(self, with_model: str = "gemini/gemini-2.0-flash-lite") -> None:
        """Initialize the OnlyVideoToBlog class"""
        self.model = with_model

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]

        response = await acompletion(api_key="", model=self.model, messages=messages, temperature=0.1)
        return str(response.choices[0].message.content)

    def get_blog_generation_system_prompt(self) -> str:
        """Return the system prompt for blog generation."""
        return """
        You are a highly skilled blog writer specializing in transforming complex information into engaging and easily
        digestible content.  Your task is to create a compelling blog post based on a video transcript provided by the
        user.

        The goal is to explain the video's content through the lens of a light, fictional story. Think of how a CEO or
        other executive might use a relatable narrative to illustrate a point.  This story should be interwoven seamlessly
        with explanations of the key concepts from the video.

        Specifically:

        *   **Focus on Clarity:**  Ensure the blog post is easy to understand, even for readers unfamiliar with the
        video's topic.
        *   **Storytelling Emphasis:**  The fictional narrative should be the *primary* method of explaining the video's
        content, not just an afterthought.  Consider using characters, a specific scenario, or a problem/solution
        framework.
        *   **Executive Storytelling Style:**  Emulate the tone and style of a CXO sharing a relevant anecdote. This
        includes:
            *   A relatable and human element.
            *   A clear takeaway message or lesson.
            *   A focus on the big picture and practical applications.
        *   **Accuracy:**  Maintain the factual accuracy of the video's content while framing it within the fictional story.

        The user will provide the video transcript.  Your output should be a complete and ready-to-publish blog post. """

    async def generate_blog(self, transcript: str) -> str:
        """Generate a blog post from a given video transcript."""
        system_prompt = self.get_blog_generation_system_prompt()
        return await self.make_llm_call(system_prompt, transcript)
