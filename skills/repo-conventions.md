# Skill: repo-conventions

This is the "written-down intent" primitive — the thing that stops the loop
re-deriving your project from zero every iteration. agent_loop.py's maker
prompt loads this file's contents into the LOG SO FAR context alongside
LOOP_STATE.md (in the full version below you'd concatenate both).

## When this skill applies
Any task touching this repo.

## Conventions
- All Python files use 4-space indents, no tabs.
- Every new .py file that defines behavior gets a matching test_*.py using
  plain `assert` statements (pytest, no unittest classes).
- Never add a dependency outside the Python standard library without saying
  so explicitly in a comment.
- Commit messages (if the loop commits) are one line, imperative mood,
  under 72 characters.

## Known gotchas
- This repo has no network access during test runs. Any test that calls
  out to a URL will hang and fail the loop's time budget — don't write one.
