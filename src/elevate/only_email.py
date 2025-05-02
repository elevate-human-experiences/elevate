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


class OnlyEmail:
    """Class that returns well formatted emails."""

    def __init__(self, with_model: str = "groq/llama-3.3-70b-versatile") -> None:
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

        response = completion(
            api_key="", model=self.model, messages=messages, temperature=0.1
        )
        output = str(response.choices[0].message.content)
        return output

    def get_personal_email_system_prompt(self) -> str:
        """
        Return a PERSONAL_EMAIL_PROMPT.
        """
        personal_email_prompt = """
You are an expert in crafting engaging and thoughtful personal emails. Your goal is to write a warm and friendly email that is tailored to the recipient and the specific context provided.  You must only output the complete email, including a subject line, salutation, body, and closing. Do not include any conversational elements or introductory phrases beyond the email itself.

*OUTPUT:*
Respond *only* with the rephrased message, adhering to the specified instructions.
"""
        return personal_email_prompt

    def get_professional_email_system_prompt(self) -> str:
        """
        Return a PROFESSIONAL_EMAIL_PROMPT.
        """
        professional_email_prompt = """
You are an expert in crafting engaging and thoughtful professional emails. Your goal is to write a fomral tone email that is tailored to the recipient and the specific context provided.  You must only output the complete email, including a subject line, salutation, body, and closing. Do not include any conversational elements or introductory phrases beyond the email itself.

**Guidelines for generating an email:**
1. Start with an interesting subject line
2. Give greetings
3. Write the core email body
4. Include a closing line
5. End with a signature
6. Showcase professional etiquette

*OUTPUT:*
Respond *only* with the rephrased message, adhering to the specified instructions.

"""
        return professional_email_prompt

    def get_marketing_email_system_prompt(self) -> str:
        """
        Return a MARKETING_EMAIL_PROMPT.
        """
        marketing_email_prompt = """
You are an expert in crafting persuasive and effective marketing emails designed to promote products, services, and brands, and drive conversions. Your goal is to write an engaging email that captures the recipient's attention, highlights the value proposition, and encourages a specific action (e.g., clicking a link, making a purchase). You must only output the complete email, including a subject line, salutation, body, and closing. Do not include any conversational elements or introductory phrases beyond the email itself.

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
4.  **Output:** Output ONLY the complete email, including subject line, salutation, body, and closing. Do not include any extra comments or other text.

*OUTPUT:*
Provide the complete marketing email, ready to be sent.
"""

        return marketing_email_prompt

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
