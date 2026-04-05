# Phase 2: Runtime packaging (Wave 1) - Research

**Researched:** 2026-04-04
**Domain:** AI coding agent runtime packaging (Cursor rules, Claude Code skills, invocation documentation)
**Confidence:** HIGH

## Summary

Phase 2 packages Phase 1's seven canonical prompts into runtime-native entry points for Cursor and Claude Code. The domain is well-understood: both Cursor's `.mdc` rule format and Claude Code's `SKILL.md` format are documented with official specifications. The primary challenge is architectural, not technical — designing wrapper files that activate cleanly, stay out of the way when TTT isn't in use, and avoid duplicating prompt content.

Cursor's runtime offers two complementary mechanisms: `.cursor/rules/*.mdc` files for context injection and `.cursor/agents/*.md` files for subagent delegation. The decided two-layer activation (thin bootstrap rule + glob-activated `ttt.mdc`) maps cleanly onto the "agent-decided" + "auto-attached" rule types. Claude Code's SKILL.md format supports rich features (forked context, subagent preloading, dynamic context injection) but the decided approach — moderate triggers, entry-point with reference loading — is the right level of complexity for Phase 2.

**Primary recommendation:** Build the Cursor wrapper as two `.mdc` files (bootstrap + main) plus optional `.cursor/agents/` subagent definitions. Build the Claude Code wrapper as a single `skills/ttt/SKILL.md` with supporting references to `prompts/`. Write INVOCATION.md as a table-based matrix. Keep all runtime READMEs agent-first, directive, and under 200 lines.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Cursor rule activation & shape
- **Always-on via lightweight trigger + glob**: A small always-on trigger (skill file or thin rule) handles first invocation ("start TTT") before any `ttt/` directory exists. Once `ttt/` is created, `ttt.mdc` activates via glob on the `ttt/` directory — keeps context window clean when TTT isn't in use.
- **Summary + pointer**: `ttt.mdc` contains a condensed overview of phases and flow, then says "load `prompts/choreographer.md` for full instructions." It is NOT a comprehensive standalone document.
- **Split spawn logic**: `ttt.mdc` includes Cursor-specific Task/delegate syntax for spawning subagents. `prompts/choreographer.md` retains runtime-agnostic spawn intent. Both layers exist — Cursor-specific on top, generic underneath.
- **README structure**: `runtime/cursor/README.md` has a quick-start section at top (3–5 steps), then detailed reference below (fallback behaviors, troubleshooting, edge cases).

#### SKILL.md design
- **Trigger breadth**: Moderate — frontmatter triggers on 'TTT', 'product spec', 'product management', 'validate idea'. Not so broad it fires on every "build" or "brainstorm" mention. Not so narrow it only fires on the exact phrase "TTT".
- **Duplication tolerance**: Some duplication of choreographer logic in SKILL.md is acceptable if it makes the Claude Code experience better. SKILL.md doesn't need to stay perfectly in sync with every choreographer change — only structural changes (phase additions, gate changes) require an update.

#### Setup & distribution
- **Three paths available**: Copy files into project, clone the repo, or install as skill. All three documented.
- **Primary path**: Skill install (most native to each runtime). Documented first and most prominently.
- **Update mechanism**: Skill reinstall (primary) + git pull (secondary). Both documented.
- **Repo layout mirrors user layout**: The TTT repo is structured exactly as it would appear in a user's project (`prompts/`, `skills/`, `.cursor/`). Extra files (docs, evals, planning) coexist but the core set is copy-ready.
- **Per-project artifacts**: Each project gets its own `ttt/` folder with its own `ttt_state.json` and artifacts. No central/shared artifact store.
- **Gitignore policy**: User's choice. Document both options (commit for version-controlled specs, gitignore for working files) without enforcing either.
- **Verify installation**: User says "TTT" — if the agent responds with the Clarify phase intro, it's working. No special test command needed.
- **Dependencies**: Web search recommended (Validate phase works best with it). Document graceful degradation without it per Phase 0 decisions.

