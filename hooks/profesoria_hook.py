#!/usr/bin/env python3
"""ProfesorIA hook: marks a session active on /profesoria and re-injects a
reminder after compaction or resume, so the teacher doesn't fade in long sessions.

Must never break a session: any problem -> no output, exit 0.
"""
import json
import os
import re
import sys
from pathlib import Path

SAFE_ID = re.compile(r"^[A-Za-z0-9_-]+$")
# ponytail: kept tiny on purpose; a long file gets summarised away by the next compaction.
CORE_RULES = Path(__file__).resolve().parent.parent / "skills" / "profesoria" / "core-rules.md"


def _core_rules(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except (OSError, ValueError):
        return ""


def _personality(home: Path) -> str:
    try:
        for line in (home / "profile.md").read_text(encoding="utf-8").splitlines():
            key, _, value = line.partition(":")
            if key.strip() == "personality" and value.strip():
                return value.strip()
    except (OSError, ValueError):
        pass
    return "unknown"


def main(stdin_text: str, home: Path, rules_path: Path = CORE_RULES) -> str:
    try:
        event = json.loads(stdin_text)
        name = event.get("hook_event_name")
        sid = event.get("session_id", "")
    except (ValueError, AttributeError):
        return ""
    if not isinstance(sid, str) or not SAFE_ID.match(sid):
        return ""
    marker = home / "active" / sid

    if name == "UserPromptSubmit" and str(event.get("prompt", "")).strip().startswith("/profesoria"):
        # ponytail: natural-language activation creates no marker (the skill can't see session_id).
        # Old markers are never cleaned up (empty files); add cleanup if active/ ever grows noticeably.
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
        return ""

    if name == "SessionStart" and event.get("source") in ("compact", "resume") and marker.exists():
        context = (
            f"ProfesorIA is active in this session (personality: {_personality(home)}). "
            "Invoke the profesoria skill and keep teaching per its rules. "
            "Resume silently (no announcement) and save any pending map changes now."
        )
        rules = _core_rules(rules_path)
        if rules:
            context += "\nCore rules:\n" + rules
        return json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }})
    return ""


if __name__ == "__main__":
    try:
        home = Path(os.environ.get("PROFESORIA_HOME", "~/.claude/profesoria")).expanduser()
        out = main(sys.stdin.read(), home)
        if out:
            print(out)
    except Exception:
        pass
    sys.exit(0)
