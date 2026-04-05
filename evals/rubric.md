# TTT Evaluation Rubric

**Version:** 1.0
**Date:** 2026-04-05
**Dimensions:** 5 (coherence, specificity, relevance, comprehensiveness, actionability)
**Scale:** 1–5 per dimension per artifact
**Passing threshold:** All dimensions ≥ 3 for each artifact

---

## How to Use This Rubric

1. Score each artifact individually on all 5 dimensions using the per-artifact tables below.
2. Multiply each dimension score by the artifact's weight from the dimension weights table.
3. Sum weighted scores per artifact to get the weighted artifact score (max 5.0).
4. After all 9 artifacts are scored, run the 5 cross-file alignment passes.
5. Compute the overall score using the formulas in Scoring Mechanics.
6. Record all failure modes observed during scoring.

Scores 2 and 4 are interpolations between the defined anchors. Score 2 sits between 1 (fails) and 3 (partial). Score 4 sits between 3 (partial) and 5 (fully meets). Use judgment — do not define them per artifact.

Use the Notes field in the scorecard to record per-section diagnostic detail (e.g., "Comprehensiveness 3: Porter's all 5 present but BMC missing 2 blocks, whitespace thin"). This gives section-level diagnosis without requiring formal per-section numerical scores.

---

## Dimensions

**Coherence:** Internal consistency within a file. Are all elements aligned? Do assertions support each other? No contradictions between sections.

**Specificity:** Precision and concreteness. Are claims backed by specific details, not generalities? Is the user/problem/solution narrowed to one clear thing, not a vague category?

**Relevance:** Alignment with upstream artifacts. Does this file serve the product thesis in `clarification.md`? Does it address what `definition.md` requires? No tangential content.

**Comprehensiveness:** Completeness against the required template. Are all required sections present and substantively filled? No empty or stub sections. Quality gate thresholds met.

**Actionability:** Usability by the next consumer (agent or human). Can the next phase's agent use this file without asking clarifying questions? Can a developer build from the spec without guessing?

---

## Per-Artifact Scoring Tables

### 1. clarification.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | Core elements contradict (thesis vs platform, user vs constraints). | One significant inconsistency that doesn't block downstream. | All elements internally consistent. Assumptions align with constraints. |
| Specificity | Thesis is a paragraph, not a sentence. User is "everyone." No platform rationale. | Thesis is one sentence but vague. User specificity 4–5. Platform chosen without strong rationale. | Thesis is one precise sentence. Specificity ≥ 7. Platform has context-aware rationale. |
| Relevance | N/A — first artifact, no upstream to align with. | N/A | N/A |
| Comprehensiveness | Missing sections (no goal type, no constraints, no assumptions). | All sections present but some thin (assumptions list incomplete, missing confidence levels). | All sections filled per template. Quality gate passes: thesis = 1 sentence, goal = 1 primary, specificity ≥ 6. |
| Actionability | Researchers couldn't use this to focus their research. | Researchers could work from this but would need to guess on some parameters. | Market and User Researchers have unambiguous input. No clarification needed. |