#### Documentation structure
- **Audience**: AI agent first. READMEs and INVOCATION.md are instruction documents for the agent, not user guides. Writing style should be directive and precise, not explanatory.

### Claude's Discretion
- Coexistence strategy for `ttt.mdc` with other `.cursor/rules/` files
- Level of manual-fallback documentation in Cursor README (detailed step-by-step vs. brief acknowledgment)
- SKILL.md role relative to choreographer (entry-point-only vs. orchestration layer vs. self-contained)
- SKILL.md depth and structure (current draft level vs. more/less)
- INVOCATION.md format (table, flowchart, or hybrid)
- Runtime README role (extras beyond rule/skill files, or pure reference)
- Whether a top-level project README is needed for Phase 2

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

## Standard Stack

This phase produces markdown files, not code. There are no library dependencies. The "stack" is the file formats and conventions of each target runtime.

### Core: Cursor Rule Format (`.mdc`)

**Source:** Cursor official docs (cursor.com/docs), create-rule skill, community forums
**Confidence:** HIGH

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | What the rule does; agent reads this to decide relevance |
| `globs` | string or array | File patterns for auto-attachment (e.g., `ttt/**`) |
| `alwaysApply` | boolean | If `true`, loaded into every conversation |

Four rule types based on frontmatter configuration:

| Type | Configuration | When loaded |
|------|---------------|-------------|
| Always-apply | `alwaysApply: true` | Every conversation |
| Auto-attached | `globs: "pattern"` | When editing files matching the glob |
| Agent-decided | `alwaysApply: false` + description, no globs | When agent determines relevance from description |
| Manual | `alwaysApply: false`, no globs, no description | Only when user references with `@rule-name` |

File location: `.cursor/rules/*.mdc` (project) or `~/.cursor/rules/*.mdc` (global).

### Core: Cursor Subagent Format (`.cursor/agents/`)

**Source:** Cursor official docs (cursor.com/docs/subagents)
**Confidence:** HIGH

Custom subagents are markdown files in `.cursor/agents/` (project) or `~/.cursor/agents/` (global).

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | No | From filename | Display name and identifier |
| `description` | string | No | — | Agent reads this to decide when to delegate |
| `model` | string | No | `inherit` | `fast`, `inherit`, or specific model ID |
| `readonly` | boolean | No | `false` | Restrict write permissions |
| `is_background` | boolean | No | `false` | Run without blocking parent |

Key capabilities:
- Auto-delegation based on description content
- Explicit invocation via `/name` syntax or natural language
- Parallel execution (multiple Task calls in one message)
- Foreground (blocking) and background modes
- Child subagent spawning (since Cursor 2.5)
- Resumable via agent ID

### Core: Claude Code SKILL.md Format

**Source:** Claude Code official docs (code.claude.com/docs/en/skills.md)
**Confidence:** HIGH

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No (uses dir name) | Lowercase, hyphens, max 64 chars. Becomes `/slash-command`. |
| `description` | Recommended | What + when. Front-load key terms. Truncated at 250 chars in listing. |
| `disable-model-invocation` | No | `true` = user-only invocation |
| `user-invocable` | No | `false` = Claude-only (background knowledge) |
| `allowed-tools` | No | Tools granted without per-use approval |
| `model` | No | Model override when skill is active |
| `context` | No | `fork` = run in isolated subagent |
| `agent` | No | Subagent type when `context: fork` (e.g., `Explore`, `Plan`) |
| `paths` | No | Glob patterns for auto-activation |

File locations:
- Project: `.claude/skills/skill-name/SKILL.md`
- Global: `~/.claude/skills/skill-name/SKILL.md`

Key capabilities:
- Auto-invocation based on description matching
- Manual invocation via `/skill-name`
- `$ARGUMENTS` substitution for parameterized invocation
- `` !`command` `` syntax for dynamic context injection (shell preprocessing)
- `context: fork` for subagent isolation
- Supporting files referenced from SKILL.md (progressive disclosure)
- 500-line recommended limit for SKILL.md

### Alternatives Considered

