from typing import Type
from pydantic import BaseModel
from litellm import completion


class OnlyJudgeLLMs:
    """
    Class to evaluate LLM outputs based on defined scoring criteria.

    This evaluation uses an LLM call to transform the provided text into a structured JSON
    evaluation that strictly conforms to a given Pydantic schema (which defines the scoring criteria).
    """

    def __init__(self, with_model: str = "o3-mini") -> None:
        """
        Initialize the OnlyJudgeLLMs class with the specified LLM model.

        Args:
            with_model: Identifier for the LLM model.
        """
        self.model = with_model

    def get_judgment_prompt(self) -> str:
        """
        Constructs a system prompt that instructs the LLM to evaluate the text based on provided criteria,
        acknowledging that each criterion may have a different scoring or assessment format.
        The prompt encourages step-by-step reasoning and planning on how to judge each criterion,
        then asks for a strictly valid JSON response matching the schema.
        """
        prompt = (
            "You are an expert evaluator of LLM outputs. You have been given multiple criteria, and each "
            "criterion might use a different method of assessment (e.g., a numerical scale, a boolean check, "
            "a pass/fail judgment, or something else entirely).\n\n"
            "Your task is to:\n"
            "1. Identify the type of rating/assessment required for each criterion as indicated by the schema.\n"
            "2. Plan how you will judge each criterion based on the provided text.\n"
            "3. Carefully analyze the text to assess how well it meets each criterion.\n"
            "4. Assign the correct rating or answer for each criterion (e.g., if it's a numeric scale, choose a value "
            "within that range; if it's a boolean check, choose the appropriate true/false or pass/fail).\n"
            "5. Provide a brief factual justification for each rating or assessment, using direct references or "
            "observations from the text.\n\n"
            "Important:\n"
            "- If a numeric scale is provided, use the full range realistically. Do not default to the highest or lowest "
            "score unless it is justified.\n"
            "- Return only a valid JSON object that exactly matches the schema—no extra commentary or text outside "
            "the JSON.\n"
            "- Do not reveal your internal chain-of-thought; simply provide the final ratings and justifications.\n"
        )
        return prompt

    def evaluate(
        self, text: str, criteria: Type[BaseModel], system_prompt: str | None = None
    ) -> BaseModel:
        """
        Evaluates the given text against the scoring criteria defined in the Pydantic model.

        This method builds an evaluation prompt (unless one is provided), makes an LLM call, and then parses
        the resulting JSON into an instance of the scoring criteria model.

        Args:
            text: The LLM output text to be evaluated.
            criteria: A Pydantic model representing the scoring criteria.
            system_prompt: An optional custom system prompt to override the default evaluation prompt.

        Returns:
            An instance of the criteria model populated with the evaluation metrics.

        Raises:
            ValueError: If the output cannot be parsed according to the criteria schema.
        """
        if system_prompt is None:
            system_prompt = self.get_judgment_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
        response = completion(
            model=self.model,
            messages=messages,
            response_format=criteria,
        )
        try:
            evaluation_result = criteria.model_validate_json(
                response.choices[0].message.content
            )
        except Exception as e:
            raise ValueError(
                f"Failed to parse evaluation result: {e}\nOutput received: {response.choices[0].message}"
            )
        return evaluation_result
