import asyncio
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from elevate.only_python import OnlyPython


console = Console()


def select_genai_snippet(menu_input: str) -> str:
    match menu_input:
        case "1":
            return "only_email/__init__.py"
        case "2":
            return "only_rephrase/__init__.py"
        case _:
            raise ValueError("Invalid menu type specified.")


def read_geni_snippet(genai_snippet: str) -> str:
    with Path(genai_snippet).open() as file:
        return file.read()


async def main(with_model: str = "gpt-4o-mini") -> None:
    """Run the command-line interface."""
    console.print("[bold green]Welcome to the Elevate CLI Agent![/bold green]")
    console.print(f"[yellow]Using model: {with_model}[/yellow]")
    while True:
        console.print("\n[bold cyan]Menu[/bold cyan]\n1. Generate an email\n2. Reframe the message\n3. Exit")
        menu_input = Prompt.ask("[bold blue]Enter your choice[/bold blue]")
        if menu_input.lower() == "3":
            break
        user_input = Prompt.ask("[magenta]Enter your prompt[/magenta]")
        only_python = OnlyPython()
        from elevate.only_python import PythonInput

        input_data = PythonInput(task=user_input, purpose="CLI automation", experience_level="intermediate")
        output = await only_python.create_code(input_data)
        console.print(f"[green]\nOutput:[/green]\n{output}")


if __name__ == "__main__":
    asyncio.run(main())