| Instead of | Could use | Tradeoff |
|------------|-----------|----------|
| `.mdc` bootstrap rule | Cursor skill (`.cursor/skills/`) for bootstrap | Skills and rules serve different purposes in Cursor. A skill is a better fit for orchestration workflows. However, the decided approach uses a thin `.mdc` rule for the bootstrap, which is simpler and keeps the activation mechanism uniform. |
| Two `.mdc` files (bootstrap + main) | Single agent-decided `.mdc` with no glob | Would work but loads into context even when user isn't using TTT. The glob-based approach keeps context clean per the locked decision. |
| Separate `.cursor/agents/` files per TTT subagent | All spawn logic inline in `ttt.mdc` | Agent files provide cleaner isolation and auto-delegation. However, since TTT's subagents are dynamically spawned with different prompts per phase, the choreographer handles delegation, not static agent files. Cursor's Task tool with inline prompts is the right mechanism. |

## Architecture Patterns

### Recommended File Structure (Phase 2 deliverables)

```
TTT repo (also mirrors user's project after install):
├── .cursor/
│   └── rules/
│       └── ttt.mdc                    # Glob-activated main rule (summary + pointer)
├── skills/
│   └── ttt/
│       └── SKILL.md                   # Claude Code skill entry point
├── prompts/
│   ├── choreographer.md               # [exists] Full orchestration prompt
│   ├── market_researcher.md           # [exists] Subagent prompt
│   ├── user_researcher.md             # [exists] Subagent prompt
│   ├── product_detailer.md            # [exists] Subagent prompt
│   ├── tech_architect.md              # [exists] Subagent prompt
│   ├── design_advisor.md              # [exists] Subagent prompt
│   └── test_eval_generator.md         # [exists] Subagent prompt
├── runtime/
│   ├── README.md                      # Index with links to runtime-specific docs
│   ├── INVOCATION.md                  # Unified invocation matrix (both runtimes)
│   ├── cursor/
│   │   └── README.md                  # Cursor setup, fallbacks, troubleshooting
│   └── claude-code/
│       └── README.md                  # Claude Code install, testing notes
└── schemas/
    └── ttt_state.example.json         # [exists] State schema reference
```

### Pattern 1: Two-Layer Cursor Activation

**What:** A thin always-on bootstrap handles first-time "TTT" invocation. Once `ttt/` exists, the glob-activated `ttt.mdc` takes over.

**Implementation approach:**

The bootstrap layer can use the **agent-decided** rule type (`alwaysApply: false` + description, no globs). Cursor's agent reads the description and decides when the rule is relevant — this activates on "TTT" mentions without being always-on. This is lighter than `alwaysApply: true` because it only injects the rule content when the agent deems it relevant.

```yaml
# .cursor/rules/ttt.mdc
---
description: >
  TTT (To The T) product management skill. Activates when user mentions TTT,
  product spec, product management, or validate idea. Orchestrates multi-phase
  product specification from idea to coding-agent-ready spec.
globs: ttt/**
alwaysApply: false
---
```

**Key insight:** Cursor's `.mdc` format allows BOTH `globs` and `description` on the same file. With `alwaysApply: false`, the description triggers agent-decided loading AND the glob triggers auto-attachment when `ttt/` files are being edited. This means a **single `.mdc` file can serve both bootstrap and ongoing activation** — the agent-decided path handles first invocation (no `ttt/` yet), and the glob path handles mid-session file edits.

**Recommendation:** Use a single `ttt.mdc` with both `description` and `globs` fields. This eliminates the need for a separate bootstrap file while honoring the locked decision's intent (activate before `ttt/` exists via description, activate on `ttt/` via glob).

### Pattern 2: Summary + Pointer Rule Content

**What:** `ttt.mdc` contains a condensed overview, then directs the agent to load the full choreographer.

**Structure for ttt.mdc body (after frontmatter):**

