#!/usr/bin/env python3
"""Validate an implementation-orchestrator acceptance harness."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


CRITERION_ID = re.compile(r"AC-[A-Z0-9][A-Z0-9-]*$")


def require_string(value: Any, name: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{name} must be a non-empty string")


def require_relative_path(value: Any, name: str, errors: list[str]) -> None:
    require_string(value, name, errors)
    if isinstance(value, str):
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"{name} must be repository-relative")


def validate(data: dict[str, Any], repo_root: Path, frozen: bool) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must equal 1")
    for field in ("goal", "consumer_entry"):
        require_string(data.get(field), field, errors)

    immutable_paths = data.get("immutable_paths")
    if not isinstance(immutable_paths, list) or not immutable_paths:
        errors.append("immutable_paths must be a non-empty list")
        immutable_paths = []
    immutable = set()
    for index, path in enumerate(immutable_paths):
        label = f"immutable_paths[{index}]"
        require_relative_path(path, label, errors)
        if isinstance(path, str):
            immutable.add(path)
            if frozen and not (repo_root / path).is_file():
                errors.append(f"immutable path does not exist: {path}")

    criteria = data.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        errors.append("criteria must be a non-empty list")
        criteria = []
    identifiers: set[str] = set()
    tags: set[str] = set()
    for index, criterion in enumerate(criteria):
        prefix = f"criteria[{index}]"
        if not isinstance(criterion, dict):
            errors.append(f"{prefix} must be an object")
            continue
        identifier = criterion.get("id")
        if not isinstance(identifier, str) or not CRITERION_ID.fullmatch(identifier):
            errors.append(f"{prefix}.id must match AC-*")
        elif identifier in identifiers:
            errors.append(f"duplicate criterion id: {identifier}")
        else:
            identifiers.add(identifier)
        if criterion.get("required") is not True:
            errors.append(f"{prefix}.required must be true")
        for field in ("command", "expected"):
            require_string(criterion.get(field), f"{prefix}.{field}", errors)
        criterion_tags = criterion.get("tags", [])
        if not isinstance(criterion_tags, list) or not all(
            isinstance(tag, str) and tag for tag in criterion_tags
        ):
            errors.append(f"{prefix}.tags must be a list of non-empty strings")
        else:
            tags.update(criterion_tags)
        test_path = criterion.get("test_path")
        if test_path is not None:
            require_relative_path(test_path, f"{prefix}.test_path", errors)
            if isinstance(test_path, str) and test_path not in immutable:
                errors.append(f"{prefix}.test_path must appear in immutable_paths")

    risks = data.get("risks", [])
    if not isinstance(risks, list) or not all(isinstance(risk, str) for risk in risks):
        errors.append("risks must be a list of strings")
        risks = []
    required_tags = {
        "destructive": "rejection-no-side-effect",
        "external-artifact": "consumer-entry",
        "module-identity": "module-identity",
    }
    for risk, required_tag in required_tags.items():
        if risk in risks and required_tag not in tags:
            errors.append(f"risk {risk!r} requires a {required_tag!r} criterion")
    return errors


def immutable_changes(repo_root: Path, base: str, paths: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base, "--", *paths],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or "could not inspect harness changes")
    return sorted(line for line in result.stdout.splitlines() if line)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stage", choices=("plan", "frozen"), required=True)
    parser.add_argument("--base")
    args = parser.parse_args()
    try:
        manifest = Path(args.manifest).resolve()
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("manifest root must be an object")
        root = Path(args.repo_root).resolve()
        errors = validate(data, root, args.stage == "frozen")
        if args.base:
            if args.stage != "frozen":
                errors.append("--base requires --stage frozen")
            elif not errors:
                changed = immutable_changes(root, args.base, data["immutable_paths"])
                if changed:
                    errors.append("immutable paths changed: " + ", ".join(changed))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: harness is valid for stage {args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
