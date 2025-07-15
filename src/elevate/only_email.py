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

import logging

import litellm
from litellm import acompletion
from pydantic import BaseModel

from common import setup_logging


logger = setup_logging(logging.INFO)


class Email(BaseModel):
    """Pydantic model representing a structured email."""

    subject: str
    salutation: str
    body: str
    closing: str
    signature: str


class OnlyEmail:
    """Class that returns well formatted emails."""

    def __init__(self, with_model: str = "gpt-4o-mini") -> None:
        """Initialize the OnlyEmail class"""
        self.model = with_model
        # Enable JSON schema validation for structured output
        litellm.enable_json_schema_validation = True

    async def make_llm_call(self, system_prompt: str, input_text: str) -> str:
        """Make the LLM call using litellm and extract the markdown content."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text},
        ]
        response = await acompletion(api_key="", model=self.model, messages=messages, temperature=0.1)
        content = response.choices[0].message.content
        return str(content) if content else ""

    async def generate_structured_email(self, message: str, email_type: str) -> Email:
        """Generate a structured email using JSON schema validation."""
        system_prompt = self.get_email_prompt(email_type)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]

        # Build the JSON schema for the Email model
        Email.model_rebuild()
        schema = Email.model_json_schema()
        schema["type"] = "object"
        json_schema = {
            "type": "json_schema",
            "json_schema": {"name": Email.__name__, "schema": schema},
        }

        response = await acompletion(
            model=self.model,
            messages=messages,
            response_format=json_schema,
            temperature=0.1,
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("No content received from LLM response")

        return Email.model_validate_json(content)

    def get_personal_email_system_prompt(self) -> str:
        """Return a PERSONAL_EMAIL_PROMPT."""
        return """
You are an expert in crafting engaging and thoughtful personal emails. Your goal is to write a warm and friendly email that is tailored to the recipient and the specific context provided.

You must structure your response as a JSON object with the following fields:
- subject: The email subject line
- salutation: The greeting (e.g., "Dear John,")
- body: The main email content
- closing: The closing line (e.g., "Best regards,")
- signature: The sender's name/signature

*OUTPUT:*
Respond with a JSON object containing the structured email components.
"""

    def get_professional_email_system_prompt(self) -> str:
        """Return a PROFESSIONAL_EMAIL_PROMPT."""
        return """
You are an expert in crafting engaging and thoughtful professional emails. Your goal is to write a formal tone email that is tailored to the recipient and the specific context provided.

You must structure your response as a JSON object with the following fields:
- subject: The email subject line
- salutation: The greeting (e.g., "Dear Mr. Smith,")
- body: The main email content
- closing: The closing line (e.g., "Sincerely,")
- signature: The sender's name/signature

**Guidelines for generating an email:**
1. Start with an interesting subject line
2. Give greetings
3. Write the core email body
4. Include a closing line
5. End with a signature
6. Showcase professional etiquette

*OUTPUT:*
Respond with a JSON object containing the structured email components.
"""

    def get_marketing_email_system_prompt(self) -> str:
        """Return a MARKETING_EMAIL_PROMPT."""
        return """
You are an expert in crafting persuasive and effective marketing emails designed to promote products, services, and brands, and drive conversions. Your goal is to write an engaging email that captures the recipient's attention, highlights the value proposition, and encourages a specific action (e.g., clicking a link, making a purchase).

You must structure your response as a JSON object with the following fields:
- subject: The email subject line
- salutation: The greeting (e.g., "Hello there,")
- body: The main email content
- closing: The closing line (e.g., "Best wishes,")
- signature: The sender's name/signature

**INPUT:**

1.  **Target Audience:** (Describe the intended recipient segment. Be specific. E.g., "Existing customers who purchased the 'Pro' plan")

2.  **Product/Service:** (Clearly describe the product, service, or brand being promoted. Include key features and benefits. E.g., "Our new line of eco-friendly running shoes,")

3.  **Primary Goal:** (What is the desired outcome of this email? Be specific. E.g."Encourage users to upgrade to the 'Pro' plan,")

4.  **Key Selling Points:** (List 3-5 compelling reasons why the target audience should take the desired action. Focus on the benefits and value they'll receive. E.g."Easy-to-use features.")

5.  **Call to Action:** (Specify the desired action and how to perform it. Be clear and concise. E.g. "Visit our website and explore our new collection.")

6. **Content length:** (Specify the desired word count E.g. 200 words)

7.  **(Optional) Desired Tone:** (What overall tone do you want the email to convey? E.g., "Enthusiastic and energetic") If this is omitted, aim for a persuasive and benefit-driven tone.

**Guidelines for writing an email:**
1. Align your subject line and email content
2. Create relevancy
3. Personalize the email
4. Explain benefits
5. Be personable

**PROCESS:**

1.  **Understand:** Carefully review the "Target Audience," "Product/Service," "Primary Goal," "Key Selling Points," "Call to Action," "Content length" and "Desired Tone" (if provided).
2.  **Persuade & Engage:** Craft an email that effectively highlights the value proposition, addresses the target audience's needs and desires, and encourages them to take the specified action.
3.  **Structure:** Follow the guidelines to structure email.
4.  **Output:** Output a JSON object with the structured email components.

*OUTPUT:*
Respond with a JSON object containing the structured email components.
"""

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

    async def generate_email(self, message: str, email_type: str) -> str:
        """Generate an email of the specified type using an LLM."""
        try:
            system_prompt = self.get_email_prompt(email_type)
            return await self.make_llm_call(system_prompt, message)
        except ValueError as ve:
            logger.debug(f"ValueError: {ve}")
            return "Error: Invalid email type specified."
        except Exception as e:
            logger.debug(f"An error occurred: {e}")
            return "Error: An unexpected error occurred while generating the email."
