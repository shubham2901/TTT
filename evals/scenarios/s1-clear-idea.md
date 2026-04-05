# S1: Clear Idea

**Tests:** Efficient Clarify phase, proportionate questioning, tight V1 scope
**Tonal register:** Cooperative, specific, decisive

---

## Default Scenario

### Opening (Turn 1)

**User:** "I want to build a Pomodoro timer for devs that integrates with GitHub Issues. It should be a web app. I'm a solo dev using Cursor."

### Turn 2

User responds cooperatively to TTT's clarification questions:

**User:** "Targeting indie devs who track their work in GitHub. Goal is task success — completing focused work sessions tied to specific issues. No mobile for now."

### Turn 3

User responds to TTT's Validate / Vibe it!! offer:

**User:** "Let's validate against the market."

### After Scripted Turns

Evaluator continues as a cooperative user. Makes reasonable choices when TTT presents options. Accepts TTT's recommendations unless obviously wrong. Aims to complete through Specify. Documents choices in transcript.

---

## Key Checkpoints

### 1. After Turn 1 — Extraction Without Re-Asking

TTT should extract thesis, platform (web), and builder context (solo/Cursor) from the opening without re-asking any of it. Should ask ≤2 clarification questions focused on genuine gaps (target user specificity, goal type). No walls of questions — choreographer question discipline applies.

### 2. After Clarify Phase Completes

`clarification.md` should have specificity score ≥ 7. Thesis should be one sentence. Platform = web with rationale. All info from Turn 1 present without re-prompting. Quality gate should pass on first attempt given the clear input.

### 3. After Validate Synthesis

TTT should present an honest market assessment. The Pomodoro space is well-established — TTT must flag competition (Forest, Pomofocus, Toggl, etc.) and suggest differentiation angles tied to the GitHub integration whitespace. Pivot options (a–e per choreographer) should be evidence-backed, not generic.

---

## Success Definition

### Qualitative

- Clarify completes in 2–3 exchanges, not 5+
- TTT doesn't re-ask what the user already provided (platform, builder context)
- Validate surfaces competition honestly — Pomodoro space is crowded
- Define produces ≤5 V1 features, each mapped to a JTBD
- Specify artifacts are internally consistent (scope guard enforced)

### Rubric Expectations

| Dimension         | Expected | Rationale                                      |
|-------------------|----------|-------------------------------------------------|
| coherence         | 4–5      | Clear input → consistent outputs throughout     |
| specificity       | 4–5      | User provided specific details upfront           |
| relevance         | 4–5      | Research should directly match the thesis        |
| comprehensiveness | 4–5      | All sections should be filled — no gaps expected |
| actionability     | 4–5      | Clear idea → actionable, buildable spec          |

---

## Variants

### Variant A: SaaS Analytics Tool

**Opening:** "I want to build a simple analytics dashboard for Shopify stores. Shows daily revenue, top products, and conversion rate. Web app, solo dev, using Claude Code."

**Turn 2:** "Small Shopify merchants, under 100 orders/day. They find Shopify's built-in analytics confusing. Goal is task success — seeing today's numbers in under 10 seconds."

**Turn 3:** "Validate it."

**Notes:** Tests TTT with a B2B SaaS idea. Market research should surface Shopify's own analytics as indirect competitor. Domain forces different market dynamics than dev tools.

### Variant B: Developer CLI Tool

**Opening:** "Building a CLI tool that generates conventional commit messages from git diffs using an LLM. I'm a senior dev, this is a weekend project."

**Turn 2:** "Devs who use conventional commits but hate writing them manually. Task success — correct commit message in one command. No GUI needed."

**Turn 3:** "Let's see the market first."

**Notes:** Tests TTT with a dev tool. Platform should resolve to CLI without TTT suggesting web/mobile. Research should find existing tools (commitizen, aicommits, etc.). Tonal register is terse but cooperative.

---

Each variant preserves scenario intent — a clear, specific idea from a cooperative user — but forces different domain knowledge, market dynamics, and platform reasoning.