```markdown
# TTT (To The T)

[1-2 sentence overview]

## Phases
[Condensed 1-line-per-phase summary: CLARIFY → VALIDATE → DEFINE → SPECIFY → LAUNCH]

## How to start
1. Read `prompts/choreographer.md` for full orchestration instructions.
2. Check for existing `ttt/ttt_state.json` — if found, resume from saved state.
3. If fresh start, begin Clarify phase.

## Cursor-specific: Spawning subagents
[Task tool syntax for spawning researcher/specifier agents]
[Fallback: sequential in-context execution with @-file references]

## Key rules
[3-5 non-negotiable rules from choreographer, condensed]
```

**Size target:** Under 80 lines. The mdc format recommends under 50 lines for simple rules, but TTT's orchestration needs justify slightly more. The key is that this replaces a 535-line choreographer load with an ~80-line summary that points to the full prompt only when needed.

### Pattern 3: Cursor-Specific Spawn Syntax

**What:** `ttt.mdc` includes Cursor Task/delegate syntax that sits on top of the choreographer's runtime-agnostic spawn intent.

```markdown
## Spawning subagents (Cursor)

When the choreographer calls for spawning a subagent:

1. Use the Task tool to create a new subagent
2. Pass the subagent's prompt file content as the task description
3. Include input file paths in the task prompt
4. Set the subagent to foreground mode (wait for result)

For parallel agents (Validate phase: Market + User Researcher):
- Launch both Task calls in a single message for parallel execution
- If parallel unavailable, run sequentially with honest progress messaging

Fallback (no Task tool):
- Read the subagent prompt file with @prompts/[agent].md
- Execute the prompt instructions in the current context
- Same quality gates and output expectations apply
```

### Pattern 4: Claude Code SKILL.md as Entry-Point + Light Orchestration

**What:** SKILL.md serves as the entry point and includes enough orchestration context to run TTT phases, while referencing the choreographer for full details.

**Recommended structure:**

```markdown
---
name: ttt
description: Product management for solo builders. Turns a raw idea into a validated product spec. Use when user mentions TTT, product spec, product management, or validate idea.
---

# TTT (To The T)
[Brief overview — what it is, what it produces]

## When to use / When not to use
[Trigger guidance]

## What TTT produces
[Artifact table]

## How it works
[Phase overview with file references]

## Orchestration instructions
Step 1: Load prompts/choreographer.md
Step 2: Resolve artifact root
Step 3: Check for existing state
Step 4: Run phases (with subagent spawn instructions)
Step 5: Validate and assemble

## Subagent prompts
[Table mapping prompt file → agent → when used]

## Runtime notes
[Claude Code-specific behavior]

## Key rules
[Non-negotiable rules, condensed]
```

**Size target:** 150-200 lines. The existing 171-line draft is in range. Evaluate against decisions and adjust.

### Anti-Patterns to Avoid

