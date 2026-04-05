# TTT — Executable Phase Plan

**Repo:** `/Users/shubham/Desktop/PMOS/TTT`  
**Authoritative roadmap:** `plan.md`  
**Architecture:** `ttt_master_architecture_part1.md`, `ttt_master_architecture_part2.md`  
**Rule:** No agent prompt authoring until Phase 0 is **closed** (signed decisions on disk).

---

## Execution ownership (who does what)

| Owner | Scope |
|--------|--------|
| **Composer 2** | Default for all work unless a row below says otherwise: Phase 0 spikes/docs, subagent prompts **except** the orchestrator choreographer deliverable, Phase 2 Cursor wrapper + invocation docs, Phase 3 eval assets, fixes after review. |
| **Opus — session 1 (orchestrator only)** | **Orchestrator** work only: `prompts/choreographer.md` and any **orchestration instructions** that belong in the Cursor entry (e.g. sequencing/delegation narrative inside `.cursor/rules/ttt.mdc`). **Do not** author or rewrite `SKILL.md` in this session — keep prompt writing for orchestrator and skill **strictly separate**. |
| **Opus — session 2 (SKILL.md only)** | **Claude Code skill** only: `skills/ttt/SKILL.md` (frontmatter + body, references to `prompts/*`). No choreographer rewrites here unless review phase files bugs. |
| **Opus — separate thread (Phase R)** | **Review phase only** (new chat/thread): read-only critique and change requests across **all** prompts, **code**, **runtime** docs, and packaging — not blended with authoring sessions above. (*Named **R** to avoid confusion with TTT product **Phase 4 (SPECIFY)** in the architecture.*) |

**Workflow:** Run Opus orchestrator session after Phase 0 closes and before/with early Phase 1 (choreographer must exist before dependent prompts). Run Opus `SKILL.md` session after Phase 1 prompt set is stable enough to reference (typically after Composer finishes 1.2–1.5, or in parallel once paths are frozen). Run **Phase R** after Phase 2 Wave 1 (or when you want a full pass: prompts + Cursor + Claude artifacts); address findings with **Composer 2** unless a fix explicitly needs Opus (then use a fresh Opus authoring pass, not the review thread).

---

## How to use this document

1. Execute tasks **in dependency order** (task IDs). Same **wave** = can parallelize if no file overlap.
2. Each task has **verify** (how to prove done) and **done** (acceptance).
3. **Goal-backward** blocks state what must be *true* for the phase to succeed; tasks map to those truths.

---

## Global dependency overview

```text
Phase 0 (gates, Composer 2) ──► Phase 1 (Composer 2 + Opus choreographer/orchestration)
        ──► Phase 2 Wave 1 (Composer 2 Cursor + Opus SKILL.md only)
        ──► Phase R (Opus review, separate thread) ──► fixes (Composer 2 default)
        ──► Phase 3 (evals, Composer 2); full eval runs best after Phase 2 ± Phase R
```

| After completing | Unblocks |
|------------------|----------|
| Phase 0 | Phase 1 only |
| Phase 1 | Phase 2 packaging; Phase 3 scenario dry-runs with manual orchestration |
| Phase 2 Wave 1 | End-to-end TTT in Cursor + Claude Code with declared spawn/search/path behavior |
| Phase R (Opus review) | Nothing automatically — produces findings; implement fixes with Composer 2 (or targeted Opus if you choose) |
| Phase 3 | Measured prompt quality loop |

---

## Risks and assumptions

