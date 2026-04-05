# Phase 3: Evals — Research

**Researched:** 2026-04-05
**Domain:** LLM evaluation frameworks, rubric design, eval harness tooling, LLM-as-judge calibration
**Confidence:** HIGH

## Summary

Phase 3 builds a repeatable evaluation framework for TTT: scenario scripts that exercise the five-phase flow, a rubric that scores each artifact on five dimensions, a CLI harness that orchestrates runs and collects bundles, and an LLM-judge prompt calibrated against human scores. The domain is well-understood: LLM-as-judge evaluation is mature (2024–2026 research provides strong patterns), and the inputs are fully specified by TTT's existing prompts and architecture.

The primary challenge is **rubric calibration** — TTT produces 8–10 structured markdown files across a multi-turn conversation, and scoring must capture both individual file quality and cross-file alignment. The secondary challenge is **scenario fidelity** — multi-turn scripts must exercise specific TTT behaviors (quality gates, pivot handling, scope guard, Vibe it!!) without over-constraining the agent's natural conversational style.

**Primary recommendation:** Four scenario files with 2–3 variants each, a single rubric with per-artifact dimension weights, a Python CLI harness for guided execution and bundle collection, and a Claude-targeted LLM-judge prompt with 2–3 calibration examples.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Scenario design
- **Multi-turn scripts** — each scenario scripts the first 2–3 turns including how the user responds to TTT clarification questions, not just an opening line
- **Key checkpoints** — specify 2–3 critical intermediate moments per scenario rather than full expected traces or end-state only
- **2–3 variants per scenario** — vary by product domain (SaaS vs mobile vs dev tool) to stress different TTT behaviors
- **Naming: ID + name** — S1: Clear Idea, S2: Vague Explorer, S3: Crowded Market, S4: Vibe It
- **Realistic tonal range** — scripted user responses vary across scenarios: some cooperative, some terse, some rambling
- **Vibe it!! (S4)** — two variants: immediate trigger in first message, and delayed trigger after one exchange
- **Dual success definitions** — qualitative bullets for quick scanning + rubric dimension mapping with expected score ranges

#### Rubric granularity
- **Hybrid scoring** — whole-file scores per dimension for quick assessment + per-section breakdown for diagnosis
- **Artifact-specific weights** — different dimension weights per file type; weights predefined in rubric.md
- **Separate cross-file alignment pass** — score individual files first, then dedicated cross-file alignment checks
- **5 dimensions** — coherence, specificity, relevance, comprehensiveness, actionability
- **Detailed anchor text** — multi-line anchors with specific examples per dimension per artifact
- **Table format** — rows = dimensions, columns = 1–5 scale anchors
- **Seeded failure taxonomy** — start with 5–10 likely failure modes; scorers can add new ones
- **Both aggregate + per-file views** — per-file detail for diagnosis + weighted aggregate summary for comparison
- **Passing threshold + comparative tracking** — minimum acceptable score: all dimensions ≥ 3; improvement tracking between runs
- **Versioned rubric** — version number and changelog; scores reference which rubric version was used

#### Eval execution workflow
- **Structured harness** — runnable CLI script, not just a markdown checklist
- **Eval bundles** — artifacts collected into `evals/runs/{scenario}-{date}/`
- **Full transcript capture** — complete conversation transcript alongside artifacts
- **Score after full run** — complete entire scenario, then score all artifacts together
- **Side-by-side comparison** — when re-running after prompt revisions, score both runs and compare dimension by dimension
- **Sole evaluator (v1)** — author runs all evals; can assume project context
- **Full package bundles** — each run bundle contains: artifacts, transcript, scores, prompt versions, TTT state snapshots, evaluator notes

#### LLM judge
- **Calibration-ready** — runnable prompt + 2–3 example judgments for calibration benchmarking
- **Claude-targeted** — optimize for Claude's strengths (long context, structured output)
- **Input: artifacts + transcript** — judge assesses both generated files and conversation quality
- **Dual output format** — structured JSON for comparison tooling + markdown summary for human review

### Claude's Discretion
- Cross-file alignment checking approach (what steps per pair vs what to check)
- Exact failure mode seeds for the taxonomy
- Harness script implementation language and structure
- How to structure calibration examples in the LLM judge prompt

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

## Standard Stack

### Core: Markdown (scenarios, rubric, protocol, judge prompt)

**Confidence:** HIGH

All static eval assets are markdown files. No special tooling needed to read or edit. The harness script reads these files programmatically to guide execution.

