# TTT (TO THE T)

**Get the right spec the first time. Then build it reliably.**

You know the feeling. You have an idea, you open Cursor, and three weeks later you realize you built the wrong thing. The market has 50 competitors, your user was wrong, or you shipped 12 features when you needed 3.

TTT fixes that. It's the product manager you never hired — for solo vibecoders who ship fast and want to ship right.

```
npx to-the-t@latest
```

---

*"I had the idea on Monday, TTT killed it by Tuesday, suggested something better by Wednesday, and I was coding by Thursday."*

---

## The Problem

The beginning is easy. The end is hard.

Every vibecoder knows this. You describe what you want, AI generates code, and the first few prompts create something that looks real. Then you hit production. Authentication breaks. The database schema is wrong. You realize nobody actually wants what you built.

Tools like **GSD** solve the "how do I build reliably" problem. GSD is your **program manager** — it keeps Claude on track, prevents context rot, and makes sure your code doesn't fall apart.

But nothing solves the "should I build this at all" problem.

**TTT is your product manager.** It answers the questions you skip: *Is this idea good? Who's the user? What's the smallest thing I can ship that people actually want?*

Use TTT to figure out **what** to build. Use GSD to build it **reliably**.

```
Your idea
    │
    ▼
  TTT → Validated spec (13 files)
    │
    ▼
  GSD → Reliable execution
    │
    ▼
  You → Ship something people actually want
```

---

## How It Works

One command. Five phases. You talk, TTT thinks, argues back, researches, and hands you files your coding agent can build from.

### 1. Clarify

You describe your idea. TTT narrows it until it's actually specific.

```
You:  "AI tool for creators"
TTT:  "That's vague. There are 50+ creator tools. YouTube? Instagram? 
       What kind of creators? What's their actual pain?"
You:  "YouTube creators who want to make Shorts from long videos"
TTT:  "Better. Indie creators under 10K subs, or established ones?"
```

Most vibecoders skip this. They jump straight to building. Three weeks later they realize they built for the wrong person.

### 2. Validate

TTT spawns two research agents in parallel:

