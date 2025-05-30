import fire
import os
from typing import Dict, Any, Callable

from elevate.only_video_to_blog import OnlyVideoToBlog
from elevate.only_summary import OnlySummary
from elevate.only_email import OnlyEmail
from elevate.only_rephrase import OnlyRephrase
from elevate.only_python import OnlyPython
from elevate.only_markdown import OnlyMarkdown


class UIBeautifier:
    """
    Provides methods for beautifying the UI of the CLI application.
    """

    COLOR_RESET = "\033[0m"  # Reset to default color
    COLOR_GREEN = "\033[92m"
    COLOR_YELLOW = "\033[93m"
    COLOR_RED = "\033[91m"
    COLOR_BLUE = "\033[94m"
    COLOR_MAGENTA = "\033[95m"
    COLOR_CYAN = "\033[96m"

    def print_section_header(self, title: str, color: str = COLOR_CYAN) -> None:
        """Prints a formatted section header with color."""
        width = os.get_terminal_size().columns  # Use terminal width
        padding = (width - len(title) - 2) // 2  # Calculate padding
        header = "{}{}{}{}".format(
            color, "*" * padding, " " + title + " ", "*" * padding + self.COLOR_RESET
        )
        print(header.center(width) + "\n")  # Center the header

    def print_colored_text(self, text: str, color: str = COLOR_GREEN) -> None:
        """Prints text with a specified color."""
        print(f"{color}{text}{self.COLOR_RESET}\n")

    def print_menu(self, menu_items: Dict[str, str], color: str = COLOR_YELLOW) -> None:
        """Prints a formatted menu with color."""
        self.print_section_header("Marketing Workflow Menu", color)
        for key, value in menu_items.items():
            self.print_colored_text(f"{key}. {value}", color)
        # Use full terminal width
        print("*" * os.get_terminal_size().columns + "\n")

    def print_prompt(self, prompt: str, color: str = COLOR_YELLOW) -> str:
        """Prints a colored prompt and returns user input."""
        return input(f"{color}{prompt}{self.COLOR_RESET}")


