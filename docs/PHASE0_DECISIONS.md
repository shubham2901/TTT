# Phase 0 decisions — TTT runtime gates

**Status:** Phase 0 **closed** (checklist complete; see Sign-off).  
**Spike log:** [phase0-spike-log.md](./phase0-spike-log.md)  
**Next:** After sign-off, start **Phase 1** (core prompts) per [PHASE_PLAN.md](../PHASE_PLAN.md).

---

## Phase 0 closed checklist

Tick when true. **Do not** pre-check without review.

Y Cursor default orchestration pattern reviewed and accepted
Y Claude Code default orchestration pattern reviewed and accepted
Y Web search matrix + degradation rules reviewed and accepted
Y Artifact paths, collision fallback, and backup rule reviewed and accepted
Y Execution ordering (parallel vs staggered) reviewed and accepted
Y Spike log reviewed (ASSUMPTION items either verified or accepted as risk)

---

## User summary

- TTT writes its files under a `**ttt/`** folder at your project (or package) root. If that folder already exists for something else, TTT uses `**ttt-docs/**` or `**ttt-artifacts/**` instead and remembers the path.
- Before replacing a full set of outputs, TTT ~~(or you, if tooling is manual)~~ should **copy the old bundle** to `ttt/_backup/<timestamp>/`.
- **Market and User research** work best with web search. If search is not available, the assistant stays **brief and factual**, keeps the same report **sections** (mark gaps as N/A), and may **skip the Validate step only if you explicitly agree** — that choice is recorded.
- If research fails because search is blocked, TTT **escalates to you after one** failed attempt on that cause (paste links or change mode) instead of burning three generic retries.
- When two researchers cannot run at the same time, you see **honest** progress (“Market first, then User”). The **same files** are still expected as when they run in parallel.
- **Cursor** and **Claude Code** may use **slightly different wording**, but the rules above stay the same.

---

## Sign-off

- **Reviewed by:** Shubham **Date:** 04/04/26
- Phase 0 is **closed for planning purposes** when the checklist above is complete and maintainers agree spikes/assumptions are acceptable.

---

## Maintainer detail

### § Assumptions by subsystem


| Subsystem       | Spiked vs assumed                                | Notes                                                                               |
| --------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------- |
| **Cursor**      | Mostly **ASSUMPTION** (see spike log 2026-04-04) | Confirm Task/delegate + parallel behavior on your Cursor build.                     |
| **Claude Code** | Mostly **ASSUMPTION**                            | Confirm skill path + file visibility on real `claude` sessions.                     |
| **Web search**  | **ASSUMPTION** per runtime                       | Fill matrix below after live probe; defaults are conservative (partial / degraded). |


---

### § Cursor

