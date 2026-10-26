#!/usr/bin/env python3
"""Install ProfesorIA into Claude Code: link the skill, add the hook and permissions.

    python3 install.py              # install (safe to run again)
    python3 install.py --uninstall  # remove what install added; your progress stays

Uses $CLAUDE_CONFIG_DIR if set, otherwise ~/.claude. Stdlib only.
"""
import json
import os
import shutil
import sys
from pathlib import Path

HOOK_EVENTS = ("UserPromptSubmit", "SessionStart")
PERMISSIONS = ("Write(~/.claude/profesoria/**)", "Edit(~/.claude/profesoria/**)")
HOOK_MARK = "profesoria_hook.py"


def _fail(msg: str):
    sys.exit(f"ProfesorIA: {msg} Nothing was changed.")


def _load_settings(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as e:
        _fail(f"{path} is not valid JSON ({e}).")
    if not isinstance(data, dict):
        _fail(f"{path} is not a JSON object.")
    return data


def _write_settings(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)  # atomic: settings.json is never left half-written


def _ours(group: dict) -> bool:
    return any(HOOK_MARK in str(h.get("command", "")) for h in group.get("hooks", []))


def install(claude_home: Path, repo: Path) -> None:
    skill_src = (repo / "skills" / "profesoria").resolve()
    link = claude_home / "skills" / "profesoria"
    settings_path = claude_home / "settings.json"

    # Check everything before touching anything.
    if link.is_symlink():
        relink = link.resolve() != skill_src
    elif link.exists():
        _fail(f"{link} already exists and isn't a ProfesorIA link. Move it away first.")
    else:
        relink = True
    data = _load_settings(settings_path)

    backup = settings_path.with_name("settings.json.bak-profesoria")
    if settings_path.exists() and not backup.exists():
        shutil.copy2(settings_path, backup)

    if relink:
        if link.is_symlink():
            link.unlink()
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(skill_src)

    command = f'python3 "{(repo / "hooks" / HOOK_MARK).resolve()}"'
    hooks = data.setdefault("hooks", {})
    for event in HOOK_EVENTS:
        groups = hooks.setdefault(event, [])
        if not any(_ours(g) for g in groups):
            groups.append({"hooks": [{"type": "command", "command": command, "timeout": 5}]})
    allow = data.setdefault("permissions", {}).setdefault("allow", [])
    allow.extend(r for r in PERMISSIONS if r not in allow)
    _write_settings(settings_path, data)


def uninstall(claude_home: Path, repo: Path) -> None:
    link = claude_home / "skills" / "profesoria"
    settings_path = claude_home / "settings.json"
    data = _load_settings(settings_path)

    if link.is_symlink():
        link.unlink()
    hooks = data.get("hooks", {})
    for event in HOOK_EVENTS:
        if event in hooks:
            hooks[event] = [g for g in hooks[event] if not _ours(g)]
            if not hooks[event]:
                del hooks[event]
    perms = data.get("permissions", {})
    if "allow" in perms:
        perms["allow"] = [r for r in perms["allow"] if r not in PERMISSIONS]
    if settings_path.exists():
        _write_settings(settings_path, data)


def main(argv) -> None:
    home = Path(os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude").expanduser()
    repo = Path(__file__).resolve().parent
    if "--uninstall" in argv:
        uninstall(home, repo)
        print("ProfesorIA removed. Your profile and map in ~/.claude/profesoria/ were kept.")
    else:
        install(home, repo)
        print("ProfesorIA installed. Start a new Claude Code session and type /profesoria")


if __name__ == "__main__":
    main(sys.argv[1:])
