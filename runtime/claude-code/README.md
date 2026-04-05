# TTT — Claude Code Runtime

Claude Code runtime entry point for TTT (To The T). This document covers installation, activation, execution model, and troubleshooting.

---

## Quick-start

1. Install TTT as a skill (see Installation below).
2. Start a Claude Code session in a project directory.
3. Say "TTT" or use `/ttt` — the skill activates from description matching.
4. If the agent responds with the Clarify phase intro, TTT is working.
5. If resuming: the agent reads `ttt/ttt_state.json` and picks up where you left off.

---

## Installation

### Method 1: Skill install (recommended)

Copy `skills/ttt/SKILL.md` and the `prompts/` directory into your project. Claude Code auto-discovers skills from `skills/` or `.claude/skills/`. Ensure `prompts/` and `schemas/` directories are present at project root.

```
your-project/
  skills/ttt/SKILL.md
  prompts/
    choreographer.md
    market_researcher.md
    user_researcher.md
    product_detailer.md
    tech_architect.md
    design_advisor.md
    test_eval_generator.md
  schemas/
    ttt_state.example.json
```

### Method 2: Clone the repo

```bash
git clone <repo-url>
```

The repo layout mirrors the expected user layout. All paths resolve from project root.

### Method 3: Manual copy

Copy these into your project, preserving directory structure:

- `skills/ttt/SKILL.md`
- `prompts/` (all 7 prompt files)
- `schemas/ttt_state.example.json`

---

## How activation works

Claude Code reads the `SKILL.md` description field to decide relevance to the current conversation.

**Triggers:** "TTT", "To The T", "product spec", "product management", "validate idea".

**Manual invocation:** `/ttt` slash command.

**Auto-invocation:** Claude Code activates the skill when it determines the description matches user intent — no explicit command needed.

---

## Subagent execution

SKILL.md instructs the agent to load `prompts/choreographer.md` as the orchestrator. The Choreographer manages all phase logic and spawns subagent prompts as needed.

**Subagent prompts** live in `prompts/`. The Choreographer determines when to invoke each one based on the current phase.

**Execution model:**

- If `context: fork` is available, use it for subagent isolation. Each subagent runs in its own context with its prompt file loaded.
- If `context: fork` is unavailable, run subagent prompts sequentially in the current context.
- Sequential execution produces identical output files and meets the same quality gates.
- Use honest progress messaging: tell the user which agent runs first ("Running Market Researcher first, then User Researcher").

---

## Web search

Web search is recommended for the Validate phase. Market Researcher and User Researcher produce stronger output with live data.

**Graceful degradation:** If web search is unavailable or blocked:

- Keep full section structure; mark missing data as "N/A — web search unavailable".
- Escalate to user after one search-blocked failure. Do not burn retries on repeated search failures.
- User can paste sources, switch environment, or acknowledge skipping Validate.

---

## Updating

**Primary:** Reinstall the skill — copy updated `skills/ttt/SKILL.md` and `prompts/` files over existing ones.

**Secondary:** `git pull` if using the clone method.

Only structural changes to TTT require `SKILL.md` updates. Prompt file updates take effect immediately on next run.

---

## Verification

After installation, verify the setup:

1. Say "TTT" in a Claude Code session. If the Clarify phase intro appears, the skill is working.
2. Check that `prompts/choreographer.md` is readable from the project root.
3. Verify `schemas/ttt_state.example.json` is accessible.

---

## Troubleshooting

**Skill not activating:**
- Confirm `skills/ttt/SKILL.md` exists and the description field is intact.
- Ensure the file is in `skills/` or `.claude/skills/` where Claude Code discovers skills.

**Path errors during execution:**
- Ensure `prompts/` directory is at the project root, not nested inside another directory.
- All prompt file references in SKILL.md use project-root-relative paths.

**Missing prompts:**
- Verify all 7 prompt files exist in `prompts/`: `choreographer.md`, `market_researcher.md`, `user_researcher.md`, `product_detailer.md`, `tech_architect.md`, `design_advisor.md`, `test_eval_generator.md`.

**State file issues:**
- If `ttt/ttt_state.json` is corrupted, delete it to force a fresh start.
- Reference `schemas/ttt_state.example.json` for the expected state schema.
