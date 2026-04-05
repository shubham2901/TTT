---
phase: 03-evals
plan: 01
subsystem: testing
tags: [eval, scenarios, multi-turn, rubric, vibe-it]

requires:
  - phase: 01-core-prompts
    provides: "Choreographer prompt with phase flows, quality gates, pivot handling, Vibe it!! protocol"
provides:
  - "Four eval scenario scripts (S1–S4) with multi-turn conversations"
  - "11 unique test configurations across 4 scenarios with domain variants"
  - "Dual success definitions mapping to 5 rubric dimensions"
  - "Key checkpoint specifications referencing choreographer behaviors"
affects: [03-evals-rubric, 03-evals-harness, eval-runs]

tech-stack:
  added: []
  patterns: [multi-turn-scenario-scripts, checkpoint-based-verification, dual-success-definitions]

key-files:
  created:
    - evals/scenarios/s1-clear-idea.md
    - evals/scenarios/s2-vague-explorer.md
    - evals/scenarios/s3-crowded-market.md
    - evals/scenarios/s4-vibe-it.md
  modified: []

key-decisions:
  - "Table format for rubric expectations in each scenario for quick scanning"
  - "S4 uses structurally different variants (immediate vs delayed trigger) rather than domain variation"
  - "Each scenario includes post-scripted-turns guidance for evaluator behavior"

patterns-established:
  - "Scenario structure: header → scripted turns → checkpoints → success definition → variants"
  - "Checkpoint naming: numbered with behavioral focus (what TTT should do, not what output looks like)"
  - "Tonal variation across scenarios: cooperative (S1), rambling (S2), defensive (S3), impatient (S4)"

requirements-completed: [P3-T1]

duration: 12min
completed: 2026-04-05
---

# Phase 3 Plan 01: Eval Scenarios Summary

**Four multi-turn scenario scripts (S1–S4) covering clear idea, vague exploration, crowded market, and Vibe it!! fast path with 11 total test configurations**

## Performance

- **Duration:** 12 min
- **Started:** 2026-04-05
- **Completed:** 2026-04-05
- **Tasks:** 4
- **Files created:** 4

## Accomplishments

- Created S1 (Clear Idea): tests efficient Clarify with cooperative user, 3 checkpoints, 2 domain variants (SaaS + CLI)
- Created S2 (Vague Explorer): tests thesis narrowing with rambling user, 3 checkpoints, 2 domain variants (B2B + personal)
- Created S3 (Crowded Market): tests honest weakness signaling and pivot handling, 3 checkpoints, 2 domain variants (dev tool + consumer)
- Created S4 (Vibe It): tests fast path with 2 structurally different variants (immediate + delayed trigger), 5 checkpoints total

## Files Created

- `evals/scenarios/s1-clear-idea.md` — Clear, specific idea scenario (94 lines)
- `evals/scenarios/s2-vague-explorer.md` — Vague, broad idea scenario (94 lines)
- `evals/scenarios/s3-crowded-market.md` — Crowded market with pivot scenario (94 lines)
- `evals/scenarios/s4-vibe-it.md` — Vibe it!! fast path scenario (88 lines)

## Decisions Made

- Used markdown tables for rubric expectations instead of bullet lists — easier to scan across dimensions
- S4 structures variants by trigger timing (immediate vs delayed) rather than product domain, since the Vibe it!! behavior difference is the test target
- Included post-scripted-turns guidance in each scenario to standardize evaluator behavior after scripts end

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Verification

| Check | Result |
|-------|--------|
| S1 exists, 80–120 lines | 94 lines ✓ |
| S2 exists, 80–120 lines | 94 lines ✓ |
| S3 exists, 80–120 lines | 94 lines ✓ |
| S4 exists, 80–120 lines | 88 lines ✓ |
| S1: 3 turns, 3 checkpoints, 2 variants | ✓ |
| S2: 3 turns, 3 checkpoints, 2 variants | ✓ |
| S3: 3 turns, 3 checkpoints, 2 variants | ✓ |
| S4: 2 variants, 5 checkpoints total | ✓ |
| Contains "Pomodoro" (S1) | ✓ |
| Contains "AI for creators" (S2) | ✓ |
| Contains "todo app" (S3) | ✓ |
| Contains "Vibe it!!" (S4) | ✓ |
| 11 unique configurations total | 3+3+3+2 = 11 ✓ |
| Tonal range: cooperative, rambling, defensive, impatient | ✓ |
| Product domains: dev tools, SaaS, consumer, B2B — no defaults repeat | ✓ |
| Dual success definitions in all scenarios | ✓ |
| Rubric dimensions referenced: coherence, specificity, relevance, comprehensiveness, actionability | ✓ |

## Self-Check: PASSED

All 4 scenario files exist with correct line counts and content structure.

## Next Phase Readiness

- Scenario scripts ready for Plan 02 (rubric with artifact-specific anchors) — success definitions map to the 5 rubric dimensions
- Scenario checkpoints reference choreographer behaviors that rubric anchors should codify
- Harness (Plan 03) can read scenario files programmatically for `new` command

---
*Phase: 03-evals*
*Completed: 2026-04-05*
