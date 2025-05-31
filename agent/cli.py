import logging
import sys
from pathlib import Path

from fire import Fire
from prompt_toolkit import prompt

from common import setup_logging


logger = setup_logging(logging.DEBUG)


# Add the "src" folder to the PYTHONPATH for pytest
sys.path.insert(0, Path(__file__).resolve().parent.parent.joinpath("src").as_posix())


def main(with_model: str = "gpt-4o-mini") -> None:
    """Run the command-line interface."""
    logger.debug("Welcome to the Elevate CLI Agent!")
    logger.debug("Type 'exit' to quit.")
    logger.debug(f"Using model: {with_model}")
    logger.debug("You can start typing your queries below:")
    while True:
        user_input = prompt("You: ")
        if user_input.lower() == "exit":
            break
        logger.debug(f"Elevate: {user_input}")


if __name__ == "__main__":
    Fire(main)
