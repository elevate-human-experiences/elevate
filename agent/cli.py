import asyncio
import sys
import traceback

from dotenv import load_dotenv
from fire import Fire
from litellm import acompletion
from rich.console import Console
from rich.prompt import Prompt

from common import setup_logging


logger = setup_logging(logging.DEBUG)

console = Console()


async def main(with_model: str = "anthropic/claude-3-7-sonnet-20250219") -> None:
    """Run the command-line interface for the Elevate CLI Agent."""
    load_dotenv()
    console.print("[bold green]Welcome to the Elevate CLI Agent![/bold green]")
    console.print("[bold white]Type 'exit' to quit.[/bold white]")
    console.print(f"[bold white]Using model: {with_model}[/bold white]")
    console.print("[bold white]You can start typing your queries below:[/bold white]\n")

    messages = []
    try:
        while True:
            user_input = Prompt.ask("[yellow]User[/yellow]")
            if user_input.lower() == "exit":
                break

            messages.append({"role": "user", "content": user_input})

            # ————————————
            # Start a streaming Claude call with “thinking” enabled
            # ————————————
            stream = await acompletion(
                model=with_model,
                messages=messages,
                thinking={"type": "enabled", "budget_tokens": 2048},
                allowed_openai_params=["thinking"],
                stream=True,
            )

            thinking_started = False
            answer_started = False
            full_assistant_content = ""

            # ————————————
            # Process each streamed chunk
            # ————————————
            async for chunk in stream:
                delta = None
                if isinstance(chunk, dict) and "choices" in chunk:
                    choices = chunk["choices"]
                    if isinstance(choices, list) and len(choices) > 0:
                        delta = choices[0].get("delta", {})
                else:
                    choices = getattr(chunk, "choices", None)
                    if isinstance(choices, list) and len(choices) > 0:
                        delta = getattr(choices[0], "delta", {})

                if not delta:
                    continue

                # ————————————
                # 1) If this delta has reasoning_content, print it and flush immediately
                # ————————————
                if delta.get("reasoning_content"):
                    token = delta["reasoning_content"]
                    if not thinking_started:
                        thinking_started = True
                        console.print(
                            "[cyan]Assistant (Thinking):[/cyan] ",
                            end="",
                            highlight=False,
                        )
                    console.print(token, end="", highlight=False)
                    # Force the console to flush so the user sees reasoning in real time:
                    console.file.flush()

                # ————————————
                # 2) If this same delta also has content, insert a newline first
                # ————————————
                if delta.get("content"):
                    token = delta["content"]
                    if not answer_started:
                        answer_started = True
                        if thinking_started:
                            console.print()  # finish thinking line
                        console.print("[blue]Assistant:[/blue] ", end="", highlight=False)
                        console.file.flush()  # flush before streaming content
                    console.print(token, end="", highlight=False)
                    full_assistant_content += token
                    console.file.flush()  # ensure the answer tokens appear as they stream

            # After the stream ends, break line & append the assistant's content to history
            console.print("\n")
            if not full_assistant_content.strip():
                full_assistant_content = "[no content received]"
            messages.append({"role": "assistant", "content": full_assistant_content})

    except (KeyboardInterrupt, asyncio.CancelledError):
        console.print("\n[red]Keyboard interrupt received. Exiting gracefully.[/red]")
        return
    except Exception:
        console.print("[red]❌ Error communicating with the model.[/red]")
        traceback.print_exc(file=sys.stderr)


def fire_main(with_model: str = "anthropic/claude-3-7-sonnet-20250219") -> None:
    asyncio.run(main(with_model=with_model))

if __name__ == "__main__":
    Fire(fire_main)
