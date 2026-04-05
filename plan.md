# TTT Build + Eval Plan

## Status
Phase 0 closed. Phase 1: canonical prompts in `prompts/` (+ `schemas/ttt_state.example.json`). Phase 2 packaging next per `PHASE_PLAN.md`.

---

## Who executes what

- **Composer 2:** Default for all implementation work unless noted below (Phase 0 spikes/docs, six subagent prompts after choreographer exists, Cursor rules + runtime docs, eval assets, triage after review).
- **Opus — orchestrator-only session:** `prompts/choreographer.md` and orchestration-oriented content for Cursor (see `PHASE_PLAN.md`). **Do not** write `SKILL.md` in this session.
- **Opus — SKILL.md-only session:** `skills/ttt/SKILL.md` only. **Do not** rewrite the choreographer here unless fixing a review finding.
- **Opus — Phase R (separate chat/thread):** Full review of prompts, code, and runtime; output captured in `docs/OPUS_REVIEW.md`. Not mixed with the two authoring sessions above.

Detailed task IDs and dependencies: **`PHASE_PLAN.md`**.

---

## What We're Building

TTT (To The T) is a multi-agent product management skill for vibe coders.
Full architecture: ttt_master_architecture_part1.md + ttt_master_architecture_part2.md

---

## Phase 0: Resolve before building anything

These decisions gate everything downstream.

1. Subagent spawning mechanism for Cursor (Task tool? @-mention? rules file?)
2. Subagent spawning mechanism for Claude Code (skill format + subprocess?)
3. Web search access for Market + User Researcher in each runtime
4. Where TTT writes files relative to the user's project directory

Do not write a single prompt until Phase 0 is resolved.

---

## Phase 1: Core prompts (runtime-agnostic)

Write all 7 agent prompts as plain markdown. No runtime packaging yet.
These are the canonical source. All runtimes will wrap these — never fork them.

### 1.1 Choreographer system prompt
Inputs: ttt_state.json, all phase flow logic from Part 1
Must encode:
- All 5 phase flows with exact step sequences
- Quality gate logic (validate, retry up to 3x, surface to user on failure)
- Define-to-Specify gap assessment (6 checks)
- Spec completeness check (8 checks)
- Scope guard (≤5 V1 features, JTBD mapping enforcement)
- Vibe it!! heuristics and defaults
- Pivot handling (narrow vs broad classification)
- Session resume from ttt_state.json
- Progress labels (never "Phase X of Y")
- Blank input handling (joke bank rotation)
- Interaction rules (max 2 questions, analogies, escape hatches, tone)

### 1.2 Market Researcher prompt
Inputs: clarification.md
Must encode:
- Porter's Five Forces structure
- Competitor SWOT format (min 2 direct, max 8 total)
- Business Model Canvas (all 9 blocks)
- Whitespace analysis (min 3 with evidence)
- Timing assessment (supporting + opposing trends)
- Source quality rules (Reddit, YouTube, Wikipedia, research sites — no flimsy blogs)
- Data confidence labeling for weak/stale data

### 1.3 User Researcher prompt
Inputs: clarification.md
Must encode:
- Maslow's Hierarchy (relevant levels only, no force-fitting)
- Reiss's 16 desires (pick 3–5, justify each)
- Seven Sins compulsions (honest about none-apply)
- JTBD format (functional + emotional + psychological layers + current workaround + pain level)
- Source quality rules (same as Market Researcher)
- Key quotes requirement (min 2 sourced)

### 1.4 Product Detailer prompt
Inputs: definition.md, market_research.md, user_research.md
Must encode:
- 4 user journeys (onboarding, activation, core loop, retention)
- Feature specification format (action, system response, edge cases, acceptance criteria)
- Screen/view inventory
- 4 state definitions (empty, loading, error, success)
- V1-only scope (no extras from definition.md)

### 1.5 Tech Architect prompt
Inputs: definition.md (including build preferences)
Must encode:
- Stack decision format for all layers (frontend, backend, DB, auth, hosting)
- "Take the best call" heuristic: vibecoding-friendly, well-documented, extensible
- Data model format
- API route format
- External dependency listing
- Infrastructure notes for coding agent

### 1.6 Design Advisor prompt
Inputs: definition.md, solution.md
Must encode:
- UX philosophy (2–3 principles, product-specific not generic)
- Design reference format (what to borrow from each reference)
- Layout description for primary + secondary views
- Component patterns
- Typography, color, spacing systems
- All 4 states with visual approach
- Responsive behavior rules

### 1.7 Test & Eval Generator prompt
Inputs: definition.md, solution.md
Must encode:
- Acceptance test table format (ID, scenario, input, expected, priority)
- User journey test coverage (all 4 journeys)
- Performance benchmark format
- Success metric from definition.md referenced and measurable
- "What good looks like" + "What failure looks like"

---

## Phase 2: Runtime packaging

### Wave 1: Cursor + Claude Code

#### Cursor
- Entry point: skill file or .cursor/rules approach (resolve in Phase 0)
- Subagent spawning: Task tool where available; document manual parallel fallback
- File write location: user's project directory (confirm in Phase 0)

#### Claude Code
- Entry point: Claude Code skill format (SKILL.md structure from skill-creator)
- Subagent spawning: skill-native mechanism
- File write location: same as Cursor

### Wave 2 (later): Windsurf, VS Code, Codex
- Same prompts, different wrapper docs
- No prompt changes — adapter only

### Wave 3 (later): Anti Gravity, claude.ai, Claude Desktop
- These may require UX-level adaptations (no persistent file system in claude.ai)
- Design separately

