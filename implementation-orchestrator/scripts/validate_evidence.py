#!/usr/bin/env python3
"""Validate implementation evidence from planning through final verification."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


IDENTIFIER = re.compile(r"(?:AC|RISK|CHECK)-[A-Z0-9][A-Z0-9-]*$")
STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN"}


def identifiers(items: Any, section: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{section} must be a list")
        return set()
    values: set[str] = set()
    for index, item in enumerate(items):
        prefix = f"{section}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        identifier = item.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            errors.append(f"{prefix}.id must match AC-*, RISK-*, or CHECK-*")
        elif identifier in values:
            errors.append(f"duplicate id: {identifier}")
        else:
            values.add(identifier)
    return values


def validate(data: dict[str, Any], final: bool) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must equal 1")
    acceptance_ids = identifiers(
        data.get("acceptance_criteria"), "acceptance_criteria", errors
    )
    risk_ids = identifiers(data.get("risks", []), "risks", errors)
    check_ids = identifiers(data.get("selected_checks", []), "selected_checks", errors)
    for criterion in data.get("acceptance_criteria", []):
        if isinstance(criterion, dict) and criterion.get("required") is not True:
            errors.append(
                f"acceptance criterion {criterion.get('id')} must be required"
            )
    for check in data.get("selected_checks", []):
        if not isinstance(check, dict):
            continue
        references = check.get("risk_ids", [])
        if not isinstance(references, list) or not set(references) <= risk_ids:
            errors.append(f"selected check {check.get('id')} has unknown risk_ids")

    if not final:
        if data.get("results"):
            errors.append("results must be empty during the plan stage")
        return errors

    results = data.get("results")
    if not isinstance(results, list):
        return [*errors, "results must be a list at final stage"]
    result_by_id: dict[str, dict[str, Any]] = {}
    for index, result in enumerate(results):
        prefix = f"results[{index}]"
        if not isinstance(result, dict):
            errors.append(f"{prefix} must be an object")
            continue
        identifier = result.get("id")
        if identifier not in acceptance_ids | check_ids:
            errors.append(
                f"{prefix}.id is not an acceptance criterion or selected check"
            )
            continue
        if result.get("status") not in STATUSES:
            errors.append(f"{prefix}.status must be one of {sorted(STATUSES)}")
        evidence = result.get("evidence")
        if not isinstance(evidence, list) or not all(
            isinstance(item, str) and item for item in evidence
        ):
            errors.append(f"{prefix}.evidence must be a non-empty list of strings")
        result_by_id[identifier] = result

    accepted_risks = {
        item.get("subject_id")
        for item in data.get("residual_risks", [])
        if isinstance(item, dict)
        and isinstance(item.get("subject_id"), str)
        and isinstance(item.get("accepted_by"), str)
        and item["accepted_by"].strip()
    }
    for identifier in acceptance_ids | check_ids:
        result = result_by_id.get(identifier)
        if result is None:
            errors.append(f"missing final result for {identifier}")
        elif result.get("status") != "PASS" and identifier not in accepted_risks:
            errors.append(f"{identifier} is not PASS and has no accepted residual risk")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence")
    parser.add_argument("--stage", choices=("plan", "final"), required=True)
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("evidence root must be an object")
        errors = validate(data, args.stage == "final")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: implementation evidence is valid for stage {args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
