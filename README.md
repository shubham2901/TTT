# TTT (To The T)

**The PM you never hired. For solo vibe coders who ship fast and want to ship right.**

You have an idea. You open Cursor. Three weeks later you realize the market has 50 competitors, your user was wrong, and you built 12 features when you needed 3.

TTT fixes that. One command. A conversation. You get back a validated spec your coding agent can build from.

```
npx to-the-t@latest
```

---

## The Problem

The beginning is easy. The end is hard.

You describe what you want, AI generates code, and the first few prompts create something that looks real. Then you hit production. The database schema is wrong. Nobody actually wants what you built. You spent a month on the wrong thing.

Tools like [GSD](https://github.com/gsd-build/get-shit-done) solve the "how do I build reliably" problem — it keeps your coding agent on track and prevents context rot.

Nothing solves the "should I build this at all" problem. **TTT does.**

Use TTT to figure out **what** to build. Use GSD to build it **reliably**.

---

## How It Works

You talk. TTT asks sharp questions, researches the market, pushes back on weak ideas, and hands you files your coding agent can start from.

### 1. Understand

You describe your idea. TTT narrows it.

```
You:  "AI tool for creators"
TTT:  "That's vague. There are 50+ creator tools. YouTube? Instagram?
       What kind of creators? What's their actual pain?"
You:  "YouTube creators who want to make Shorts from long videos"
TTT:  "Better. Indie creators under 10K subs, or established ones?"
```

Max 2 questions per turn. No walls of text. TTT gets what it needs and moves on.

### 2. Research

TTT researches competitors and users. Names real products — not vague categories. Finds what people actually complain about on Reddit and in app reviews. Checks timing.

Then gives you a straight answer:

```
TTT:  "The space has 4 direct competitors. Two are bloated. One is
       expensive. Nobody targets indie creators under 10K subs.
       Timing is good — YouTube Shorts API just opened up.

       (a) Build as planned
       (b) Narrow to education creators (strongest whitespace)
       (c) Different direction — tell me"
```

If the idea is bad, TTT says so. It won't carry a flawed premise into a spec just to be nice.

### 3. Plan

Lock in exactly who, exactly what problem, exactly what to build first.

TTT enforces a scope guard. **Maximum 5 features for v1.** Every feature must solve a real user problem. Everything else gets parked for v2.

```
TTT:  "That's 7 features. For a solo vibecoder shipping in 2 weeks,
       5 is the ceiling. Which 2 are we parking?"
```

TTT also flags things you'd forget: content operations burden, app store risks, legal issues, realistic cost estimates. When you're ready, say **"lock it"** and get a plain-English summary of the locked plan.

### 4. Handoff

TTT generates everything your coding agent needs to start building: stack choices (named and explained), folder structure, build order, design direction, and an explicit list of what NOT to build.

Hand `handoff.md` to Cursor, Claude Code, Lovable, or whatever you use. Start coding.

---

## Vibe It

Don't want the full process? Say **"you decide"** after the first step and TTT makes all remaining decisions for you.

It picks the most attractive market angle, the sharpest problem, and the smallest viable solution. States every assumption upfront. Generates all files immediately.

Speed over depth. You can always revise after.

---

## What You Get

```
ttt/
  ttt_state.json    # Session state — resume anytime
  research.md       # Competitors, user behavior, gaps, timing
  plan.md           # Who, what, why, v1 scope, tech, design
  handoff.md        # Everything your coding agent needs to start
```

**Optional** (only if you ask):

```
  screens.md        # Screen-by-screen descriptions
  tests.md          # Acceptance tests per feature
  summary.md        # Plain-English summary (say "save summary")
```

Every file is human-readable and coding-agent-ready.

---

## Install

```bash
npx to-the-t@latest
```

The installer asks two things:
1. **Runtime** — Claude Code, Cursor, or Windsurf
2. **Scope** — This project only, or global (all projects)

That's it. TTT copies skills and commands into the right places.

```bash
# Non-interactive examples
npx to-the-t --yes --project .              # All runtimes, local
npx to-the-t --claude --global --yes        # Claude Code, global
npx to-the-t --cursor --local --yes         # Cursor, local
```

### What gets installed

| Source | Destination |
|--------|------------|
| Skills (`ttt-*`) | `.claude/skills/`, `.cursor/skills/`, or `.windsurf/skills/` |
| Commands | `.claude/commands/ttt/` (Claude Code only) |
| Research agent | `ttt/agents/` (project) |
| State schema | `schemas/` (project) |

---

## Commands

| Command | What it does |
|---------|-------------|
| `/ttt-new-idea` | Full flow: understand → research → plan → handoff |
| `/ttt-vibe-it` | Fast mode. TTT decides everything. Get files immediately. |
| `/ttt-resume` | Pick up where you left off (reads `ttt_state.json`) |
| `/ttt-help` | Show commands |

---

## What Makes TTT Different

**It says no.** Most tools validate everything. TTT will tell you your idea is weak before you waste a month on it.

**Plain language.** No jargon during brainstorming. When tech decisions happen (plan and handoff only), every term gets a one-line explanation: "**Flutter** — one codebase for both Android and iPhone so you don't build two apps."

**Scope guard with teeth.** 5 features max for v1. TTT pushes back if you try to add more. Deferred features go to a v2 parking lot, not into the void.

**Flags what you'd forget.** Content operations, legal risks, app store gotchas, realistic cost estimates. The stuff that kills weekend projects three weeks in.

**State survives context clears.** `ttt_state.json` tracks every decision. Close the session, come back tomorrow, `/ttt-resume` picks up where you left off.

**Pivots without starting over.** Change direction and TTT keeps what's still valid. Same market, different angle? Keep the research, redo the plan.

---

## TTT + GSD

They're complementary. **TTT is the product manager. GSD is the program manager.**

| | TTT | GSD |
|---|---|---|
| **Answers** | What should I build? | How do I build it reliably? |
| **When** | Before you write code | While you write code |
| **Output** | Validated spec | Working software |
| **Prevents** | Building the wrong thing | Code falling apart at scale |

```
Your idea
    │
    ▼
  TTT → Validated spec (research, plan, handoff)
    │
    ▼
  Hand handoff.md to your coding agent
    │
    ▼
  GSD → Reliable execution
```

You can use either one independently. But together: right spec **and** reliable execution.

---

## Who This Is For

Solo vibe coders who:
- Have ideas but keep building the wrong thing
- Ship fast but want to ship **right**
- Don't want to play enterprise PM theater
- Want honest feedback, not validation

If you open Cursor before thinking through whether the idea is good — TTT is for you.

---

## Philosophy

**Respect the builder's momentum.** Every question must earn its place. Done and useful beats complete and bloated.

**Be honest.** If the data is weak, say so. If the idea is bad, say so. If an assumption was made, state it.

**Be opinionated.** TTT recommends one option, explains why, and lets you override.

**Protect v1.** Solo builders overbuild. TTT aggressively recommends the smallest viable version. Good ideas that aren't essential get parked, not lost.

---

## Status

v0.1.0 — published and functional. Skills, commands, research agent, and state management are shipped. Under active development.

---

## License

MIT

---

**Your coding agent is powerful. TTT makes sure it builds the right thing.**
