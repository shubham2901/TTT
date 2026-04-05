# Plan 02-03 Summary — Invocation Matrix & Runtime Index

**Status:** Complete
**Date:** 2026-04-04

## What was done

Created one new file and replaced the existing stub for the runtime index:

1. **`runtime/INVOCATION.md`** (70 lines) — Unified invocation matrix:
   - Table 1: Phase → Agent → Files matrix (11 rows covering all 7 agents + choreographer across all phases)
   - Table 2: Runtime-Specific Invocation (13 rows comparing Cursor vs Claude Code)
   - Shared behavioral contract section (6 non-negotiable behaviors)
   - Vibe it!! path note
   - References to Phase 0 decisions, choreographer, and state schema

2. **`runtime/README.md`** (52 lines, replaced 18-line stub) — Runtime index:
   - Entry points table (Cursor + Claude Code with entry point files and setup guides)
   - Link to INVOCATION.md with description
   - Shared behavior note pointing to Phase 0 decisions
   - Canonical prompts note (never fork prompt content)
   - Future adapters list (Windsurf, VS Code, Codex, claude.ai, Anti Gravity)
   - References section

## Verification

- [x] INVOCATION.md has complete phase→agent→files matrix (11 rows)
- [x] INVOCATION.md has runtime differences table (13 rows)
- [x] Both tables are valid markdown tables
- [x] All prompt file references match actual files in `prompts/`
- [x] References `.cursor/rules/ttt.mdc` and `skills/ttt/SKILL.md`
- [x] runtime/README.md links to cursor/README.md, claude-code/README.md, INVOCATION.md
- [x] runtime/README.md lists future adapters
- [x] runtime/README.md total: 52 lines (target: 40-60)
- [x] Both files are accurate against Plans 01 and 02 outputs
- [x] No file overlap with Plan 01 or Plan 02

## Requirement satisfied

**P2-T3:** Single table maps user action → which prompt file → expected outputs. INVOCATION.md covers all agents, all phases, both runtimes. runtime/README.md serves as complete index to all runtime documentation.
