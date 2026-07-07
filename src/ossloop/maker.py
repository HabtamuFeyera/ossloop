"""The maker — proposes the next concrete action as shell commands.

Keeping the action space to "shell commands in a fenced block" is what lets
a 20b local model act reliably without a heavier tool-calling harness.
"""

import re
import subprocess
from pathlib import Path

from .model_client import call_model
from .state import LoopState

MAKER_SYSTEM = """You are the maker in a coding loop. You will be given a goal,
the current state of a repo (file listing + relevant contents), and a log of
what has already been tried. Propose ONE small, concrete next step as shell
commands that operate inside the given repo directory.

Rules:
- Output ONLY a single ```bash fenced code block, nothing else.
- Use `cat > file << 'EOF' ... EOF` to write files.
- Make the smallest change that moves toward the goal.
- Do not repeat a step the log says already succeeded.
"""


def load_skills(skills_dir: Path) -> str:
    """The Skills primitive: concatenate project-knowledge files so the
    maker doesn't have to re-guess conventions every iteration."""
    if not skills_dir.exists():
        return "(no skills found)"
    parts = []
    for f in sorted(skills_dir.glob("*.md")):
        parts.append(f"--- skill: {f.name} ---\n{f.read_text()}")
    return "\n\n".join(parts) if parts else "(no skills found)"


def maker_step(repo: Path, goal: str, state: LoopState, skills_dir: Path) -> str:
    listing = subprocess.run(
        ["bash", "-c", f"cd {repo} && find . -not -path './.git/*' -type f"],
        capture_output=True, text=True
    ).stdout
    user = f"""GOAL:
{goal}

PROJECT SKILLS (conventions you must follow):
{load_skills(skills_dir)}

CURRENT FILES in {repo}:
{listing or '(empty repo)'}

LOG SO FAR:
{state.read()}

Propose the next shell command(s) to run, working directory is {repo}."""
    reply = call_model(MAKER_SYSTEM, user, temperature=0.3)
    match = re.search(r"```bash\n(.*?)```", reply, re.DOTALL)
    return match.group(1).strip() if match else reply.strip()


def run_commands(repo: Path, commands: str) -> str:
    result = subprocess.run(
        ["bash", "-c", commands],
        cwd=repo, capture_output=True, text=True, timeout=120
    )
    return (
        f"$ {commands}\n--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}\n--- exit: {result.returncode} ---"
    )
