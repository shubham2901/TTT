# TO THE T (TTT)

**The product manager you never hired. For solo vibe coders who ship fast and want to ship right.**

TTT answers the two questions every solo builder skips: "Should I build this?" and "What exactly should I build?" It takes a vague idea and turns it into a validated, scoped, build-ready spec. Before you write a single line of code.

This is built after getting inspired by GSD https://github.com/gsd-build/get-shit-done. TTT will tell you what you should actually build and how. GSD will help you build it reliably. While GSD is your hero program manager, TTT will be your hero product manager.

---

*"I had the idea on Monday, TTT killed it by Tuesday, suggested something better by Wednesday, and I was coding by Thursday."*

---

## Why This Exists

Solo developers skip PM work. Every time. You have an idea, you open Cursor, and three weeks later you realize the market has 50 competitors, your user is wrong, or you built 12 features when you needed 3.

Tools like GSD solve the "how do I build reliably" problem. Nothing solves the "should I build this at all" problem. TTT does.


---

## How It Works

One command. Five phases. You talk, TTT thinks, argues back, researches, and hands you files your coding agent can build from.

### → Clarify

You describe your idea. TTT narrows it.

```
You:  "AI tool for creators"
TTT:  "That's a 3/10 on specificity. There are 50+ creator tools.
       Are you thinking YouTube? Instagram? What kind of creators? 
       What's their actual pain?"
You:  "YouTube creators who want to make Shorts from long videos"
TTT:  "Better. 7/10. Indie creators under 10K subs, or established ones?"
```

TTT doesn't stop until the idea is one clear sentence and the user is specific enough to research.

### → Validate

TTT spawns two research agents in parallel:

**Market Researcher** runs Porter's Five Forces on the industry, SWOT on every competitor it finds, maps the Business Model Canvas, and identifies at least 3 whitespace opportunities. Real frameworks. Real structure. Not vibes.

**User Researcher** maps user needs against Maslow's hierarchy, identifies core desires using Reiss's 16 motivators, checks for compulsion loops, and builds Jobs To Be Done with functional, emotional, and psychological layers.

Then TTT synthesizes everything and gives you a straight answer:

```
TTT:  "The space has 4 direct competitors. Two are bloated. One is 
       expensive. Nobody is targeting indie creators under 10K subs. 
       Timing is good - YouTube Shorts API just opened up.

       Your call:
       1. Build as-is
       2. Narrow to creators in education niche (strongest whitespace)
       3. Pivot to thumbnail generation (highest-pain JTBD)
       4. Your own direction"
```

If the idea is bad, TTT says so. It won't carry a flawed premise into a spec.

### → Define

Lock in exactly who, exactly what problem, and exactly what solution. TTT enforces a scope guard here. Maximum 5 features for v1. Every feature must map to a real user job. Everything else gets parked for v2.

```
TTT:  "That's 7 features. For a solo vibecoder shipping in 2 weeks, 
       5 is the ceiling. Which 2 are we parking for v2?"
```

TTT also collects your build preferences: tech stack, design references, coding agent, timeline. If you don't care, say "Take the best call" and TTT decides.

### → Specify

TTT spawns 4 agents in two waves:

**Wave 1:** Product Detailer maps every user journey, specifies every feature with edge cases, builds a screen inventory, and defines all states (empty, loading, error, success).

**Wave 2 (parallel):** Tech Architect picks the exact stack with rationale. Design Advisor creates a UX philosophy and component system. Test & Eval Generator writes acceptance tests for every feature.

Then TTT runs a completeness check. Every feature has tests? Every screen has design guidance? No scope leak? No orphaned data models? It catches drift before you see the output.

### → Launch Plan (optional)

Distribution, metrics, v2 triggers. Skip it if you just want to ship.

---

## Vibe it!!

Don't want the full process? Say "Vibe it!!" after the first phase (or anytime) and TTT makes all remaining decisions for you.

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

