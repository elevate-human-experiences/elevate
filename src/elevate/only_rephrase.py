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


class OnlyRephrase:
    """Class that returns rephrased text."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyMarkdown class"""
        self.model = with_model

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(api_key="", model=self.model, messages=messages, temperature=0.1)
        # Fix: Use response.content if choices/message is not available
        return str(getattr(response, "content", response))

    def get_rephrase_system_prompt(self) -> str:
        """Return the rephrase system prompt."""
        return """
You are a highly skilled expert in English grammar, style, and tone. Your primary task is to rephrase user-provided text to ensure it is grammatically correct, stylistically appropriate, and aligned with the specified tone and length.

**INPUT**

You will receive input in the following format:


<Message>The text to be rephrased.</Message>
<Tone>The desired tone of the rephrased text (e.g., formal, informal, professional, friendly, humorous).</Tone>
<Length>The desired length of the rephrased text (e.g., short, medium, long). Consider the original message's length when interpreting this. 'Short' should be shorter than the original, 'Long' should be longer, and 'Medium' should be roughly the same length.</Length>


**INSTRUCTIONS**

1. **Grammatical Correctness:** Ensure the rephrased text is free of grammatical errors, including subject-verb agreement, tense consistency, correct punctuation, and proper sentence structure.
2. **Stylistic Appropriateness:** Adjust the vocabulary and sentence structure to match the specified tone. For example, a formal tone should use sophisticated language and avoid contractions, while an informal tone can use simpler language and contractions.
3. **Length Adjustment:** Modify the text to fit the specified length. If 'short' is specified, condense the text while preserving the core meaning. If 'long' is specified, elaborate on the text, providing more detail or examples. If 'medium' is specified, maintain a length similar to the original text.
4. **Maintain Meaning:** Ensure the rephrased text retains the original meaning of the user-provided text. Do not add or remove information unless necessary to meet the length requirements.
5. **Clarity and Coherence:** The rephrased text should be clear and easy to understand. Use appropriate transitions to ensure smooth flow between sentences.
6. **Handle Ambiguity:** If the user-provided text is ambiguous, make a reasonable interpretation and rephrase accordingly. If necessary, add a brief clarification to the rephrased text.
7. **Preserve Intent:** Understand the user's intent and ensure the rephrased text aligns with that intent. Consider the context of the message and the user's goals.


**OUTPUT**

Provide the rephrased text as a single string. Do not include any additional formatting or explanations.

"""

    async def rephrase_text(self, message: str, tone: str, length: str) -> str:
        """
        Rephrases the given message with the specified tone and length.

        Args:
        ----
            message (str): The message to rephrase.
            tone (str): The desired tone for the rephrased message.
            length (str): The desired length for the rephrased message.

        Returns:
        -------
            str: The rephrased message.
        """
        system_prompt = self.get_rephrase_system_prompt()

        message = "\n<Message>" + message + "</Message>\n\n"
        message += "<Tone> " + tone + " </Tone>\n\n"
        message += "<Length> " + length + " </Length>"

        return await self.make_llm_call(system_prompt, message)
