import json
import logging
from pathlib import Path

import fire
import pandas as pd
from rich.console import Console


def main() -> None:
    """Run the report summarization script."""
    logging.basicConfig(level=logging.INFO)
    console = Console()
    model_reports = {}
    report_dir = Path(__file__).parent / "reports"

    # Load each JSON report
    for file in report_dir.rglob("*.json"):
        with file.open() as fp:
            data = json.load(fp)
        model_name = file.name.replace("report_", "").replace(".json", "")
        model_reports[model_name] = data

    # For each model, build two mappings by test_file:
    #   1) counts: {test_file: {"total": int, "passed": int, "time": float}}
    #   2) failures: a list of (test_file, nodeid, failure_message)
    per_model_summary = {}
    all_failures = []  # collect (model, test_file, nodeid, message)

    for model, report in model_reports.items():
        tests = report.get("tests", [])
        by_file = {}
        for entry in tests:
            nodeid = entry["nodeid"]
            test_file = nodeid.split("::")[0]
            outcome = entry.get("outcome", "unknown")
            duration = entry.get("duration", 0.0)

            # Initialize if this is the first time seeing this file
            if test_file not in by_file:
                by_file[test_file] = {"total": 0, "passed": 0, "time": 0.0}

            # Increment total count
            by_file[test_file]["total"] += 1

            # If passed, increment passed count
            if outcome == "passed":
                by_file[test_file]["passed"] += 1

            # Accumulate duration (regardless of pass/fail)
            by_file[test_file]["time"] += duration

            # If failure (anything other than "passed"), record message
            if outcome != "passed":
                # Some JSON reports include a "longrepr" or "message" field for failures
                # We try common keys; otherwise stringify the whole entry
                failure_text = ""
                if "longrepr" in entry:
                    failure_text = entry["longrepr"]
                elif "message" in entry:
                    failure_text = entry["message"]
                else:
                    failure_text = json.dumps(entry, indent=2)
                all_failures.append((model, test_file, nodeid, failure_text))

        per_model_summary[model] = by_file

    # Collect a union of all test files across all models
    all_files: set[str] = set()
    for by_file in per_model_summary.values():
        all_files.update(by_file.keys())

    # Build a table: rows = test_file
    # Also, collect model display names with date for headers
    model_headers = {}
    for model in sorted(per_model_summary.keys()):
        # Try to get date from filename (assumes format: report_<model>-<date>.json)
        for file in report_dir.iterdir():
            if file.name.startswith(f"report_{model}") and file.name.endswith(".json"):
                parts = file.name.replace("report_", "").replace(".json", "").split("-")
                date = parts[-1] if len(parts) > 1 else ""
                model_headers[model] = f"{model} {date}" if date else model
                break
        else:
            model_headers[model] = model

    rows = []
    for test_file in sorted(all_files):
        row = {"Test File": test_file}
        for model in sorted(per_model_summary.keys()):
            stats = per_model_summary[model].get(test_file, {"passed": 0, "total": 0, "time": 0.0})
            passed = stats.get("passed", 0)
            total = stats.get("total", 0)
            failed = total - passed
            time = round(stats.get("time", 0.0), 3)
            cell = f"✅ {passed:2d}  ❌ {failed:2d}  ⏱️ {time}s"
            row[model_headers[model]] = cell
        rows.append(row)

    # Create DataFrame
    summary_df = pd.DataFrame(rows)
    summary_df = summary_df.set_index("Test File")

    # Print the summary table
    console.print("\n[bold yellow]===== Test Summary by Model =====[/bold yellow]\n")
    console.print(summary_df.to_markdown(tablefmt="github"))


if __name__ == "__main__":
    fire.Fire(main)
