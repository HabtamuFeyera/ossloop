#!/usr/bin/env bash
# scripts/parallel_worktrees.sh — the "worktrees" primitive.
#
# Runs several ossloop instances against the SAME repo history at the same
# time, each in its own isolated checkout, so two local-model loops editing
# different features cannot physically collide on the same files.

set -euo pipefail
cd "$(dirname "$0")/.."     # repo root

BASE_REPO="./examples/test_repo"
if [ ! -d "$BASE_REPO/.git" ]; then
    mkdir -p "$BASE_REPO"
    git -C "$BASE_REPO" init -q
    git -C "$BASE_REPO" commit --allow-empty -q -m "init"
fi

declare -A GOALS=(
    ["feature-hello"]="Create hello.py that prints 'hello loop engineering' and test_hello.py that verifies it."
    ["feature-add"]="Create mathutils.py with an add(a, b) function and test_mathutils.py that checks add(2, 3) == 5."
)

PIDS=()

for BRANCH in "${!GOALS[@]}"; do
    WORKTREE_DIR="./examples/worktrees/$BRANCH"
    mkdir -p ./examples/worktrees

    # Each loop gets its own working directory sharing the same repo
    # history — this is the actual collision-prevention mechanism, not
    # anything AI-specific.
    if [ ! -d "$WORKTREE_DIR" ]; then
        git -C "$BASE_REPO" worktree add -b "$BRANCH" "../worktrees/$BRANCH" -q
    fi

    echo "[dispatch] $BRANCH -> $WORKTREE_DIR"
    (
        PYTHONPATH=./src python3 -m ossloop.cli \
            --repo "$WORKTREE_DIR" \
            --goal "${GOALS[$BRANCH]}" \
            --max-iterations 6 \
            --max-seconds 400 \
            --skills ./skills \
            > "./examples/worktrees/${BRANCH}.log" 2>&1
    ) &
    PIDS+=($!)
done

echo "[dispatch] ${#PIDS[@]} loops running in parallel: ${PIDS[*]}"
wait "${PIDS[@]}"
echo "[dispatch] all loops finished — check ./examples/worktrees/*.log and each worktree's LOOP_STATE.md"

# A verifier sub-agent step would run here, over each worktree's diff,
# before anything gets merged back to the base repo. Left as an exercise:
# call checker_step() from ossloop.checker against `git -C "$WORKTREE_DIR" diff`.
