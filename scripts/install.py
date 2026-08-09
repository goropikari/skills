#!/usr/bin/env python3
"""Synchronize active skills into the configured skill directories."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path


STATE_FILE = ".skills-install-state"
TARGET_DIRECTORIES = (Path(".claude/skills"), Path(".agents/skills"))


def active_skill_directories(repository_root: Path) -> list[Path]:
    candidates = (
        *repository_root.glob("*/SKILL.md"),
        *repository_root.glob("implementation/*/SKILL.md"),
        *repository_root.glob("quality/*/SKILL.md"),
        *repository_root.glob("reviews/*/SKILL.md"),
    )
    return sorted(
        {
            skill_file.parent.relative_to(repository_root)
            for skill_file in candidates
            if "deprecated" not in skill_file.relative_to(repository_root).parts
        }
    )


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def write_state(state_path: Path, skill_names: list[str]) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=state_path.parent,
        prefix=f"{STATE_FILE}.",
        suffix=".tmp",
        delete=False,
    ) as temporary_state:
        temporary_state.write("\n".join(skill_names))
        temporary_state.write("\n")
        temporary_path = Path(temporary_state.name)
    os.replace(temporary_path, state_path)


def synchronize(repository_root: Path, target_root: Path) -> None:
    target_root.mkdir(parents=True, exist_ok=True)
    skill_directories = active_skill_directories(repository_root)
    skill_names = [skill_directory.name for skill_directory in skill_directories]
    current_names = set(skill_names)
    state_path = target_root / STATE_FILE

    if state_path.is_file():
        for old_name in state_path.read_text(encoding="utf-8").splitlines():
            if not old_name or old_name.startswith(".") or "/" in old_name:
                continue
            if old_name not in current_names:
                stale_path = target_root / old_name
                remove_path(stale_path)
                print(f"remove {stale_path}")

    for skill_directory, skill_name in zip(skill_directories, skill_names):
        source_path = repository_root / skill_directory
        copy_path = target_root / skill_name
        remove_path(copy_path)
        shutil.copytree(source_path, copy_path)
        print(f"copy {source_path} -> {copy_path}")

    write_state(state_path, skill_names)


def main() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    for relative_target in TARGET_DIRECTORIES:
        synchronize(repository_root, Path.home() / relative_target)


if __name__ == "__main__":
    main()
