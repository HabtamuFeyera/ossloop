"""The verifier — runs real, objective checks (here: pytest).

This is the ground truth the checker gets to see; it's not asking the model
"do you think it works", it's asking it to read actual test output.
"""

import subprocess
from pathlib import Path


def run_verification(repo: Path) -> str:
    result = subprocess.run(
        ["bash", "-c", "python3 -m pytest -q 2>&1 || true"],
        cwd=repo, capture_output=True, text=True, timeout=120
    )
    return result.stdout