### Core: Python 3.10+ (harness script)

**Confidence:** HIGH

The harness uses Python stdlib only: `pathlib`, `shutil`, `json`, `datetime`, `os`, `sys`, `subprocess`. No external dependencies. Python is the natural choice given:
- TTT targets vibecoder developers who likely have Python available
- stdlib provides everything needed (file ops, JSON, dates, CLI)
- No build step, no dependency management

### Core: Claude API via Anthropic SDK (LLM judge — future)

**Confidence:** MEDIUM (deferred to v2 of evals)

The judge prompt is authored in Phase 3. Automated execution against the Claude API is a future step (plan.md §3.4 step 7). The prompt is designed to work with Claude's long-context window (200K tokens — easily fits all artifacts + transcript).

### Alternatives Considered

| Instead of | Could use | Tradeoff |
|------------|-----------|----------|
| Python harness | Shell script (bash) | Bash is simpler for file ops but worse for JSON manipulation, scoring aggregation, and cross-platform support. Python's `pathlib` and `json` modules make bundle management clean. |
| Markdown rubric | YAML/JSON rubric | Machine-parseable but harder for humans to read and edit. Since v1 is human-scored, markdown is better. The LLM judge can parse markdown rubric tables. |
| Single rubric file | Per-artifact rubric files | More modular but harder to maintain consistency across dimensions. A single rubric with artifact-specific sections is the right granularity. |
| Separate scenario files | Single scenarios.md | Single file is easier to cross-reference but harder for the harness to select. Separate files per scenario support programmatic selection and keep each file focused. |

## Architecture Patterns

### Pattern 1: Multi-Turn Scenario Scripts

**What:** Each scenario provides scripted user messages for the first 2–3 turns, with key checkpoints that mark critical intermediate moments.

**Structure:**

```markdown
# S1: Clear Idea

## Opening
User: "[first message]"

## Expected TTT behavior
- [what the choreographer should do]
- [checkpoint 1: what should happen by this point]

## Turn 2
User responds to TTT's clarification: "[scripted response]"

## Expected behavior after Turn 2
- [checkpoint 2: what should be true]

## Turn 3 (if applicable)
User: "[response to TTT's options]"

## After scripted turns
Evaluator continues naturally, making reasonable choices when TTT presents options. Document choices in transcript.

## Success definition
Qualitative:
- [bullet 1]
- [bullet 2]

Rubric mapping:
- coherence: 4–5 expected
- specificity: 4–5 expected
- ...

## Variants
### Variant A: [domain]
Opening: "[different product idea]"
Turn 2: "[domain-appropriate response]"

### Variant B: [domain]
...
```

**Key insight:** Scripts cover the first 2–3 turns to seed the conversation deterministically. After that, the evaluator plays a reasonable user. This tests TTT's ability to handle the scripted triggers (clear vs vague, pivot-worthy vs strong) while allowing natural conversation to emerge. Checkpoints mark critical behaviors that must happen regardless of conversational variation.

### Pattern 2: Dimension-Based Rubric with Anchored Scales

**What:** Five evaluation dimensions, each with a 1–5 scale where every score level has concrete anchor text specific to the artifact being scored.

**Structure:**

```markdown
## Dimension: Coherence

### clarification.md
| Score | Anchor |
|-------|--------|
| 5 | All elements (thesis, user, platform, goal, constraints) are internally consistent. No contradictions. Assumptions align with constraints. |
| 4 | Consistent with at most one minor tension that doesn't affect downstream phases. |
| 3 | One significant inconsistency (e.g., platform choice contradicts user description). Fixable without restarting. |
| 2 | Multiple inconsistencies. Downstream phases would produce conflicting outputs. |
| 1 | Core elements contradict each other. Thesis and user description are misaligned. |
```

**Key insight:** Generic anchors ("good", "adequate", "poor") produce unreliable scores. Artifact-specific anchors with concrete examples force consistent scoring. The same dimension (coherence) means different things for `clarification.md` vs `tech_architecture.md`.

### Pattern 3: CLI-Guided Eval Harness

**What:** A Python script that walks the evaluator through setup, execution, artifact collection, scoring, and comparison.

**Workflow:**

