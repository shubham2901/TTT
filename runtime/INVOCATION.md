# TTT — Invocation Matrix

Maps the TTT conversation flow to prompt files, inputs, outputs, and runtime-specific invocation.

---

## Flow → Agent → Files

| Step | Agent | Prompt file | Typical inputs | Output file(s) | Notes |
|------|-------|-------------|----------------|----------------|-------|
| Orchestration | Choreographer | `prompts/choreographer.md` | User messages, prior artifacts | (conversation; silent state updates) | Always loaded for TTT |
| Understand | Choreographer | `prompts/choreographer.md` | User input | — | No separate prompt; clarifies in chat |
| Research | Researcher | `prompts/researcher.md` | Idea, audience, platform, constraints (from choreographer) | `research.md` | Spawn via Task tool or run inline |
| Plan | Choreographer | `prompts/choreographer.md` | `research.md` (and conversation) | `plan.md` | Choreographer writes |
| Handoff | Choreographer | `prompts/choreographer.md` | `plan.md` (and conversation) | `handoff.md` | Choreographer writes |
| Optional | Choreographer | `prompts/choreographer.md` | `plan.md` | `screens.md`, `tests.md` | Only if user asks |

**Shortcut:** After the idea is clear enough, the user may say **"you decide"** to skip research and move faster with stated assumptions (see `prompts/choreographer.md`).

**Additional prompts (not in the default handoff path):** `product_detailer.md`, `tech_architect.md`, `design_advisor.md`, `test_eval_generator.md` remain in `prompts/` for extended / legacy Specify-style workflows. The current choreographer does not require them for `research.md` → `plan.md` → `handoff.md`.

All artifact paths are under `{artifact_root}/` (default: `ttt/`). Prompt paths are project-root-relative.

---

## Runtime-Specific Invocation

| Action | Cursor | Claude Code |
|--------|--------|-------------|
| Entry point file | `.cursor/rules/ttt.mdc` | `skills/ttt/SKILL.md` |
| Start TTT | Say "TTT" in Agent chat | Say "TTT" or `/ttt` |
| Activation mechanism | Agent-decided (description match) + glob (`ttt/**`) | Description matching + `/ttt` slash command |
| Load choreographer | Agent reads `@prompts/choreographer.md` | Agent reads `prompts/choreographer.md` |
| Spawn researcher | Task tool (foreground, blocking) | Sequential in-context (or fork if available) |
| Subagent fallback | Read prompt inline with `@prompts/researcher.md` | Read prompt inline |
| File path syntax | `@` paths (e.g., `@prompts/choreographer.md`) | Project-root-relative (e.g., `prompts/choreographer.md`) |
| Web search | Recommended for research — escalate after 1 blocked failure | Same |
| State persistence | `ttt/ttt_state.json` | `ttt/ttt_state.json` |
| Resume session | Agent reads state file on session start | Agent reads state file on session start |
| Install method | Copy `.cursor/rules/ttt.mdc` + `prompts/` | Copy `skills/ttt/SKILL.md` + `prompts/` |
| Setup docs | `runtime/cursor/README.md` | `runtime/claude-code/README.md` |

---

## Behavioral contract (shared)

Both runtimes honor these behaviors (see also `docs/PHASE0_DECISIONS.md` where applicable):

- Identical canonical prompts — never fork prompt text in wrappers.
- **Research:** Do not silently skip when the user expected research; skipping with **"you decide"** is explicit.
- Search-blocked failures escalate to the user after one attempt.
- State persisted in `ttt_state.json` on meaningful progress (without narrating to the user).
- Scope guard: max 5 V1 features, each tied to a user problem.

---

## References

- Phase 0 decisions: `docs/PHASE0_DECISIONS.md`
- Choreographer: `prompts/choreographer.md`
- Researcher: `prompts/researcher.md`
- Example state: `schemas/ttt_state.example.json`
