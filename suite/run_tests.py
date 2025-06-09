# run_all_models.py

import re
import subprocess
from pathlib import Path

from fire import Fire
from rich.console import Console


def main(with_model: str = "groq/llama-3.3-70b-versatile") -> None:
    """Run pytest for the specified model."""
    if not re.match(r"^[\w\-\/\.]+$", with_model):
        raise ValueError(f"Invalid model name: {with_model}")
    report_dir = Path(__file__).parent / "reports"
    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)
    console = Console()
    json_file = report_dir / f"report_{with_model}.json"

    cmd = [
        "pytest",
        f"--with-model={with_model}",
        "--disable-warnings",
        "--json-report",
        f"--json-report-file={json_file}",
        "--durations=0",
    ]

    result = subprocess.run(cmd, check=False, cwd=Path(__file__).parent.parent)  # noqa: S603
    if result.returncode != 0:
        console.print(
            f"[yellow]⚠ pytest exited with code {result.returncode} for model={with_model}. Continuing…[/yellow]"
        )
    else:
        console.print(f"[green]✔ Completed pytest for model={with_model}, JSON report at {json_file}[/green]")


if __name__ == "__main__":
    Fire(main)