```
harness.py new <scenario-id> [--variant <variant>]
  → creates evals/runs/{scenario}-{date}/
  → copies scenario script for reference
  → prints "Start TTT in your agent. Use this opening message: ..."

harness.py collect <run-dir>
  → copies ttt/ artifacts into the run bundle
  → copies ttt_state.json snapshot
  → prompts for transcript paste or file path
  → records prompt versions (git hash or file checksums)

harness.py score <run-dir>
  → loads rubric dimensions and artifacts
  → walks through each artifact × dimension
  → prompts for score (1–5) + notes
  → saves scores to scores.json + scores.md

harness.py compare <run-dir-1> <run-dir-2>
  → loads both score files
  → prints dimension-by-dimension comparison
  → highlights improvements and regressions
```

**Key insight:** The harness doesn't automate TTT execution — it automates the bookkeeping around manual execution. The evaluator runs TTT in their agent (Cursor or Claude Code), then uses the harness to collect, score, and compare. This keeps the eval realistic (same environment as real usage) while making the scoring systematic.

### Pattern 4: LLM-Judge Prompt with Calibration Anchoring

**What:** A structured prompt that takes artifacts + transcript as input and produces scores + reasoning in both JSON and markdown formats.

**Design principles from current research:**
- **Concrete rubrics** — the judge prompt embeds the full rubric with anchor text, not just dimension names
- **Calibration examples** — 2–3 pre-scored examples with reasoning, showing the judge what a 5 vs a 3 vs a 1 looks like
- **Structural validators** — catch defects that LLM judges miss (e.g., missing sections, empty fields) before running the judge
- **Positivity bias mitigation** — explicit instruction to look for defects, not just strengths; "score what's missing, not just what's present"
- **Artifact-at-a-time** — score each file individually before cross-file alignment, matching the human workflow

**Calibration approach:** Provide 2–3 calibration examples in the judge prompt. Each example includes:
1. A snippet of an artifact (not a full file — the prompt would be too long)
2. A score with full reasoning
3. The reasoning explicitly references anchor text from the rubric

This grounds the judge's scoring to the rubric rather than its own intuition.

### Anti-Patterns to Avoid

- **Testing the harness, not TTT:** The eval framework should be invisible to TTT's behavior. Scenarios should feel like real user conversations, not synthetic test cases.
- **Over-scripting scenarios:** Scripting every turn removes the test of TTT's conversational ability. Script the first 2–3 turns to seed behavior, then let the evaluator play a reasonable user.
- **Dimension proliferation:** More than 5–7 dimensions causes scorer fatigue and reduces reliability. The decided 5 dimensions (coherence, specificity, relevance, comprehensiveness, actionability) are the right number.
- **Unversioned rubric changes:** Changing rubric anchors between runs without versioning makes comparisons meaningless. Always bump the version.
- **Scoring during the run:** Cognitive bias — the evaluator starts looking for issues to score rather than playing a natural user. Complete the full run, then score.
- **Judge without calibration:** An uncalibrated LLM judge produces scores that don't align with human expectations. Always include calibration examples and validate against human scores before trusting.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Artifact collection | Manual cp/mv per file | `harness.py collect` with pathlib | Consistent bundle structure, no missed files |
| Score tracking | Freeform notes | Structured JSON scores via `harness.py score` | Enables automated comparison |
| Prompt version tracking | Manual git hash copy | `harness.py collect` reads git status/checksums | Reproducibility without effort |
| Cross-file alignment | Ad hoc visual comparison | Rubric's dedicated cross-file section | Systematic, repeatable checks |

## Common Pitfalls

### Pitfall 1: Rubric Drift Between Runs
**What goes wrong:** Evaluator adjusts anchor text or weights between runs without incrementing the rubric version. Scores from different rubric versions are incomparable.
**How to avoid:** Rubric has a version number (semver) and changelog. Every score file records `rubric_version`. The harness validates that scores reference a valid rubric version.
**Warning signs:** Scores "improve" across runs but the rubric also changed.

### Pitfall 2: Scenario Contamination
**What goes wrong:** After running S1 multiple times, the evaluator has memorized ideal TTT outputs and unconsciously steers the conversation toward them.
**How to avoid:** Use variants (different product domains) to force different outputs. The evaluator plays a reasonable user, not an ideal one. Document in protocol: "Play the role naturally. Don't optimize for score."
**Warning signs:** Every run of S1 produces nearly identical transcripts.

### Pitfall 3: LLM Judge Positivity Bias
**What goes wrong:** The LLM judge scores everything 4–5 because RLHF training optimizes for "helpful" = "positive." It focuses on what's present, not what's missing.
**How to avoid:** Include explicit defect-hunting instructions: "For each dimension, first list what's missing or weak before listing what's present." Include a calibration example scored at 2 to show that low scores are expected when warranted.
**Warning signs:** Judge never scores below 3. Scores don't differentiate between strong and weak artifacts.

