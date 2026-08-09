#!/usr/bin/env python3
"""Scaffold a repository-specific, read-only quality inspection tool."""

import argparse
from pathlib import Path


TEMPLATE = '''#!/usr/bin/env python3
"""Deterministic repository-specific quality check: {purpose}"""

import argparse
import sys
from pathlib import Path


def check(repo_root: Path) -> list[str]:
    """Return one message per violated invariant; return an empty list on success."""
    violations = []
    # Inspect repository files here. Keep this function read-only and deterministic.
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description={purpose_repr})
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    violations = check(Path(args.repo_root).resolve())
    if violations:
        print("QUALITY_FAIL")
        for violation in violations[:100]:
            print(f"- {{violation}}")
        return 1
    print("QUALITY_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "name", help="lowercase tool name, for example check-api-contract"
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if not args.name.replace("-", "").isalnum() or args.name != args.name.lower():
        raise SystemExit(
            "name must contain only lowercase letters, digits, and hyphens"
        )
    root = Path(args.repo_root).resolve()
    path = root / ".quality" / "tools" / f"{args.name}.py"
    if path.exists() and not args.force:
        raise SystemExit(
            f"already exists: {path}; pass --force explicitly to replace it"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        TEMPLATE.format(purpose=args.purpose, purpose_repr=repr(args.purpose)),
        encoding="utf-8",
    )
    print(path)


if __name__ == "__main__":
    main()