- **Default orchestration:** Prefer **rules-driven** flow (`.cursor/rules/ttt.mdc` in Phase 2) + **Composer** for sequential work. Use **Task / delegate** when available to isolate subagent prompts; reference files under `prompts/*.md` with `@` paths.
- **Parallel vs staggered:** If two agents cannot run together, run **Market Researcher then User Researcher** with **explicit user-visible ordering**. Outputs must match parallel semantics (same filenames and quality bar).
- **Partial failure:** If one researcher completes and the other fails, **surface to user** — retry, pivot, or paste sources; do not silently ship half a Validate phase.
- **Evidence:** [phase0-spike-log.md § Cursor](./phase0-spike-log.md#cursor)

---

### § Claude Code

- **Default orchestration:** **Skill entry** `skills/ttt/SKILL.md` (Phase 2) with steps that load `prompts/*.md` and orchestrate phases per architecture. Subagent-style work may be **manual prompt handoff** if the runtime has no true parallel spawn.
- **Parallel vs staggered:** Same as Cursor: **honest ordering**, **identical artifact contract**.
- **Partial failure:** Same escalation behavior as Cursor.
- **Evidence:** [phase0-spike-log.md § Claude Code](./phase0-spike-log.md#claude-code)

---

### § Web search

**Tone when degrading:** Brief and factual — what is missing, what the user can do.

**Research outputs:** Keep **full section structure** for `market_research.md` / `user_research.md`; use **N/A + reason** where data is missing.

**Skip Validate:** Allowed **only** with **explicit user acknowledgment**; record in `**ttt_state.json`** (e.g. under `decisions` and/or `session` — choreographer must write a durable note).

**Search-blocked failures:** After **one** failure where the primary cause is unavailable search/browse, **escalate to user** (paste sources, run elsewhere, or acknowledge skip). Do **not** consume the full three generic retries on that cause.


| Runtime     | Search / browse                    | User fallback                                                       |
| ----------- | ---------------------------------- | ------------------------------------------------------------------- |
| Cursor      | **Partial** (ASSUMPTION — confirm) | Paste sources; optional skip Validate + ack; escalate fast on block |
| Claude Code | **Partial** (ASSUMPTION — confirm) | Same                                                                |


---

### § Paths

**Default artifact root:** `<workspace-or-package-root>/ttt/`  
**Optional variant (maintainer):** `docs/ttt/` if the team prefers artifacts colocated with docs — still a single namespaced tree.

**Collision:** If `ttt/` exists and is **not** TTT’s bundle (unrelated content), use fallback order: `**ttt-docs/`** → `**ttt-artifacts/**`. First writable unused option wins.

**Recording resolved root:** Choreographer persists the chosen directory in `**ttt_state.json`** as `**session.artifact_root**` (string, relative path from workspace root, e.g. `ttt`, `apps/web/ttt`, `.ttt`). If missing, implementations default to `ttt/` and create it.

**Backup before overwrite:** Immediately before regenerating the full artifact set, copy existing TTT outputs to:

`{artifact_root}/_backup/<ISO-8601-UTC-timestamp>/`  
(copy all tracked markdown + `ttt_state.json` that live under `{artifact_root}`).

**Monorepo:**


| Mode                  | Artifact root pattern    | State                                     |
| --------------------- | ------------------------ | ----------------------------------------- |
| Single product thesis | `<repo>/ttt/`            | `session.artifact_root`: `ttt`            |
| Per package / app     | `<repo>/apps/<pkg>/ttt/` | `session.artifact_root`: `apps/<pkg>/ttt` |


**Artifact file list** (relative to `{artifact_root}` unless noted):


| File                   | Path pattern                             |
| ---------------------- | ---------------------------------------- |
| ttt_state.json         | `{artifact_root}/ttt_state.json`         |
| clarification.md       | `{artifact_root}/clarification.md`       |
| market_research.md     | `{artifact_root}/market_research.md`     |
| user_research.md       | `{artifact_root}/user_research.md`       |
| definition.md          | `{artifact_root}/definition.md`          |
| solution.md            | `{artifact_root}/solution.md`            |
| tech_architecture.md   | `{artifact_root}/tech_architecture.md`   |
| design_guideline.md    | `{artifact_root}/design_guideline.md`    |
| test_eval.md           | `{artifact_root}/test_eval.md`           |
| coding_agent_prompt.md | `{artifact_root}/coding_agent_prompt.md` |
| blueprint.md           | `{artifact_root}/blueprint.md`           |
| versions.md            | `{artifact_root}/versions.md`            |
| launch.md              | `{artifact_root}/launch.md` (optional)   |


---

### § Execution ordering

**Ideal:** **Market Researcher** and **User Researcher** in **parallel** during Validate.

**Fallback:** **Staggered** runs — tell the user **which agent runs first** and that the **second follows**. Same **files** and **quality expectations** as parallel.

**Partial failure:** **Same escalation** as parallel (no silent half-Validate).

**Runtime wording:** Cursor vs Claude Code may use **slightly different** user-facing strings; **non‑negotiable** behaviors:

- Honest ordering when staggered
- Identical artifact set and structure
- No silent skip of Validate
- Search-blocked → fast user escalation
- Skip Validate only with explicit acknowledgment + state record

---

*Document version: 2026-04-04 — Phase 0 execution*