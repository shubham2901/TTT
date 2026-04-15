# TTT — User guide (skill + plugin)

TTT (To The T) turns a vague product idea into **research**, a locked **plan**, and a **handoff** your coding agent can build from.

## Install

From a clone of this repository:

```bash
node bin/install.js
# or, after `npm link` / global install of the `to-the-t` package:
ttt
```

Non-interactive examples:

```bash
# Local project (current directory): Claude + Cursor + Windsurf skill dirs + project files
ttt --yes --project .
node bin/install.js --yes --project .

# Claude Code only, global skills
ttt --claude --global --yes

# Cursor only, project-local
ttt --cursor --local --yes --project /path/to/app
```

After publish to npm:

```bash
npx to-the-t --yes --project .
```

### What gets copied

| Source | Destination (typical) |
|--------|------------------------|
| `skills/ttt-*/` | `.claude/skills/`, `.cursor/skills/`, `.windsurf/skills/` (per flags) |
| `commands/ttt/*.md` | `.claude/commands/ttt/` (Claude only) |
| `agents/*.md` | `ttt/agents/` (project) |
| `schemas/*.json` | `schemas/` (project) |

Optional `--with-prompts` also copies `prompts/` and `.cursor/rules/ttt.mdc` for legacy Cursor rule workflows (installer flag `--with-prompts`; include `prompts` in your project if you copy manually).

## Commands

| Command | What it does |
|--------|----------------|
| `/ttt-new-idea` | Full flow: clarify → research → plan → handoff (max 5 V1 features). |
| `/ttt-vibe-it` | Fast mode: explicit assumptions; ships research, plan, handoff quickly without full research. |
| `/ttt-resume` | Continue from `ttt_state.json` and existing files under `{artifact_root}/`. |
| `/ttt-help` | Show this command list. |

## Run

1. Open your project in **Cursor** or **Claude Code** (or **Windsurf** if you use that skill path).
2. Invoke a slash command above (e.g. **`/ttt-new-idea`**) or say **TTT** / **To The T** / **product spec** so the skill matches.
3. Follow the conversation. The choreographer prompt in `skills/ttt-new-idea/SKILL.md` drives behavior for the main flow.
4. Research uses **`ttt/agents/researcher.md`** (installed path) or **`prompts/researcher.md`** in the repo.

## State file

- **JSON Schema:** `schemas/ttt_state.schema.json` — validate `ttt_state.json` in tooling if you want.
- **Example:** `schemas/ttt_state.example.json` — sample populated session.

## Outputs

Under `{artifact_root}` (usually `ttt/`):

- `ttt_state.json` — progress and decisions
- `research.md`, `plan.md`, `handoff.md` — core files
- Optional: `screens.md`, `tests.md`, `summary.md` (see skill prompt)

## Pairing with GSD

TTT is **what** to build; [GSD](https://github.com/gsd-build/get-shit-done) is **how** to execute plans. Use TTT first, then hand `handoff.md` to your builder workflow.
