import re
import subprocess
import time
from pathlib import Path

from fire import Fire
from rich.console import Console


def main(with_model: str = "groq/llama-3.3-70b-versatile") -> None:
    """Run pytest for the specified model, one test case at a time with a delay and append detailed results to a single JSON report."""
    if not re.match(r"^[\w\-\/\.]+$", with_model):
        raise ValueError(f"Invalid model name: {with_model}")
    report_dir = Path(__file__).parent / "reports"
    if len(with_model.split("/")) > 1:
        report_dir /= with_model.split("/")[0]
        model_folder = with_model.split("/")[1]
    else:
        report_dir /= "openai"
        model_folder = with_model
    report_dir /= model_folder
    report_dir.mkdir(parents=True, exist_ok=True)
    console = Console()

    # Discover all test files
    test_files = [str(x) for x in Path(__file__).parent.parent.glob("tests/test_*.py")]

    for test_file in test_files:
        if test_file.endswith("test_elevate.py"):
            continue
        console.print(f"[blue]Running pytest for model={with_model}, file={test_file}...[/blue]")
        test_json_file = report_dir / Path(test_file).name.replace("test_", "").replace(".py", ".json")
        cmd = [
            "pytest",
            test_file,  # Run only this test file
            "--with-model",
            f"{with_model}",
            "--json-report",
            f"--json-report-file={test_json_file.as_posix()}",
            "--json-report-indent=4",
            "--json-report-summary",
            "--durations=0",
        ]

        # Capture the output of the pytest command
        result = subprocess.run(cmd, check=False, cwd=Path(__file__).parent.parent, capture_output=True, text=True)  # noqa: S603
        if result.returncode != 0:
            console.print(
                f"[yellow]⚠ pytest exited with code {result.returncode} for model={with_model}, file={test_file}. Continuing…[/yellow]"
            )
            # Print the error output
            if result.stderr:
                console.print(f"[red]STDERR:[/red]\n{result.stderr}")
            if result.stdout:
                console.print(f"[red]STDOUT:[/red]\n{result.stdout}")
        else:
            console.print(
                f"[green]✔ Completed pytest for model={with_model}, file={test_file}, appending detailed results to JSON report[/green]"
            )
            if result.stdout:
                console.print(f"[green]STDOUT:[/green]\n{result.stdout}")

        console.print("[blue]Sleeping for 10s to avoid rate limit...[/blue]")
        time.sleep(10)


if __name__ == "__main__":
    Fire(main)
