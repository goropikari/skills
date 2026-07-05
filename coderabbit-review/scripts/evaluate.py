#!/usr/bin/env python3
import subprocess
import json
import sys
import os
import time
from collections import defaultdict


def build_command():
    """Builds the coderabbit review command, adding --config if .coderabbit.yaml exists."""
    cmd = ["coderabbit", "review", "--agent"]
    config_path = ".coderabbit.yaml"
    if os.path.isfile(config_path):
        print(f"Found {config_path}, loading as config.", file=sys.stderr)
        cmd.extend(["-c", config_path])
    return cmd


def run_review(retry_count=2):
    """Runs coderabbit review and returns findings, with retry logic for API limits."""
    cmd = build_command()
    for attempt in range(retry_count + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            findings = []
            hit_limit = False

            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    # Monitor status for API limits or quotas
                    if data.get("type") == "status":
                        msg = data.get("message", "").lower()
                        if "limit" in msg or "quota" in msg or "rate" in msg:
                            print(
                                f"CodeRabbit Status: {data.get('message')}",
                                file=sys.stderr,
                            )
                            if data.get("status") == "error":
                                hit_limit = True

                    if data.get("type") == "finding":
                        findings.append(data)
                except json.JSONDecodeError:
                    continue

            if hit_limit and not findings:
                if attempt < retry_count:
                    wait_time = (attempt + 1) * 10
                    print(
                        f"Hit API limit/error, retrying in {wait_time}s... (Attempt {attempt + 1}/{retry_count})",
                        file=sys.stderr,
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    return None

            return findings

        except subprocess.CalledProcessError as e:
            if attempt < retry_count:
                wait_time = (attempt + 1) * 10
                print(
                    f"Process failed, retrying in {wait_time}s... (Attempt {attempt + 1}/{retry_count})",
                    file=sys.stderr,
                )
                time.sleep(wait_time)
                continue
            print(f"Error running coderabbit: {e.stderr}", file=sys.stderr)
            return None


def main():
    print("Starting 3 runs of CodeRabbit review...")
    all_runs = []

    for i in range(3):
        if i > 0:
            # Wait between runs to reduce likelihood of hitting rate limits
            time.sleep(5)

        print(f"Run {i + 1}/3...")
        findings = run_review()

        if findings is None:
            print(f"Aborting: Run {i + 1} failed completely.")
            break

        all_runs.append(findings)

    if not all_runs:
        print("No successful runs completed. Report not generated.")
        return

    # Evaluate results
    report = []
    report.append("# CodeRabbit Evaluation Report")
    report.append("")
    report.append(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Completed runs: {len(all_runs)}/3")
    report.append("")

    # Summary of findings per run
    report.append("## Summary of Findings")
    for i, findings in enumerate(all_runs):
        report.append(f"- Run {i + 1}: {len(findings)} findings")
    report.append("")

    # Compare findings
    # Key: (fileName, codegenInstructions)
    finding_map = defaultdict(list)
    for i, findings in enumerate(all_runs):
        for f in findings:
            key = (f.get("fileName"), f.get("codegenInstructions"))
            finding_map[key].append(i + 1)

    report.append("## Comparison Analysis")
    report.append("")

    consistent = []
    variable = []

    for (file_name, instructions), runs in finding_map.items():
        if len(runs) == len(all_runs):
            consistent.append((file_name, instructions))
        else:
            variable.append((file_name, instructions, runs))

    report.append(f"### Consistent Findings (All {len(all_runs)} runs)")
    if not consistent:
        report.append("No findings were consistent across all runs.")
    for file_name, instructions in consistent:
        report.append(f"- **{file_name}**: {instructions}")
    report.append("")

    report.append("### Variable Findings (Found in some runs)")
    if not variable:
        report.append("No variable findings.")
    for file_name, instructions, runs in variable:
        report.append(
            f"- **{file_name}** (Runs: {', '.join(map(str, runs))}): {instructions}"
        )
    report.append("")

    # Output to markdown file
    output_file = "coderabbit_evaluation.md"
    try:
        with open(output_file, "w") as f:
            f.write("\n".join(report))
        print(f"Evaluation report generated: {output_file}")
    except IOError as e:
        print(f"Failed to write report: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
