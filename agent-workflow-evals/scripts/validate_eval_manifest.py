#!/usr/bin/env python3
"""Validate an agent-workflow-evals manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


IDENTIFIER = re.compile(r"(?:WF|TASK)-[A-Z0-9][A-Z0-9-]*$")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must equal 1")
    for section, required_key in (("workflows", "skill"), ("tasks", "harness")):
        entries = data.get(section)
        if not isinstance(entries, list) or not entries:
            errors.append(f"{section} must be a non-empty list")
            continue
        identifiers: set[str] = set()
        for index, entry in enumerate(entries):
            prefix = f"{section}[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{prefix} must be an object")
                continue
            identifier = entry.get("id")
            if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
                errors.append(f"{prefix}.id must match WF-* or TASK-*")
            elif identifier in identifiers:
                errors.append(f"duplicate {section} id: {identifier}")
            else:
                identifiers.add(identifier)
            value = entry.get(required_key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}.{required_key} must be a non-empty string")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("manifest root must be an object")
        errors = validate(data)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: evaluation manifest is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
