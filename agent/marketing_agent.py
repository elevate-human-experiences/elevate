import asyncio
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

import aiofiles  # type: ignore
import fire
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from elevate.only_demo_script import OnlyDemoScript
from elevate.only_email import OnlyEmail
from elevate.only_markdown import OnlyMarkdown
from elevate.only_python import OnlyPython
from elevate.only_qa import OnlyQA
from elevate.only_rephrase import OnlyRephrase
from elevate.only_slides import OnlySlides
from elevate.only_summary import OnlySummary
from elevate.only_video_to_blog import OnlyVideoToBlog


# VERY IMPORTANT: Disable LiteLLM verbose logging before any imports or code that uses litellm.
os.environ["LITELLM_VERBOSE"] = "0"

console = Console()

# Global flag for LiteLLM logging
litellm_logging_enabled = False


class UIBeautifier:
    """Provides methods for beautifying the UI of the CLI application using Rich."""

    def print_title(self, title: str) -> None:
        """
        Prints the title of the application within a Rich Panel.

        Args:
        ----
            title: The title to display.
        """
        console.print(Panel(f"[bold blue]{title}[/bold blue]", border_style="blue", padding=1, box=box.DOUBLE))

    def print_section_header(self, title: str, color: str = "cyan") -> None:
        """
        Prints a section header using a Rich rule.

        Args:
        ----
            title: The title of the section.
            color: The color of the rule and title.
        """
        console.rule(f"[bold {color}]{title}[/bold {color}]", style=color)

    def print_colored_text(self, text: str, color: str = "green") -> None:
        """
        Prints text with a specified color.

        Args:
        ----
            text: The text to print.
            color: The color of the text.
        """
        console.print(f"[{color}]{text}[/{color}]")

    def print_menu(self, menu_items: dict[str, str]) -> None:
        """
        Prints a menu using a Rich table.

        Args:
        ----
            menu_items: A dictionary where keys are menu item keys and values are descriptions.
        """
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column(style="cyan", justify="right")
        table.add_column(style="white")
        for key, value in menu_items.items():
            table.add_row(f"[{key}]", value)
        console.print(table)

    def get_user_input(self, prompt: str, color: str = "yellow", choices: list[str] | None = None) -> Any:
        """
        Prompts the user for input with a specified color.

        Args:
        ----
            prompt: The prompt message to display to the user.
            color: The color of the prompt. Defaults to "yellow".
            choices: An optional list of valid choices. If provided, the prompt will enforce selection from these choices.

        Returns:
        -------
            The user's input as a string.
        """
        prompt_text = f"[bold {color}]{prompt}[/bold {color}]"
        panel = Panel(
            prompt_text, box=box.ROUNDED, border_style=color, padding=1, title="[bold]Input[/bold]", title_align="left"
        )
        console.print(panel, end="> ")  # Print the panel and the > symbol
        return Prompt.ask("")  # Use an empty string to only show the cursor

    def get_integer_input(self, prompt: str, color: str = "yellow", default: int | None = None) -> Any:
        """
        Prompts the user for integer input with validation and an optional default value.

        Args:
        ----
            prompt: The prompt message to display to the user.
            color: The color of the prompt.
            default: An optional default integer value.

        Returns:
        -------
            The user's input as an integer.
        """
        prompt_text = f"[bold {color}]{prompt}[/bold {color}]"
        panel = Panel(
            prompt_text, box=box.ROUNDED, border_style=color, padding=1, title="[bold]Input[/bold]", title_align="left"
        )
        console.print(panel, end="> ")  # Print the panel and the > symbol
        return IntPrompt.ask("")

    def print_markdown(self, content: str, title: str = "Content") -> None:
        """
        Prints content as Markdown with a title.

        Args:
        ----
            content: The Markdown content to print.
            title: The title to display above the Markdown.
        """
        self.print_section_header(title, "green")
        md = Markdown(content)
        console.print(md)

    def print_content(self, content: str, title: str = "Content") -> None:
        """
        Prints content within a Rich Panel.

        Args:
        ----
            content: The content to print.
            title: The title of the Panel.
        """
        self.print_section_header(title, "green")
        console.print(Panel(content, title=title, border_style="green"))

    def print_success(self, message: str) -> None:
        """
        Prints a success message.

        Args:
        ----
            message: The message to display.
        """
        console.print(f"[bold green][✓] {message}[/bold green]")

    def print_error(self, message: str) -> None:
        """
        Prints an error message.

        Args:
        ----
            message: The error message to display.
        """
        console.print(f"[bold red][X] {message}[/bold red]")