---

## Phase 3: Evals

### 3.1 Eval scenarios (fixed inputs)

S1 — Clear, specific idea
Example start: "I want to build a Pomodoro timer for devs that integrates with GitHub Issues"
Success: Efficient path to locked definition, tight V1 scope, proportionate questions

S2 — Vague / broad idea
Example start: "Something with AI for creators, not sure what exactly"
Success: Thesis narrows measurably across turns, user not annoyed by over-questioning

S3 — Weak market / crowded space
Example start: "A generic task manager with AI features"
Success: Honest weakness signaling, evidence-backed pivot menu, user's agency respected

S4 — Vibe it!! early trigger
Example start: "I want a meal planning app. Vibe it!!"
Success: All artifacts generated, assumptions stated explicitly, no silent scope creep

### 3.2 Judgment criteria (per output file)

#### clarification.md
- Coherence: All elements (thesis, user, platform, goal, constraints) are internally consistent
- Specificity: Exactly one platform, one user cohort, one primary goal

#### market_research.md
- Accuracy: Claims are sourced; weak/stale data is labeled
- Comprehensiveness: All required sections filled (Porter's all 5, BMC all 9, min 3 whitespaces)
- Relevance: Research directly addresses the product thesis in clarification.md

#### user_research.md
- Accuracy: Claims are sourced; quotes are real and linked
- Comprehensiveness: All required sections (Maslow 2+ levels, Reiss 3–5, JTBD min 2 with all 3 layers)
- Relevance: User profile and jobs directly match target user in clarification.md

#### definition.md
- Coherence: User, problem, solution, features, and success metric are internally consistent
- Specificity: One primary problem, one user cohort, ≤5 V1 features
- Relevance with clarification: Cohort is a refinement of clarification's user, not a divergence
- Comprehensiveness: All sections filled, V2 parking lot exists, build preferences complete

#### solution.md + tech_architecture.md + design_guideline.md + test_eval.md + coding_agent_prompt.md
- Coherence: All elements within each file are internally consistent
- Specificity: One platform, one user, one goal reflected throughout
- Relevance with clarification: Product thesis is traceable to clarification.md
- Relevance with definition: Every V1 feature accounted for; no scope creep
- Comprehensiveness: All required sections present per Part 2 templates
- Cross-file alignment:
  - solution.md ↔ tech_architecture.md: Every feature has data models and routes; no orphaned models
  - solution.md ↔ design_guideline.md: Every screen has design guidance; all 4 states covered
  - solution.md ↔ test_eval.md: Every feature has happy path + edge case test
  - All files ↔ coding_agent_prompt.md: Build order respects tech dependencies; V2 parking lot consistent

### 3.3 Scoring

Scale: 1–5 per dimension
- 5: Fully meets criterion with clear evidence
- 3: Partially meets; gaps present but minor
- 1: Fails criterion; significant rework needed

Method (phased):
- v1: Human scoring of transcripts + artifact bundles against above criteria
- v2: LLM-as-judge pairwise (calibrated against v1 human scores)

### 3.4 Eval execution sequence

1. Run S1 manually end-to-end after prompts exist
2. Human-score all output files on all dimensions
3. Document failure modes (where did each agent fall short and why?)
4. Use failure modes to revise prompts
5. Re-run same scenario; compare artifact quality
6. Repeat for S2, S3, S4
7. Once human baseline exists: draft LLM judge prompt; calibrate vs human scores

---

## Delivery checklist

### Must build
- [ ] SKILL.md entry point (Cursor)
- [ ] SKILL.md entry point (Claude Code)
- [ ] Choreographer prompt
- [ ] Market Researcher prompt
- [ ] User Researcher prompt
- [ ] Product Detailer prompt
- [ ] Tech Architect prompt
- [ ] Design Advisor prompt
- [ ] Test & Eval Generator prompt
- [ ] Quality gate validation logic (embedded in Choreographer)
- [ ] Gap assessment logic (embedded in Choreographer)
- [ ] ttt_state.json read/write logic

### Should build
- [ ] Session resume flow
- [ ] Retry orchestration with user escalation
- [ ] Pivot handling (narrow vs broad)
- [ ] Context clear recommendation logic

### Build later
- [ ] Quick mode (targeted file updates)
- [ ] Config/settings (depth, model profiles)
- [ ] GSD bridge command
- [ ] Full joke bank (start with 4 hardcoded, one per category)

### Not yet defined (design before building)
- [ ] Exact subagent spawning syntax per runtime
- [ ] Web search integration per runtime
- [ ] File write path convention per runtime
- [ ] Error handling for runtimes without subagent support

---

## Files this project produces

| File | Owner | Phase |
|------|-------|-------|
| ttt_state.json | Choreographer | All phases |
| clarification.md | Choreographer | Phase 1 |
| market_research.md | Market Researcher | Phase 2 |
| user_research.md | User Researcher | Phase 2 |
| definition.md | Choreographer | Phase 3 |
| solution.md | Product Detailer | Phase 4 Wave 1 |
| tech_architecture.md | Tech Architect | Phase 4 Wave 2 |
| design_guideline.md | Design Advisor | Phase 4 Wave 2 |
| test_eval.md | Test & Eval Generator | Phase 4 Wave 2 |
| coding_agent_prompt.md | Choreographer | Phase 4 final |
| blueprint.md | Choreographer | Phase 4 final |
| versions.md | Choreographer | All phases |
| launch.md | Choreographer | Phase 5 (optional) |