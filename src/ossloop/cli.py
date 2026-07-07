#!/usr/bin/env python3
"""CLI entry point.

Usage:
    python3 -m ossloop.cli --repo ./examples/test_repo \\
        --goal "create hello.py that prints 'hello loop engineering'" \\
        --max-iterations 6 --max-seconds 600
"""

import argparse
import sys
from pathlib import Path

from .loop import run_loop


def main():
    ap = argparse.ArgumentParser(prog="ossloop")
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--goal", required=True)
    ap.add_argument("--max-iterations", type=int, default=6)
    ap.add_argument("--max-seconds", type=int, default=600)
    ap.add_argument("--skills", type=Path, default=Path("skills"))
    args = ap.parse_args()

    args.repo.mkdir(parents=True, exist_ok=True)
    ok = run_loop(args.repo, args.goal, args.max_iterations, args.max_seconds, args.skills)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