| Risk / assumption | Mitigation |
|-------------------|------------|
| **Cursor `Task`/subagent APIs change** | Record *current* behavior in `docs/PHASE0_DECISIONS.md`; version the date; fallback = sequential @-file handoff documented in runtime README. |
| **Claude Code skill + subprocess semantics differ by install** | Phase 0 spike: confirm skill load path and whether child sessions see project files; document in `runtime/claude-code/README.md`. |
| **Web search not available in some runtimes** | Prompts must state: use built-in search when present; otherwise instruct user to paste sources or run research in an environment with search. Encode both paths in Phase 1 researcher prompts *after* Phase 0 records capability. |
| **No persistent filesystem (future claude.ai)** | Out of scope for Wave 1; Phase 0 only scopes **repo + Cursor + Claude Code** paths. Wave 3 adapters listed as later work in `plan.md`. |
| **Parallel research agents** | Architecture assumes Market + User in parallel; if runtime cannot parallelize, Choreographer instructions must allow **staggered** runs (same outputs). |
| **Design Advisor / Test Eval want `solution.md`** | Use **Phase 4 Option A** (Part 1): Product Detailer first wave, then Tech + Design + Test in parallel — reflected in `prompts/choreographer.md` in Phase 1. |
| **Mixing Opus authoring threads** | Orchestrator vs `SKILL.md` vs Phase R review **must** stay separate sessions; review thread stays read/critique-first to avoid draft-and-review in one context. |

---

# Phase 0 — Runtime gates (must complete first)

## Phase goal (outcome-shaped)

**Operators know exactly how TTT spawns subagents, uses web search, and writes artifacts in Cursor and Claude Code — without opening Part 1/2.**

## Goal-backward verification (must be true)

| ID | Truth (observable) | Evidence on disk |
|----|--------------------|------------------|
| P0-T1 | Cursor subagent strategy is **chosen** and documented | `docs/PHASE0_DECISIONS.md` § Cursor |
| P0-T2 | Claude Code skill/subprocess strategy is **chosen** and documented | `docs/PHASE0_DECISIONS.md` § Claude Code |
| P0-T3 | Web search expectation per runtime is **explicit** (available / degraded / manual) | Same file, § Web search |
| P0-T4 | Default **artifact root** relative to user project is **fixed** (e.g. `./ttt/` or repo root) | Same file, § Paths + example path table |
| P0-T5 | A **spike log** proves what was actually tried (not guessed) | `docs/phase0-spike-log.md` |

## Target files (create in Phase 0)

| Path | Purpose |
|------|---------|
| `docs/PHASE0_DECISIONS.md` | Locked defaults, alternatives, “if X then Y” for executor |
| `docs/phase0-spike-log.md` | Dated commands/attempts: Task tool, rules, skill load, search |
| `runtime/README.md` | Index: where Cursor vs Claude Code wrappers will live after Phase 2 |

## Phase 0 — Task table

| ID | Task | Depends on | Files created/updated | Verify | Done (acceptance) |
|----|------|------------|------------------------|--------|---------------------|
| **0.1** | **Spike: Cursor** — Confirm how to run isolated agent work (e.g. Task tool, Composer 2 agents, or manual copy-paste workflow). Capture constraints in spike log. **Owner: Composer 2.** | — | `docs/phase0-spike-log.md` | Log contains dated subsection “Cursor” with what was tried and result | P0-T1 satisfied: decision paragraph + recommended default workflow in `PHASE0_DECISIONS.md` |
| **0.2** | **Spike: Claude Code** — Confirm skill directory layout expectation, how to invoke “subagent” or secondary context, file visibility. **Owner: Composer 2.** | — | `docs/phase0-spike-log.md` | Log subsection “Claude Code” with dated evidence | P0-T2 satisfied in decisions doc |
| **0.3** | **Spike: Web search** — For each target runtime (Cursor agent, Claude Code), note whether browsing/search is available and how prompts should degrade. **Owner: Composer 2.** | 0.1, 0.2 | `docs/phase0-spike-log.md`, `docs/PHASE0_DECISIONS.md` | Decisions doc has a matrix: Runtime × Search capability × User fallback | P0-T3 satisfied |
| **0.4** | **Decide artifact paths** — Choose directory for `ttt_state.json`, `clarification.md`, … (see plan.md table). Document naming, overwrite rules, multi-session. **Owner: Composer 2.** | 0.1, 0.2 | `docs/PHASE0_DECISIONS.md` | Table lists every artifact from `plan.md` → absolute/relative path pattern | P0-T4 satisfied |
| **0.5** | **Synthesize + gate** — Merge spike log into decisions; add “Phase 0 closed” checklist at top of `PHASE0_DECISIONS.md`; stub `runtime/README.md` pointing forward to Phase 2. **Owner: Composer 2.** | 0.1–0.4 | `docs/PHASE0_DECISIONS.md`, `runtime/README.md` | Checklist all `[x]`; `runtime/README.md` lists upcoming `runtime/cursor/`, `runtime/claude-code/` | P0-T5 + Phase 0 goal met; **Phase 1 allowed** |

