from fire import Fire
from prompt_toolkit import prompt

import sys
from pathlib import Path

# Add the "src" folder to the PYTHONPATH for pytest
sys.path.insert(0, Path(__file__).resolve().parent.parent.joinpath("src").as_posix())


def main(with_model: str = "gpt-4o-mini") -> None:
    """Run the command-line interface."""
    print("Welcome to the Elevate CLI Agent!")
    print("Type 'exit' to quit.")
    print("Using model:", with_model)
    print("You can start typing your queries below:")
    while True:
        user_input = prompt("You: ")
        if user_input.lower() == "exit":
            break
        # Here you would call the LLM with the user input
        # For now, we'll just echo it back
        print(f"Elevate: {user_input}")


if __name__ == "__main__":
    Fire(main)
