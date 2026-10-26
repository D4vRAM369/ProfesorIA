# Project docs templates (absorbed from Chronicler)

Used at session close (`session-close.md`). Instructions are in English; **the generated docs are written in the user's `language:`**. File names stay as below (Spanish), so projects documented earlier by Chronicler keep working.

## Who the docs are for

Write the docs **from zero, for a reader with no prior knowledge**: the user six months from now, and other beginners who might read the repo. Treat every term, tool or command as if the reader sees it for the first time, even "basic" ones (what a terminal is, what a package is, what an API is).

The knowledge map does **not** filter the docs. A concept marked ✅ for the user still gets explained in the glossary. The map only governs teacher notes in the chat.

## Golden rules

1. **Append, never overwrite.** If `docs/` already exists (made by Chronicler or by a previous session), extend those same files, under a new session header (`## Sesión N — YYYY-MM-DD`) or as new entries. Never rewrite existing content, never delete it, never create parallel files with similar names.
2. Never document only the *what*: always the *why* and the *what for*.
3. Every error that appeared in the session → `05_ERRORES_Y_SOLUCIONES.md`. Errors are premium content.
4. Every new technical term → `00_GLOSARIO.md`.
5. Every step must be reproducible by a stranger who wasn't in the session.
6. Don't rewrite history: if something was tried first and failed, document that too.
7. No filler. Every line must add something.
8. Code in the docs always has comments that explain the *why*, not the obvious.

## File tree

Create any missing file with its base header; leave existing ones alone except for appending.

```
docs/
├── README.md                    ← project front page
├── 00_GLOSARIO.md               ← technical terms in plain words (always updated)
├── 01_SETUP.md                  ← environment setup
├── 02_ARQUITECTURA.md           ← design decisions and structure
├── 03_PASO_A_PASO.md            ← the heart: how it was built, step by step
├── 04_CONCEPTOS.md              ← concepts learned during the project
├── 05_ERRORES_Y_SOLUCIONES.md   ← real errors, root cause and fix
├── 06_SIGUIENTE_NIVEL.md        ← what could be improved or expanded
└── 07_DAW_DAM_CLASE.md          ← ONLY if profile has `daw_dam_class: true`
```

`07_DAW_DAM_CLASE.md` is created and maintained **only when `profile.md` has `daw_dam_class: true`**. It's a teaching guide that walks through the project from zero like a vocational-school class (DAW/DAM, the Spanish web and multiplatform development courses). Unlike `03_PASO_A_PASO.md`, which is technical and reproducible, it explains *why each piece matters*, with analogies. Update it when a new "lesson" is completed or the stack changes.

## What goes where

| Event in the session | File |
|---|---|
| Stack chosen or changed | `02_ARQUITECTURA.md` |
| Something installed or configured | `01_SETUP.md` |
| New code written | `03_PASO_A_PASO.md` |
| An error appeared | `05_ERRORES_Y_SOLUCIONES.md` |
| New technical term used | `00_GLOSARIO.md` |
| Design decision taken | `02_ARQUITECTURA.md` |
| New concept learned | `04_CONCEPTOS.md` |
| Ideas for later | `06_SIGUIENTE_NIVEL.md` |
| Lesson completed / stack changed (if enabled) | `07_DAW_DAM_CLASE.md` |

## Templates

### `README.md`

```markdown
# [Project name]

> [One sentence: what it does and what it's for]

## ¿Qué es esto?
[Plain-language description: what it does, who would use it, what problem it solves.]

## ¿Qué vas a aprender siguiendo esta documentación?
- [Concept 1]
- [Concept N]

## Stack tecnológico
| Tecnología | Versión | Para qué se usa |
|---|---|---|

## Estructura del proyecto
[directory tree]

## Cómo seguir esta documentación
Lee los archivos en orden: 01 → 02 → 03 → …
```

### `00_GLOSARIO.md` entry

```markdown
## [Term]

**Definición simple:** [one sentence, for someone who never programmed]
**Definición técnica:** [more precise]
**Analogía:** [real-world comparison]
**En este proyecto lo usamos para:** [specific context]
**Ejemplo:**
[minimal code that shows the concept]
```

### `03_PASO_A_PASO.md` step

```markdown
## Paso N: [Descriptive name]

**Qué vamos a hacer:** [one sentence]
**Por qué lo hacemos así:** [the reason behind the decision]
**Resultado esperado:** [what should happen when the step is done]

### Instrucciones
[Clear prose]
[Code with comments on every important line]

> 💡 **Nota para aprendices:** [an insight, a common trap, something learned here]
> ⚠️ **Errores comunes:** [typical errors in this step, if any]

**Verificación:** [a concrete way to check the step worked]
```

### `05_ERRORES_Y_SOLUCIONES.md` entry

```markdown
## Error: [Short description]

**Fecha:** [when]
**Contexto:** [what was being attempted]
**El error exacto:**
[full error message]
**Por qué ocurrió:** [root cause: not just "it failed" but why the system produces it]
**Cómo se resolvió:** [exact steps]
**Qué aprendimos:** [the lasting insight: the most valuable part]
```

### `04_CONCEPTOS.md` entry

```markdown
## [Concept]

**Qué es:** [one sentence]
**Para qué sirve:** [the problem it solves]
**Analogía:** [real-world comparison]
**Dónde aparece en el proyecto:** [file / function]
**Se conecta con:** [concepts already known it builds on]
```
