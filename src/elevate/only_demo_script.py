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
Only demo script module for the Elevate app.

This module provides the OnlyDemoScript class, which is responsible for
generating prodcut demo script it to Markdown
using the litellm library and the large language model.
"""

import re

from litellm import acompletion


class OnlyDemoScript:
    """Class that only returns demo script in Markdown syntax."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyDemoScript class"""
        self.model = with_model

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Makes the LLM call using litellm, extracting the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(model=self.model, messages=messages, temperature=0.1)
        # Fix: Use response.content if choices/message is not available
        output = str(response.choices[0].message.content)
        pattern = r"```markdown\n((?:(?!```).|\n)*?)```"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            return match.group(1).strip()
        return output

    def get_demo_script_generation_system_prompt(self, presentation_type: str, demo_length_in_minutes: int) -> str:
        """Return a system prompt to generate demo script content from the input text into Markdown syntax."""
        return f"""ROLE:
You are an expert product demo script writer, transforming technical documentation into captivating, story-driven product demonstrations.

**Input Parameters:**

*   **Product Technical Documentation:** (A comprehensive document detailing the product's features, functionality, and technical specifications.)
*   **Presentation Type:** (e.g., Technical, Business, Executive Overview, Investor Pitch) {presentation_type}
*   **Demo Length:** (in minutes, e.g., 5, 10, 15, 30) {demo_length_in_minutes}

**Instructions:**

1.  **Digest the Documentation:** Thoroughly analyze the `Product Technical Documentation` to understand the product's capabilities, limitations, and unique features. Identify the core problem it solves and the target audience's needs.

2.  **Understand the Audience & Craft the Story:** Analyze the `Presentation Type` to determine the audience's level of technical understanding, key interests, and desired outcomes. Develop an engaging narrative or story that connects the product's features to the audience's needs and aspirations. Frame the demonstration as a journey or a problem-solving adventure where the product is the hero.

    *   Consider using storytelling techniques such as:
        *   **Problem/Solution:** Introduce a relatable problem the audience faces and then showcase how the product provides the solution.
        *   **User Journey:** Follow a fictional user as they interact with the product and experience its benefits.
        *   **Case Study:** Present a real-world scenario where the product was used successfully.

3.  **Structure the Script:** Organize the script into a logical flow that supports the story:

    *   **Introduction (Brief & Engaging):** Start with a compelling hook that grabs the audience's attention and introduces the problem or scenario. Introduce the product and briefly explain its relevance to the story. (Approximately 10% of demo length).
    *   **Story-Driven Demonstration:** Weave the product's features and functionality into the narrative. Show, don't just tell. Use vivid language and create a sense of immersion. Focus on the "why" behind each feature, not just the "what." Include relevant use cases and scenarios that resonate with the audience. (Approximately 70% of demo length).
    *   **Climax & Resolution:**  Showcase the product's transformative power by demonstrating how it solves the problem or achieves a positive outcome in the story.
    *   **Call to Action:** Clearly state the next steps you want the audience to take (e.g., sign up for a trial, schedule a meeting, visit a website, request a quote).  Make it a natural extension of the story. (Approximately 10% of demo length).
    *   **Q&A Prep:** Anticipate potential questions based on the story and the product's features. Prepare brief, informative answers that reinforce the narrative. (This is not included in the script itself but inform your choices).

4.  **Content Guidelines:**

    *   **Storytelling Language:** Use descriptive language and imagery to paint a picture for the audience. Create a sense of emotion and connection.
    *   **Benefit-Oriented:** Emphasize the benefits of using the product within the context of the story. Focus on how the product improves the user's life or solves their problems.
    *   **Clear and Concise:** Avoid technical jargon unless appropriate for the `Presentation Type`. Translate technical details into relatable benefits.
    *   **Time Management:** Adhere to the `Demo Length` constraint. The script should be designed to be delivered within the specified time. Estimate the time each section will take.
    *   **Visual Cues:** Include brief descriptions of what the presenter should be showing on the screen at each stage. Use brackets, e.g., `[Show the character encountering the problem]` or `[Demonstrate how the product solves the problem with a click]`. Visuals should support and enhance the story.

5.  **Output Format:** Generate a well-formatted script, including:

    *   Speaker cues (e.g., "Presenter:").
    *   Clear transitions between scenes or segments of the story.
    *   Visual cues (as described above).
    *   Estimated time for each section.
    *   Incorporate storytelling elements (e.g., character names, scene descriptions, dialogue).
    *   Write the demo script in Markdown format.

**Example:**

If the `Presentation Type` is "Business" and the `Demo Length` is 15 minutes, you might tell the story of a fictional business owner struggling with a specific problem.  As the demo progresses, the product is introduced as the solution, and its features are demonstrated in the context of the business owner's journey to overcome the challenge.

**IMPORTANT:**  Remember that you are crafting a story-driven script. Prioritize engagement, relevance, and emotional connection. The product should be the hero of the story, but the story should be relatable and compelling on its own. The `Product Technical Documentation` provides the foundation for the product's capabilities, but your creativity brings the story to life.
"""

    async def generate_demo_script(self, input_text: str, presentation_type: str, demo_length_in_minutes: int) -> str:
        """Generate slides from the given input."""
        system_prompt = self.get_demo_script_generation_system_prompt(
            presentation_type, demo_length_in_minutes
        )  # Get the system prompt
        return await self.make_llm_call(system_prompt, input_text)
