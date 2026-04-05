---
name: ttt
description: Product management for solo builders. Turns a raw idea into a validated product spec. Use when user says TTT, product spec, product management, or validate idea.
---

# TTT (To The T)

A product management layer for vibe coders. You think of the idea. TTT figures out what to build, for whom, why it will work, and hands your coding agent a complete spec.

## When to use

- User says "TTT", "To The T", "product spec", "product management", or "validate idea"
- User has a raw product idea and wants to validate and spec it before building
- User wants market research, user research, or competitive analysis for a product idea

## When not to use

- User is already building and wants code help (not product thinking)
- User wants to debug, test, or deploy existing code
- Task is about an existing codebase with no product planning intent

---

## What TTT produces

A bundle of interconnected artifacts under a `ttt/` directory in the user's project:

| File | Purpose |
|------|---------|
| `ttt_state.json` | Session state, decisions, progress — your memory across context clears |
| `clarification.md` | Idea clarity: thesis, user, platform, constraints |
| `market_research.md` | Industry analysis, competitors, whitespace, timing |
| `user_research.md` | User needs, desires, compulsions, jobs to be done |
| `definition.md` | User cohort, problem, solution direction, V1 scope, build preferences |
| `solution.md` | User journeys, feature specs, screen inventory, states |
| `tech_architecture.md` | Stack, data models, API routes, infrastructure |
| `design_guideline.md` | UX philosophy, visual system, layout, component patterns |
| `test_eval.md` | Acceptance tests, journey tests, success criteria |
| `coding_agent_prompt.md` | Day-0 handoff prompt for the coding agent |
| `blueprint.md` | File manifest, connections, reading order |
| `versions.md` | Changelog, pivots, scope changes |
| `launch.md` | Distribution, metrics, V2 triggers (optional) |

The final handoff: give `coding_agent_prompt.md` to your coding agent and start building.

---

## How it works

### Architecture

One orchestrator (the Choreographer) manages the full flow. Six specialist subagents do focused work when called.

```
User ◄──► Choreographer ──► Subagents
              │
              ├── Clarify    (Choreographer talks to user)
              ├── Validate   (Market Researcher + User Researcher)
              ├── Define     (Choreographer talks to user)
              ├── Specify    (Product Detailer → Tech Architect + Design Advisor + Test & Eval Generator)
              └── Launch     (Choreographer, optional)
```

### Phases

**Clarify** — Understand the idea. Narrow to a one-line thesis. Evaluate target user specificity. Lock platform, constraints, goal type. Output: `clarification.md`.

**Validate** — Two researchers run (parallel when possible, staggered if not): one analyzes the market (Porter's, SWOT, BMC, whitespace, timing), the other analyzes the user (Maslow, Reiss, JTBD, compulsions). Choreographer synthesizes and presents pivot options if the research suggests a better angle. Output: `market_research.md`, `user_research.md`.

**Define** — Lock the user cohort, primary problem (one, not three), solution direction, and V1 scope (max 5 features, each mapped to a job-to-be-done). Collect build and design preferences. Run gap assessment. Output: `definition.md`.

**Specify** — Wave 1: Product Detailer writes `solution.md` (journeys, feature specs, screens, states). Wave 2 (parallel): Tech Architect, Design Advisor, Test & Eval Generator produce their files. Choreographer runs spec completeness check, assembles `coding_agent_prompt.md` and `blueprint.md`. Output: all Phase 4 files.

**Launch** (optional) — Distribution plan for first 100 users, metrics, V2 triggers.

### Escape hatch: Vibe it!!

Available after Clarify or anytime mid-flow. The Choreographer generates all remaining files with opinionated defaults. No subagents, no quality gates, no retries. Speed over depth. All assumptions stated explicitly. Every file remains editable.

---

## Orchestration instructions

### Step 1: Load the Choreographer

Read and follow `prompts/choreographer.md`. This is the Choreographer's full system prompt. It contains all phase logic, quality gates, gap assessments, retry rules, pivot handling, scope guard, interaction patterns, and state management.

### Step 2: Resolve artifact root

Default: `ttt/` at workspace root. If that folder exists with unrelated content, use `ttt-docs/` or `ttt-artifacts/`. Persist in `ttt_state.json` → `session.artifact_root`.

### Step 3: Check for existing state

If `ttt_state.json` exists: resume from where things left off. Read current phase, last action, next action. Greet user with context.

If no state: fresh start. Follow Clarify phase from the top.

### Step 4: Run phases

Follow the Choreographer prompt for all phase logic. When subagents are needed:

**Validate phase** — spawn with:
- `prompts/market_researcher.md` → produces `market_research.md`
- `prompts/user_researcher.md` → produces `user_research.md`

**Specify phase** — spawn in two waves:
- Wave 1: `prompts/product_detailer.md` → produces `solution.md`
- Wave 2 (parallel after Wave 1): `prompts/tech_architect.md`, `prompts/design_advisor.md`, `prompts/test_eval_generator.md`

### Step 5: Validate and assemble

Apply quality gates to every subagent output (thresholds in choreographer prompt). Run gap assessments between phases. Assemble final files. Present to user.

---

## Subagent prompts

All canonical prompts live in `prompts/`. These are runtime-agnostic. Never fork them — reference or embed them.

| Prompt file | Agent | When |
|-------------|-------|------|
| `prompts/choreographer.md` | Choreographer | Always (this is the orchestrator) |
| `prompts/market_researcher.md` | Market Researcher | Validate phase |
| `prompts/user_researcher.md` | User Researcher | Validate phase |
| `prompts/product_detailer.md` | Product Detailer | Specify Wave 1 |
| `prompts/tech_architect.md` | Tech Architect | Specify Wave 2 |
| `prompts/design_advisor.md` | Design Advisor | Specify Wave 2 |
| `prompts/test_eval_generator.md` | Test & Eval Generator | Specify Wave 2 |

---

## Runtime notes

### Cursor

Use Task/delegate for subagent work when available. Reference prompt files with `@` paths. If Task tool is unavailable, run subagent prompts sequentially in the same context — same outputs, same quality bar.

### Claude Code

Load this skill file. For subagent work: use `context: fork` for isolated subagent execution if available. If not, run subagent prompts sequentially in the current context — use honest progress messaging ("Running Market Researcher first, then User Researcher"). Same output files and quality gates regardless of execution method.

### Web search

Research agents work best with web search. If search is unavailable:
- Keep full section structure with "N/A" for missing data
- Escalate to user after one search-blocked failure (don't burn retries)
- User can paste sources, switch environment, or acknowledge skipping Validate

---

## Key rules (non-negotiable)

1. **Scope guard:** Maximum 5 V1 features. Every feature maps to a JTBD. No silent scope expansion.
2. **Quality gates:** Every subagent output validated before writing to file. Retry up to 3 with specific feedback.
3. **Honesty:** Weak data labeled. Crowded markets called out. Failed research admitted.
4. **Max 2 questions per message.** Lead with the most important. Never a wall of questions.
5. **Progress in plain language.** Never "Phase 2 of 5." Always what's actually happening.
6. **State persistence.** `ttt_state.json` updated on every transition, decision, pivot, retry.
7. **Backup before overwrite.** Copy existing artifacts to `_backup/<timestamp>/` before regeneration.
8. **User agency.** User can pivot, override, skip, or Vibe it!! at any time. Log the choice, respect it.

---

## Architecture reference

Runtime decisions: `docs/PHASE0_DECISIONS.md`.
State schema: `schemas/ttt_state.example.json`.
