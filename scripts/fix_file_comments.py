#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


DEFAULT_HEADER = """/*
 * Synth Template
 *
 * Based on SideQuest Starting Point by baconpaul, adopted by David303ttl.
 *
 * Copyright 2024-2025, Paul Walker and contributors.
 * Copyright 2026, Pawel Marczak
 *
 * This source repo is released under the MIT license, but has
 * GPL3 dependencies, as such the combined work will be
 * released under GPL3.
 *
 * The source code and license are at https://github.com/David303ttl/synth-template
 * Original template at https://github.com/baconpaul/sidequest-startingpoint
 */
"""


def strip_leading_header(lines: list[str]) -> tuple[list[str], bool]:
    """
    Remove an existing leading file header comment (/* ... */ or leading // lines).
    Mimics the legacy Perl behavior: only touches the very top of the file.
    """
    i = 0
    # Skip initial blank lines
    while i < len(lines) and lines[i].strip() == "":
        i += 1

    if i >= len(lines):
        return lines, False

    # Leading block comment
    if lines[i].lstrip().startswith("/*"):
        j = i
        while j < len(lines):
            if "*/" in lines[j]:
                j += 1
                return lines[:i] + lines[j:], True
            j += 1
        # Unterminated comment: don't touch
        return lines, False

    # Leading // comment lines
    if lines[i].lstrip().startswith("//"):
        j = i
        while j < len(lines) and lines[j].lstrip().startswith("//"):
            j += 1
        return lines[:i] + lines[j:], True

    return lines, False


def maybe_run_clang_format(path: Path, clang_format: str | None) -> None:
    if clang_format is None:
        return
    try:
        subprocess.run([clang_format, "-i", str(path)], check=False)
    except Exception:
        return


def process_file(path: Path, header: str, clang_format: str | None, dry_run: bool) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    lines = original.splitlines(keepends=True)
    stripped, removed = strip_leading_header(lines)

    updated = header
    if not updated.endswith("\n"):
        updated += "\n"
    updated += "".join(stripped).lstrip("\ufeff")

    if updated == original:
        return False

    if dry_run:
        print(f"Would update {path}")
        return True

    path.write_text(updated, encoding="utf-8", newline="")
    maybe_run_clang_format(path, clang_format)
    print(f"Updated header in {path}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Standardize file header comments in src/ and tests/.")
    ap.add_argument("--dry-run", action="store_true", help="Print what would change without writing files.")
    ap.add_argument("--no-format", action="store_true", help="Do not run clang-format even if present.")
    args = ap.parse_args()

    clang_format = None
    if not args.no_format:
        clang_format = shutil.which("clang-format")

    repo_root = Path(__file__).resolve().parent.parent
    changed = 0

    for folder in ("src", "tests"):
        base = repo_root / folder
        if not base.exists():
            continue
        for ext in ("*.h", "*.cpp"):
            for path in base.rglob(ext):
                if process_file(path, DEFAULT_HEADER, clang_format, args.dry_run):
                    changed += 1

    print(f"Done. Files modified: {changed}{' (dry-run)' if args.dry_run else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