### Phase 0 closure checklist (copy into `docs/PHASE0_DECISIONS.md` when complete)

- [ ] Cursor: default orchestration pattern written
- [ ] Claude Code: default orchestration pattern written  
- [ ] Web search: matrix + prompt degradation rule written  
- [ ] Paths: artifact root + file list written  
- [ ] Spike log references dated evidence  

---

# Phase 1 — Core prompts (runtime-agnostic markdown)

## Phase goal

**Seven canonical prompt files exist** that fully encode Part 1 flows, gates, and Part 2 output shapes — suitable for copy-paste or wrapper inclusion without editing content per IDE.

## Goal-backward verification

| ID | Truth | Evidence |
|----|-------|----------|
| P1-T1 | Choreographer encodes all five phase flows, gates, retries, pivot, Vibe it!!, resume, UX rules | `prompts/choreographer.md` |
| P1-T2 | Researchers encode structures + source rules from `plan.md` §1.2–1.3 | `prompts/market_researcher.md`, `prompts/user_researcher.md` |
| P1-T3 | Spec agents encode inputs/outputs per `plan.md` §1.4–1.7 and Option A ordering | Four files below |
| P1-T4 | Every artifact in `plan.md` output table has a **template or explicit “write this section”** pointer | Prompts reference Part 2 sections OR `templates/` stubs |
| P1-T5 | Prompts reference **artifact paths** consistent with Phase 0 | Cross-check against `docs/PHASE0_DECISIONS.md` |

## Target files (create in Phase 1)

| Path | Agent |
|------|--------|
| `prompts/choreographer.md` | Choreographer |
| `prompts/market_researcher.md` | Market Researcher |
| `prompts/user_researcher.md` | User Researcher |
| `prompts/product_detailer.md` | Product Detailer |
| `prompts/tech_architect.md` | Tech Architect |
| `prompts/design_advisor.md` | Design Advisor |
| `prompts/test_eval_generator.md` | Test & Eval Generator |
| `templates/README.md` | Optional index pointing to Part 2 for full schemas |
| `schemas/ttt_state.example.json` | **Copy** of Part 2 example `ttt_state.json` for prompt testing (not runtime logic) |

## Phase 1 — Task table

