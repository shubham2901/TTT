# Phase 2: Runtime packaging (Wave 1) - Context

**Gathered:** 2026-04-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Package Phase 1's seven canonical prompts into runtime-native entry points for Cursor and Claude Code. Produce `.cursor/rules/ttt.mdc`, `skills/ttt/SKILL.md`, runtime READMEs, and `runtime/INVOCATION.md`. No prompt content changes — wrappers only. Wave 2/3 runtimes (Windsurf, VS Code, Codex, claude.ai) are out of scope.

</domain>

<decisions>
## Implementation Decisions

### Cursor rule activation & shape
- **Always-on via lightweight trigger + glob**: A small always-on trigger (skill file or thin rule) handles first invocation ("start TTT") before any `ttt/` directory exists. Once `ttt/` is created, `ttt.mdc` activates via glob on the `ttt/` directory — keeps context window clean when TTT isn't in use.
- **Summary + pointer**: `ttt.mdc` contains a condensed overview of phases and flow, then says "load `prompts/choreographer.md` for full instructions." It is NOT a comprehensive standalone document.
- **Split spawn logic**: `ttt.mdc` includes Cursor-specific Task/delegate syntax for spawning subagents. `prompts/choreographer.md` retains runtime-agnostic spawn intent. Both layers exist — Cursor-specific on top, generic underneath.
- **README structure**: `runtime/cursor/README.md` has a quick-start section at top (3–5 steps), then detailed reference below (fallback behaviors, troubleshooting, edge cases).

### SKILL.md design
- **Trigger breadth**: Moderate — frontmatter triggers on 'TTT', 'product spec', 'product management', 'validate idea'. Not so broad it fires on every "build" or "brainstorm" mention. Not so narrow it only fires on the exact phrase "TTT".
- **Duplication tolerance**: Some duplication of choreographer logic in SKILL.md is acceptable if it makes the Claude Code experience better. SKILL.md doesn't need to stay perfectly in sync with every choreographer change — only structural changes (phase additions, gate changes) require an update.

### Setup & distribution
- **Three paths available**: Copy files into project, clone the repo, or install as skill. All three documented.
- **Primary path**: Skill install (most native to each runtime). Documented first and most prominently.
- **Update mechanism**: Skill reinstall (primary) + git pull (secondary). Both documented.
- **Repo layout mirrors user layout**: The TTT repo is structured exactly as it would appear in a user's project (`prompts/`, `skills/`, `.cursor/`). Extra files (docs, evals, planning) coexist but the core set is copy-ready.
- **Per-project artifacts**: Each project gets its own `ttt/` folder with its own `ttt_state.json` and artifacts. No central/shared artifact store.
- **Gitignore policy**: User's choice. Document both options (commit for version-controlled specs, gitignore for working files) without enforcing either.
- **Verify installation**: User says "TTT" — if the agent responds with the Clarify phase intro, it's working. No special test command needed.
- **Dependencies**: Web search recommended (Validate phase works best with it). Document graceful degradation without it per Phase 0 decisions.

### Documentation structure
- **Audience**: AI agent first. READMEs and INVOCATION.md are instruction documents for the agent, not user guides. Writing style should be directive and precise, not explanatory.

### Claude's Discretion
- Coexistence strategy for `ttt.mdc` with other `.cursor/rules/` files
- Level of manual-fallback documentation in Cursor README (detailed step-by-step vs. brief acknowledgment)
- SKILL.md role relative to choreographer (entry-point-only vs. orchestration layer vs. self-contained)
- SKILL.md depth and structure (current draft level vs. more/less)
- INVOCATION.md format (table, flowchart, or hybrid)
- Runtime README role (extras beyond rule/skill files, or pure reference)
- Whether a top-level project README is needed for Phase 2

</decisions>

<specifics>
## Specific Ideas

- First-run experience matters: TTT needs to activate even before `ttt/` exists (user's first "TTT" invocation). A lightweight always-on trigger handles this bootstrap, then the glob-based rule takes over.
- Skill install as primary distribution — aligns with how both Cursor and Claude Code natively discover capabilities.
- "Just say TTT" as the verification test — zero friction, immediate feedback.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 02-runtime-packaging-wave-1*
*Context gathered: 2026-04-04*
