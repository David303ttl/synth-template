#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NamespacePair:
    ns1: str
    ns2: str


def detect_current_namespaces(repo_root: Path) -> NamespacePair | None:
    files_to_check = [
        repo_root / "src" / "configuration.h",
        repo_root / "src" / "engine" / "engine.h",
        repo_root / "src" / "engine" / "patch.h",
        repo_root / "src" / "engine" / "voice.h",
    ]

    for file in files_to_check:
        if not file.exists():
            continue
        text = file.read_text(encoding="utf-8", errors="replace")

        m = re.search(r"\bnamespace\s+(\w+)::(\w+)(?:::.*)?\s*\{", text)
        if m:
            return NamespacePair(m.group(1), m.group(2))

        ns_stack: list[str] = []
        for line in text.splitlines():
            m2 = re.search(r"\bnamespace\s+(\w+)\s*\{", line)
            if m2:
                ns_stack.append(m2.group(1))
                if len(ns_stack) >= 2:
                    return NamespacePair(ns_stack[0], ns_stack[1])
            m3 = re.search(r"(\w+)::(\w+)::", line)
            if m3:
                return NamespacePair(m3.group(1), m3.group(2))

    return None


def apply_migration(text: str, old: NamespacePair, new: NamespacePair) -> tuple[str, bool]:
    original = text

    # Nested namespace openings: namespace old1::old2::sub {  -> namespace new1::new2::sub {
    text = re.sub(
        rf"\bnamespace\s+{re.escape(old.ns1)}::{re.escape(old.ns2)}((?:::\w+)*)\s*\{{",
        rf"namespace {new.ns1}::{new.ns2}\1 {{",
        text,
    )

    # Old style openings: namespace old1 { / namespace old2 {
    if old.ns1 != new.ns1:
        text = re.sub(rf"\bnamespace\s+{re.escape(old.ns1)}\s*\{{", f"namespace {new.ns1} {{", text)
    if old.ns2 != new.ns2:
        text = re.sub(rf"\bnamespace\s+{re.escape(old.ns2)}\s*\{{", f"namespace {new.ns2} {{", text)

    # Namespace references: old1::old2:: -> new1::new2::
    text = text.replace(f"{old.ns1}::{old.ns2}::", f"{new.ns1}::{new.ns2}::")

    # Namespace alias: namespace x = old1::... -> namespace x = new1::...
    if old.ns1 != new.ns1:
        text = re.sub(
            rf"(\bnamespace\s+\w+\s*=\s*){re.escape(old.ns1)}::",
            rf"\1{new.ns1}::",
            text,
        )

    # Closing comments for nested namespaces: } // namespace old1::old2...
    text = text.replace(
        f"// namespace {old.ns1}::{old.ns2}", f"// namespace {new.ns1}::{new.ns2}"
    )

    # Closing comments for old style: } // namespace old1 / old2
    if old.ns1 != new.ns1:
        text = re.sub(
            rf"(\}}\s*//\s*namespace\s+){re.escape(old.ns1)}\b", rf"\1{new.ns1}", text
        )
    if old.ns2 != new.ns2:
        text = re.sub(
            rf"(\}}\s*//\s*namespace\s+){re.escape(old.ns2)}\b", rf"\1{new.ns2}", text
        )

    # Split multi-close lines: } // namespace x } // namespace old2 } // namespace old1
    # (Best-effort; only handles this exact three-level inline pattern.)
    text = re.sub(
        rf"\}}\s*//\s*namespace\s+(\w+)\s*\}}\s*//\s*namespace\s+{re.escape(old.ns2)}\s*\}}\s*//\s*namespace\s+{re.escape(old.ns1)}",
        rf"}} // namespace \1\n}} // namespace {new.ns2}\n}} // namespace {new.ns1}",
        text,
    )

    # Plugin ID: org.old1.old2 -> org.new1.new2
    text = text.replace(f"org.{old.ns1}.{old.ns2}", f"org.{new.ns1}.{new.ns2}")

    return text, text != original


def iter_source_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for folder in ("src", "tests"):
        base = repo_root / folder
        if not base.exists():
            continue
        for ext in ("*.h", "*.cpp"):
            files.extend(base.rglob(ext))
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="Migrate the project's base namespace (two-level).")
    ap.add_argument("new_ns1", nargs="?", help="New first namespace (e.g., yourname)")
    ap.add_argument("new_ns2", nargs="?", help="New second namespace (e.g., yourproject)")
    ap.add_argument("--old-ns1", help="Override detected first namespace")
    ap.add_argument("--old-ns2", help="Override detected second namespace")
    ap.add_argument("--dry-run", action="store_true", help="Print what would change without writing files.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    detected = detect_current_namespaces(repo_root)
    if not detected and (not args.old_ns1 or not args.old_ns2):
        raise SystemExit("Could not auto-detect current namespaces. Provide --old-ns1 and --old-ns2.")

    old = NamespacePair(args.old_ns1 or detected.ns1, args.old_ns2 or detected.ns2)  # type: ignore[union-attr]

    if args.new_ns1 is None:
        raise SystemExit("Provide new_ns1 (and optionally new_ns2). Example: python scripts/fix_namespace.py myname myproject")

    new_ns2 = args.new_ns2 or old.ns2
    new = NamespacePair(args.new_ns1.strip(), new_ns2.strip())

    if old == new:
        raise SystemExit("Old and new namespaces are the same. Nothing to do.")

    print(f"Detected current namespaces: '{old.ns1}' :: '{old.ns2}'")
    print(f"Migrating to: '{new.ns1}' :: '{new.ns2}'")

    modified_files = 0
    for path in iter_source_files(repo_root):
        original = path.read_text(encoding="utf-8", errors="replace")
        updated, changed = apply_migration(original, old, new)
        if not changed:
            continue
        modified_files += 1
        if args.dry_run:
            print(f"Would update {path.relative_to(repo_root)}")
        else:
            path.write_text(updated, encoding="utf-8", newline="")
            print(f"Updated {path.relative_to(repo_root)}")

    print(f"Done. Files modified: {modified_files}{' (dry-run)' if args.dry_run else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