class MarketingWorkflow:
    """Orchestrates marketing content generation workflows."""

    def __init__(self) -> None:
        """Initializes the MarketingWorkflow with language model and tools."""
        llm = "gemini/gemini-2.0-flash-lite"  # Consider making this configurable via CLI
        self.blog_generator = OnlyVideoToBlog(llm)
        self.summary_generator = OnlySummary(llm)
        self.email_generator = OnlyEmail(llm)
        self.rephrase_tool = OnlyRephrase(llm)
        self.python_tool = OnlyPython(llm)
        self.markdown_tool = OnlyMarkdown(llm)
        self.slide_tool = OnlySlides(llm)
        self.demo_script_tool = OnlyDemoScript(llm)
        self.qa_tool = OnlyQA(llm)
        self.ui = UIBeautifier()

    async def rephrase_content(self, content: str) -> Any:
        """
        Rephrases content based on user-specified tone and length.

        Args:
        ----
            content: The content to rephrase.

        Returns:
        -------
            The rephrased content.
        """
        self.ui.print_section_header("Rephrasing Content", "magenta")
        while True:
            tone = self.ui.get_user_input("Enter rephrase tone:", "yellow")
            length_str = self.ui.get_user_input("Enter rephrase message length in words:", "yellow")
            try:
                length = int(length_str)
                if length <= 0:
                    self.ui.print_error("Length must be a positive integer.")
                    continue
            except ValueError:
                self.ui.print_error("Invalid length. Please enter a number.")
                continue

            self.ui.print_colored_text(f"Rephrasing with tone: {tone}, and length: {length}", "cyan")
            rephrased_content = await self.rephrase_tool.rephrase_text(content, tone, str(length))
            self.ui.print_content(rephrased_content, title="Rephrased content")
            return rephrased_content

    async def process_with_rephrase(
        self,
        generate_func: Callable[..., Any],
        prompt: str,
        file_name: str,
        *args: Any,
    ) -> Any:
        """
        Processes content with an optional rephrase step and saves to a file.

        Args:
        ----
            generate_func: The function to generate the initial content.
            prompt: The prompt to display to the user when asking about rephrasing.
            file_name: The name of the file to save the content to.
            *args: Arguments to pass to the generate_func.

        Returns:
        -------
            The generated (and possibly rephrased) content.
        """
        content = await generate_func(*args)
        self.ui.print_content(content, title="Generated Content")

        while True:
            rephrase_choice = self.ui.get_user_input(
                f"Do you want to rephrase the {prompt}? (y/n)", "yellow", choices=["y", "n"]
            )
            if rephrase_choice.lower() == "y":
                content = await self.rephrase_content(content)
            else:
                try:
                    output_dir = Path("output")
                    output_dir.mkdir(parents=True, exist_ok=True)
                    file_path = output_dir / file_name
                    async with aiofiles.open(file_path, "w") as file:
                        await file.write(content)
                    self.ui.print_success(f"Contents written to file: {file_path}")
                except Exception as e:
                    self.ui.print_error(f"Error writing content to file: {e}")
                break
        return content

    async def generate_blog(self, technical_content: str, number_of_words: int) -> Any:
        """
        Generates a blog post and handles optional rephrasing.

        Args:
        ----
            technical_content: The technical content to base the blog post on.
            number_of_words: The desired number of words for the blog post.

        Returns:
        -------
            The generated (and possibly rephrased) blog post.
        """
        self.ui.print_section_header("Generating Blog Post")
        return await self.process_with_rephrase(
            self.blog_generator.generate_blog,
            "blog content",
            "blog.md",
            technical_content,
            number_of_words,
        )

    async def generate_summary(self, technical_content: str, summary_type: str) -> Any:
        """
        Generates a summary of the provided content.

        Args:
        ----
            technical_content: The technical content to summarize.
            summary_type: The type of summary to generate (e.g., "Executive Summary").

        Returns:
        -------
            The generated (and possibly rephrased) summary.
        """
        self.ui.print_section_header("Generating Summary")
        return await self.process_with_rephrase(
            self.summary_generator.summarize_and_convert_to_markdown,
            "video summary",
            "summary.md",
            technical_content,
            summary_type,
        )

    async def generate_emails(self, technical_content: str, email_type: str = "marketing") -> Any:
        """
        Generates marketing emails based on the given content.

        Args:
        ----
            technical_content: The technical content to base the emails on.
            email_type: The type of email to generate (e.g., "marketing").

        Returns:
        -------
            The generated (and possibly rephrased) emails.
        """
        self.ui.print_section_header("Generating Emails")
        return await self.process_with_rephrase(
            self.email_generator.generate_email,
            "emails",
            "email.md",
            technical_content,
            email_type,
        )

    async def generate_markdown(self, technical_content: str) -> Any:
        """
        Generates markdown documentation from the given content.

        Args:
        ----
            technical_content: The technical content to convert to Markdown.

        Returns:
        -------
            The generated (and possibly rephrased) Markdown documentation.
        """
        self.ui.print_section_header("Generating Markdown Documentation")
        return await self.process_with_rephrase(
            self.markdown_tool.convert_to_markdown,
            "markdown.md",
            "markdown.md",
            technical_content,
        )

    async def generate_slides(self, technical_content: str, type_of_slides: str, number_of_slides: int) -> Any:
        """
        Generates slides in Markdown format.

        Args:
        ----
            technical_content: The technical content to base the slides on.
            type_of_slides: The type of slides to generate (e.g., "presentation").
            number_of_slides: The number of slides to generate.

        Returns:
        -------
            The generated (and possibly rephrased) slides.
        """
        self.ui.print_section_header("Generating Slides")
        return await self.process_with_rephrase(
            self.slide_tool.generate_slides,
            "slides",
            "slides.md",
            technical_content,
            type_of_slides,
            number_of_slides,
        )

    async def generate_demo_script(
        self, technical_content: str, presentation_type: str, demo_length_in_minutes: int
    ) -> Any:
        """
        Generates a demo script in Markdown format.

        Args:
        ----
            technical_content: The technical content to base the demo script on.
            presentation_type: The type of presentation (e.g., "product demo").
            demo_length_in_minutes: The desired length of the demo in minutes.

        Returns:
        -------
            The generated (and possibly rephrased) demo script.
        """
        self.ui.print_section_header("Generating Demo Script")
        return await self.process_with_rephrase(
            self.demo_script_tool.generate_demo_script,
            "demo script",
            "demo_script.md",
            technical_content,
            presentation_type,
            demo_length_in_minutes,
        )

    async def generate_answers(self, technical_content: str, question: str) -> Any:
        """
        Generates answers to questions based on technical content.

        Args:
        ----
            technical_content: The technical content to use for answering the question.
            question: The question to answer.

        Returns:
        -------
            The generated answer.
        """
        self.ui.print_section_header("Generating Answers")
        answer = await self.qa_tool.generate_answers(technical_content + "\n" + question)
        self.ui.print_content(answer, title="Answer")
        return answer

    async def execute(self, technical_content: str, email_type: str = "marketing") -> dict[str, str]:
        """
        Executes the marketing workflow based on user selection from the menu.

        Args:
        ----
            technical_content: The technical content to use for the workflow.
            email_type: The type of email to generate (e.g., "marketing").

        Returns:
        -------
            A dictionary containing the results of the workflow.
        """
        results: dict[str, str] = {}

        menu_items = {
            "1": "Generate Blog Post",
            "2": "Generate Summary",
            "3": "Generate External marketing emails",
            "4": "Generate Slides in Markdown format",
            "5": "Generate Demo script in Markdown format",
            "6": "Q&A",
            "7": "Exit",
        }

        while True:
            self.ui.print_menu(menu_items)
            choice = self.ui.get_user_input("Enter your choice", "yellow", choices=list(menu_items.keys()))

            if choice == "1":
                number_of_words = self.ui.get_integer_input(
                    "Enter the desired number of words for the blog:", "yellow", default=500
                )
                results["blog_content"] = await self.generate_blog(technical_content, number_of_words=number_of_words)

            elif choice == "2":
                self.ui.print_section_header("Choose Summary Type", "yellow")
                summary_choices = {
                    "1": "Executive Summary",
                    "2": "LinkedIn Post",
                    "3": "Press Release",
                }
                self.ui.print_menu(summary_choices)
                summary_type_choice = self.ui.get_user_input(
                    "Choose summary type", "yellow", choices=list(summary_choices.keys())
                )
                summary_type = summary_choices[summary_type_choice]
                results["video_summary"] = await self.generate_summary(technical_content, summary_type)

            elif choice == "3":
                results["emails"] = await self.generate_emails(technical_content, email_type)

            elif choice == "4":
                self.ui.print_section_header("Generate Slides", "yellow")
                type_of_slides = self.ui.get_user_input(
                    "Please type of presentation that you would like to generate (Technical/Business):", "yellow"
                )
                number_of_slides = self.ui.get_integer_input(
                    "Please enter number of slides to generate:", "yellow", default=10
                )
                results["slides"] = await self.generate_slides(technical_content, type_of_slides, number_of_slides)

            elif choice == "5":
                self.ui.print_section_header("Generate Demo Script", "yellow")
                presentation_type = self.ui.get_user_input(
                    "Please type of demo that you would like to generate (Technical/Business):", "yellow"
                )
                demo_length_in_minutes = self.ui.get_integer_input(
                    "Please enter demo length in minutes:", "yellow", default=5
                )
                results["demo_script"] = await self.generate_demo_script(
                    technical_content, presentation_type, demo_length_in_minutes
                )

            elif choice == "6":
                while True:
                    question = self.ui.get_user_input("Please enter your question:", "yellow")
                    results["answer"] = await self.generate_answers(technical_content, question)
                    qa_choices = {
                        "1": "Ask another question",
                        "2": "Exit Q&A",
                    }
                    self.ui.print_menu(qa_choices)
                    qa_choice = self.ui.get_user_input("Choose an action", "yellow", choices=list(qa_choices.keys()))
                    if qa_choice == "2":
                        break

            elif choice == "7":
                self.ui.print_success("Workflow Complete!")
                break

            else:
                self.ui.print_error("Invalid choice. Please try again.")

        return results


def run_workflow(transcript_file: str, email_type: str = "marketing") -> None:
    """
    Runs the marketing workflow CLI application.

    Args:
    ----
        transcript_file: The path to the transcript file.
        email_type: The type of email to generate.
    """

    async def _run() -> None:
        workflow = MarketingWorkflow()
        workflow.ui.print_title("Marketing Workflow CLI")  # Print the title

        try:
            async with aiofiles.open(transcript_file) as f:
                technical_content = await f.read()
        except FileNotFoundError:
            workflow.ui.print_error(f"Transcript file not found at {transcript_file}")
            return
        except Exception as e:
            workflow.ui.print_error(f"Error reading transcript file: {e}")
            return

        results = await workflow.execute(technical_content, email_type)

        workflow.ui.print_section_header("Workflow Results", "blue")
        for key, value in results.items():
            workflow.ui.print_markdown(value, title=key.replace("_", " ").title())

    asyncio.run(_run())


if __name__ == "__main__":
    fire.Fire(run_workflow)
