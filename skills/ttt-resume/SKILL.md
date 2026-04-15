---
name: ttt-resume
description: Resume a TTT session from ttt_state.json and existing artifacts.
---

# /ttt-resume

## Description

Continues the TTT flow from saved state: reads `{artifact_root}/ttt_state.json`, loads completed files, and picks up at `current.phase` / `current.status`.

## Usage

`/ttt-resume` in a project that already has TTT outputs (typically under `ttt/`).

## What it does

1. **Resolve artifact root** — From `session.artifact_root` in `ttt_state.json`, or default `ttt/` (then fallbacks per main choreographer if missing).
2. **Load state** — Read `ttt_state.json` fully once; do not dump raw JSON to the user.
3. **Load artifacts** — Read only what you need for the next step: e.g. `research.md` if entering plan, `plan.md` if finishing handoff.
4. **Continue** — Follow the same rules as the main choreographer (`skills/ttt-new-idea`) for tone, max 2 questions, file formats, plan lock, and optional screens/tests.
5. **Update state** — After each significant step, update `ttt_state.json` (phases, current, decisions, session timestamps).

## Output

Updates existing files and `ttt_state.json`; may create missing deliverables (e.g. complete `handoff.md`).

## Integration

- Full orchestration and templates: **`skills/ttt-new-idea`** (`## Prompt` choreographer body) when behavior is not specified here.
- Research subagent: `ttt/agents/researcher.md` when resuming into or redoing **research**.

## Prompt

You are **TTT resume mode**.

1. Locate `ttt_state.json` at `{artifact_root}/ttt_state.json` where `{artifact_root}` is `session.artifact_root` from state if the file exists at that path; otherwise try `ttt/ttt_state.json`, `ttt-docs/ttt_state.json`, `ttt-artifacts/ttt_state.json` in order. If none exist, say you cannot resume and suggest `/ttt-new-idea`.

2. Read `current.phase` and `phases.*.status` to decide **what's next**:
   - **understand** not complete → continue Part 1 (clarify idea) per choreographer.
   - **research** not complete → run researcher agent with `ttt/agents/researcher.md` unless user previously skipped; then present findings per choreographer Part 2.
   - **plan** not complete → continue Part 3; write or update `plan.md`.
   - **handoff** not complete → Part 4; write `handoff.md`.

3. **Tone:** Same as choreographer — plain language, no internal phase names to the user, no narrating file operations.

4. **Backup:** If regenerating a file that already exists, move prior version to `{artifact_root}/_backup/<timestamp>/` per choreographer.

5. **Questions:** Max 2 per turn; orient the user briefly ("Here's where we left off: …") then ask only what's blocking the next step.

6. Always refresh `session.last_active` and relevant `current` fields when you finish a turn that changes progress.
