# TTT agent prompts (canonical)

Runtime-agnostic system prompts. Wrappers (Cursor rules, `SKILL.md`) should **include or @-reference** these files — do not fork prompt text.

**Artifact paths:** Resolve `{artifact_root}` from `ttt_state.json` → `session.artifact_root`, with defaults and fallbacks per **`docs/PHASE0_DECISIONS.md`**.

| File | Agent |
|------|--------|
| `choreographer.md` | Choreographer (orchestration, user-facing) |
| `market_researcher.md` | Market Researcher |
| `user_researcher.md` | User Researcher |
| `product_detailer.md` | Product Detailer (Specify wave 1) |
| `tech_architect.md` | Tech Architect (Specify wave 2) |
| `design_advisor.md` | Design Advisor (Specify wave 2) |
| `test_eval_generator.md` | Test & Eval Generator (Specify wave 2) |

**Specify ordering:** Wave 1 = Product Detailer → `solution.md`. Wave 2 = Tech Architect, Design Advisor, Test & Eval Generator in parallel (each consumes `solution.md` where required).

Example state shape: `schemas/ttt_state.example.json`.
