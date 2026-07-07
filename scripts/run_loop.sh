#!/usr/bin/env bash
# scripts/run_loop.sh — the "automations" primitive.
#
# Point cron (or a systemd timer, or a GitHub Actions schedule step) at
# THIS script, not at the model, and the loop becomes a heartbeat instead
# of a one-off session.
#
# Install as a heartbeat with:
#   crontab -e
#   */15 * * * * /path/to/ossloop/scripts/run_loop.sh >> /path/to/loop.log 2>&1

set -euo pipefail
cd "$(dirname "$0")/.."     # repo root

REPO="./examples/test_repo"
GOAL="Create hello.py in the repo root that prints exactly 'hello loop engineering', and create test_hello.py that imports hello.py's output via subprocess and asserts it matches."

mkdir -p "$REPO"

echo "[$(date -Iseconds)] starting loop run"
PYTHONPATH=./src python3 -m ossloop.cli \
    --repo "$REPO" \
    --goal "$GOAL" \
    --max-iterations 6 \
    --max-seconds 600 \
    --skills ./skills

STATUS=$?
echo "[$(date -Iseconds)] loop run finished with status $STATUS"

# Anything the loop couldn't finish lands here for a human — the
# "triage inbox" from the article, implemented as the simplest possible
# thing: append to a file if the loop didn't succeed.
if [ "$STATUS" -ne 0 ]; then
    echo "[$(date -Iseconds)] goal not met — see $REPO/LOOP_STATE.md" >> triage_inbox.md
fi
