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

Both runtimes honor the same behavioral contract defined in `docs/PHASE0_DECISIONS.md` where it still applies. Core artifact set: `research.md`, `plan.md`, `handoff.md` (plus optional `screens.md`, `tests.md`). Same scope guard, state persistence, and search degradation expectations regardless of runtime.

---

## Canonical prompts

All prompts live in `prompts/`. Both runtimes reference these files — never fork prompt content.

**Core path:** `choreographer.md` (orchestration) and `researcher.md` (combined market + user research).

**Additional files** (optional / extended workflows): `product_detailer.md`, `tech_architect.md`, `design_advisor.md`, `test_eval_generator.md` — present for legacy or advanced Specify-style use; the default choreographer flow does not require them for the three core outputs above.

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
