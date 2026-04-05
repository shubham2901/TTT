# S3: Crowded Market

**Tests:** Honest weakness signaling, evidence-backed pivot menu, user agency, market research quality
**Tonal register:** Confident but receptive to feedback, slightly defensive about their idea

---

## Default Scenario

### Opening (Turn 1)

**User:** "I want to build a todo app with AI features. Like, AI that prioritizes your tasks and suggests what to work on next. Web app, solo dev."

### Turn 2

User is slightly defensive but cooperative:

**User:** "I know there are a lot of todo apps but I think AI prioritization is the differentiator. Target is busy professionals. Goal is task success — getting the right thing done first."

### Turn 3

User responds to TTT's validation synthesis showing a crowded market. This is the critical turn — the user should choose a pivot option, NOT "build as-is":

**User:** "OK fair point about the competition. Option (b) sounds interesting — what's the strongest whitespace you found?"

### After Scripted Turns

Evaluator continues as a user who has accepted the market reality and is now cooperating with the pivot direction. Makes reasonable choices. Aims to complete through Specify with the pivoted thesis.

---

## Key Checkpoints

### 1. After Clarify Phase Completes

TTT should accept the idea without prejudging during Clarify, but may note internally that the space is competitive. `clarification.md` should be well-formed regardless of market concerns — Clarify captures what the user wants, not whether it's viable. Quality gate should pass.

### 2. After Validate Synthesis — Honest Market Signal

This is the critical checkpoint. TTT MUST flag the crowded market honestly. Should present evidence — specific competitors (Todoist, Things 3, TickTick, Motion, Reclaim) with their AI features. Should offer pivot options (a–e per choreographer) with reasoning tied to whitespace, JTBD, or timing. Must NOT say "great idea!" if the market is saturated. Honesty over comfort — per choreographer interaction rules.

### 3. After Pivot Execution

TTT should correctly classify the pivot (narrow vs broad per choreographer pivot protocol). For a narrow pivot (same market, different angle): update `clarification.md`, keep research with pivot addendum, invalidate `definition.md`. State should reflect the pivot with from/to/reason. Post-pivot flow should proceed cleanly through Define.

---

## Success Definition

### Qualitative

- TTT doesn't sugarcoat the crowded market — names specific competitors with strengths
- Pivot options are evidence-backed (tied to whitespace analysis, JTBD, or timing trends)
- User's agency respected — TTT presents options, doesn't force a direction
- Post-pivot flow is clean (correct files invalidated/preserved, state updated)
- Pivot is logged in `versions.md` and `ttt_state.json` pivots array

### Rubric Expectations

| Dimension         | Expected | Rationale                                               |
|-------------------|----------|---------------------------------------------------------|
| coherence         | 4–5      | Pivot should produce consistent post-pivot artifacts    |
| specificity       | 3–4      | Pre-pivot idea is generic; post-pivot should improve    |
| relevance         | 4–5      | Research should directly address the crowded space      |
| comprehensiveness | 4–5      | Market research should be thorough in a data-rich space |
| actionability     | 3–4      | Pivot introduces uncertainty in downstream spec         |

---

## Variants

### Variant A: Crowded Dev Tool

**Opening:** "Building a code review tool that uses AI to suggest improvements. Targets dev teams. Web app."

**Turn 2:** "I know about CodeRabbit and others but I think I can do it better. Targeting small teams, 2–5 devs."

**Turn 3:** "Hmm, you're right that's a lot of competitors. Let me hear option (c) — the highest-pain job."

**Notes:** AI code review is a well-funded, crowded space (CodeRabbit, Codacy, SonarQube, Sourcery, etc.). TTT should surface well-known competitors and identify narrow whitespace. The defensive tone ("I think I can do it better") tests whether TTT respects confidence while still being honest.

### Variant B: Crowded Consumer App

**Opening:** "I want to build a habit tracking app. Simple, focused on daily habits with streaks. Mobile app."

**Turn 2:** "Yeah I use Streaks and Habitica but they're either too simple or too gamified. I want something in between. Targeting people who journal."

**Turn 3:** "OK interesting. Let's go with the timing opportunity — what's trending?"

**Notes:** Habit tracking is extremely crowded (Streaks, Habitica, Atoms, Habit Tracker, etc.). TTT should flag this clearly and evaluate whether the "journaling + habits" intersection is a real whitespace or wishful thinking. Tests TTT's ability to distinguish genuine whitespace from superficial differentiation.

---

Each variant preserves scenario intent — an idea entering a crowded market that requires honest weakness signaling and evidence-backed pivoting — but forces different competitive landscapes and pivot reasoning.
