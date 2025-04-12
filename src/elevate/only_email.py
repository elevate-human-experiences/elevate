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
"""OnlyEmail class for generating emails using LLMs."""

from litellm import completion

from elevate.only_email_prompts import (
    MARKETING_EMAIL_PROMPT,
    PERSONAL_EMAIL_PROMPT,
    PROFESSIONAL_EMAIL_PROMPT,
)


class OnlyEmail:
    """Class that returns well formatted emails."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyMarkdown class"""
        self.model = with_model

    def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """
        Makes the LLM call using litellm, extracting the markdown content.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]

        response = completion(model=self.model, messages=messages, temperature=0.1)
        output = str(response.choices[0].message.content)
        return output

    def get_personal_email_system_prompt(self) -> str:
        """
        Return a PERSONAL_EMAIL_PROMPT.
        """
        return PERSONAL_EMAIL_PROMPT

    def get_professional_email_system_prompt(self) -> str:
        """
        Return a PROFESSIONAL_EMAIL_PROMPT.
        """
        return PROFESSIONAL_EMAIL_PROMPT

    def get_marketing_email_system_prompt(self) -> str:
        """
        Return a MARKETING_EMAIL_PROMPT.
        """
        return MARKETING_EMAIL_PROMPT

    def get_email_prompt(self, email_type: str) -> str:
        """Return the appropriate email prompt based on the email type."""
        match email_type.lower():
            case "personal":
                return self.get_personal_email_system_prompt()
            case "professional":
                return self.get_professional_email_system_prompt()
            case "marketing":
                return self.get_marketing_email_system_prompt()
            case _:
                raise ValueError("Invalid email type specified.")

    def generate_email(self, message: str, email_type: str) -> str:
        """Generates an email of the specified type using an LLM.

        Args:
            message: The email content.
            email_type:  The type of email (personal, professional, marketing).

        Returns:
            The generated email or an error message.
        """
        try:
            system_prompt = self.get_email_prompt(email_type)
            return self.make_llm_call(system_prompt, message)

        except ValueError as ve:
            print(f"ValueError: {ve}")  # Log the error.
            return "Error: Invalid email type specified."
        except Exception as e:
            print(f"An error occurred: {e}")  # Log the error.
            return "Error: An unexpected error occurred while generating the email."