## Architecture

7 agents. 1 Choreographer orchestrating 6 specialized subagents.

```
                        ┌──────────────────┐
                        │   CHOREOGRAPHER   │
                        │                   │
                        │  Talks to you     │
                        │  Manages state    │
                        │  Enforces scope   │
                        │  Validates output │
                        └────────┬─────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                                  │
        VALIDATE (parallel)                SPECIFY (2 waves)
                │                                  │
       ┌────────┼────────┐            ┌─────┬──────┼──────┬─────┐
       │                 │            │     │      │      │
   Market            User          Product Tech  Design  Test
   Researcher     Researcher       Detailer Arch. Advisor  Eval
       │                 │            │     │      │      │
       ▼                 ▼            ▼     ▼      ▼      ▼
  market_research  user_research  solution tech   design  test_eval
       .md              .md         .md    .md     .md     .md
```

The Choreographer handles Phases 1, 3, and 5 directly (conversation, no heavy lifting). It spawns subagents only in Phases 2 and 4 where deep research and specification happen. Each subagent gets a fresh context window. Quality gates validate every output before it's written to disk. Failed outputs get retried up to 3 times with specific feedback.

---

## What Makes TTT Different

**It says no.** If your idea doesn't hold up against market reality, TTT tells you before you waste a month building it. Most tools validate everything. TTT has an existential crisis manager built into the research phase.

**Structured PM frameworks.** Not "analyze the market." Porter's Five Forces for industry structure. SWOT per competitor. Business Model Canvas. Maslow's and Reiss's desires for user psychology. JTBD with three layers. The same frameworks a senior PM would use.

**Scope guard with teeth.** Maximum 5 features for v1. Every feature must map to a real user job. TTT will push back if you try to add more. Deferred features go to a V2 parking lot, not into the void.

**Gap assessment.** Between Define and Specify, TTT checks: does your problem target an actual whitespace? Does your solution address the highest-pain job? Do your features exploit a competitor weakness? It catches misalignment before specification begins.

**Spec completeness check.** After specification, TTT verifies: every feature has tests, every screen has design guidance, no scope leaks, no orphaned data models, cross-file consistency. Drift gets caught before you see the output.

**State that survives crashes.** `ttt_state.json` tracks every decision, every assumption, every pivot, every retry. Close the session, come back tomorrow, TTT picks up exactly where you left off.

**Pivots without starting over.** Change direction and TTT evaluates what's still valid. Same market, different angle? Keep the research, redo the definition. New market entirely? Re-research only what changed. Files that are still valid are preserved.

---

## Pairing with GSD

TTT and [GSD](https://github.com/gsd-build/get-shit-done) are complementary.

TTT answers **what** to build. GSD answers **how** to build it reliably.

```
Your idea
    │
    ▼
  TTT ──→ Validated spec (13 files)
    │
    ▼
  You ──→ Hand coding_agent_prompt.md to your coding agent
    │
    ▼
  GSD ──→ Reliable execution with context engineering
```

TTT doesn't assume you use GSD. The output works with any coding agent. A GSD bridge command is planned for a future version.

---

## Status

TTT is under active development. The architecture is designed. Agent prompts and the skill file are being built.

---

## Philosophy

**Respect the builder's momentum.** Every question and every phase must earn its place. Done and useful beats complete and bloated.

**Be honest.** If the data is weak, say so. If the idea is bad, say so. If an assumption was made, state it.

**Be opinionated.** TTT has a point of view. It doesn't present 5 equal options and ask you to choose. It recommends one, explains why, and lets you override.

**Protect v1.** Solo builders overbuild. TTT aggressively recommends the smallest viable version. Good ideas that aren't essential get parked, not lost.

**Plain language.** No jargon. An arts teacher with zero tech exposure should feel comfortable at every step.

---

## License

MIT

---

**Your coding agent is powerful. TTT makes sure it builds the right thing.**