### Pitfall 4: Transcript Capture Gaps
**What goes wrong:** Evaluator forgets to save the full conversation transcript. Without it, scores can't be audited or used for LLM judge calibration.
**How to avoid:** The harness's `collect` command explicitly prompts for transcript. Protocol lists transcript capture as a blocking step.
**Warning signs:** Run bundles missing transcript.md. Can't reproduce how a score was derived.

### Pitfall 5: Cross-File Alignment Blind Spot
**What goes wrong:** Individual files score well but don't align with each other — e.g., `solution.md` has features not in `definition.md`, or `tech_architecture.md` has data models for V2 features.
**How to avoid:** Score individual files first, then run the dedicated cross-file alignment section. This mirrors TTT's own spec completeness check (8 checks in choreographer.md).
**Warning signs:** High per-file scores but broken downstream handoff (coding agent gets conflicting instructions).

## Discretion Recommendations

### 1. Cross-File Alignment Checking Approach

**Recommendation:** Four directed comparison passes, each checking specific alignment properties.

| Pass | Files Compared | What to Check |
|------|---------------|---------------|
| 1 | solution.md ↔ definition.md | Every V1 feature specified. No scope leak. User cohort consistent. |
| 2 | solution.md ↔ tech_architecture.md | Every feature has data models and routes. No orphaned models. |
| 3 | solution.md ↔ design_guideline.md | Every screen has design guidance. All 4 states covered in design. |
| 4 | solution.md ↔ test_eval.md | Every feature has happy path + edge case test. Success metric testable. |

Plus a global pass: product thesis, user cohort, and V1 feature list consistent across ALL files.

This directly mirrors the choreographer's 8-check spec completeness assessment, which makes cross-file alignment scoring consistent with TTT's own quality gates.

**Confidence:** HIGH — directly derived from choreographer.md spec completeness checks.

### 2. Failure Mode Seeds for the Taxonomy

**Recommendation:** Start with these 10 failure modes, organized by where they occur:

**Conversation quality:**
1. **Over-questioning** — TTT asks more than 2 questions per message or re-asks what the user already provided
2. **Silent assumption** — TTT makes a shaping assumption without stating it
3. **Premature convergence** — TTT locks the thesis before the user's input justifies it

