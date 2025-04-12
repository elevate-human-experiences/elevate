from dotenv import load_dotenv
from litellm import completion

from elevate.only_email_prompts import (
    MARKETING_EMAIL_PROMPT,
    PERSONAL_EMAIL_PROMPT,
    PROFESSIONAL_EMAIL_PROMPT,
)

# Load environment variables
load_dotenv()


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

    def generate_email(self, message: str, email_type: str) -> str:
        """Generates an email of the specified type using an LLM.

        Args:
            message: The email content.
            email_type:  The type of email (personal, professional, marketing).

        Returns:
            The generated email or an error message.
        """
        try:
            match email_type.lower():  # Use match/case for cleaner code
                case "personal":
                    system_prompt = self.get_personal_email_system_prompt()
                    return self.make_llm_call(system_prompt, message)
                case "professional":
                    system_prompt = self.get_professional_email_system_prompt()
                    return self.make_llm_call(system_prompt, message)
                case "marketing":
                    system_prompt = self.get_marketing_email_system_prompt()
                    return self.make_llm_call(system_prompt, message)
                case _:
                    return (
                        "Error: Invalid email type specified."  # Handle invalid input
                    )

        except Exception as e:
            print(f"An error occurred: {e}")  # Log the error.
            return "Error: An unexpected error occurred while generating the email."
