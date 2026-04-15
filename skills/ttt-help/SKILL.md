---
name: ttt-help
description: List TTT slash commands and what each does.
---

# /ttt-help

## Description

Shows available TTT commands for the installed skill pack.

## Usage

`/ttt-help`

## What it does

Output the command reference below (you may add one line on how skills are installed: `ttt` CLI / `npx to-the-t` from the package `to-the-t`).

## Prompt

Reply with this table (markdown). Do not add unrelated tooling.

| Command | What it does |
|--------|----------------|
| `/ttt-new-idea` | Full flow: clarify → research → plan → handoff (max 5 V1 features). |
| `/ttt-vibe-it` | Fast mode: I take explicit assumptions; provide research, plan, handoff quickly without full research. |
| `/ttt-resume` | Continue from `ttt_state.json` and existing files in `{artifact_root}/`. |
| `/ttt-help` | This reference. |

**Artifacts:** Defaults live under `ttt/` (see `ttt_state.json` → `session.artifact_root`). **State + schema:** `ttt_state.json` — see `schemas/ttt_state.schema.json` in the package.

**Pairing:** TTT is *what* to build; use your execution system (e.g. GSD) for *how* to build.
