# Phase 0: Runtime gates - Context

**Gathered:** 2026-04-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Lock how Cursor and Claude Code spawn subagents, use web search, and write TTT artifacts **before** authoring agent prompts. Scope matches `plan.md` Phase 0 and `PHASE_PLAN.md` Phase 0 (gates only — no prompt files in this phase).

</domain>

<decisions>
## Implementation Decisions

### Artifact home & coexistence

- **Default artifact root:** Dedicated namespaced directory (e.g. `./ttt/` or `docs/ttt/`) — easy to `.gitignore`; exact folder name is a planner/research detail.
- **Name collision:** If the chosen folder already exists with unrelated content, **automatically fall back** to an alternate path (e.g. `.ttt/` or `ttt-artifacts/`) rather than overwriting or stopping by default.
- **Re-runs / overwrite:** Before overwriting an existing artifact bundle, **backup once** to something like `ttt/_backup/<timestamp>/` (exact naming for planner).
- **Monorepos:** Artifacts may live **per package** (e.g. `apps/web/ttt/`) — choreographer or state should record which path applies; not forced single root for the whole repo.

### No / degraded web search

- **Validate phase when search is unavailable:** Offer **skip Validate** with **explicit user acknowledgment**, recorded in `ttt_state` (per user choice — do not silently skip).
- **Tone:** **Brief and factual** when explaining degradation — what is missing and what you need from the user.
- **Research file shape:** Keep **all required sections** in `market_research.md` / `user_research.md`; mark gaps explicitly (N/A + why) rather than relaxing structure.
- **Retries when search is the blocker:** **Fast escalation** — after **one** failed attempt driven by blocked search/browse, escalate to user (paste sources or switch mode) rather than burning full retry budget.

### Parallel vs staggered subagents

- **Progress copy (staggered):** **Honest ordering** — say which agent runs first and that the other follows.
- **End state:** **Identical outputs** to parallel runs (same files and quality expectations); only wall-clock time differs.
- **Partial failure (staggered):** If the first researcher passes and the second fails after policy, **surface to user** with the same escalation paths as in parallel (fix / retry / pivot) — no silent partial phase.
- **Cursor vs Claude Code:** **Small wording differences allowed** per runtime if UX differs; core rules (honest stagger, escalation) stay aligned.

### Phase 0 closure / evidence

- **Spike log detail:** **High-level notes are acceptable** in `docs/phase0-spike-log.md` **provided** `docs/PHASE0_DECISIONS.md` states **clear, unambiguous defaults** for each gate.
- **Assumptions without live re-test:** **Planner/Claude discretion per subsystem** (Cursor vs Claude Code vs search) — document which areas were spiked vs assumed in `PHASE0_DECISIONS.md`.
- **Audience for decisions doc:** **Both** — short **user-facing** summary plus **maintainer** detail in `PHASE0_DECISIONS.md`.
- **Sign-off ritual:** **Planner/Claude discretion** — define a lightweight, repeatable “Phase 0 closed” ritual in the decisions doc when drafting it.

### Claude's Discretion

- Per-subsystem assumption policy (Cursor vs Claude vs search) — set explicit bullets in `PHASE0_DECISIONS.md` during Phase 0 synthesis.
- Exact default folder name (`ttt/` vs `docs/ttt/`), backup folder naming, and fallback path naming.
- Exact sign-off checklist wording and placement (top of `PHASE0_DECISIONS.md` vs separate file).

</decisions>

<specifics>
## Specific Ideas

- Backup-before-overwrite must be real on disk (not only described in prompts).
- Skip Validate is always opt-in with acknowledgment — aligns with momentum but preserves user agency.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within Phase 0 scope.

</deferred>

---

*Phase: 00-runtime-gates*
*Context gathered: 2026-04-04*
