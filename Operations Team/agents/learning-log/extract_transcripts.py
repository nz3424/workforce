#!/usr/bin/env python3
"""
Extract a given local date's user/assistant text turns from all Claude Code
session transcripts, across every project, for the /recap daily-recap pass.

Skips tool_use, tool_result, and thinking blocks (the bulk of transcript
size) so the output stays small enough to read directly. Skips subagent
sidechains — only the top-level conversation is relevant to what Nick
personally learned.

Usage: python3 extract_transcripts.py [YYYY-MM-DD]   # defaults to local today
"""
import json
import sys
import glob
from datetime import datetime
from pathlib import Path

target_date = sys.argv[1] if len(sys.argv) > 1 else datetime.now().astimezone().strftime("%Y-%m-%d")


def local_date(ts_iso):
    dt = datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
    return dt.astimezone().strftime("%Y-%m-%d")


def extract_text(content):
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                t = block.get("text", "").strip()
                if t:
                    parts.append(t)
        return "\n".join(parts)
    return ""


root = Path.home() / ".claude" / "projects"
sessions = {}  # (project_cwd, session_id) -> list of (timestamp, role, text)

for path in glob.glob(str(root / "*" / "*.jsonl")):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except OSError:
        continue
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("isSidechain"):
            continue
        if obj.get("type") not in ("user", "assistant"):
            continue
        ts = obj.get("timestamp")
        if not ts or local_date(ts) != target_date:
            continue
        msg = obj.get("message", {})
        text = extract_text(msg.get("content"))
        if not text:
            continue
        cwd = obj.get("cwd", "unknown-project")
        session_id = obj.get("sessionId", Path(path).stem)
        key = (cwd, session_id)
        sessions.setdefault(key, []).append((ts, msg.get("role", obj.get("type")), text))

if not sessions:
    print(f"No transcript activity found for {target_date}.")
    sys.exit(0)

for (cwd, session_id), turns in sessions.items():
    turns.sort(key=lambda x: x[0])
    print(f"\n{'=' * 70}\nProject: {cwd}\nSession: {session_id}\n{'=' * 70}")
    for ts, role, text in turns:
        snippet = text if len(text) <= 600 else text[:600] + " […]"
        print(f"\n[{role}] {snippet}")
