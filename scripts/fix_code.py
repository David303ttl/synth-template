#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(script: Path, args: list[str]) -> int:
    cmd = [sys.executable, str(script), *args]
    print(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run repo maintenance scripts in sequence.")
    ap.add_argument("--dry-run", action="store_true", help="Pass --dry-run to sub-scripts where supported.")
    ap.add_argument("--no-format", action="store_true", help="Pass --no-format to fix_file_comments.py.")
    ap.add_argument("--src-token", default="david303ttl_synth",
                    help='Replacement token for "src" in guard names (default: david303ttl_synth).')
    args = ap.parse_args()

    scripts_dir = Path(__file__).resolve().parent
    code = 0

    hg_args = ["--src-token", args.src_token]
    if args.dry_run:
        hg_args.append("--dry-run")
    code = max(code, run(scripts_dir / "fix_header_guards.py", hg_args))

    fc_args: list[str] = []
    if args.dry_run:
        fc_args.append("--dry-run")
    if args.no_format:
        fc_args.append("--no-format")
    code = max(code, run(scripts_dir / "fix_file_comments.py", fc_args))

    return code


if __name__ == "__main__":
    raise SystemExit(main())

