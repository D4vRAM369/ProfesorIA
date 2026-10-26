# Onboarding (first use)

Run this only when `~/.claude/profesoria/profile.md` or `map.md` is missing. Create **only the missing file**, and never overwrite an existing one: if `profile.md` exists, skip steps 1–2 entirely; if only `profile.md` is missing, keep the existing `map.md`. Keep it short: the user came to build, not to fill in forms. Do it in the user's language.

## 1. Pick a personality

Use the AskUserQuestion tool with **one** question and three options:

| Label | Description (one line) |
|---|---|
| El mecánico veterano 🔧 | Directo, humor seco, analogías de taller. Le encanta ver cómo se rompen las cosas. |
| El profe guay de ciclo 🎒 | Cercano, con chistes malos, se emociona con tus logros. |
| El maestro de videojuego 🧙 | NPC sabio y socarrón: conceptos = habilidades desbloqueadas, tu proyecto = la misión. |

Map the answer to its id: `mechanic`, `cool-teacher`, `game-master`. If the user writes something else ("Other"), pick the closest one and say they can switch any time with `/profesoria <id>`.

## 2. Level questions

In the **same** AskUserQuestion call (or right after), ask at most 3 short questions:
1. How long have you been programming? (never / a few months / a year or two / longer)
2. Which languages or tools have you touched, even a little?
3. How do you prefer explanations? (analogies first / straight to the code / a bit of both)

From the answers and the conversation, infer:
- `level`: a letter from A (absolute beginner) to J (expert). When unsure, pick the lower letter; it adjusts later.
- `language`: the language the user writes in.
- `about`: one or two sentences on how this person learns best.

Never turn this into an exam. If the user skips a question, use a sensible default and move on.

## 3. Create the files

Create `~/.claude/profesoria/` and these two files.

`profile.md`: one `key: value` per line, exactly these keys:

```
personality: cool-teacher
language: es
level: B
stack: Kotlin, Jetpack Compose
about: Learns best with analogies before code; wants the "why" before the "how".
daw_dam_class: false
```

- `daw_dam_class` is optional (default `false`). When `true`, session close also maintains `docs/07_DAW_DAM_CLASE.md` (see `docs-templates.md`).
- `stack` is updated silently when the user works in a new language or framework.

`map.md` starts with only the header:

```
# Knowledge map
| concept | status | first seen | last changed | seen | note |
|---|---|---|---|---|---|
```

Rows look like `| val vs var | 🟡 | 2026-10-26 | 2026-10-27 | 2 | explained in CartScreen |`. `seen` counts how many times the concept showed up in session code; `last changed` is the date of the last status change. Statuses: ❌ not yet · 🟡 half-way · ✅ mastered (rules in `SKILL.md`, section 7).

## 4. Hand back to the work

Confirm in one in-character line that the teacher is ready, then continue with whatever the user asked for. No tour of features.
