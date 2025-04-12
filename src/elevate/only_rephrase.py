from dotenv import load_dotenv
from litellm import completion

from elevate.only_rephrase_prompt import REPHRASE_PROMPT

# Load environment variables
load_dotenv()


class OnlyRephrase:
    """Class that returns rephrased text."""

    def __init__(self, with_model: str = "gemini/gemini-2.0-flash-lite") -> None:
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

    def get_rephrase_system_prompt(self) -> str:
        """Returns the rephrase system prompt.

        Returns:
            str: A string containing the rephrase system prompt.
        """
        return REPHRASE_PROMPT

    def rephrase_text(self, message: str, tone: str, length: str) -> str:
        """Rephrases the given message with the specified tone and length.

        Args:
            message (str): The message to rephrase.
            tone (str): The desired tone for the rephrased message.
            length (str): The desired length for the rephrased message.

        Returns:
            str: The rephrased message.
        """
        system_prompt = self.get_rephrase_system_prompt()

        message = "\n<Message>" + message + "</Message>\n\n"
        message += "<Tone> " + tone + " </Tone>\n\n"
        message += "<Length> " + length + " </Length>"

        return self.make_llm_call(system_prompt, message)
