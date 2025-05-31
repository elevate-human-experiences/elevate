import asyncio
import logging
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

import aiofiles  # type: ignore
import fire

from common import setup_logging
from elevate.only_email import OnlyEmail
from elevate.only_markdown import OnlyMarkdown
from elevate.only_python import OnlyPython
from elevate.only_rephrase import OnlyRephrase
from elevate.only_summary import OnlySummary
from elevate.only_video_to_blog import OnlyVideoToBlog


logger = setup_logging(logging.DEBUG)


class UIBeautifier:
    """Provides methods for beautifying the UI of the CLI application."""

    COLOR_RESET = "\033[0m"  # Reset to default color
    COLOR_GREEN = "\033[92m"
    COLOR_YELLOW = "\033[93m"
    COLOR_RED = "\033[91m"
    COLOR_BLUE = "\033[94m"
    COLOR_MAGENTA = "\033[95m"
    COLOR_CYAN = "\033[96m"

    def print_section_header(self, title: str, color: str = COLOR_CYAN) -> None:
        """Print a formatted section header with color."""
        width = os.get_terminal_size().columns
        padding = (width - len(title) - 2) // 2
        header = f"{color}{'*' * padding} {title} {'*' * padding}{self.COLOR_RESET}"
        logger.debug(f"{header.center(width)}\n")

    def print_colored_text(self, text: str, color: str = COLOR_GREEN) -> None:
        """Print text with a specified color."""
        logger.debug(f"{color}{text}{self.COLOR_RESET}\n")

    def print_menu(self, menu_items: dict[str, str], color: str = COLOR_YELLOW) -> None:
        """Print a formatted menu with color."""
        self.print_section_header("Marketing Workflow Menu", color)
        for key, value in menu_items.items():
            self.print_colored_text(f"{key}. {value}", color)
        logger.debug("%s", "*" * os.get_terminal_size().columns + "\n")

    def print_prompt(self, prompt: str, color: str = COLOR_YELLOW) -> str:
        """Print a colored prompt and return user input."""
        return input(f"{color}{prompt}{self.COLOR_RESET}")


class MarketingWorkflow:
    def __init__(self) -> None:
        self.blog_generator = OnlyVideoToBlog("gemini/gemini-2.0-flash-lite")
        self.summary_generator = OnlySummary("gemini/gemini-2.0-flash-lite")
        self.email_generator = OnlyEmail("gemini/gemini-2.0-flash-lite")
        self.rephrase_tool = OnlyRephrase("gemini/gemini-2.0-flash-lite")
        self.python_tool = OnlyPython("gemini/gemini-2.0-flash-lite")
        self.markdown_tool = OnlyMarkdown("gemini/gemini-2.0-flash-lite")
        self.ui = UIBeautifier()  # Instantiate the beautifier

    async def rephrase_content(self, content: str) -> str:
        """Rephrase the given content with user-specified tone and length, beautified."""
        self.ui.print_section_header("Rephrasing Content", self.ui.COLOR_MAGENTA)
        while True:
            tone = self.ui.print_prompt("Enter rephrase tone: ", self.ui.COLOR_YELLOW)
            length_str = self.ui.print_prompt("Enter rephrase message length in words: ", self.ui.COLOR_YELLOW)
            try:
                length = int(length_str)
            except ValueError:
                logger.debug(", Invalid length. Please enter a number. , \n")
                continue
            logger.debug(f"\nRephrasing with tone: {tone}, and length: {length} \n")
            rephrased_content = await self.rephrase_tool.rephrase_text(content, tone, str(length))
            self.ui.print_colored_text("Rephrased content:\n", self.ui.COLOR_GREEN)
            logger.debug(f"{rephrased_content}\n")
            return rephrased_content

    async def process_with_rephrase(
        self,
        generate_func: Callable[..., Any],
        prompt: str,
        file_name: str,
        *args: Any,
    ) -> str:
        """Generate content and repeatedly rephrase it based on user input."""
        content = await generate_func(*args)
        self.ui.print_colored_text("Content generated:\n\n", self.ui.COLOR_GREEN)
        logger.debug(f"{content}\n")
        while True:
            rephrase = input(f"Rephrase {prompt}? (y/n): ").lower()
            if rephrase == "y":
                content = await self.rephrase_content(content)
            else:
                try:
                    Path("output").mkdir(parents=True, exist_ok=True)
                    with (Path("output") / file_name).open("w") as file:
                        file.write(content)
                    self.ui.print_colored_text(
                        f"Contents written in file output/{file_name}",
                        self.ui.COLOR_BLUE,
                    )
                except Exception as e:
                    logger.debug(f"Error writing the contents to file {e}")
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
            choice = input("Enter your choice: ")
            if choice == "1":
                results["blog_content"] = await self.generate_blog(video_transcript)
            elif choice == "2":
                results["video_summary"] = await self.generate_summary(video_transcript)
            elif choice == "3":
                if "blog_content" not in results:
                    logger.debug(", Please generate blog content first (option 1). , \n")
                    continue
                results["emails"] = await self.generate_emails(results["blog_content"], email_type)
            elif choice == "4":
                if "blog_content" not in results:
                    logger.debug(", Please generate blog content first (option 1). , \n")
                    continue
                results["markdown_docs"] = await self.generate_markdown(results["blog_content"])
            elif choice == "5":
                self.ui.print_colored_text("Workflow Complete", self.ui.COLOR_GREEN)
                break
            else:
                logger.debug(", Invalid choice. Please try again. , \n")
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
            logger.debug(f"Error: Transcript file not found at {transcript_file}")
            return
        except Exception as e:
            logger.debug(f"Error reading transcript file: {e}")
            return
        workflow = MarketingWorkflow()
        results = await workflow.execute(video_transcript, email_type)
        logger.debug("\nWorkflow Results:")
        for key, value in results.items():
            logger.debug(f"\n{key}:\n{value}\n")

    asyncio.run(_run())


if __name__ == "__main__":
    fire.Fire(run_workflow)
