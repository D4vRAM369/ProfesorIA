# Session close and progress card

## Close flow

Run only when the user explicitly asks to close: "cierra la sesión", "close the session", or the same request in their language. The close flow writes files into the user's project, so never run the close flow on a guess: if the end is only implied (a goodbye, a pause), offer it in one line ("¿Cierro la sesión y genero la documentación?") and wait. In order:

1. **Save the map.** Write every pending change to `~/.claude/profesoria/map.md` (and `level:` / `stack:` in `profile.md` if they changed). This is the one write that must always happen.
2. **Project docs.** Generate or append the project's `docs/` following `docs-templates.md`. If `docs/` already exists, **append**: never overwrite or delete existing content. Only document what happened in this session.
3. **Session summary.** Show it in chat, in the user's language and in the personality's voice (lightly: the structure stays readable):

   ```
   📋 RESUMEN DE SESIÓN

   PROYECTO: [name]
   FECHA: [YYYY-MM-DD]

   ✅ LO QUE LOGRAMOS:
   - [achievement]

   📚 CONCEPTOS APRENDIDOS:
   - [concept]: [one-line explanation]

   🔜 PRÓXIMOS PASOS:
   - [step]

   ❓ PENDIENTES/DUDAS:
   - [anything left unresolved]
   ```

   Also append it to `docs/03_PASO_A_PASO.md` under the session header.

4. **Transcript offer, once.** Check whether a transcript skill is installed: `ls ~/.claude/skills/cc-transcript ~/.claude/skills/transcript 2>/dev/null`, or look for a `transcript` / `cc-transcript` skill in the available skills list. If one exists, mention **once**, in one line, that the user can export this conversation with `/transcript`. If none exists, say nothing about it. Never repeat the offer in the same session, even if the user keeps working after the close.

Near the end of a long session (the user is wrapping up but hasn't said "cierra la sesión"), you may remind them **once** that "cierra la sesión" will generate the docs. That counts as the reminder; don't nag.

## Progress card (`/profesoria progreso`)

A short card in the personality's voice, built from `map.md` and `profile.md`. Never longer than about 6 lines:

```
🎓 <emoji> Ficha de <user name or "aprendiz"> — Nivel: <level letter + short label>
Desbloqueado esta semana: 🔓 <✅ items whose `last changed` is within the last 7 days>
En camino: 🟡 <🟡 items, up to 3>
Próximo jefe final: <the ❌ concept with the highest `seen` count>
```

- Empty sections are omitted, not shown as "none".
- If the map is still empty, say so in one friendly line and that it fills itself as they build.
- Show the card, then return to the work. No follow-up questions.