**Research quality:**
4. **Unsourced claims** — research states facts without evidence or attribution
5. **Stale data** — data points from 2+ years ago used without confidence labeling
6. **Missing sections** — required sections (e.g., Porter's force, BMC block) empty or absent

**Specification quality:**
7. **Scope creep** — features appear in solution.md that aren't in definition.md V1
8. **Missing journey** — one or more of the 4 required user journeys absent
9. **Orphaned model** — data model or API route in tech_architecture.md that serves no V1 feature
10. **Generic design** — design_guideline.md gives generic advice ("use good contrast") instead of product-specific guidance

Evaluators can add new failure modes during scoring. New modes get added to the taxonomy for future runs.

**Confidence:** HIGH — derived from TTT's quality gates and the judgment criteria in plan.md §3.2.

### 3. Harness Script Implementation

**Recommendation:** Python 3.10+ with stdlib only. Four subcommands: `new`, `collect`, `score`, `compare`.

Structure:
```
evals/
├── harness.py          # CLI entry point (~300 lines)
├── scenarios/          # Scenario scripts
├── rubric.md           # Scoring framework
├── scorecard.md        # Blank score template
├── protocol.md         # Step-by-step guide
├── judge.md            # LLM judge prompt
└── runs/               # Run bundles (created by harness)
    └── .gitkeep
```

The harness reads scenario files and rubric programmatically. It creates structured run directories. It writes JSON scores for machine comparison and markdown scores for human review.

**Confidence:** HIGH — stdlib covers all needs. No external dependencies reduces friction.

### 4. Calibration Example Structure in LLM Judge

**Recommendation:** Three calibration examples, each showing a different quality level.

Each calibration example contains:
1. **Artifact context** — which file type and a representative excerpt (200–400 words, not full file)
2. **Dimension scores** — all 5 dimensions scored
3. **Reasoning chain** — for each dimension, explicit reference to rubric anchor text: "This scores 4 on coherence because [specific observation], which matches the 4 anchor: '[anchor text]'"
4. **Overall assessment** — 2–3 sentences synthesizing the scores

Example quality levels:
- **Example 1 (high, ~4.5 avg):** Strong clarification.md — specific thesis, consistent elements, one minor assumption gap
- **Example 2 (medium, ~3.0 avg):** Adequate market_research.md — sections present but thin evidence, some unsourced claims
- **Example 3 (low, ~1.5 avg):** Weak solution.md — missing journeys, scope leak, no edge cases

This spread teaches the judge the full range of the scale. The medium example is critical — it shows that 3 is "partially meets, gaps present but minor," not "bad."

**Confidence:** HIGH — aligns with calibration anchoring best practices from LLM-as-judge research (2025–2026).

## State of the Art

| Old Approach | Current Approach (2025–2026) | When Changed | Impact |
|--------------|------------------------------|--------------|--------|
| Fixed rubric dimensions for all tasks | Task-adaptive rubrics (AdaRubric) | 2025–2026 | Dynamic dimensions per task type. TTT uses fixed dimensions since our artifacts are known. |
| Single-pass LLM judge | Structured validators + LLM judge | 2025–2026 | Pre-judge structural checks catch defects LLMs miss (missing sections, empty fields) |
| Pairwise comparison judging | Pointwise scoring with calibration anchors | 2024–2026 | Better for absolute quality assessment (vs relative ranking). Matches TTT's 1–5 scale. |
| Uncalibrated LLM scores | Calibration via gold-standard human labels | 2025–2026 | ~80% agreement with human evaluators when calibrated. Without calibration: unreliable. |
| Manual eval bookkeeping | Eval harness tools (MASEval, HAL) | 2025–2026 | Automated bundle collection, score tracking, comparison. TTT builds a lightweight custom harness. |

## Open Questions

1. **Harness interactivity level**
   - What we know: The harness guides the evaluator step-by-step. Scoring needs per-dimension input.
   - What's unclear: Whether the harness should use interactive prompts (input()) or accept scores via file/args.
   - Recommendation: Interactive prompts for `score` command (evaluator reads artifact, enters score + notes). File-based for `compare` (reads existing score files). Interactive UX is appropriate for the sole-evaluator v1 model.

2. **Transcript format**
   - What we know: Full conversation transcript must be captured alongside artifacts.
   - What's unclear: Whether to standardize on a specific transcript format (raw text vs structured JSON with turn boundaries).
   - Recommendation: Accept raw text (copy-paste from agent UI). The harness writes it to `transcript.md` in the bundle. Structured format can be added later for LLM judge input.

3. **Partial scenario scoring**
   - What we know: Scenarios run end-to-end. Some scenarios might stall or fail partway through.
   - What's unclear: How to score a run that didn't complete all phases.
   - Recommendation: Score what was produced. Mark incomplete artifacts. Use failure taxonomy to classify why the run stalled. Incomplete runs are valuable data for prompt iteration.

## Sources

### Primary (HIGH confidence)
- TTT choreographer prompt: `prompts/choreographer.md` — quality gates, phase flows, spec completeness checks
- TTT architecture Part 2: `ttt_master_architecture_part2.md` — file templates, quality gate thresholds
- TTT plan.md §3: Eval scenarios, judgment criteria, scoring, execution sequence
- Phase 3 context: `.planning/phases/03-evals/03-CONTEXT.md` — locked decisions on scenarios, rubric, harness, judge

### Secondary (MEDIUM confidence)
- AdaRubric (2026): Task-adaptive rubric generation for LLM agent evaluation (arxiv.org/abs/2603.21362)
- FairJudge (2026): Debiased LLM-as-judge with curriculum training (arxiv.org/abs/2602.06625)
- Noise-Response Calibration (2026): Causal intervention protocol for LLM judges (arxiv.org/abs/2603.17172)
- MASEval (2026): Multi-agent system evaluation library (github.com/parameterlab/MASEval)

### Tertiary (LOW confidence)
- LLM-as-judge blog posts (various, 2025–2026): Community patterns for calibration and bias mitigation

## Metadata

**Confidence breakdown:**
- Scenario design: HIGH — directly specified in plan.md and CONTEXT.md with concrete decisions
- Rubric framework: HIGH — dimensions and approach are locked; anchor text is the main authoring work
- Harness design: HIGH — stdlib Python, straightforward file ops, well-understood CLI patterns
- LLM judge: MEDIUM — prompt design is well-understood but calibration effectiveness depends on human baseline quality

**Research date:** 2026-04-05
**Valid until:** 2026-05-05 (30 days — eval frameworks are stable; LLM-as-judge research is actively evolving)
