import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from install import install, uninstall, HOOK_EVENTS, PERMISSIONS  # noqa: E402


def settings(home):
    return json.loads((home / "settings.json").read_text())


def hook_commands(s, event):
    return [h["command"] for g in s.get("hooks", {}).get(event, []) for h in g.get("hooks", [])]


def test_fresh_install(tmp_path):
    install(tmp_path, ROOT)
    link = tmp_path / "skills" / "profesoria"
    assert link.is_symlink() and link.resolve() == (ROOT / "skills/profesoria").resolve()
    s = settings(tmp_path)
    for ev in HOOK_EVENTS:
        assert sum("profesoria_hook.py" in c for c in hook_commands(s, ev)) == 1
    for rule in PERMISSIONS:
        assert rule in s["permissions"]["allow"]


def test_install_twice_is_idempotent(tmp_path):
    install(tmp_path, ROOT)
    install(tmp_path, ROOT)
    s = settings(tmp_path)
    for ev in HOOK_EVENTS:
        assert sum("profesoria_hook.py" in c for c in hook_commands(s, ev)) == 1
    assert len(s["permissions"]["allow"]) == len(PERMISSIONS)


def test_preserves_existing_settings_and_backs_up(tmp_path):
    original = {
        "model": "sonnet",
        "hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "node other.js"}]}]},
        "permissions": {"allow": ["Bash(ls)"]},
    }
    (tmp_path / "settings.json").write_text(json.dumps(original))
    install(tmp_path, ROOT)
    s = settings(tmp_path)
    assert s["model"] == "sonnet"
    assert "node other.js" in hook_commands(s, "SessionStart")
    assert "Bash(ls)" in s["permissions"]["allow"]
    assert json.loads((tmp_path / "settings.json.bak-profesoria").read_text()) == original


def test_existing_manual_hook_not_duplicated(tmp_path):
    manual = {"hooks": {ev: [{"hooks": [{"type": "command",
              "command": "python3 /old/path/hooks/profesoria_hook.py"}]}] for ev in HOOK_EVENTS}}
    (tmp_path / "settings.json").write_text(json.dumps(manual))
    install(tmp_path, ROOT)
    s = settings(tmp_path)
    for ev in HOOK_EVENTS:
        assert sum("profesoria_hook.py" in c for c in hook_commands(s, ev)) == 1


def test_invalid_settings_aborts_untouched(tmp_path):
    (tmp_path / "settings.json").write_text("{not json")
    with pytest.raises(SystemExit):
        install(tmp_path, ROOT)
    assert (tmp_path / "settings.json").read_text() == "{not json"
    assert not (tmp_path / "skills" / "profesoria").exists()


def test_foreign_skill_dir_aborts_untouched(tmp_path):
    (tmp_path / "skills" / "profesoria").mkdir(parents=True)
    (tmp_path / "skills" / "profesoria" / "SKILL.md").write_text("someone else's")
    with pytest.raises(SystemExit):
        install(tmp_path, ROOT)
    assert (tmp_path / "skills" / "profesoria" / "SKILL.md").read_text() == "someone else's"
    assert not (tmp_path / "settings.json").exists()


def test_uninstall_removes_only_ours(tmp_path):
    (tmp_path / "settings.json").write_text(json.dumps(
        {"hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "node other.js"}]}]},
         "permissions": {"allow": ["Bash(ls)"]}}))
    install(tmp_path, ROOT)
    (tmp_path / "profesoria").mkdir()
    (tmp_path / "profesoria" / "map.md").write_text("my progress")
    uninstall(tmp_path, ROOT)
    s = settings(tmp_path)
    assert not (tmp_path / "skills" / "profesoria").exists()
    for ev in HOOK_EVENTS:
        assert not any("profesoria_hook.py" in c for c in hook_commands(s, ev))
    assert "node other.js" in hook_commands(s, "SessionStart")
    assert s["permissions"]["allow"] == ["Bash(ls)"]
    assert (tmp_path / "profesoria" / "map.md").read_text() == "my progress"


def test_cli_uses_claude_config_dir(tmp_path):
    r = subprocess.run([sys.executable, str(ROOT / "install.py")], capture_output=True, text=True,
                       env={"CLAUDE_CONFIG_DIR": str(tmp_path), "PATH": "/usr/bin:/bin"})
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "skills" / "profesoria").is_symlink()