- **Duplicating choreographer.md into ttt.mdc:** The locked decision says "summary + pointer." Never copy the full 535-line choreographer into the rule file.
- **Making SKILL.md a thin pointer only:** The Claude Code experience benefits from having enough orchestration context inline. A 5-line "go read choreographer.md" would force an extra file load on every invocation.
- **Using `alwaysApply: true` for ttt.mdc:** This wastes context window tokens on every Cursor session, even when TTT isn't in use. The agent-decided + glob combination is strictly better.
- **Runtime-specific logic in prompts/*.md:** The canonical prompts must stay runtime-agnostic. Cursor Task syntax goes in `ttt.mdc`. Claude Code orchestration goes in `SKILL.md`.
- **Overly broad SKILL.md triggers:** Triggering on "build" or "brainstorm" would fire on most coding conversations. The decided moderate breadth (TTT, product spec, product management, validate idea) is correct.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Rule file format | Custom config format | Standard `.mdc` YAML frontmatter | Cursor parses this natively; custom formats won't load |
| Skill activation logic | Custom trigger system | SKILL.md `description` field + Claude Code's built-in matching | The runtime handles matching; custom logic adds failure modes |
| Subagent delegation | Custom subprocess management | Cursor Task tool / Claude Code's native delegation | Both runtimes handle context isolation, tool inheritance, and result return |
| Distribution | Custom installer script | `git clone` + native skill discovery paths | Both runtimes auto-discover from standard directories |

**Key insight:** Phase 2 produces static markdown files that each runtime interprets natively. There is no custom code to write — only content and structure decisions.

## Common Pitfalls

### Pitfall 1: Context Window Bloat from Over-Inclusive Rules
**What goes wrong:** Putting too much content in `ttt.mdc` causes it to consume context on every agent-decided load, leaving less room for the actual work.
**Why it happens:** Temptation to make the rule self-contained to avoid an extra file read.
**How to avoid:** Keep `ttt.mdc` under 80 lines. Use "read `prompts/choreographer.md` for full instructions" as the explicit delegation. The agent loads the choreographer only when actually running TTT.
**Warning signs:** Agent seems slow or forgetful during TTT phases = context pressure.

### Pitfall 2: Glob Pattern Mismatch
**What goes wrong:** The `globs: ttt/**` pattern in `ttt.mdc` doesn't match when the artifact root is `ttt-docs/` or `ttt-artifacts/` (collision fallback from Phase 0).
**Why it happens:** The glob is static in the `.mdc` file, but the artifact root can vary per project.
**How to avoid:** The agent-decided activation (via description) handles this — it fires on "TTT" mentions regardless of the artifact directory name. The glob is a bonus for mid-session file edits, not the primary activation path. Document this explicitly in `runtime/cursor/README.md`.
**Warning signs:** Rule stops auto-loading after TTT uses a fallback artifact root.

### Pitfall 3: SKILL.md Description Truncation
**What goes wrong:** Claude Code truncates SKILL.md descriptions at 250 characters in the skill listing. If key trigger terms are buried past the cutoff, the skill doesn't auto-activate.
**Why it happens:** Claude Code's context budget for skill descriptions is limited (1% of context window, minimum 8000 chars across all skills).
**How to avoid:** Front-load the description: "Product management for solo builders. Turns a raw idea into a validated product spec." Put trigger terms early. Keep description under 200 chars.
**Warning signs:** Skill doesn't activate when user says "TTT" or "product spec."

### Pitfall 4: Stale Spawn Syntax
**What goes wrong:** Cursor's Task tool API or subagent format changes, breaking the spawn instructions in `ttt.mdc`.
**Why it happens:** Both runtimes are actively evolving (Cursor subagents documented as of 2.5+, Claude Code skills format has grown significantly).
**How to avoid:** Keep spawn instructions in `ttt.mdc` minimal and reference-style. Document the fallback path (sequential in-context execution) prominently. Date-stamp the runtime READMEs.
**Warning signs:** "Task tool not found" errors in Cursor, or SKILL.md fields being ignored in Claude Code.

### Pitfall 5: Misaligned File Paths Between Runtimes
**What goes wrong:** Cursor uses `@prompts/choreographer.md` path syntax while Claude Code uses relative paths from skill directory. A single path convention doesn't work for both.
**Why it happens:** Different runtimes resolve file references differently.
**How to avoid:** In `ttt.mdc`, use Cursor's `@` path syntax. In `SKILL.md`, use relative paths from the project root (not from the skill directory). Document the difference in INVOCATION.md.
**Warning signs:** "File not found" when agent tries to load a prompt.

### Pitfall 6: Bootstrap vs. Ongoing Activation Confusion
**What goes wrong:** The bootstrap trigger and the glob-based trigger conflict or double-load, injecting TTT context twice.
**Why it happens:** When both the agent-decided path (description match) and the glob path (`ttt/**`) fire simultaneously.
**How to avoid:** Using a single `.mdc` file with both `description` and `globs` eliminates this — it's one rule loaded once, via whichever path matches first. If using two separate files, the bootstrap should detect `ttt/` existence and defer.
**Warning signs:** Duplicate TTT instructions in agent context.

## Discretion Recommendations

These are areas marked as Claude's Discretion in CONTEXT.md. Research-backed recommendations follow.

### 1. Coexistence Strategy for `ttt.mdc` with Other `.cursor/rules/` Files

**Recommendation:** Namespace by filename, scope by glob.

TTT should use a single `ttt.mdc` file (not multiple `ttt-*.mdc` files). With `alwaysApply: false` and `globs: ttt/**`, it stays out of the way for all non-TTT work. The description-based activation handles "TTT" invocations.

No special coexistence logic needed. Cursor loads rules independently — multiple rules can be active simultaneously without conflict as long as they don't give contradictory instructions for the same files.

**Confidence:** HIGH — verified against Cursor docs on rule loading behavior.

### 2. Manual-Fallback Documentation Level in Cursor README

**Recommendation:** Brief acknowledgment with one concrete fallback pattern.

Cursor 2.5+ supports subagents natively. The Task tool is the expected path. Document the fallback as:

> **If Task tool is unavailable:** Run subagent prompts sequentially in the current context. Read the prompt file with `@prompts/[agent].md`, provide the input files, and execute. Same outputs and quality gates apply. Tell the user which agent runs first.

One paragraph, not a multi-page walkthrough. The fallback is a degraded mode, not a first-class path.

**Confidence:** HIGH — subagent support is well-documented and stable in current Cursor.

### 3. SKILL.md Role Relative to Choreographer

**Recommendation:** Entry-point + light orchestration layer.

The SKILL.md should contain enough context that Claude Code can:
1. Recognize when to activate (description matching)
2. Understand TTT's phase flow at a high level
3. Know to load `prompts/choreographer.md` for full instructions
4. Know how to spawn subagents and reference prompt files
5. Apply key non-negotiable rules (scope guard, quality gates, state persistence)

This means ~150-200 lines of orchestration context, with explicit "read choreographer.md for full phase logic" pointers. Not a self-contained duplicate, not a 5-line stub.

**Confidence:** HIGH — aligns with Claude Code's progressive disclosure pattern (SKILL.md as overview, supporting files for detail).

### 4. SKILL.md Depth and Structure

**Recommendation:** The existing 171-line draft is close to the right depth. Adjust to match the CONTEXT.md decisions:

Changes needed from current draft:
- Update trigger terms in frontmatter description to match decided moderate breadth
- Ensure orchestration instructions reference prompt files by relative path from project root
- Add Claude Code-specific notes on subagent execution (sequential is OK, honest progress messaging)
- Verify "when to use" / "when not to use" aligns with decided trigger breadth
- Ensure key rules section includes the non-negotiables from choreographer

The current draft's structure (overview → what it produces → how it works → orchestration → subagent prompts → runtime notes → key rules) is sound.

**Confidence:** HIGH — evaluated existing draft against CONTEXT.md decisions and Claude Code SKILL.md best practices.

### 5. INVOCATION.md Format

**Recommendation:** Table-based matrix.

A table is the most agent-parseable format. Agents can scan rows/columns quickly. Flowcharts require visual interpretation that LLMs handle less reliably.

Structure:

```markdown
# Invocation Matrix

## Phase → Agent → Files

| Phase | Agent | Prompt File | Input Files | Output File | Parallel? |
|-------|-------|-------------|-------------|-------------|-----------|
| Clarify | Choreographer | choreographer.md | (user input) | clarification.md | N/A |
| Validate | Market Researcher | market_researcher.md | clarification.md | market_research.md | Yes (with User Researcher) |
| ... | ... | ... | ... | ... | ... |

## Runtime-Specific Invocation

| Action | Cursor | Claude Code |
|--------|--------|-------------|
| Start TTT | Say "TTT" in Agent chat | Say "TTT" or `/ttt` |
| Load choreographer | Agent reads via @-path | Agent reads via relative path |
| Spawn subagent | Task tool (foreground) | Sequential in-context or context:fork |
| ... | ... | ... |
```

**Confidence:** HIGH — table format is standard for cross-reference documentation aimed at AI agents.

### 6. Runtime README Role

**Recommendation:** Pure reference — setup, verification, fallbacks, troubleshooting, edge cases.

The rule file (`ttt.mdc`) and skill file (`SKILL.md`) carry the operational instructions. READMEs should NOT duplicate orchestration logic. They should cover:

- **Quick-start:** 3-5 steps to get TTT working (per locked decision)
- **Verification:** "Say TTT. If Clarify phase starts, it's working."
- **Fallback behaviors:** What happens when Task tool / web search is unavailable
- **Troubleshooting:** Common issues and fixes
- **Edge cases:** Artifact root collision, context window limits, session resume after crash

Target: 100-150 lines per README. Agent-first writing style.

**Confidence:** HIGH — follows the locked decision that docs are for the agent, not the user.

### 7. Top-Level Project README

**Recommendation:** Yes, create a minimal one.

The TTT repo needs a README.md at root for:
- Repo discoverability (GitHub, cloning)
- Directing users to the right runtime entry point
- Listing the three installation paths (skill install > clone > copy)

Keep it under 60 lines. Not an exhaustive guide — a signpost.

**Confidence:** MEDIUM — not strictly required for Phase 2 function, but standard practice for any distributable repo.

## Code Examples

### Example 1: Complete `ttt.mdc` Frontmatter

```yaml
---
description: >
  TTT (To The T) product management skill for solo builders. Activates when
  user mentions TTT, product spec, product management, or validate idea.
  Orchestrates idea → validated spec across five phases (Clarify, Validate,
  Define, Specify, Launch). Read prompts/choreographer.md for full instructions.
globs: ttt/**
alwaysApply: false
---
```

This uses agent-decided activation (description-based) for first-time invocation and glob-based auto-attachment for mid-session `ttt/` file edits. `alwaysApply: false` keeps it out of non-TTT conversations.

### Example 2: Claude Code SKILL.md Frontmatter

```yaml
---
name: ttt
description: >
  Product management for solo builders. Turns a raw idea into a complete,
  validated product spec before code is written. Use when user says TTT,
  product spec, product management, or validate idea.
---
```

Description is 178 characters — under the 250-char truncation limit. Front-loads the key use case. Trigger terms are in the first two sentences.

### Example 3: Task Tool Spawn Instruction (for ttt.mdc)

```markdown
## Spawning subagents

When a phase requires subagent work:

1. Read the agent's prompt file (e.g., `prompts/market_researcher.md`)
2. Use the Task tool to spawn a foreground subagent with:
   - The prompt file content as the system instruction
   - Input file paths listed explicitly in the task description
   - Expected output filename stated
3. Validate the returned output against quality gates in choreographer.md
4. If validation fails, retry with feedback (max 3 attempts)

For parallel spawns (e.g., Validate phase):
- Issue multiple Task tool calls in a single response
- Both agents run simultaneously

Fallback (Task tool unavailable):
- Read prompt file content inline with @prompts/[agent].md
- Execute sequentially in current context
- Same outputs and quality expectations apply
```

### Example 4: Cursor Subagent File (optional, for enhanced delegation)

```yaml
---
name: ttt-researcher
description: >
  TTT research subagent. Use when the TTT choreographer needs market or user
  research. Reads researcher prompt files and executes research with web search.
model: inherit
---

You are a TTT research subagent. Your task will specify which researcher role
to take (Market Researcher or User Researcher) and provide the prompt file
content and input files.

Follow the prompt instructions exactly. Return the complete research output.
If web search is unavailable, keep full section structure with "N/A" notes
and escalate to the user.
```

Note: This is OPTIONAL. The choreographer can spawn Task tool calls with inline prompts without pre-defined agent files. Agent files add auto-delegation but aren't required.

## State of the Art

| Old Approach (Pre-2026) | Current Approach (2026) | When Changed | Impact |
|--------------------------|-------------------------|--------------|--------|
| `.cursorrules` single file | `.cursor/rules/*.mdc` multi-file | Late 2024 | Focused, scoped rules instead of monolithic config |
| No subagent support in Cursor | `.cursor/agents/` + Task tool | Cursor 2.5 (2025-2026) | Native subagent delegation with context isolation |
| Claude Code commands (`.claude/commands/`) | Skills (`.claude/skills/`) | 2025-2026 | Skills support subagent execution, progressive disclosure, dynamic context |
| Basic SKILL.md (name + description) | Rich frontmatter (`context`, `agent`, `paths`, `allowed-tools`, etc.) | 2026 | Skills can fork into subagents, restrict tools, inject dynamic context |

**Deprecated/outdated:**
- `.cursorrules` (single file): Migrated to `.cursor/rules/*.mdc`. Legacy files still work but shouldn't be used for new projects.
- `.claude/commands/`: Merged into skills system. Files at `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` are equivalent. Skills recommended for new development.

## Open Questions

1. **Cursor skill vs rule for bootstrap**
   - What we know: The decision says "skill file or thin rule" for the bootstrap layer. Cursor supports both `.cursor/skills/` and `.cursor/rules/`.
   - What's unclear: Whether a skill-based bootstrap would provide better auto-activation than an agent-decided rule.
   - Recommendation: Use a single `.mdc` rule with both description and globs. A Cursor skill would add a second entry point that could conflict with Claude Code's `skills/ttt/SKILL.md` namespace. Keeping Cursor's entry in `.cursor/rules/` and Claude Code's in `skills/ttt/` provides clean separation.

2. **Cross-runtime skill namespace collision**
   - What we know: Cursor discovers skills from `.claude/skills/` for compatibility. The TTT repo has `skills/ttt/SKILL.md` (intended for Claude Code).
   - What's unclear: Whether Cursor will auto-load `skills/ttt/SKILL.md` alongside `ttt.mdc`, causing duplicate activation.
   - Recommendation: Test this during implementation. If collision occurs, the `ttt.mdc` description-based activation should take precedence. Document the behavior in `runtime/cursor/README.md`. The existing SKILL.md at `skills/ttt/` (not `.claude/skills/ttt/`) may not be auto-discovered by Cursor since it's not in the standard Cursor skill path.

3. **SKILL.md path references**
   - What we know: SKILL.md references prompt files by relative path. The decision says "reference prompt files by relative path."
   - What's unclear: Whether Claude Code resolves paths relative to the SKILL.md location (`skills/ttt/`) or relative to the project root.
   - Recommendation: Use project-root-relative paths (e.g., `prompts/choreographer.md`, not `../../prompts/choreographer.md`). Claude Code skills run with the project root as working directory. Test during implementation and document in `runtime/claude-code/README.md`.

## Sources

### Primary (HIGH confidence)
- Cursor official docs: `cursor.com/docs/subagents` — Subagent format, Task tool, configuration fields, execution modes
- Claude Code official docs: `code.claude.com/docs/en/skills.md` — SKILL.md format, frontmatter fields, invocation control, supporting files, dynamic context
- Cursor rules format: `cursor.com/docs/context/rules` (via WebSearch) — `.mdc` frontmatter fields, four rule types, glob patterns
- Existing project files: `skills/ttt/SKILL.md` (171 lines), `prompts/choreographer.md` (535 lines), `docs/PHASE0_DECISIONS.md`, `PHASE_PLAN.md`
- `create-rule` skill: `~/.cursor/skills-cursor/create-rule/SKILL.md` — Rule format reference, best practices
- `create-skill` skill: `~/.cursor/skills-cursor/create-skill/SKILL.md` — Skill format reference, authoring principles

### Secondary (MEDIUM confidence)
- Cursor community forum: `forum.cursor.com/t/rule-frontmatter-format/146274` — Frontmatter format discussions
- localskills.sh: "The Complete Guide to Cursor Rules in 2026" — Rule type taxonomy
- skillsdirectory.com: "Installing Skills" — Claude Code skill installation methods

### Tertiary (LOW confidence)
- Medium article on Cursor subagents (March 2026) — Community guide, may not reflect latest changes

## Metadata

**Confidence breakdown:**
- Standard stack (file formats): HIGH — verified against official Cursor and Claude Code documentation
- Architecture (file structure, activation patterns): HIGH — combines official docs with locked decisions from CONTEXT.md
- Pitfalls: HIGH — derived from documented format constraints and real limitations
- Discretion recommendations: HIGH to MEDIUM — recommendations are well-grounded but implementation will validate

**Research date:** 2026-04-04
**Valid until:** 2026-05-04 (30 days — both runtimes are stable but actively evolving)
