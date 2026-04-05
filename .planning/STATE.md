# Project state — TTT

**Last updated:** 2026-04-05

## Current focus

- **Phase 0** closed. **Phase 1** complete. **Phase 2** complete: runtime packaging for Cursor and Claude Code.
- **Phase 3** (Evals): Plan 01 (scenarios) complete. Plan 02 (rubric + scorecard) complete. **Plan 03 (harness + judge) complete.** Phase 3 fully complete.
- **Phase R** (Opus review): not started.
- **Opus (when you choose):** Refine `prompts/choreographer.md` / orchestration copy; separate session.

## Phase 3 progress

| Plan | Name | Status |
|------|------|--------|
| 03-01 | Eval scenarios | **Complete** |
| 03-02 | Rubric + scorecard | **Complete** |
| 03-03 | Harness + judge | **Complete** |

### Plan 03 deliverables

| File | Lines | Purpose |
|------|-------|---------|
| `evals/protocol.md` | 100 | 7-step evaluator guide referencing harness commands |
| `evals/harness.py` | 326 | Python CLI (stdlib only) with new/collect/score/compare subcommands |
| `evals/judge.md` | 235 | Self-contained LLM-judge prompt with calibration examples |
| `evals/runs/.gitkeep` | 0 | Empty directory for eval run bundles |

### Plan 02 deliverables

| File | Lines | Purpose |
|------|-------|---------|
| `evals/rubric.md` | 250 | Versioned 5-dimension scoring framework for all 9 TTT artifacts |
| `evals/scorecard.md` | 120 | Blank fill-in template for recording scores per eval run |

## Phase 2 deliverables

| File | Lines | Purpose |
|------|-------|---------|
| `.cursor/rules/ttt.mdc` | 43 | Cursor entry point (agent-decided + glob activation) |
| `skills/ttt/SKILL.md` | 167 | Claude Code skill entry point (updated) |
| `runtime/cursor/README.md` | 120 | Cursor setup, fallbacks, troubleshooting |
| `runtime/claude-code/README.md` | 130 | Claude Code install, testing, troubleshooting |
| `runtime/INVOCATION.md` | 70 | Unified invocation matrix (both runtimes) |
| `runtime/README.md` | 52 | Runtime index with future adapter plans |

## Session Continuity

Last session: 2026-04-05
Stopped at: Completed 03-03-PLAN.md (harness + judge) — Phase 3 fully complete
Resume file: `.planning/phases/03-evals/03-03-SUMMARY.md`

## Resume pointers

- Phase 3 plans: `.planning/phases/03-evals/03-0{1,2,3}-PLAN.md`
- Phase 3 summaries: `.planning/phases/03-evals/03-0{1,2,3}-SUMMARY.md`
- Phase 3 research: `.planning/phases/03-evals/03-RESEARCH.md`
- Phase 3 context: `.planning/phases/03-evals/03-CONTEXT.md`
- Eval protocol: `evals/protocol.md`
- Eval harness: `evals/harness.py`
- Eval judge prompt: `evals/judge.md`
- Eval rubric: `evals/rubric.md`
- Eval scorecard: `evals/scorecard.md`
- Eval scenarios: `evals/scenarios/s{1,2,3,4}-*.md`
- Eval runs: `evals/runs/`
- Phase 2 summaries: `.planning/phases/02-runtime-packaging-wave-1/02-0{1,2,3}-SUMMARY.md`
- Phase 2 context: `.planning/phases/02-runtime-packaging-wave-1/02-CONTEXT.md`
- Phase 0 context: `.planning/phases/00-runtime-gates/00-CONTEXT.md`
- Decisions: `docs/PHASE0_DECISIONS.md`
- Spikes: `docs/phase0-spike-log.md`

## Decisions

- Rubric uses artifact-specific anchor text at 1/3/5 scale levels, not generic descriptors
- Research artifacts weight comprehensiveness highest; spec artifacts weight actionability highest
- Cross-file alignment mirrors choreographer's spec completeness checks (4 directed + 1 global pass)
- Pass/fail requires no single dimension < 3 across any artifact — prevents strong files from masking weak ones
- Harness weights stored as index-matched lists for conciseness
- Judge prompt embeds condensed rubric table (not all 9 artifact tables) to stay self-contained under 250 lines
- Scorecard generation is code-driven for reliability with computed fields

## Notes

- Authoritative product plan: `plan.md`
- Executable task plan: `PHASE_PLAN.md`
