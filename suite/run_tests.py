import json
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
    report_dir.mkdir(exist_ok=True)
    console = Console()
    json_file = report_dir / f"report_{with_model}.json"  # Single JSON report file

    # Ensure the JSON report file exists
    if not json_file.exists():
        with json_file.open("w") as f:
            json.dump({}, f)

    # Discover all test files
    test_files = [str(x) for x in Path(__file__).parent.parent.glob("tests/test_*.py")]

    for test_file in test_files:
        cmd = [
            "pytest",
            test_file,  # Run only this test file
            f"--with-model={with_model}",
            "--json-report",
            "--durations=0",
        ]

        # Capture the output of the pytest command
        result = subprocess.run(cmd, check=False, cwd=Path(__file__).parent.parent, capture_output=True, text=True)  # noqa: S603
        if result.returncode != 0:
            console.print(
                f"[yellow]⚠ pytest exited with code {result.returncode} for model={with_model}, file={test_file}. Continuing…[/yellow]"
            )
        else:
            console.print(
                f"[green]✔ Completed pytest for model={with_model}, file={test_file}, appending detailed results to JSON report[/green]"
            )

        # Append detailed test results to the JSON report file
        with json_file.open("r+") as f:
            try:
                report_data = json.load(f)  # Load existing data
            except json.JSONDecodeError:
                report_data = {}  # Initialize empty data if file is corrupted or empty

            # Add detailed test results for the current test file
            report_data[test_file] = {
                "nodeid": test_file,
                "outcome": "passed" if result.returncode == 0 else "failed",
                "result": [
                    {
                        "nodeid": line.split("::")[0],
                        "type": "Coroutine",  # Example: Replace with actual type parsing logic
                        "lineno": int(line.split(":")[-1])
                        if ":" in line and line.split(":")[-1].strip().isdigit()
                        else None,
                    }
                    for line in result.stdout.splitlines()
                    if "::" in line
                ],
            }
            f.seek(0)
            json.dump(report_data, f, indent=4)  # Write updated data
            f.truncate()

        console.print("[blue]Sleeping for 1 minute to avoid rate limit...[/blue]")
        time.sleep(60)


if __name__ == "__main__":
    Fire(main)
