"""Unit tests that don't require a running Ollama instance."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ossloop.state import LoopState  # noqa: E402


def test_state_creates_file(tmp_path):
    p = tmp_path / "LOOP_STATE.md"
    state = LoopState(p)
    assert p.exists()
    assert "Loop State" in state.read()


def test_state_appends(tmp_path):
    p = tmp_path / "LOOP_STATE.md"
    state = LoopState(p)
    state.append("iteration 1: did a thing")
    state.append("iteration 2: did another thing")
    contents = state.read()
    assert "iteration 1" in contents
    assert "iteration 2" in contents
