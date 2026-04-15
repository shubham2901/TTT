# TTT agent prompts (canonical)

Runtime-agnostic system prompts. Wrappers (Cursor rules, `SKILL.md`) should **include or @-reference** these files — do not fork prompt text.

**Artifact paths:** Resolve `{artifact_root}` from `ttt_state.json` → `session.artifact_root`, with defaults and fallbacks per **`docs/PHASE0_DECISIONS.md`**.

## Core flow (default choreographer)

| File | Role |
|------|------|
| `choreographer.md` | Orchestration, tone, `research.md` / `plan.md` / `handoff.md` templates, optional `screens.md` / `tests.md` |
| `researcher.md` | Combined market + user research (spawned for the research step) |

**Primary outputs:** `research.md`, `plan.md`, `handoff.md` (under `{artifact_root}/`).

## Optional / extended prompts

These files are **not** required for the default `research.md` → `plan.md` → `handoff.md` path. Keep them for advanced or legacy Specify-style workflows.

| File | Role |
|------|------|
| `product_detailer.md` | Extended product / solution detail |
| `tech_architect.md` | Technical architecture |
| `design_advisor.md` | Design guidance |
| `test_eval_generator.md` | Tests and evaluation criteria |

Example state shape: `schemas/ttt_state.example.json`.
