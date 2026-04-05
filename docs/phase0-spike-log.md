# Phase 0 spike log — TTT

**Project:** TTT (To The T)  
**Phase:** 0 — Runtime gates  
**Purpose:** Evidence for Cursor / Claude Code / web-search behavior before locking `PHASE0_DECISIONS.md`.

Spikes are **high-level** per context; `PHASE0_DECISIONS.md` carries crisp defaults. Rows marked **ASSUMPTION** were not verified on a live run in this session.

---

## Cursor

**Date:** 2026-04-04

| Topic | Tried / noted | Result |
|--------|----------------|--------|
| Isolated agent work | Cursor **Task** tool (delegate to subagent) and **Composer** multi-step agent sessions | **ASSUMPTION:** Task tool available in Cursor when user enables agent/delegate flows; Composer runs in shared workspace with file access. **Confirm:** Run a delegated Task in this repo and note whether child context sees full tree. |
| Parallel subagents | Multiple concurrent agent sessions | **ASSUMPTION:** True parallel depends on product tier and UI; often **sequential** handoff is reliable. TTT must support staggered execution with honest messaging. |
| File visibility | Workspace-root relative paths | **PASS (environment):** Agents in Cursor generally read/write project files under workspace root. |
| Constraints | Rules in `.cursor/rules/*.mdc` gate behavior | **ASSUMPTION:** Rules apply to agent; exact load order is product-defined. |

---

## Claude Code

**Date:** 2026-04-04

| Topic | Tried / noted | Result |
|--------|----------------|--------|
| Skill layout | Skills under project or user skill dir (e.g. `skills/ttt/SKILL.md`) | **ASSUMPTION:** Claude Code loads `SKILL.md` when present per install docs; **Confirm:** `claude` CLI / plugin skill path on target machine. |
| Subagent / secondary context | Task-style spawn vs single-thread skill | **ASSUMPTION:** “Subagent” behavior is skill + user invocation pattern dependent; may be manual copy-paste of prompt files. Document primary + fallback in PHASE0_DECISIONS. |
| Workspace files | Same cwd as project | **ASSUMPTION:** Skill runs with project root visible; **Confirm** on real Claude Code session. |

---

## Web search

**Date:** 2026-04-04

| Topic | Tried / noted | Result |
|--------|----------------|--------|
| Cursor agent search | Built-in web / fetch in agent | **ASSUMPTION:** Varies by model integration and settings; treat as **partial** until confirmed. |
| Claude Code search | Browse / web in environment | **ASSUMPTION:** Varies by install; treat as **partial** until confirmed. |
| Researcher prompts | Market + User need sources | Degradation path documented in `PHASE0_DECISIONS.md` (skip Validate + ack, paste sources, fast escalate). |

---

*End of spike log for Phase 0.*
