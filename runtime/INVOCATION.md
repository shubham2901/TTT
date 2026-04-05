# TTT — Invocation Matrix

Maps every TTT phase to prompt files, inputs, outputs, and runtime-specific invocation.

---

## Phase → Agent → Files

| Phase | Agent | Prompt File | Input Files | Output File | Parallel? |
|-------|-------|-------------|-------------|-------------|-----------|
| Clarify | Choreographer | `prompts/choreographer.md` | (user input) | `clarification.md` | N/A (direct) |
| Validate | Market Researcher | `prompts/market_researcher.md` | `clarification.md` | `market_research.md` | Yes (with User Researcher) |
| Validate | User Researcher | `prompts/user_researcher.md` | `clarification.md` | `user_research.md` | Yes (with Market Researcher) |
| Validate | Choreographer | `prompts/choreographer.md` | `market_research.md`, `user_research.md` | (synthesis — presented to user) | N/A (after both researchers) |
| Define | Choreographer | `prompts/choreographer.md` | `clarification.md`, `market_research.md`, `user_research.md` | `definition.md` | N/A (direct) |
| Specify W1 | Product Detailer | `prompts/product_detailer.md` | `definition.md`, `market_research.md`, `user_research.md` | `solution.md` | No (runs first) |
| Specify W2 | Tech Architect | `prompts/tech_architect.md` | `definition.md` | `tech_architecture.md` | Yes (with Design + Test) |
| Specify W2 | Design Advisor | `prompts/design_advisor.md` | `definition.md`, `solution.md` | `design_guideline.md` | Yes (with Tech + Test) |
| Specify W2 | Test & Eval Gen | `prompts/test_eval_generator.md` | `definition.md`, `solution.md` | `test_eval.md` | Yes (with Tech + Design) |
| Specify | Choreographer | `prompts/choreographer.md` | all Specify outputs | `coding_agent_prompt.md`, `blueprint.md`, `versions.md` | N/A (final assembly) |
| Launch | Choreographer | `prompts/choreographer.md` | all prior outputs | `launch.md` | N/A (optional) |

All output files are written to `{artifact_root}/` (default: `ttt/`). Input file paths are relative to `{artifact_root}/` except prompt files which are at project root.

---

## Runtime-Specific Invocation

| Action | Cursor | Claude Code |
|--------|--------|-------------|
| Entry point file | `.cursor/rules/ttt.mdc` | `skills/ttt/SKILL.md` |
| Start TTT | Say "TTT" in Agent chat | Say "TTT" or `/ttt` |
| Activation mechanism | Agent-decided (description match) + glob (`ttt/**`) | Description matching + `/ttt` slash command |
| Load choreographer | Agent reads `@prompts/choreographer.md` | Agent reads `prompts/choreographer.md` |
| Spawn subagent | Task tool (foreground, blocking) | Sequential in-context (or `context: fork` if available) |
| Parallel subagents | Multiple Task calls in one response | Sequential with honest progress messaging |
| Subagent fallback | Read prompt inline with `@prompts/[agent].md` | Read prompt inline |
| File path syntax | `@` paths (e.g., `@prompts/choreographer.md`) | Project-root-relative (e.g., `prompts/choreographer.md`) |
| Web search | Partial — escalate after 1 blocked failure | Partial — same escalation |
| State persistence | `ttt/ttt_state.json` | `ttt/ttt_state.json` |
| Resume session | Agent reads state file on session start | Agent reads state file on session start |
| Install method | Copy `.cursor/rules/ttt.mdc` + `prompts/` | Copy `skills/ttt/SKILL.md` + `prompts/` |
| Setup docs | `runtime/cursor/README.md` | `runtime/claude-code/README.md` |

---

## Behavioral contract (shared)

Both runtimes honor these non-negotiable behaviors per `docs/PHASE0_DECISIONS.md`:

- Honest ordering when subagents run sequentially ("Market Researcher first, then User Researcher")
- Identical artifact set and structure regardless of runtime
- No silent skip of Validate — user must explicitly acknowledge
- Search-blocked failures escalate to user after one attempt
- State persisted in `ttt_state.json` on every transition, decision, pivot
- Scope guard: max 5 V1 features, each maps to a JTBD

---

## Vibe it!! path

Available after Clarify in both runtimes. The Choreographer generates all remaining files directly — no subagents, no quality gates, no retries. Same behavior in both runtimes. All assumptions stated explicitly. All files remain editable.

---

## References

- Phase 0 decisions: `docs/PHASE0_DECISIONS.md`
- Choreographer (full orchestration): `prompts/choreographer.md`
- State schema: `schemas/ttt_state.example.json`
