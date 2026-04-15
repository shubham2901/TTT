# TTT (To The T)

Helps you turn a raw idea into a complete plan before you build. You describe what you want to make. TTT figures out if it's worth building, who it's for, what exactly to build first, and gives you a document your coding tool can use to start.

---

## When to use

- You have a product idea and want to think it through before coding
- You want to understand competitors and what users actually need
- You want a clear plan a coding tool (Cursor, Claude, Copilot) can follow

## When not to use

- You're already building and need code help
- You want to debug or deploy existing code

---

## What TTT creates

**Three files** (plus optional extras if you want them):

| File | What it is |
|------|------------|
| **research.md** | What we learned — competitors worth knowing, what users struggle with today, whether timing is good |
| **plan.md** | What we're building — who it's for, the one problem we're solving, features for version 1, how it should look and feel |
| **handoff.md** | What to give your coding tool — tech choices explained, build order, design notes, everything needed to start coding |

**Optional files** (only if you ask):
- **screens.md** — Sketches and descriptions of each screen (or you can use tools like Google Stitch, Figma AI, or Gemini to generate these from the plan)
- **tests.md** — Test cases to verify the app works correctly
- **summary.md** — Only if you say **"save summary"** after plan lock. A chat summary is shown automatically when you lock the plan; the file is not created unless you ask.

**After you say "lock it":** You get a **plain-English summary in the chat** (not a file by default) — what the app is, who it's for, V1 features, and what you need to arrange before building (content, art, logistics). No questions in that message. You are told that fuller detail is in the files. **`handoff.md` stays the full** developer/AI-tool spec for tools like Lovable, Cursor, or Claude Code; the chat summary does not replace it.

---

## How it works

TTT is a guided conversation in four parts:

**1. Understand your idea** — We narrow down what you want to build, who it's for, and what platform (app, website, etc). Takes 2-5 messages.

**2. Research** — We look at competitors and understand what users actually do today. You'll see key findings and can decide if the idea needs adjusting.

**3. Finalize the plan** — We lock in exactly who this is for, the main problem to solve, and the 3-5 features for version 1. You confirm the tech and design direction.

**4. Create the handoff** — We generate the detailed document your coding tool needs. You can start building.

**Shortcut available:** At any point after step 1, you can say **"you decide"** — I'll make all remaining decisions with clear assumptions and generate everything quickly. Faster, but less tailored.

---

## What TTT asks you along the way

Early questions (platform/scope in **plain language** — no framework names like Flutter or React Native unless you brought them up):
- What's the idea? Who is it for?
- Have you built an app before? (So I know how much to explain)
- App or website? Android, iPhone, or both?
- What's your rough timeline and budget?

Before finalizing:
- Here are the competitors worth knowing — does this change anything?
- Here's the main problem we'd solve — does this feel right?
- Here are 3-5 features for version 1 — too many? Too few?
- Tech stack and hosting are proposed when the plan is finalized — each choice is **named and explained in one plain line** (for example: "Flutter — one codebase for Android and iPhone so you don't build two apps"). If you ask what a term means, you get a **short** answer (a few lines), then we return to the plan.

Optional:
- Want me to sketch the screens?
- Want test cases to verify it works?

---

## Practical guidance TTT provides

Beyond just planning, TTT will flag real-world considerations:

- **Competitors to actually try** — "Download X and Y, use them for 10 minutes, note what you like and hate"
- **Cost and time estimates** — Rough sense of what building this takes
- **Content and operations burden** — If your app needs fresh content (templates, posts, etc), who creates it?
- **Legal and platform risks** — Copyright issues, app store rejection risks, payment processor rules
- **Simpler alternatives** — Sometimes a WhatsApp channel or Notion page can test the idea before you build an app

---

## For developers integrating TTT

### Files

| File | Purpose |
|------|---------|
| `prompts/choreographer.md` | Main orchestration logic — always load this |
| `prompts/researcher.md` | Combined market + user research agent |
| `prompts/product_detailer.md` | Optional: extended product / solution detail (not required for default handoff) |
| `prompts/test_eval_generator.md` | Optional: tests and eval criteria (not required for default handoff) |

Other prompts in `prompts/` (`tech_architect.md`, `design_advisor.md`) are optional for advanced workflows; the default path produces `research.md`, `plan.md`, and `handoff.md` per the choreographer.

### State

TTT maintains state in `ttt_state.json` so conversations can resume after context clears. Back up existing files to `_backup/<timestamp>/` before regenerating.

### With Cursor

Reference prompts with `@` paths. Use Task tool for research if available, otherwise run sequentially.

### With Claude Code

Load this skill. Run research in current context with honest progress messages.

### Web search

Research works best with web search enabled. If unavailable, user can paste sources or skip research.

---

## Key rules

1. **Plain language** — Everyday wording for product questions. **Tech decisions** (when you finalize the plan and in the handoff): always **name the real tool or stack and add one plain line** saying what it implies for you. Never drop the term; never leave it unexplained.
2. **No surprise tech in early questions** — Brainstorming stays non-technical for stack; frameworks are discussed only when locking the plan and in `handoff.md`.
3. **Short answers if you question a term** — A few lines max, then back to the plan. No comparison tables unless you ask what your options are.
4. **Max 2 questions per message** — Lead with the most important one.
5. **Name real competitors** — Specific apps and companies, not vague categories.
6. **Small version 1** — Maximum 5 features, ideally 3. Each must solve a real user problem.
7. **Confirm before deciding** — Present defaults, get explicit "okay" before locking in.
8. **Quiet operations** — Don't narrate file reads/writes. User sees outcomes, not machinery.
9. **Honest about weaknesses** — Crowded markets, weak data, missing info — say it clearly.
10. **User can always redirect** — Pivot, override, skip, or take the shortcut. Respect it.