| ID | Task | Depends on | Files | Verify | Done |
|----|------|------------|-------|--------|------|
| **1.1** | **Choreographer prompt (orchestrator)** — Encode: CLARIFY → VALIDATE → DEFINE → SPECIFY → LAUNCH; quality gates; retry ≤3; define→specify 6 checks; spec completeness 8 checks; scope ≤5 V1; Vibe it!!; pivot narrow/broad; resume from `ttt_state.json`; progress labels; joke bank (min 4 categories per `plan.md` build-later note — **stub OK**); max 2 questions; analogies; escape hatches. **Explicitly specify Phase 4 Wave 1 = Product Detailer, Wave 2 = Tech + Design + Test parallel.** **Owner: Opus (orchestrator-only session).** Do not write `SKILL.md` in this session. | Phase 0 closed | `prompts/choreographer.md`, optionally `schemas/ttt_state.example.json` | Grep prompt for: `quality gate`, `retry`, `gap`, `Vibe`, `ttt_state`, `Product Detailer`, `wave` | P1-T1 satisfied; wave ordering unambiguous |
| **1.2** | **Research prompts** — Market + User per `plan.md` §1.2–1.3; input `clarification.md`; output filenames fixed per Phase 0 paths. **Owner: Composer 2.** | 1.1 (for path constants only — can draft in parallel if paths frozen in 0.4) | `prompts/market_researcher.md`, `prompts/user_researcher.md` | Each contains required section headings matching Part 2 templates | P1-T2 satisfied |
| **1.3** | **Product Detailer prompt** — Inputs/outputs per `plan.md` §1.4; V1-only scope. **Owner: Composer 2.** | 1.1 | `prompts/product_detailer.md` | Lists journeys, feature spec format, screens, 4 states | P1-T3 partial |
| **1.4** | **Tech / Design / Test prompts** — Per `plan.md` §1.5–1.7; Design + Test state dependency on `solution.md` from Wave 1. **Owner: Composer 2.** | 1.3 | `prompts/tech_architect.md`, `prompts/design_advisor.md`, `prompts/test_eval_generator.md` | Design/Test prompts say “read `solution.md` from prior wave” | P1-T3 satisfied |
| **1.5** | **Cross-review + path alignment** — Read `docs/PHASE0_DECISIONS.md`; update all prompts to use **the same** path tokens; add `templates/README.md` if helpful. **Owner: Composer 2** (not the Opus Phase R thread — this is implementation alignment). | 1.1–1.4, Phase 0 | All seven prompts + `templates/README.md` | Diff shows consistent path strings; no prompt references old/ambiguous locations | P1-T4, P1-T5 satisfied |

**Suggested waves:** **1.1 Opus** first (establishes constants). **1.2 || 1.3** parallel (Composer 2). **1.4** after 1.3. **1.5** last (Composer 2).

---

# Phase 2 — Runtime packaging (Wave 1: Cursor + Claude Code)

## Phase goal

**A user can invoke TTT from Cursor and from Claude Code** using repo-native entry points that **include** Phase 1 prompts (no forked prompt text — reference or embed-by-build step documented).

## Goal-backward verification

| ID | Truth | Evidence |
|----|-------|----------|
| P2-T1 | Cursor entry exists and documents spawn + search + paths | `runtime/cursor/README.md` + rules or skill file under `.cursor/` |
| P2-T2 | Claude Code entry exists (`SKILL.md`) with same behavioral contract | `skills/ttt/SKILL.md` (or `skill/ttt/SKILL.md` — pick one, document in `runtime/README.md`) |
| P2-T3 | Single table maps **user action → which prompt file → expected outputs** | `runtime/INVOCATION.md` |

## Target files

| Path | Purpose |
|------|---------|
| `.cursor/rules/ttt.mdc` | Cursor rule bundle: when to load choreographer, how to delegate (per Phase 0) |
| `runtime/cursor/README.md` | Cursor-specific setup, limitations, manual fallback |
| `skills/ttt/SKILL.md` | Claude Code skill frontmatter + body: instructions + `@prompts/...` references |
| `runtime/claude-code/README.md` | Install path, testing notes |
| `runtime/INVOCATION.md` | Unified map for both runtimes |

## Phase 2 — Task table

| ID | Task | Depends on | Files | Verify | Done |
|----|------|------------|-------|--------|------|
| **2.1** | **Cursor wrapper** — Create `.cursor/rules/ttt.mdc` implementing Phase 0 decisions; link to `prompts/*.md`; document Task vs manual fallback in `runtime/cursor/README.md`. **Orchestration-heavy prose** (how phases chain, when to spawn) may be authored by **Opus in the orchestrator session (1.1)** as a spec you paste into 2.1, or drafted here by **Composer 2** from `prompts/choreographer.md` — do not duplicate conflicting instructions. **Owner: Composer 2** for file creation and integration. | Phase 1 + Phase 0 | `.cursor/rules/ttt.mdc`, `runtime/cursor/README.md` | Files exist; README steps runnable on fresh clone | P2-T1 satisfied |
| **2.2** | **Claude Code skill** — Author `skills/ttt/SKILL.md` per skill-creator conventions; include description, when to use, steps to orchestrate phases; reference prompt files by relative path. **Owner: Opus (SKILL.md-only session).** No choreographer rewrites in this session. | Phase 1 + Phase 0 | `skills/ttt/SKILL.md`, `runtime/claude-code/README.md` | Skill file parses; README lists install command | P2-T2 satisfied |
| **2.3** | **Invocation matrix** — Write `runtime/INVOCATION.md` + update `runtime/README.md` with links to Cursor/Claude docs. **Owner: Composer 2.** | 2.1, 2.2 | `runtime/INVOCATION.md`, `runtime/README.md` | Matrix covers all 7 agents + choreographer + artifact outputs | P2-T3 satisfied |