**Market Researcher** — Analyzes competitors, finds whitespace, checks timing. Uses real frameworks (Porter's Five Forces, SWOT, Business Model Canvas), not vibes.

**User Researcher** — Maps user needs, identifies core desires, builds Jobs To Be Done with functional + emotional layers.

Then TTT gives you a straight answer:

```
TTT:  "The space has 4 direct competitors. Two are bloated. One is 
       expensive. Nobody is targeting indie creators under 10K subs. 
       Timing is good — YouTube Shorts API just opened up.

       Your call:
       1. Build as-is
       2. Narrow to creators in education niche (strongest whitespace)
       3. Pivot to thumbnail generation (highest-pain job)
       4. Your own direction"
```

If the idea is bad, TTT says so. It won't carry a flawed premise into a spec just to be nice.

### 3. Define

Lock in exactly who, exactly what problem, and exactly what solution.

TTT enforces a scope guard here. **Maximum 5 features for v1.** Every feature must map to a real user job. Everything else gets parked for v2.

```
TTT:  "That's 7 features. For a solo vibecoder shipping in 2 weeks, 
       5 is the ceiling. Which 2 are we parking for v2?"
```

This is where most weekend projects die — not from lack of skill, but from trying to build everything at once. TTT won't let you do that.

### 4. Specify

TTT spawns 4 agents in two waves:

**Wave 1:** Product Detailer maps every user journey, specifies every feature with edge cases, builds a screen inventory, defines all states (empty, loading, error, success).

**Wave 2 (parallel):** Tech Architect picks the exact stack with rationale. Design Advisor creates UX philosophy and component system. Test Generator writes acceptance tests for every feature.

Then TTT runs a completeness check. Every feature has tests? Every screen has design guidance? No scope leak? It catches drift before you see the output.

### 5. Launch Plan (optional)

Distribution, metrics, v2 triggers. Skip it if you just want to ship.

---

## Vibe It

Don't want the full process? Say **"Vibe it!!"** after the first phase (or anytime) and TTT makes all remaining decisions for you.

It picks the most attractive market angle, the most specific user, the sharpest problem, and the smallest viable solution. States every assumption upfront. Generates all spec files immediately.

Speed over depth. You can always revise after.

---

## What You Get

TTT generates a directory of markdown files. Every file is human-readable and coding-agent-ready.

```
ttt-spec/
  ttt_state.json           # Session state, decisions, pivot history
  clarification.md         # Product thesis, user, platform, constraints
  market_research.md       # Porter's, SWOT, BMC, whitespace, timing
  user_research.md         # Maslow's, Reiss, JTBD, behavior patterns  
  definition.md            # Exact user, problem, solution, scope guard
  solution.md              # User journeys, feature specs, edge cases
  tech_architecture.md     # Stack, data models, API routes
  design_guideline.md      # UX philosophy, references, components
  test_eval.md             # Acceptance tests, benchmarks, success criteria
  coding_agent_prompt.md   # Copy-paste into Cursor/Claude Code. Day 0.
  blueprint.md             # File manifest and reading order
  versions.md              # Changelog, V2 parking lot, scope changes
  launch.md                # Distribution and metrics (optional)
```

Hand `coding_agent_prompt.md` to your coding agent. It references everything else. Start building.

---

## TTT + GSD

They're complementary. **TTT is the product manager. GSD is the program manager.**

| | TTT | GSD |
|---|---|---|
| **Answers** | What should I build? | How do I build it reliably? |
| **When** | Before you write code | While you write code |
| **Output** | Validated spec | Working software |
| **Prevents** | Building the wrong thing | Code falling apart at scale |

**Workflow:**

```
/ttt-new-idea           → Figure out what to build
                        → Get spec files

/gsd-new-project        → Initialize GSD with your spec
/gsd-plan-phase 1       → Plan the work
/gsd-execute-phase 1    → Build it reliably
```

You can use TTT without GSD, or GSD without TTT. But together? You get the right spec **and** reliable execution.

---

## Why TTT Is Different

**It says no.** If your idea doesn't hold up against market reality, TTT tells you before you waste a month building it. Most tools validate everything. TTT has opinions.

**Real PM frameworks.** Not "analyze the market." Porter's Five Forces. SWOT per competitor. Business Model Canvas. Jobs To Be Done with three layers. The same frameworks a senior PM would use — without you needing to know them.

**Scope guard with teeth.** Maximum 5 features for v1. Every feature must map to a real user job. TTT pushes back if you try to add more. Deferred features go to a V2 parking lot, not into the void.

**State that survives crashes.** `ttt_state.json` tracks every decision, every assumption, every pivot. Close the session, come back tomorrow, TTT picks up exactly where you left off.

**Pivots without starting over.** Change direction and TTT evaluates what's still valid. Same market, different angle? Keep the research, redo the definition. New market entirely? Re-research only what changed.

---

## Getting Started

```
npx to-the-t@latest
```

The installer prompts you to choose:
1. **Runtime** — Claude Code, Cursor, Windsurf, etc.
2. **Location** — Global (all projects) or local (current project only)

Then:

```
/ttt-new-idea
```

Describe your idea. TTT takes it from there.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/ttt-new-idea` | Full 5-phase flow: clarify → validate → define → specify → launch |
| `/ttt-vibe-it` | Fast mode. TTT makes all decisions. Get spec files immediately. |
| `/ttt-resume` | Pick up where you left off |
| `/ttt-progress` | Where am I? What's next? |
| `/ttt-help` | Show all commands |

---

## Who This Is For

Solo vibecoders who:
- Have ideas but keep building the wrong thing
- Ship fast but want to ship **right**
- Don't want to play enterprise PM theater
- Want honest feedback, not validation

If you're the kind of person who opens Cursor before thinking through whether the idea is good — TTT is for you.

---

## Status

Under active development. Architecture designed. Agent prompts being built.

---

## Philosophy

**Respect the builder's momentum.** Every question must earn its place. Done and useful beats complete and bloated.

**Be honest.** If the data is weak, say so. If the idea is bad, say so. If an assumption was made, state it.

**Be opinionated.** TTT has a point of view. It recommends one option, explains why, and lets you override.

**Protect v1.** Solo builders overbuild. TTT aggressively recommends the smallest viable version. Good ideas that aren't essential get parked, not lost.

---

## License

MIT

---

**Your coding agent is powerful. TTT makes sure it builds the right thing.**