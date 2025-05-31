import asyncio
from collections.abc import Callable
from pathlib import Path
from typing import Any

import aiofiles  # type: ignore
import fire
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from elevate.only_email import OnlyEmail
from elevate.only_markdown import OnlyMarkdown
from elevate.only_python import OnlyPython
from elevate.only_rephrase import OnlyRephrase
from elevate.only_summary import OnlySummary
from elevate.only_video_to_blog import OnlyVideoToBlog


console = Console()


class UIBeautifier:
    """Provides methods for beautifying the UI of the CLI application using Rich."""

    def print_section_header(self, title: str, color: str = "cyan") -> None:
        header = f"[bold {color}]{'*' * 3} {title} {'*' * 3}[/bold {color}]"
        console.rule(header)

    def print_colored_text(self, text: str, color: str = "green") -> None:
        console.print(f"[{color}]{text}[/{color}]")

    def print_menu(self, menu_items: dict[str, str], color: str = "yellow") -> None:
        self.print_section_header("Marketing Workflow Menu", color)
        table = Table(show_header=False, box=None)
        for key, value in menu_items.items():
            table.add_row(f"[{color}]{key}[/{color}]", value)
        console.print(table)
        console.rule()

    def print_prompt(self, prompt: str, color: str = "yellow") -> Any:
        return Prompt.ask(f"[{color}]{prompt}[/{color}]")


class MarketingWorkflow:
    def __init__(self) -> None:
        self.blog_generator = OnlyVideoToBlog("gemini/gemini-2.0-flash-lite")
        self.summary_generator = OnlySummary("gemini/gemini-2.0-flash-lite")
        self.email_generator = OnlyEmail("gemini/gemini-2.0-flash-lite")
        self.rephrase_tool = OnlyRephrase("gemini/gemini-2.0-flash-lite")
        self.python_tool = OnlyPython("gemini/gemini-2.0-flash-lite")
        self.markdown_tool = OnlyMarkdown("gemini/gemini-2.0-flash-lite")
        self.ui = UIBeautifier()  # Instantiate the beautifier

    async def rephrase_content(self, content: str) -> Any:
        self.ui.print_section_header("Rephrasing Content", "magenta")
        while True:
            tone = self.ui.print_prompt("Enter rephrase tone:", "yellow")
            length_str = self.ui.print_prompt("Enter rephrase message length in words:", "yellow")
            try:
                length = int(length_str)
            except ValueError:
                self.ui.print_colored_text("Invalid length. Please enter a number.", "red")
                continue
            self.ui.print_colored_text(f"Rephrasing with tone: {tone}, and length: {length}", "cyan")
            rephrased_content = await self.rephrase_tool.rephrase_text(content, tone, str(length))
            self.ui.print_colored_text("Rephrased content:", "green")
            console.print(rephrased_content)
            return rephrased_content

    async def process_with_rephrase(
        self,
        generate_func: Callable[..., Any],
        prompt: str,
        file_name: str,
        *args: Any,
    ) -> str:
        content = await generate_func(*args)
        self.ui.print_colored_text("Content generated:", "green")
        console.print(content)
        while True:
            rephrase = Prompt.ask(f"Rephrase {prompt}? (y/n)", choices=["y", "n"], default="n")
            if rephrase == "y":
                content = await self.rephrase_content(content)
            else:
                try:
                    Path("output").mkdir(parents=True, exist_ok=True)
                    with (Path("output") / file_name).open("w") as file:
                        file.write(content)
                    self.ui.print_colored_text(
                        f"Contents written in file output/{file_name}",
                        "blue",
                    )
                except Exception as e:
                    self.ui.print_colored_text(f"Error writing the contents to file: {e}", "red")
                break
        return str(content)

    async def generate_blog(self, video_transcript: str) -> str:
        """Generates and optionally rephrases a blog post."""
        self.ui.print_section_header("Generating Blog Post")
        return await self.process_with_rephrase(
            self.blog_generator.generate_blog,
            "blog content",
            "blog.txt",
            video_transcript,
        )

    async def generate_summary(self, video_transcript: str) -> str:
        """Generates and optionally rephrases a video summary."""
        self.ui.print_section_header("Generating Summary")
        return await self.process_with_rephrase(
            self.summary_generator.summarize_and_convert_to_markdown,
            "video summary",
            "summary.txt",
            video_transcript,
        )

    async def generate_emails(self, blog_content: str, email_type: str = "marketing") -> str:
        """Generates and optionally rephrases emails."""
        self.ui.print_section_header("Generating Emails")
        return await self.process_with_rephrase(
            self.email_generator.generate_email,
            "emails",
            "email.txt",
            blog_content,
            email_type,
        )

    async def generate_markdown(self, blog_content: str) -> str:
        """Generates and optionally rephrases markdown documentation."""
        self.ui.print_section_header("Generating Markdown Documentation")
        return await self.process_with_rephrase(
            self.markdown_tool.convert_to_markdown,
            "markdown documentation",
            "markdown.md",
            blog_content,
        )

    async def execute(self, video_transcript: str, email_type: str = "marketing") -> dict[str, str]:
        """Execute the marketing workflow based on user selection from the menu."""
        results: dict[str, str] = {}
        while True:
            self.print_menu()
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5"])
            if choice == "1":
                results["blog_content"] = await self.generate_blog(video_transcript)
            elif choice == "2":
                results["video_summary"] = await self.generate_summary(video_transcript)
            elif choice == "3":
                if "blog_content" not in results:
                    self.ui.print_colored_text("Please generate blog content first (option 1).", "red")
                    continue
                results["emails"] = await self.generate_emails(results["blog_content"], email_type)
            elif choice == "4":
                if "blog_content" not in results:
                    self.ui.print_colored_text("Please generate blog content first (option 1).", "red")
                    continue
                results["markdown_docs"] = await self.generate_markdown(results["blog_content"])
            elif choice == "5":
                self.ui.print_colored_text("Workflow Complete", "green")
                break
        return results

    def print_menu(self) -> None:
        """Prints the menu of available components."""
        menu_items = {
            "1": "Generate Blog Post",
            "2": "Generate Summary",
            "3": "Generate Emails",
            "4": "Generate Markdown Documentation",
            "5": "Exit",
        }
        self.ui.print_menu(menu_items)


def run_workflow(transcript_file: str, email_type: str = "marketing") -> None:
    """Run the marketing workflow CLI application."""

    async def _run() -> None:
        try:
            async with aiofiles.open(transcript_file) as f:
                video_transcript = await f.read()
        except FileNotFoundError:
            console.print(f"[red]Error: Transcript file not found at {transcript_file}[/red]")
            return
        except Exception as e:
            console.print(f"[red]Error reading transcript file: {e}[/red]")
            return
        workflow = MarketingWorkflow()
        results = await workflow.execute(video_transcript, email_type)
        console.print("[bold green]\nWorkflow Results:[/bold green]")
        for key, value in results.items():
            console.print(f"[cyan]{key}[/cyan]:\n{value}\n")

    asyncio.run(_run())


if __name__ == "__main__":
    fire.Fire(run_workflow)
