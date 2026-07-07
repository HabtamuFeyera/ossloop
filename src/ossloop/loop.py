"""The loop itself — the orchestration a human used to do by hand.

Budget is enforced in iterations AND wall-clock time, since a local model
has no per-token dollar cost but very real compute/time cost.
"""

import time
from datetime import datetime
from pathlib import Path

from .checker import checker_step
from .maker import maker_step, run_commands
from .state import LoopState
from .verifier import run_verification


def run_loop(repo: Path, goal: str, max_iterations: int, max_seconds: int, skills_dir: Path) -> bool:
    state = LoopState(repo / "LOOP_STATE.md")
    start = time.time()
    state.append(f"## Loop started {datetime.now().isoformat()}\nGOAL: {goal}")

    for i in range(1, max_iterations + 1):
        elapsed = time.time() - start
        if elapsed > max_seconds:
            state.append(f"## STOPPED: time budget of {max_seconds}s exceeded")
            print(f"[loop] time budget exceeded after {i - 1} iterations")
            return False

        print(f"\n=== iteration {i}/{max_iterations} ({elapsed:.0f}s elapsed) ===")

        commands = maker_step(repo, goal, state, skills_dir)
        print("[maker proposes]\n" + commands)
        exec_log = run_commands(repo, commands)
        state.append(f"### Iteration {i} — maker action\n```\n{commands}\n```\n{exec_log}")

        test_output = run_verification(repo)
        print("[verification output]\n" + test_output)

        verdict = checker_step(goal, test_output)
        state.append(f"### Iteration {i} — checker verdict\n{verdict}")
        print(f"[checker verdict] {verdict}")

        if verdict.get("done"):
            state.append(f"## Loop finished successfully after {i} iterations")
            print(f"\n[loop] DONE after {i} iterations: {verdict.get('reason')}")
            return True

    state.append(f"## STOPPED: max_iterations ({max_iterations}) reached without success")
    print(f"\n[loop] gave up after {max_iterations} iterations")
    return False