### 2. market_research.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | Porter's summary contradicts force analysis. BMC inconsistent with competitor findings. | Minor tension between sections (e.g., timing verdict slightly misaligned with trends listed). | All sections reinforcing. Porter's summary follows from forces. BMC consistent with competitor landscape. |
| Specificity | No sources cited. Competitors described in one line each. Whitespace vague ("there's an opportunity"). | Some sources present. Competitors have partial SWOT (1–2 factors per). Whitespace evidence thin. | All claims sourced with confidence labels. Each direct competitor has full SWOT (1–3 per factor). Whitespace has specific evidence. |
| Relevance | Research about the wrong industry or market. Competitors aren't actually competing for the same user. | Research is relevant but includes tangential competitors or unrelated market trends. | All research directly addresses the product thesis. Competitors solve the same user problem. Whitespace is product-relevant. |
| Comprehensiveness | Missing entire sections (no Porter's, BMC incomplete, or no whitespace analysis). | All sections present: Porter's all 5 forces, BMC all 9 blocks, but whitespace < 3 or competitors < 2 direct. | All gates pass: Porter's 5 forces (1–4 pts each), ≥ 2 direct competitors with full SWOT, BMC all 9, whitespace ≥ 3, timing has both supporting and opposing. |
| Actionability | Choreographer cannot synthesize — missing key findings for pivot options. | Synthesizable but gaps force assumptions during Define phase. | Choreographer can directly derive whitespace, timing verdict, and pivot options without guessing. |

### 3. user_research.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | JTBD don't match the user profile. Maslow levels contradict stated desires. | Minor misalignment between needs analysis and JTBD prioritization. | User profile, needs, desires, and jobs form a coherent narrative. Pain levels consistent with needs. |
| Specificity | Generic user description. JTBD missing layers (no emotional/psychological). No quotes. | JTBD have all 3 layers but workarounds are vague. Only 1 sourced quote. | JTBD with specific workarounds and pain levels. ≥ 2 sourced quotes with links. Reiss desires justified per user segment. |
| Relevance | Research describes a different user than clarification.md's target. | User profile matches but some needs analysis (Maslow levels, Reiss desires) is tangential to the product. | All analysis directly serves the target user from clarification.md. JTBD are product-relevant. |
| Comprehensiveness | Missing sections (no JTBD, or Maslow < 2 levels, or no Reiss desires). | All sections present: Maslow ≥ 2, Reiss 3–5, JTBD ≥ 2, but compulsions missing or unjustified. | All gates pass: Maslow ≥ 2 with substance, Reiss 3–5 justified, compulsions addressed (or explicit "none"), JTBD ≥ 2 all 3 layers, ≥ 2 quotes. |
| Actionability | Choreographer cannot identify primary problem or refine user cohort from this. | Usable but primary job and pain level require interpretation. | Choreographer can directly identify highest-pain JTBD and refine user cohort without ambiguity. |

### 4. definition.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | Problem statement contradicts solution direction. Features don't serve stated user need. | Minor tension (e.g., success metric hard to connect to V1 features directly). | User, problem, solution, features, and success metric are internally consistent and mutually reinforcing. |
| Specificity | Multiple problems stated. User described broadly. > 5 V1 features listed. | One problem but vaguely stated. User specific but features lack one-line descriptions. | Exactly one primary problem. One user cohort. ≤ 5 V1 features, each with one-line description and JTBD mapping. |
| Relevance | User cohort diverges from research. Problem doesn't target any identified whitespace or JTBD. | Cohort refines clarification's user but drifts from research findings. Problem targets a JTBD but not the highest-pain one. | Cohort is a refined subset of clarification's user. Problem targets highest-pain JTBD + whitespace intersection. |
| Comprehensiveness | Missing V2 parking lot, or build preferences empty, or no success metric. | All sections present but build preferences partially filled or assumptions lack confidence levels. | All sections complete: V1 ≤ 5 with JTBD mapping, V2 parking lot, build prefs all filled, measurable success metric. |
| Actionability | Spec agents would produce conflicting or unusable outputs from this definition. | Spec agents can work but will need to make assumptions about preference gaps. | All Phase 4 agents (Product Detailer, Tech Architect, Design Advisor, Test Gen) have unambiguous input. |

### 5. solution.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | Journeys reference features not in spec. States contradict feature behavior. | Minor inconsistency (e.g., screen inventory missing one view from journeys). | Journeys, feature specs, screen inventory, and states form a consistent product picture. |
| Specificity | Features described as one-liners without edge cases or acceptance criteria. | Features have user action and system response but edge cases thin (< 1 per feature). | Every feature has user action, system response, ≥ 1 edge case with handling, and acceptance criteria. |
| Relevance | Contains features not in definition.md V1 (scope leak). Journeys cover V2 capabilities. | All V1 features present but journeys include capabilities not backed by V1 feature list. | Exact V1 feature coverage from definition.md. No scope leak. 4 journeys map to V1 capabilities only. |
| Comprehensiveness | < 4 journeys. Missing screen inventory or state definitions entirely. | All 4 journeys present but one is thin. Screen inventory present but states < 4 defined. | 4 journeys (onboarding, activation, core loop, retention). Screen inventory complete. All 4 states defined. |
| Actionability | Tech Architect can't derive data models — features too vague to implement. | Implementable but edge case gaps will cause developer clarification questions. | Tech Architect, Design Advisor, and Test Gen can derive their outputs without ambiguity. |

### 6. tech_architecture.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | Stack choices contradict each other (e.g., mobile framework for CLI tool). Data models don't match routes. | Minor tension (e.g., auth choice doesn't perfectly complement hosting platform). | Stack, data models, routes, and infrastructure form a consistent and buildable technical plan. |
| Specificity | "Use a database" without specifying which. No rationale for any choice. | Specific choices but rationale is generic ("it's popular"). Missing version numbers. | Exact frameworks and versions with context-specific rationale referencing vibecoding context, docs quality, extensibility. |
| Relevance | Stack doesn't match build preferences in definition.md. Data models include V2 entities. | Stack matches preferences but some data models serve no V1 feature (orphans). | Stack respects all build preferences. Every model and route serves a V1 feature. No orphans. |
| Comprehensiveness | Missing entire layers (no auth choice, no hosting, no data models). | All layers covered but API routes incomplete or external dependencies not listed. | All stack layers with rationale, data models for all V1 entities, API routes mapping to features, external deps listed. |
| Actionability | Developer can't start building — critical decisions unmade, no setup guidance. | Developer can start but will need to research gaps (missing env vars, unclear route params). | Developer can scaffold the entire project from this file. Setup instructions, env vars, and deployment notes present. |

### 7. design_guideline.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | UX principles contradict design references. Typography and spacing don't match stated density preference. | Minor inconsistency (e.g., color system doesn't fully support stated dark mode plan). | Principles, references, layout, typography, color, spacing, and states form a unified design language. |
| Specificity | "Use good contrast" or "make it clean" — generic advice applicable to any product. | Product-specific principles but missing concrete values (no font sizes, no hex codes, no spacing units). | 2–3 product-specific UX principles. Concrete typography scale, color codes, and spacing base unit defined. |
| Relevance | Design references from an unrelated industry. Doesn't match definition.md design preferences. | References match user preferences but some guidance doesn't serve V1 screens in solution.md. | References match definition.md's design preferences. Guidance covers every V1 screen from solution.md. |
| Comprehensiveness | No primary layout description. Missing state definitions or no responsive rules. | Layout described for primary view. Some states covered but < 4. Responsive partially addressed. | Primary + secondary view layouts, component patterns, full type/color/spacing systems, all 4 states, responsive rules. |
| Actionability | Developer can't style the app — guidance too vague for implementation. | Developer can build most UI but will improvise for uncovered screens or missing states. | Developer can implement every screen with consistent styling. No design decisions left to improvise. |

### 8. test_eval.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | Test scenarios don't match feature specs from solution.md. Success metric contradicts test targets. | Minor misalignment (e.g., priority levels inconsistent across features). | Tests directly verify feature specs. Success metric is testable and consistent with journey test criteria. |
| Specificity | "Test that it works" — no inputs, expected outputs, or priority levels. | Tests have scenario descriptions but inputs/outputs are vague. Edge cases lack concrete triggers. | Every test has specific input, expected output, and priority level. Edge cases have concrete trigger conditions. |
| Relevance | Tests for features not in V1. Missing tests for actual V1 features. | All V1 features tested but some test scenarios cover capabilities not in solution.md. | Every test maps to a V1 feature in solution.md. No orphaned tests. Success metric from definition.md referenced. |
| Comprehensiveness | < 1 happy path per feature. No journey tests. No performance benchmarks. | Happy path per feature but edge cases < 1 per feature. Journey tests < 4. Benchmarks missing. | Happy path + ≥ 1 edge case per feature. All 4 journey tests. Performance benchmarks present. Success metric measurable. |
| Actionability | Developer can't write automated tests from this — too vague to translate into code. | Developer can write most tests but will need to invent edge case details and expected outputs. | Developer can directly translate each row into a test case. No ambiguity in expected behavior. |

### 9. coding_agent_prompt.md

| Dimension | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|-----------|-----------|-------------|-----------------|
| Coherence | Build order violates tech dependencies. Rules contradict file references. V2 list inconsistent. | Minor ordering issue that doesn't block (e.g., one step could start earlier). | Build order respects all dependencies. Rules align with referenced files. V2 list consistent. |
| Specificity | "Build the app" — no structure, no build order, no implementation rules. | File references present but folder structure missing or build order lacks dependency reasoning. | Proposed folder structure, specific build order with dependency reasoning, concrete rules list. |
| Relevance | References wrong or missing files. V2 parking lot inconsistent with definition.md + versions.md. | All files referenced but V2 parking lot slightly outdated or one file reference stale. | References all output files. V2 parking lot matches definition.md + versions.md exactly. |
| Comprehensiveness | Missing stack summary or build order entirely. No rules section. No V2 list. | Stack summary and build order present but missing rules or V2 parking lot. | Stack, folder structure, build order, rules, all file references, and V2 parking lot present. |
| Actionability | Coding agent would ask "what am I building?" immediately. | Coding agent can start but will need to re-read definition.md for context and priorities. | Coding agent can begin building immediately. First action is unambiguous. No back-referencing needed to start. |

---

## Dimension Weights

Relative weight of each dimension per artifact. Weights reflect what matters most for each file type.

| Artifact | Coherence | Specificity | Relevance | Comprehensiveness | Actionability |
|----------|-----------|-------------|-----------|-------------------|---------------|
| clarification.md | 0.25 | 0.30 | — | 0.25 | 0.20 |
| market_research.md | 0.15 | 0.20 | 0.20 | 0.30 | 0.15 |
| user_research.md | 0.15 | 0.20 | 0.20 | 0.30 | 0.15 |
| definition.md | 0.25 | 0.25 | 0.20 | 0.15 | 0.15 |
| solution.md | 0.20 | 0.20 | 0.15 | 0.20 | 0.25 |
| tech_architecture.md | 0.20 | 0.15 | 0.15 | 0.20 | 0.30 |
| design_guideline.md | 0.20 | 0.20 | 0.15 | 0.20 | 0.25 |
| test_eval.md | 0.15 | 0.20 | 0.15 | 0.25 | 0.25 |
| coding_agent_prompt.md | 0.25 | 0.15 | 0.15 | 0.20 | 0.25 |

`clarification.md` has no relevance weight — it is the first artifact with no upstream to align against. All other rows sum to 1.0.

Research artifacts (market_research, user_research) weight comprehensiveness highest — completeness of analytical frameworks matters most. Spec artifacts (solution, tech_architecture, design_guideline, test_eval) weight actionability highest — downstream consumers must use the output without guessing. Definition weights coherence and specificity — the pivot between research and specification must be sharp and precise.

---

## Cross-File Alignment

Scored AFTER all individual artifacts. Four directed comparison passes plus one global consistency pass.

| Pass | Files | What to check | 1 (Fails) | 3 (Partial) | 5 (Fully meets) |
|------|-------|---------------|-----------|-------------|-----------------|
| 1 | solution.md ↔ definition.md | Every V1 feature specified. No scope leak. User cohort consistent. | Missing features or scope leak present. | Minor gap: 1 feature underspecified or slight cohort drift. | Perfect feature coverage, no scope leak, cohort consistent. |
| 2 | tech_architecture.md ↔ solution.md | Every feature has data models and routes. No orphaned models. | Major alignment gaps — features without tech support. | 1 orphaned model or 1 missing route. | Clean mapping, every feature backed, no orphans. |
| 3 | design_guideline.md ↔ solution.md | Every screen has design guidance. All 4 states have visual approach. | Multiple screens without design guidance. | Missing guidance for 1 screen or 1 state. | Full coverage — every screen styled, all 4 states addressed. |
| 4 | test_eval.md ↔ solution.md | Every feature has tests. Success metric is testable. | Features without any tests. | 1 feature missing edge case test. | Complete — happy path + edge case per feature, metric testable. |
| G | All files | Product thesis, user cohort, and V1 feature list consistent across all 9 files. | Conflicting descriptions across files. | Minor terminology drift between files. | Consistent terminology and content throughout. |

These passes mirror the choreographer's 8-check spec completeness assessment, ensuring eval scoring aligns with TTT's own quality gates.

---

## Failure Taxonomy

Seeded with 10 failure modes across 3 categories. Evaluators may add new modes during scoring — record additions in the run bundle for future taxonomy updates.

### Conversation quality

1. **Over-questioning** — TTT asks > 2 questions per message or re-asks information the user already provided.
2. **Silent assumption** — TTT makes a shaping assumption (thesis direction, platform choice, user narrowing) without stating it to the user.
3. **Premature convergence** — TTT locks the thesis before the user's input justifies it; skips narrowing steps when the idea is still broad.

### Research quality

4. **Unsourced claims** — Research states facts, statistics, or market positions without evidence or attribution.
5. **Stale data** — Data points from 2+ years ago used without confidence labeling ("estimated", "directional", "from 2023").
6. **Missing sections** — Required template sections empty or absent (e.g., fewer than 5 Porter's forces, BMC blocks missing, whitespace < 3).

### Specification quality

7. **Scope creep** — Features appear in solution.md that are not in definition.md V1 scope.
8. **Missing journey** — Fewer than 4 user journeys in solution.md (must have: onboarding, activation, core loop, retention).
9. **Orphaned model** — Data model or API route in tech_architecture.md that serves no V1 feature.
10. **Generic design** — design_guideline.md gives advice not specific to this product ("use good contrast", "keep it clean", "follow best practices").

### Evaluator additions

_(Add new failure modes during scoring. Include ID 11+ with category. Record in run bundle for future taxonomy updates.)_

---

## Scoring Mechanics

### Per-artifact score

Score each dimension 1–5. Multiply by weight. Sum = weighted artifact score (max 5.0).

```
weighted_artifact_score = Σ (dimension_score × dimension_weight)
```

### Artifact aggregate

Average all 9 weighted artifact scores.

```
artifact_aggregate = Σ weighted_artifact_scores / 9
```

### Cross-file alignment score

Score each of the 5 passes 1–5. Average = cross-file alignment score.

```
cross_file_score = Σ pass_scores / 5
```

### Overall score

```
overall = (artifact_aggregate × 0.7) + (cross_file_score × 0.3)
```

### Pass/fail

- **Pass:** No individual dimension score < 3 across any artifact AND overall ≥ 3.0.
- **Fail:** Any single dimension score < 3 on any artifact OR overall < 3.0.

A single dimension failure on any artifact triggers an overall fail, even if the aggregate score is high. This prevents strong artifacts from masking weak ones.

---

## Changelog

### v1.0 (2026-04-05)

- Initial rubric: 5 dimensions, 9 artifact-specific scoring tables with anchored 1/3/5 scales
- Dimension weights per artifact (research weights comprehensiveness, specs weight actionability)
- Cross-file alignment: 4 directed passes + 1 global consistency pass
- Failure taxonomy: 10 seeded modes in 3 categories (conversation, research, specification)
- Scoring mechanics: per-artifact weighted scores, aggregate, cross-file, overall formula, pass/fail criteria