**Note:** `plan.md` Wave 2/3 (Windsurf, VS Code, Codex, claude.ai) — **do not implement** until Wave 1 is verified; add a “Future adapters” subsection in `runtime/README.md` only.

---

# Phase R — Opus review (separate thread)

## Phase goal

**Independent quality pass** over the repo: prompts, any code, and runtime packaging — run in a **new Opus chat/thread** so it is not mixed with orchestrator authoring or `SKILL.md` authoring. (**R** = review; not TTT product Phase 4 SPECIFY.)

## Goal-backward verification

| ID | Truth | Evidence |
|----|-------|----------|
| PR-T1 | Review covers all seven `prompts/*.md`, `.cursor/rules/ttt.mdc`, `skills/ttt/SKILL.md`, and `runtime/**` docs | Written review output (see below) |
| PR-T2 | Findings are actionable (file + issue + suggested fix), not generic praise | Review doc sections per area |
| PR-T3 | Review thread did not also draft major new prompt text (critique-only; implementation elsewhere) | Thread scope agreed up front |

## Target output (create after review)

| Path | Purpose |
|------|--------|
| `docs/OPUS_REVIEW.md` | Consolidated findings from the Opus review thread: prompts, code, runtime, gaps vs `plan.md` / Part 1–2 |

## Phase R — Task table

| ID | Task | Depends on | Owner | Verify | Done |
|----|------|------------|-------|--------|------|
| **R.1** | **Full pass** — In a **separate Opus thread**, review alignment of prompts with architecture; Cursor vs choreographer consistency; `SKILL.md` vs Phase 0 decisions; missing sections; spawn/search/path risks; eval readiness. | Phase 2 tasks 2.1–2.3 (minimum); can also run after Phase 1 if you want prompt-only review first | **Opus (review-only thread)** | `docs/OPUS_REVIEW.md` exists with dated summary | PR-T1–T3 satisfied |
| **R.2** | **Triage fixes** — Turn `docs/OPUS_REVIEW.md` into repo changes. **Default: Composer 2.** | R.1 | Composer 2 | PR/commit addresses or explicitly defers each item | Review loop closed or deferred items listed |

**Order:** Prefer **Phase R** after **Phase 2 Wave 1** so `SKILL.md` and Cursor rules exist to review together. **Phase 3** (evals) stays Composer 2; run **full** scenario evals after packaging and ideally after Phase R triage.

---

# Phase 3 — Evals (S1–S4 + rubric + loop)

## Phase goal

**Repeatable eval protocol** exists: fixed scenarios, per-file judgment dimensions aligned with `plan.md` §3.2, 1–5 scale, human-first then LLM-judge path documented.

## Goal-backward verification

| ID | Truth | Evidence |
|----|-------|----------|
| P3-T1 | S1–S4 starter prompts and success bullets are captured | `evals/scenarios.md` |
| P3-T2 | Per-artifact rubric dimensions match `plan.md` §3.2 | `evals/rubric.md` |
| P3-T3 | Scoring + iteration procedure documented | `evals/protocol.md` |
| P3-T4 | LLM-judge prompt stub exists for v2 calibration | `evals/llm-judge-prompt.md` |

## Target files

