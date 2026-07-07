"""State — the sixth primitive. Lives on disk, not in the model's context.

Every iteration reads this in and appends to it, so the loop can be killed
and resumed and still remembers what it already tried.
"""

from pathlib import Path


class LoopState:
    def __init__(self, path: Path):
        self.path = path
        if not self.path.exists():
            self.path.write_text("# Loop State\n\n")

    def read(self) -> str:
        return self.path.read_text()

    def append(self, entry: str):
        with self.path.open("a") as f:
            f.write(entry.rstrip() + "\n\n")
