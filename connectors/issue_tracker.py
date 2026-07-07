#!/usr/bin/env python3
"""
connector_issue_tracker.py — the "plugins / connectors" primitive.

A loop that only touches the filesystem is a small loop. This is a
deliberately minimal stand-in for an MCP connector: instead of a real
Jira/Linear/GitHub Issues API, it's a local SQLite file — but the shape
is identical to a real connector: the model gets a small, fixed set of
functions it can call, and this script is what actually executes them
against the real system.

In a production loop you'd swap this file for an actual MCP server
(e.g. an MCP server wrapping the Linear or GitHub API) and the rest of
agent_loop.py's maker/checker split would not need to change — the
model would just be given more function names to choose from.
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "issue_tracker.sqlite3"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            created_by TEXT NOT NULL DEFAULT 'loop'
        )
    """)
    return conn


def create_issue(title: str) -> int:
    conn = _connect()
    cur = conn.execute("INSERT INTO issues (title) VALUES (?)", (title,))
    conn.commit()
    return cur.lastrowid


def list_open_issues():
    conn = _connect()
    return conn.execute("SELECT id, title FROM issues WHERE status = 'open'").fetchall()


def close_issue(issue_id: int):
    conn = _connect()
    conn.execute("UPDATE issues SET status = 'closed' WHERE id = ?", (issue_id,))
    conn.commit()


if __name__ == "__main__":
    # Tiny CLI so agent_loop.py's maker can call this the same way it
    # calls any other shell command:
    #   python3 connector_issue_tracker.py create "fix flaky test"
    #   python3 connector_issue_tracker.py list
    #   python3 connector_issue_tracker.py close 3
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "create":
        print(create_issue(" ".join(sys.argv[2:])))
    elif cmd == "list":
        for row in list_open_issues():
            print(row)
    elif cmd == "close":
        close_issue(int(sys.argv[2]))
        print("closed")
    else:
        print("usage: connector_issue_tracker.py [create <title>|list|close <id>]")
