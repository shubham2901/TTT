# Phase 3: Evals - Context

**Gathered:** 2026-04-05
**Status:** Ready for planning

<domain>
## Phase Boundary

Repeatable eval protocol for TTT: four fixed scenarios (S1–S4) with variants, a per-artifact rubric with scoring, an execution protocol with a runnable harness script, and a calibration-ready LLM-judge prompt. This phase produces the **evaluation framework** — it does not run full evals or iterate on prompts (that's the eval loop described in plan.md §3.4).

</domain>

<decisions>
## Implementation Decisions

### Scenario design
- **Multi-turn scripts** — each scenario scripts the first 2–3 turns including how the user responds to TTT clarification questions, not just an opening line
- **Key checkpoints** — specify 2–3 critical intermediate moments per scenario (e.g. "should ask about platform before moving to research") rather than full expected traces or end-state only
- **2–3 variants per scenario** — vary by product domain (e.g. SaaS vs mobile vs dev tool) to stress different TTT behaviors
- **Naming: ID + name** — S1: Clear Idea, S2: Vague Explorer, S3: Crowded Market, S4: Vibe It
- **Realistic tonal range** — scripted user responses vary across scenarios: some cooperative, some terse, some rambling
- **Vibe it!! (S4)** — two variants: immediate trigger in first message, and delayed trigger after one exchange
- **Dual success definitions** — qualitative bullets for quick scanning + rubric dimension mapping with expected score ranges

### Rubric granularity
- **Hybrid scoring** — whole-file scores per dimension for quick assessment + per-section breakdown for diagnosis
- **Artifact-specific weights** — different dimension weights per file type (research artifacts vs definition vs spec files); weights predefined in rubric.md
- **Separate cross-file alignment pass** — score individual files first, then a dedicated section for cross-file alignment checks (solution↔tech, solution↔design, solution↔test, all↔coding_agent_prompt)
- **5 dimensions** — coherence, specificity, relevance, comprehensiveness (from plan.md) + actionability (is the output usable by the next agent/human without rework?)
- **Detailed anchor text** — multi-line anchors with specific examples per dimension per artifact
- **Table format** — rows = dimensions, columns = 1–5 scale anchors
- **Seeded failure taxonomy** — start with 5–10 likely failure modes (e.g. "scope creep", "unsourced claims", "missing journey"), scorers can add new ones
- **Both aggregate + per-file views** — per-file detail for diagnosis + weighted aggregate summary for quick cross-run comparison
- **Passing threshold + comparative tracking** — minimum acceptable score for "shippable" (all dimensions ≥ 3) + improvement tracking between runs
- **Versioned rubric** — rubric has a version number and changelog; scores reference which rubric version was used

### Eval execution workflow
- **Structured harness** — a runnable CLI script that guides the evaluator step-by-step through the run (not just a markdown checklist)
- **Eval bundles** — artifacts collected into `evals/runs/{scenario}-{date}/` for preservation
- **Full transcript capture** — always capture the complete conversation transcript alongside artifacts
- **Score after full run** — complete the entire scenario, then score all artifacts together
- **Side-by-side comparison** — when re-running after prompt revisions, score both runs and compare dimension by dimension
- **Sole evaluator (v1)** — protocol assumes the author runs all evals; can assume project context
- **Full package bundles** — each run bundle contains: artifacts, transcript, scores, prompt versions used, TTT state snapshots, and evaluator notes

### LLM judge
- **Calibration-ready** — a runnable prompt + 2–3 example judgments for calibration benchmarking (not just a skeleton)
- **Claude-targeted** — optimize for Claude's strengths (long context, structured output)
- **Input: artifacts + transcript** — judge assesses both the generated files and the conversation quality
- **Dual output format** — structured JSON for comparison tooling + markdown summary for human review

### Claude's Discretion
- Cross-file alignment checking approach (what steps per pair vs what to check)
- Exact failure mode seeds for the taxonomy
- Harness script implementation language and structure
- How to structure the calibration examples in the LLM judge prompt

</decisions>

<specifics>
## Specific Ideas

- Scenarios use product domains to vary (SaaS tool, mobile app, dev tool, etc.) — not just persona differences
- S4 has two explicit variants: "Vibe it!!" in message one vs after one exchange — both need to be tested
- The harness is a runnable script, not just documentation — it should orchestrate the eval flow and collect artifacts
- Rubric versioning matters because dimensions and weights will evolve as eval runs reveal what matters most

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-evals*
*Context gathered: 2026-04-05*
