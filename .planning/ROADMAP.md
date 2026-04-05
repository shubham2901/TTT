# Roadmap — TTT (To The T)

Aligned with `plan.md` and `PHASE_PLAN.md`.

## Phases

### Phase 0: Runtime gates
**Goal:** Lock how Cursor and Claude Code spawn subagents, use web search, and write artifacts before any prompt authoring.

### Phase 1: Core prompts
**Goal:** Seven canonical agent prompts as markdown, paths consistent with Phase 0.

### Phase 2: Runtime packaging (Wave 1)
**Goal:** Package Phase 1's seven canonical prompts into runtime-native entry points for Cursor (`.cursor/rules/ttt.mdc`) and Claude Code (`skills/ttt/SKILL.md`), with unified invocation documentation.

**Requirements:** P2-T1, P2-T2, P2-T3
**Plans:** 3 plans

Plans:
- [x] 02-01-PLAN.md — Cursor wrapper (ttt.mdc + runtime/cursor/README.md)
- [x] 02-02-PLAN.md — Claude Code skill (SKILL.md update + runtime/claude-code/README.md)
- [x] 02-03-PLAN.md — Invocation matrix (INVOCATION.md + runtime/README.md update)

### Phase R: Opus review
**Goal:** Separate-thread review → `docs/OPUS_REVIEW.md`; triage with Composer 2.

### Phase 3: Evals
**Goal:** Scenarios S1–S4, rubric, protocol, LLM-judge stub.

**Requirements:** P3-T1, P3-T2, P3-T3, P3-T4
**Plans:** 3 plans

Plans:
- [x] 03-01-PLAN.md — Scenario scripts (S1–S4 with 2–3 variants each, multi-turn, checkpoints)
- [x] 03-02-PLAN.md — Rubric + scoring (5 dimensions, per-artifact anchors, weights, failure taxonomy, scorecard)
- [x] 03-03-PLAN.md — Protocol + harness + LLM judge (CLI harness.py, eval protocol, judge prompt with calibration)
