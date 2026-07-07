"""The checker — a SEPARATE call, with a strict/adversarial system prompt,
fed only the goal + test output (not the maker's own reasoning). This is
the maker/checker split running on a single loop, deliberately isolated.
"""

import json
import re

from .model_client import call_model

CHECKER_SYSTEM = """You are a strict, skeptical verifier. You did not write the
code. You are given a goal and the actual output of running the test suite.
Decide only from that evidence whether the goal is fully met.
Respond with ONLY a JSON object: {"done": true|false, "reason": "..."}.
Do not trust claims of success that are not backed by the test output."""


def checker_step(goal: str, test_output: str) -> dict:
    user = f"""GOAL:
{goal}

TEST OUTPUT:
{test_output}

Is the goal fully and verifiably met? Respond with the JSON object only."""
    reply = call_model(CHECKER_SYSTEM, user, temperature=0.0)
    try:
        json_str = re.search(r"\{.*\}", reply, re.DOTALL).group(0)
        return json.loads(json_str)
    except Exception:
        return {"done": False, "reason": f"unparseable checker reply: {reply[:200]}"}
