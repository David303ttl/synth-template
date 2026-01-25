#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


def compute_guard(relpath: str, src_token: str) -> str:
    hg = relpath.replace("\\", "/")
    hg = hg.replace("/", "_").replace(".", "_").replace("-", "_")
    # Maintain legacy behavior: replace the first occurrence of "src" with "{src_token}"
    hg = re.sub(r"\bsrc\b", src_token, hg, count=1)
    return hg.upper()


def replace_top_guard(lines: list[str], guard: str) -> tuple[list[str], bool]:
    """
    If the file already has an include guard, rewrite it to `guard`.
    Returns (new_lines, modified).
    """
    modified = False
    ifndef_i = None
    define_i = None

    for i, line in enumerate(lines[:200]):
        if ifndef_i is None and re.match(r"^\s*#ifndef\b", line):
            ifndef_i = i
            continue
        if ifndef_i is not None and define_i is None and re.match(r"^\s*#define\b", line):
            define_i = i
            break

    if ifndef_i is None or define_i is None:
        return lines, modified

    old_ifndef = lines[ifndef_i]
    old_define = lines[define_i]

    new_ifndef = re.sub(r"^(\s*#ifndef\s+)\S+(\s*)$", rf"\1{guard}\2", old_ifndef)
    new_define = re.sub(r"^(\s*#define\s+)\S+(\s*)$", rf"\1{guard}\2", old_define)
    if new_ifndef != old_ifndef:
        lines[ifndef_i] = new_ifndef
        modified = True
    if new_define != old_define:
        lines[define_i] = new_define
        modified = True

    # Update the closing #endif comment (best-effort).
    # Prefer the last #endif in the file.
    for i in range(len(lines) - 1, -1, -1):
        if re.match(r"^\s*#endif\b", lines[i]):
            new_endif = re.sub(r"^\s*#endif\b.*$", f"#endif // {guard}\n", lines[i])
            if new_endif != lines[i]:
                lines[i] = new_endif
                modified = True
            break

    return lines, modified


def replace_pragma_once(text: str, guard: str) -> tuple[str, bool]:
    """
    Replace '#pragma once' with an include guard and ensure a closing '#endif' exists.
    """
    if "#pragma once" not in text:
        return text, False

    lines = text.splitlines(keepends=True)
    modified = False

    # Replace pragma once line(s)
    new_lines: list[str] = []
    replaced = False
    for line in lines:
        if re.match(r"^\s*#pragma\s+once\s*$", line):
            new_lines.append(f"#ifndef {guard}\n#define {guard}\n")
            replaced = True
            modified = True
        else:
            new_lines.append(line)

    if not replaced:
        return text, False

    # Ensure trailing #endif exists
    joined = "".join(new_lines)
    if not re.search(r"^\s*#endif\b", joined, flags=re.MULTILINE):
        if not joined.endswith("\n"):
            joined += "\n"
        joined += f"\n#endif // {guard}\n"
        modified = True

    return joined, modified


def process_header(abs_path: Path, relpath: str, src_token: str, dry_run: bool) -> bool:
    rel = relpath.replace("\\", "/")
    guard = compute_guard(rel, src_token=src_token)
    original = abs_path.read_text(encoding="utf-8", errors="replace")

    text, m1 = replace_pragma_once(original, guard)
    lines = text.splitlines(keepends=True)
    lines, m2 = replace_top_guard(lines, guard)
    updated = "".join(lines)

    if not (m1 or m2) or updated == original:
        return False

    if dry_run:
        print(f"Would update {relpath}")
        return True

    abs_path.write_text(updated, encoding="utf-8", newline="")
    print(f"Updated {relpath} -> {guard}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Standardize header guards in src/ and tests/.")
    ap.add_argument("--src-token", default="david303ttl_synth",
                    help='Replacement token for "src" in guard names (default: david303ttl_synth).')
    ap.add_argument("--dry-run", action="store_true", help="Print what would change without writing files.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    changed = 0

    for folder in ("src", "tests"):
        base = repo_root / folder
        if not base.exists():
            continue
        for path in base.rglob("*.h"):
            relpath = str(path.relative_to(repo_root)).replace("\\", "/")
            if process_header(path, relpath, args.src_token, args.dry_run):
                changed += 1

    print(f"Done. Files modified: {changed}{' (dry-run)' if args.dry_run else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
