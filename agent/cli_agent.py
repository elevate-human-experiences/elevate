import asyncio
import logging
from pathlib import Path

from common import setup_logging
from elevate.only_python import OnlyPython


logger = setup_logging(logging.DEBUG)


def select_genai_snippet(menu_input: str) -> str:
    match menu_input:
        case "1":
            return "only_email.py"
        case "2":
            return "only_rephrase.py"
        case _:
            raise ValueError("Invalid menu type specified.")


def read_geni_snippet(genai_snippet: str) -> str:
    with Path(genai_snippet).open() as file:
        return file.read()


async def main(with_model: str = "gpt-4o-mini") -> None:
    """Run the command-line interface."""
    logger.debug("Welcome to the Elevate CLI Agent!")
    logger.debug(f"Using model: {with_model}")
    while True:
        logger.debug("\nMenu \n1. Genrate an email \n2. Reframe the message\n3. exit")
        menu_input = input("Enter your choice: ")
        if menu_input.lower() == "3":
            break
        user_input = input("Enter your prompt: ")
        genai_snippet_code_file_name = "src/elevate/" + select_genai_snippet(menu_input)
        genai_snippet_code = read_geni_snippet(genai_snippet_code_file_name)
        only_python = OnlyPython()
        output = await only_python.generate_code(user_input, "", False, False, genai_snippet_code)
        logger.debug(f"\nOutput:\n{output}")


if __name__ == "__main__":
    asyncio.run(main())
