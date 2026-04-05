# TTT — Runtime Documentation

Index for runtime-specific entry points, setup guides, and the unified invocation matrix.

---

## Entry points

| Runtime | Entry Point | Setup Guide |
|---------|-------------|-------------|
| Cursor | `.cursor/rules/ttt.mdc` | `runtime/cursor/README.md` |
| Claude Code | `skills/ttt/SKILL.md` | `runtime/claude-code/README.md` |

---

## Invocation matrix

`runtime/INVOCATION.md` — Maps every TTT phase to prompt files, inputs, outputs, and runtime differences. Single source of truth for which agent runs when, with what inputs, producing what outputs.

---

## Shared behavior

Both runtimes honor the same behavioral contract defined in `docs/PHASE0_DECISIONS.md`. Identical artifact set, scope guard, state persistence, and search degradation rules regardless of runtime.

---

## Canonical prompts

All prompts live in `prompts/`. Both runtimes reference these files — never fork prompt content. Seven prompt files: choreographer, market researcher, user researcher, product detailer, tech architect, design advisor, test & eval generator.

---

## Future adapters (Wave 2/3)

Planned runtimes not yet supported:

- **Windsurf** (Wave 2)
- **VS Code** (Wave 2)
- **Codex** (Wave 2)
- **claude.ai / Claude Desktop** (Wave 3 — may need UX adaptations for no persistent filesystem)
- **Anti Gravity** (Wave 3)

Same canonical prompts. Different wrapper files. No prompt changes — adapter only.

---

## References

- Phase 0 decisions: `docs/PHASE0_DECISIONS.md`
- Product plan: `plan.md`
- State schema: `schemas/ttt_state.example.json`