| Path | Purpose |
|------|---------|
| `evals/scenarios.md` | S1–S4 inputs + expected high-level outcomes |
| `evals/rubric.md` | Dimensions per file; 1–5 anchor text |
| `evals/protocol.md` | Order: run → human score → log failures → revise prompts → rerun |
| `evals/llm-judge-prompt.md` | Template for automated judging (calibrate later) |
| `evals/README.md` | How to bundle transcripts + artifacts for scoring |

## Phase 3 — Task table

| ID | Task | Depends on | Files | Verify | Done |
|----|------|------------|-------|--------|------|
| **3.1** | **Scenarios** — Lift S1–S4 from `plan.md` §3.1; add “artifact bundle checklist” per run. **Owner: Composer 2.** | Phase 1 (prompts exist for dry run) | `evals/scenarios.md`, `evals/README.md` | Each scenario lists required outputs | P3-T1 satisfied |
| **3.2** | **Rubric** — Formalize §3.2 tables into scoring sheet friendly format; include cross-file alignment checks. **Owner: Composer 2.** | 3.1 | `evals/rubric.md` | Every file from `plan.md` table has dimensions | P3-T2 satisfied |
| **3.3** | **Protocol + LLM stub** — §3.3–3.4 steps; failure log template; LLM judge prompt with “use rubric” instruction. **Owner: Composer 2.** | 3.2 | `evals/protocol.md`, `evals/llm-judge-prompt.md` | Protocol numbered steps match `plan.md` | P3-T3, P3-T4 satisfied |

**Dependency:** Phase 3 can start after **Phase 1** for rubric/protocol authoring; **full** S1 end-to-end requires **Phase 2 Wave 1** (or heroic manual orchestration using prompts only).

---

# Traceability matrix (plan.md delivery checklist → this plan)

| `plan.md` item | Addressed by |
|----------------|--------------|
| Phase 0 gates | Phase 0 tasks 0.1–0.5 |
| Seven agent prompts | Phase 1 tasks 1.1–1.4 |
| Quality gate + gap logic in Choreographer | Task 1.1 |
| `ttt_state.json` read/write | Choreographer prompt 1.1 + example `schemas/ttt_state.example.json` |
| SKILL / Cursor entry | Phase 2 tasks 2.1–2.2 |
| Session resume, retry, pivot | Choreographer 1.1 (should); explicit UX in wrapper READMEs 2.1–2.3 |
| Evals S1–S4 + scoring | Phase 3 |
| Opus cross-cutting review | Phase R → `docs/OPUS_REVIEW.md` |
| “Build later” (quick mode, config, GSD bridge, full joke bank) | **Out of scope** for this PHASE_PLAN — do not implement until explicitly scheduled |

---

# Execution checklist (printable)

- [ ] **P0** `docs/PHASE0_DECISIONS.md` complete; Phase 0 closed checklist checked (**Composer 2**)  
- [ ] **P0** `docs/phase0-spike-log.md` complete  
- [ ] **P1** `prompts/choreographer.md` from **Opus orchestrator-only** session  
- [ ] **P1** Remaining six prompts + alignment task 1.5 (**Composer 2**)  
- [ ] **P1** `schemas/ttt_state.example.json` present (optional but recommended)  
- [ ] **P2** `.cursor/rules/ttt.mdc` + `runtime/cursor/*` (**Composer 2**)  
- [ ] **P2** `skills/ttt/SKILL.md` (**Opus SKILL.md-only** session)  
- [ ] **P2** `runtime/INVOCATION.md` + `runtime/README.md` (**Composer 2**)  
- [ ] **Phase R** Opus **separate-thread** review → `docs/OPUS_REVIEW.md`; triage with **Composer 2**  
- [ ] **P3** `evals/*` complete (**Composer 2**)  
- [ ] Spot-check: Choreographer mentions **Product Detailer wave 1** then **parallel trio**  

---

**Absolute path:** `/Users/shubham/Desktop/PMOS/TTT/PHASE_PLAN.md`