class MarketingWorkflow:
    def __init__(self) -> None:
        # self.config = config or {} #Removed
        self.blog_generator = OnlyVideoToBlog("gemini/gemini-2.0-flash-lite")
        self.summary_generator = OnlySummary("gemini/gemini-2.0-flash-lite")
        self.email_generator = OnlyEmail("gemini/gemini-2.0-flash-lite")
        self.rephrase_tool = OnlyRephrase("gemini/gemini-2.0-flash-lite")
        self.python_tool = OnlyPython("gemini/gemini-2.0-flash-lite")
        self.markdown_tool = OnlyMarkdown("gemini/gemini-2.0-flash-lite")
        self.ui = UIBeautifier()  # Instantiate the beautifier

    def rephrase_content(self, content: str) -> str:
        """Rephrases the given content with user-specified tone and length, beautified."""
        self.ui.print_section_header("Rephrasing Content", self.ui.COLOR_MAGENTA)
        # Add Pattern
        # print("*********************************************************************\n")
        while True:
            tone = self.ui.print_prompt(
                "Enter rephrase tone: ", self.ui.COLOR_YELLOW
            )  # Use print_prompt
            length_str = self.ui.print_prompt(
                "Enter rephrase message length in words: ", self.ui.COLOR_YELLOW
            )  # Use print_prompt
            try:
                length = int(length_str)
            except ValueError:
                print(
                    "{}, Invalid length. Please enter a number. {}, \n".format(
                        self.ui.COLOR_RED, self.ui.COLOR_RESET
                    )
                )
                continue

            print(f"\nRephrasing with tone: {tone}, and length: {length} \n")
            rephrased_content = str(
                self.rephrase_tool.rephrase_text(content, tone, str(length))
            )
            self.ui.print_colored_text("Rephrased content:\n", self.ui.COLOR_GREEN)
            print(f"{rephrased_content}\n")
            # Add Pattern
            print(
                "*********************************************************************\n"
            )
            return rephrased_content  # No need to rephrase again

    def process_with_rephrase(
        self,
        generate_func: Callable[
            ..., str
        ],  # Specify Callable's argument types and return type
        prompt: str,
        file_name: str,
        *args: Any,  # Add type annotation to args
    ) -> str:
        """
        Generic function to generate content and then repeatedly rephrase it
        based on user input.
        """
        content = generate_func(*args)  # Generate initial content
        self.ui.print_colored_text("Content generated:\n\n", self.ui.COLOR_GREEN)
        print(content + "\n")

        while True:
            rephrase = input(f"Rephrase {prompt}? (y/n): ").lower()
            if rephrase == "y":
                content = self.rephrase_content(content)  # Rephrase content
            else:
                try:
                    os.makedirs("output", exist_ok=True)
                    with open(f"output/{file_name}", "w") as file:
                        file.write(content)
                    self.ui.print_colored_text(
                        f"Contents written in file output/{file_name}",
                        self.ui.COLOR_BLUE,
                    )
                except Exception as e:
                    print(
                        "{}, Error writing the contents to file {}, {} \n".format(
                            self.ui.COLOR_RED, e, self.ui.COLOR_RESET
                        )
                    )
                break  # Exit the rephrasing loop

        return str(content)  # Return the final content (rephrased or original)

    def generate_blog(self, video_transcript: str) -> str:
        """Generates and optionally rephrases a blog post."""
        self.ui.print_section_header("Generating Blog Post")
        return self.process_with_rephrase(
            self.blog_generator.generate_blog,
            "blog content",
            "blog.txt",
            video_transcript,
        )

    def generate_summary(self, video_transcript: str) -> str:
        """Generates and optionally rephrases a video summary."""
        self.ui.print_section_header("Generating Summary")
        return self.process_with_rephrase(
            self.summary_generator.summarize_and_convert_to_markdown,
            "video summary",
            "summary.txt",
            video_transcript,
        )

    def generate_emails(self, blog_content: str, email_type: str = "marketing") -> str:
        """Generates and optionally rephrases emails."""
        self.ui.print_section_header("Generating Emails")
        return self.process_with_rephrase(
            self.email_generator.generate_email,
            "emails",
            "email.txt",
            blog_content,
            email_type,
        )

    def generate_markdown(self, blog_content: str) -> str:
        """Generates and optionally rephrases markdown documentation."""
        self.ui.print_section_header("Generating Markdown Documentation")
        return self.process_with_rephrase(
            self.markdown_tool.convert_to_markdown,
            "markdown documentation",
            "markdown.md",
            blog_content,
        )

    def execute(
        self, video_transcript: str, email_type: str = "marketing"
    ) -> Dict[str, str]:
        """
        Executes the marketing workflow based on user selection from the menu.
        """
        results: Dict[str, str] = {}  # Store results of each step

        while True:
            self.print_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                results["blog_content"] = self.generate_blog(video_transcript)
            elif choice == "2":
                results["video_summary"] = self.generate_summary(video_transcript)
            elif choice == "3":
                if "blog_content" not in results:
                    print(
                        "{}, Please generate blog content first (option 1). {}, \n".format(
                            self.ui.COLOR_RED, self.ui.COLOR_RESET
                        )
                    )
                    continue
                results["emails"] = self.generate_emails(
                    results["blog_content"], email_type
                )
            elif choice == "4":
                if "blog_content" not in results:
                    print(
                        "{}, Please generate blog content first (option 1). {}, \n".format(
                            self.ui.COLOR_RED, self.ui.COLOR_RESET
                        )
                    )
                    continue
                results["markdown_docs"] = self.generate_markdown(
                    results["blog_content"]
                )
            elif choice == "5":
                self.ui.print_colored_text("Workflow Complete", self.ui.COLOR_GREEN)
                break
            else:
                print(
                    "{}, Invalid choice. Please try again. {}, \n".format(
                        self.ui.COLOR_RED, self.ui.COLOR_RESET
                    )
                )

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
    """
    Runs the marketing workflow CLI application.

    Args:
        transcript_file: Path to the file containing the video transcript.
        email_type: The type of email to generate (default: marketing).
    """

    try:
        with open(transcript_file) as f:
            video_transcript = f.read()
    except FileNotFoundError:
        print("Error: Transcript file not found at  ", transcript_file, "\n")
        return
    except Exception as e:
        print("Error reading transcript file: ", e, "\n")
        return

    workflow = MarketingWorkflow()
    results = workflow.execute(video_transcript, email_type)

    print("\nWorkflow Results:")
    for key, value in results.items():
        print(f"\n{key}:\n{value}\n")


if __name__ == "__main__":
    fire.Fire(run_workflow)
