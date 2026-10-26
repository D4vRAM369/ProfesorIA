import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = str(ROOT / "hooks/profesoria_hook.py")
sys.path.insert(0, str(ROOT / "hooks"))

from profesoria_hook import main  # noqa: E402


def ev(**kw):
    return json.dumps(kw)


def mark(home, sid="s1"):
    (home / "active").mkdir(exist_ok=True)
    (home / "active" / sid).touch()


def test_activation_creates_marker(tmp_path):
    out = main(ev(hook_event_name="UserPromptSubmit", session_id="s1", prompt="/profesoria npc"), tmp_path)
    assert out == ""
    assert (tmp_path / "active" / "s1").exists()


def test_other_prompt_no_marker(tmp_path):
    main(ev(hook_event_name="UserPromptSubmit", session_id="s1", prompt="hola"), tmp_path)
    assert not (tmp_path / "active" / "s1").exists()


def test_reminder_after_compact(tmp_path):
    mark(tmp_path)
    (tmp_path / "profile.md").write_text("personality: mechanic\nlanguage: es\n")
    out = json.loads(main(ev(hook_event_name="SessionStart", session_id="s1", source="compact"), tmp_path))
    ctx = out["hookSpecificOutput"]["additionalContext"]
    assert out["hookSpecificOutput"]["hookEventName"] == "SessionStart"
    assert "ProfesorIA is active" in ctx and "mechanic" in ctx


def test_no_reminder_on_fresh_startup(tmp_path):
    mark(tmp_path)
    assert main(ev(hook_event_name="SessionStart", session_id="s1", source="startup"), tmp_path) == ""


def test_no_reminder_for_other_session(tmp_path):
    mark(tmp_path, "other")
    assert main(ev(hook_event_name="SessionStart", session_id="s1", source="compact"), tmp_path) == ""


def test_reminder_without_profile(tmp_path):
    mark(tmp_path)
    out = main(ev(hook_event_name="SessionStart", session_id="s1", source="resume"), tmp_path)
    assert "unknown" in out


def test_garbage_stdin_is_silent(tmp_path):
    for bad in ["", "not json", "[]", ev(hook_event_name="SessionStart"),
                ev(hook_event_name="UserPromptSubmit", session_id="../x", prompt="/profesoria")]:
        assert main(bad, tmp_path) == ""
    assert not (tmp_path / "x").exists()


def test_cli_exits_zero_on_garbage(tmp_path):
    r = subprocess.run([sys.executable, HOOK], input="{{", text=True, capture_output=True,
                       env={**os.environ, "PROFESORIA_HOME": str(tmp_path)})
    assert r.returncode == 0 and r.stdout == ""


def test_reminder_survives_non_utf8_profile(tmp_path):
    mark(tmp_path)
    (tmp_path / "profile.md").write_bytes(b"personality: \xff\xfe\n")
    out = main(ev(hook_event_name="SessionStart", session_id="s1", source="compact"), tmp_path)
    assert "ProfesorIA is active" in out


def test_reminder_resumes_silently_and_saves_map(tmp_path):
    mark(tmp_path)
    ctx = json.loads(main(ev(hook_event_name="SessionStart", session_id="s1", source="compact"),
                          tmp_path))["hookSpecificOutput"]["additionalContext"]
    assert "silently" in ctx and "map" in ctx
