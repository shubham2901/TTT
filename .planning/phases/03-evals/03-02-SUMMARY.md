---
phase: 03-evals
plan: 02
subsystem: testing
tags: [evaluation, rubric, scoring, quality-gates]

requires:
  - phase: 01-core-prompts
    provides: Quality gate definitions and artifact templates (choreographer.md, architecture Part 2)
provides:
  - Versioned evaluation rubric with 5-dimension scoring framework for all 9 TTT artifacts
  - Blank scorecard template for recording scores per eval run
affects: [03-evals plan 03 (LLM judge prompt uses rubric anchors), eval execution workflow]

tech-stack:
  added: []
  patterns: [dimension-weighted scoring, anchored rubric scales, cross-file alignment passes]

key-files:
  created:
    - evals/rubric.md
    - evals/scorecard.md
  modified: []

key-decisions:
  - "Artifact-specific anchor text at 1/3/5 scale levels rather than generic descriptors"
  - "Research artifacts weight comprehensiveness highest; spec artifacts weight actionability highest"
  - "Cross-file alignment as separate scoring section with 4 directed + 1 global pass, mirroring choreographer's 8-check spec completeness"
  - "Pass/fail requires no single dimension < 3 — prevents strong files from masking weak ones"

patterns-established:
  - "Dimension weights per artifact type: research emphasizes completeness, specs emphasize usability"
  - "Failure taxonomy as living document: seeded with 10 modes, evaluators add during scoring"

requirements-completed: [P3-T2]

duration: 12min
completed: 2026-04-05
---

# Phase 3 Plan 02: Evaluation Rubric & Scorecard Summary

**Versioned 5-dimension rubric with artifact-specific anchored scales, per-artifact weights, cross-file alignment passes, seeded failure taxonomy, and blank scorecard template**

## Performance

- **Duration:** 12 min
- **Started:** 2026-04-05
- **Completed:** 2026-04-05
- **Tasks:** 2
- **Files created:** 2

## Accomplishments

- Created `evals/rubric.md` (250 lines) — complete scoring framework with 5 dimensions (coherence, specificity, relevance, comprehensiveness, actionability) scored on a 1–5 scale across all 9 TTT artifacts
- Created `evals/scorecard.md` (120 lines) — blank fill-in template matching rubric structure exactly, ready for evaluators to copy per run
- Rubric includes per-artifact dimension weights, cross-file alignment section (4 directed + 1 global pass), 10-mode failure taxonomy, and scoring mechanics with aggregation formulas

## Task Details

1. **Task 1: Create evals/rubric.md** — 250 lines with v1.0 header, 9 artifact-specific scoring tables with anchored 1/3/5 scales, dimension weights, cross-file alignment, failure taxonomy, scoring mechanics, and changelog
2. **Task 2: Create evals/scorecard.md** — 120 lines as a blank template with per-artifact × 5-dimension scoring tables, cross-file alignment, summary with pass/fail, and qualitative sections

## Files Created

- `evals/rubric.md` — Canonical scoring framework for TTT eval runs (v1.0)
- `evals/scorecard.md` — Blank score recording template copied into each run bundle

## Decisions Made

- Anchor text is artifact-specific rather than generic — "coherence" means different things for `clarification.md` (thesis vs platform alignment) vs `tech_architecture.md` (stack vs data model alignment)
- Weights sum to 1.0 per artifact row; `clarification.md` has no relevance weight since it has no upstream artifact
- Pass/fail has a strict floor: any single dimension < 3 triggers overall fail, even if aggregate is high
- Cross-file alignment passes directly mirror the choreographer's spec completeness checks for consistency between TTT's own quality gates and the eval framework

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Rubric and scorecard are complete and self-contained — an evaluator can score a TTT run using only these two files
- Plan 03 (LLM judge prompt) can reference rubric anchor text for calibration examples
- Plan 01 (scenarios) can reference rubric dimensions for expected score ranges in success definitions

---
*Phase: 03-evals*
*Completed: 2026-04-05*
