import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills/profesoria/SKILL.md"
# Personal strings that must never reach public files: one per line in a
# git-ignored local file, so the list itself is never published.
FORBIDDEN_FILE = ROOT / "tests/forbidden.local.txt"


def parse_frontmatter(path):
    text = path.read_text()
    block = text.split("---", 2)[1]
    meta = {}
    for line in block.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta


def referenced_md_paths(path):
    # relative .md paths written in backticks, e.g. `references/onboarding.md`
    return {
        p for p in re.findall(r"`([\w\-./<>]+\.md)`", path.read_text())
        if "/" in p and "<" not in p and not p.startswith(("~", "/"))
    }


def test_frontmatter():
    meta = parse_frontmatter(SKILL)
    assert meta["name"] == "profesoria"
    assert 50 < len(meta["description"]) <= 1024
    assert "/profesoria" in meta["description"]


def test_referenced_files_exist():
    refs = referenced_md_paths(SKILL)
    assert refs
    for rel in refs:
        assert (SKILL.parent / rel).is_file(), rel


def test_core_rules_present():
    text = SKILL.read_text()
    for must in ["one concept", "TODO(human)", "quiz", "/profesoria progreso",
                 "cierra la sesión", "map.md", "profile.md"]:
        assert must in text, must


def test_no_personal_data():
    if not FORBIDDEN_FILE.exists():
        pytest.skip("no tests/forbidden.local.txt")
    forbidden = [w.strip() for w in FORBIDDEN_FILE.read_text().splitlines() if w.strip()]
    for f in list((ROOT / "skills").rglob("*")) + list((ROOT / "hooks").rglob("*")):
        if f.is_file() and f.suffix in {".md", ".py", ".json"}:
            body = f.read_text()
            for bad in forbidden:
                assert bad not in body, f"{bad} in {f}"


PERS = ["mechanic", "cool-teacher", "game-master"]


def test_personalities_have_sections():
    for p in PERS:
        t = (ROOT / f"skills/profesoria/personalities/{p}.md").read_text()
        for sec in ["## Voice", "## Analogies", "## Emoji", "## Example note"]:
            assert sec in t, (p, sec)


def test_onboarding_defines_formats():
    t = (ROOT / "skills/profesoria/references/onboarding.md").read_text()
    for key in ["personality:", "language:", "level:", "stack:", "about:",
                "daw_dam_class:", "| concept | status |"]:
        assert key in t, key


def test_close_and_docs():
    close = (ROOT / "skills/profesoria/references/session-close.md").read_text()
    for must in ["progress card", "cc-transcript", "once", "append", "map.md"]:
        assert must in close, must
    docs = (ROOT / "skills/profesoria/references/docs-templates.md").read_text()
    for f in ["00_GLOSARIO.md", "03_PASO_A_PASO.md", "05_ERRORES_Y_SOLUCIONES.md", "07_DAW_DAM_CLASE.md"]:
        assert f in docs, f


def test_onboarding_never_overwrites():
    t = (ROOT / "skills/profesoria/references/onboarding.md").read_text()
    assert "only the missing file" in t and "never overwrite" in t


def test_map_schema_supports_rules():
    t = (ROOT / "skills/profesoria/references/onboarding.md").read_text()
    assert "| concept | status | first seen | last changed | seen | note |" in t


def test_reveal_not_spoiled_by_header():
    t = SKILL.read_text()
    assert "plain-language label" in t


def test_mentor_persona_suppressed():
    t = SKILL.read_text()
    assert "checkpoints" in t and "only through teacher notes" in t


def test_slash_activation_survives_compaction_hint():
    assert "survives compaction" in SKILL.read_text()


def test_close_triggers_both_languages_and_offers_on_inferred_end():
    skill = SKILL.read_text()
    close = (ROOT / "skills/profesoria/references/session-close.md").read_text()
    assert "close the session" in parse_frontmatter(SKILL)["description"]
    for t in (skill, close):
        assert "cierra la sesión" in t and "close the session" in t
    assert "offer" in close and "never run the close flow on a guess" in close
