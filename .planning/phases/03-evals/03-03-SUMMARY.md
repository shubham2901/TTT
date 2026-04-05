---
phase: 03-evals
plan: 03
subsystem: testing
tags: [eval-harness, llm-judge, python-cli, rubric, scoring]

requires:
  - phase: 03-evals (plan 01)
    provides: Scenario scripts (s1–s4) for eval runs
  - phase: 03-evals (plan 02)
    provides: Rubric with dimension weights and scorecard template
provides:
  - Step-by-step eval protocol (protocol.md)
  - Python CLI harness with 4 subcommands for eval run lifecycle (harness.py)
  - Self-contained LLM-judge prompt with calibration examples (judge.md)
  - Runs directory for eval bundles (runs/.gitkeep)
affects: [prompt-iteration, eval-loop]

tech-stack:
  added: [python-stdlib-cli]
  patterns: [argparse-subcommands, json-scoring-output, sha256-version-tracking]

key-files:
  created:
    - evals/protocol.md
    - evals/harness.py
    - evals/judge.md
    - evals/runs/.gitkeep
  modified: []

key-decisions:
  - "WEIGHTS stored as index-matched lists instead of nested dicts for conciseness"
  - "Judge uses single rubric table instead of embedding all 9 artifact-specific tables — keeps prompt under 250 lines while remaining self-contained"
  - "Scorecard generation is code-driven (_write_scorecard) rather than template-filling for reliability"

patterns-established:
  - "CLI harness pattern: argparse subcommands with Path-based file ops"
  - "Score output: dual JSON + markdown for machine and human consumers"

requirements-completed: [P3-T3, P3-T4]

duration: 12min
completed: 2026-04-05
---

# Phase 3 Plan 03: Harness + Judge Summary

**Python CLI harness (4 subcommands: new/collect/score/compare), step-by-step eval protocol, and self-contained Claude-targeted LLM-judge prompt with 3 calibration examples and embedded rubric**

## Performance

- **Duration:** ~12 min
- **Started:** 2026-04-05
- **Completed:** 2026-04-05
- **Tasks:** 4
- **Files created:** 4

## Accomplishments

- Eval protocol with 7 numbered steps, each referencing the harness command to run
- Python CLI harness (326 lines, stdlib only) automating run initialization, artifact collection, interactive scoring, and cross-run comparison
- LLM-judge prompt (235 lines) with embedded rubric dimensions, 10 failure modes, bias mitigation directives, and 3 calibration examples at high (~4.5), medium (~3.0), and low (~1.5) quality levels
- Runs directory ready for eval bundles

## Task Commits

_(Not a git repo — no commits made.)_

## Files Created/Modified

- `evals/protocol.md` — 7-step evaluator guide (100 lines) with prerequisites, harness references, and evaluation principles
- `evals/harness.py` — Python CLI (326 lines) with `new`, `collect`, `score`, `compare` subcommands; reads scenarios, rubric weights, and scorecard template; produces JSON scores and filled scorecards
- `evals/judge.md` — Self-contained LLM-judge prompt (235 lines) with condensed rubric table, evaluation process, bias mitigation, failure taxonomy (10 modes), dual output format (JSON + markdown), and 3 calibration examples
- `evals/runs/.gitkeep` — Empty file preserving runs directory

## Decisions Made

- Stored dimension weights as index-matched lists (not nested dicts) — more concise, matches dimension order in DIMENSIONS constant
- Judge prompt uses a single condensed rubric table instead of embedding all 9 per-artifact tables — keeps the prompt under 250 lines while remaining fully self-contained
- Scorecard generation is code-driven rather than text substitution — more reliable for computed fields (weighted scores, aggregates, pass/fail)

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Complete eval framework: scenarios (plan 01) + rubric/scorecard (plan 02) + harness/judge/protocol (plan 03)
- An evaluator can now run the full loop: `harness.py new` → execute TTT → `collect` → `score` → `compare`
- LLM judge prompt is ready for calibration against human scores (future eval loop step)
- Phase 3 (Evals) is complete

---
*Phase: 03-evals*
*Completed: 2026-04-05*
