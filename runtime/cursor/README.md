# TTT — Cursor Runtime

Runtime entry point for TTT in Cursor IDE. This document covers activation, subagent execution, web search degradation, installation, and troubleshooting.

---

## Quick-start

1. Confirm `.cursor/rules/ttt.mdc` exists in the project root.
2. Open a Cursor Agent chat (Cmd+L or Ctrl+L).
3. Say **"TTT"** — the agent-decided rule activates from description match.
4. If the agent responds with the Clarify phase intro, TTT is working.
5. If resuming: the agent reads `ttt/ttt_state.json` and picks up from the saved phase.

---

## How activation works

- **First invocation:** The agent reads `ttt.mdc`'s description field, decides relevance based on the user message (mentions of "TTT", "product spec", "product management", "validate idea"), and loads the rule body.
- **Ongoing editing:** When editing files under `ttt/`, the glob `ttt/**` auto-attaches the rule to context.
- Both paths load identical content — no duplicate injection occurs.
- If the artifact root resolves to `ttt-docs/` or `ttt-artifacts/` (collision fallback), the glob won't match. Agent-decided activation still works on "TTT" mentions. No action required.

---

## Subagent execution

The choreographer spawns specialist subagents during Validate and Specify phases.

**Primary method — Task tool (foreground, blocking):**
- Read the prompt file (e.g. `prompts/market_researcher.md`).
- Pass prompt content as the subagent's system instruction via Task tool.
- Include input file paths and expected output filename in the task description.
- The parent agent blocks until the subagent completes and validates output.

**Parallel execution (Validate phase):**
- Issue multiple Task calls in a single response.
- Market Researcher and User Researcher run concurrently.
- Both produce their output files independently; choreographer validates both before proceeding.

**Fallback — sequential in-context execution:**
- When the Task tool is unavailable, read the prompt inline with `@prompts/[agent].md`.
- Execute the agent's instructions within the current context, sequentially.
- Same output files and quality gates apply — no reduction in artifact quality.

**Partial failure handling:**
- If one researcher completes and the other fails, surface to user.
- Options: retry, pivot, paste sources manually. Never silently ship half a Validate phase.

---

## Web search

Per Phase 0 decisions, web search behavior during Validate:

- **Recommended** for Market Research and User Research subagents.
- If search is unavailable: keep full section structure in output files, mark gaps as "N/A — search unavailable".
- After **one** search-blocked failure, escalate to the user immediately. Do not burn remaining retries on the same cause.
- User options on escalation: paste sources directly, switch to a search-capable environment, or acknowledge skipping Validate (recorded in `ttt_state.json`).
- Skip Validate is allowed **only** with explicit user acknowledgment.

---

## Installation

Three methods, in order of preference:

**1. Skill install (primary)**
Copy `.cursor/rules/ttt.mdc` and the `prompts/` directory into the target project. The rule file bootstraps everything; prompts contain all agent instructions.

**2. Git clone**
Clone the TTT repository. Relevant files are at standard locations:
- `.cursor/rules/ttt.mdc` — rule entry point
- `prompts/` — choreographer + specialist agent prompts
- `schemas/` — JSON schemas for state and artifact validation

**3. Manual copy**
Copy these into the target project root:
- `.cursor/rules/ttt.mdc`
- `prompts/` directory (all `.md` files)
- `schemas/` directory (all `.json` files)

After any method, verify activation by opening Agent chat and saying "TTT".

---

## Troubleshooting

**Rule not activating:**
- Confirm `.cursor/rules/ttt.mdc` exists and the `description` field in frontmatter is intact.
- Check that `alwaysApply` is `false` and `globs` is `ttt/**`.
- Try mentioning "TTT" explicitly in the chat message.

**Task tool unavailable:**
- Use the sequential fallback: read the prompt with `@prompts/[agent].md` and execute in current context.
- Same outputs and quality gates apply.

**Glob not matching:**
- The artifact root may have resolved to `ttt-docs/` or `ttt-artifacts/` instead of `ttt/`.
- Agent-decided activation still works via description match — glob is a convenience, not a requirement.

**Context pressure (agent seems forgetful):**
- Clear context at recommended transition points: after Validate completes, after Define completes.
- State is persisted in `ttt_state.json` — the agent resumes cleanly from a fresh context window.

---

## Edge cases

**Artifact root collision:**
If `ttt/` is occupied by unrelated content, the choreographer resolves to `ttt-docs/` then `ttt-artifacts/`. The resolved path is persisted in `ttt_state.json` at `session.artifact_root`.

**Session resume after context clear:**
All progress is stored in `ttt_state.json`. On resume, the agent reads state and continues from the last completed step. No manual re-entry required.

**Coexistence with other rules:**
TTT's `.cursor/rules/ttt.mdc` is scoped by its description keywords and `ttt/**` glob. No conflict expected with other `.mdc` files in `.cursor/rules/`.

**"Vibe it!!" shortcut:**
At any point after Clarify, the user can say "Vibe it!!" to skip remaining phases and receive opinionated defaults. The choreographer handles this — no runtime-level action needed.
