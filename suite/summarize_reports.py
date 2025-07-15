import json
import logging
from pathlib import Path
from typing import Any

import fire
import pandas as pd
from rich.console import Console


def main() -> None:
    """Run the report summarization script."""
    logging.basicConfig(level=logging.INFO)
    console = Console()
    model_reports: dict[str, dict[str, list[dict[str, Any]]]] = {}
    report_dir = Path(__file__).parent / "reports"

    # Load each JSON report from nested structure: reports/<provider>/<model>/<test>.json
    for file in report_dir.rglob("*.json"):
        # Skip old flat structure files (report_*.json at root level)
        if file.parent == report_dir:
            continue

        with file.open() as fp:
            data = json.load(fp)

        # Extract provider and model from path structure
        parts = file.relative_to(report_dir).parts
        if len(parts) >= 3:  # provider/model/test.json
            provider = parts[0]
            model = parts[1]
            test_name = parts[2].replace(".json", "")

            provider_model_key = f"{provider}/{model}"

            if provider_model_key not in model_reports:
                model_reports[provider_model_key] = {"tests": []}

            # Add test data with test name context
            test_data = data.get("tests", [])
            for test_entry in test_data:
                # Ensure we have the test file context
                if "nodeid" in test_entry and not test_entry["nodeid"].startswith(test_name):
                    test_entry["nodeid"] = f"{test_name}::{test_entry['nodeid']}"

            model_reports[provider_model_key]["tests"].extend(test_data)

    # For each model, build two mappings by test_file:
    #   1) counts: {test_file: {"total": int, "passed": int, "time": float}}
    #   2) failures: a list of (test_file, nodeid, failure_message)
    per_model_summary = {}
    all_failures = []  # collect (model, test_file, nodeid, message)

    for provider_model, report in model_reports.items():
        tests = report.get("tests", [])
        by_file = {}
        for entry in tests:
            nodeid = entry["nodeid"]
            test_file = nodeid.split("::")[0]
            outcome = entry.get("outcome", "unknown")

            # Extract timing information from call phase only (actual test execution)
            call_duration = entry.get("call", {}).get("duration", 0.0)

            # Initialize if this is the first time seeing this file
            if test_file not in by_file:
                by_file[test_file] = {"total": 0, "passed": 0, "time": 0.0}

            # Increment total count
            by_file[test_file]["total"] += 1

            # If passed, increment passed count
            if outcome == "passed":
                by_file[test_file]["passed"] += 1

            # Accumulate duration (regardless of pass/fail)
            by_file[test_file]["time"] += call_duration

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
                all_failures.append((provider_model, test_file, nodeid, failure_text))

        per_model_summary[provider_model] = by_file

    # Collect a union of all test files across all models
    all_files: set[str] = set()
    for by_file in per_model_summary.values():
        all_files.update(by_file.keys())

    # Build a table: rows = test_file
    # Model headers are now provider/model combinations using the path format
    model_headers = {provider_model: provider_model for provider_model in sorted(per_model_summary.keys())}

    rows = []
    for test_file in sorted(all_files):
        row = {"Tests": test_file}
        for provider_model in sorted(per_model_summary.keys()):
            stats = per_model_summary[provider_model].get(test_file, {"passed": 0, "total": 0, "time": 0.0})
            passed = stats.get("passed", 0)
            total = stats.get("total", 0)
            failed = total - passed
            time = round(stats.get("time", 0.0), 3)
            cell = f"✅ {passed:2d}  ❌ {failed:2d}  ⏱️ {time}s"
            row[model_headers[provider_model]] = cell
        rows.append(row)

    # Create DataFrame
    summary_df = pd.DataFrame(rows)
    summary_df = summary_df.set_index("Tests")

    # Print the summary table
    console.print("\n[bold yellow]===== Test Summary by Provider/Model =====[/bold yellow]\n")
    console.print(summary_df.to_markdown(tablefmt="github"))


if __name__ == "__main__":
    fire.Fire(main)
