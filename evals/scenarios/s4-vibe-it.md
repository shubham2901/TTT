# S4: Vibe It

**Tests:** Vibe it!! fast path, assumption transparency, complete artifact generation, no silent scope creep
**Tonal register:** Impatient, momentum-driven, minimal engagement

---

## Variant A: Immediate Vibe It!! (Primary)

### Opening (Turn 1)

**User:** "I want a meal planning app that suggests recipes based on what's in your fridge. Vibe it!!"

### Turn 2

TTT may ask 1–2 minimal clarification questions before triggering Vibe it!! (platform, user). User responds tersely:

**User:** "Mobile. For busy people who hate planning meals. Just vibe it, go go go."

### After Scripted Turns

TTT should trigger Vibe it!! after this minimal Clarify. No further evaluator interaction expected — TTT generates all artifacts autonomously. Evaluator observes and records in transcript.

### Key Checkpoints

**1. After Turn 1 — Trigger Recognition:**
TTT should recognize "Vibe it!!" trigger immediately. Should run a minimal Clarify — at most 1–2 quick questions to fill critical gaps (platform, user target), not a full extraction flow. Speed is the priority. Choreographer question discipline still applies but bar is lower.

**2. After Vibe It!! Completion — Full Artifact Generation:**
All remaining artifacts generated (`clarification.md` through `coding_agent_prompt.md`). Assumptions presented in one block before generation per choreographer Vibe it!! protocol. No quality gates applied — this is the fast path. All files remain user-editable. `vibe_it.used: true` in `ttt_state.json`. Stack defaults used (Next.js + Supabase + Tailwind + shadcn/ui) unless the product needs something specific (mobile → React Native or similar).

---

## Variant B: Delayed Vibe It!!

### Opening (Turn 1)

**User:** "I want to build a bookmarking tool for researchers. Something that organizes papers and highlights."

### Turn 2

After TTT's initial clarification questions, user triggers Vibe it!! mid-flow:

**User:** "Academic researchers. Web app. Vibe it!! — just make it happen, I'll adjust later."

### After Scripted Turns

Same as Variant A — TTT generates all artifacts autonomously. Evaluator observes. Any Clarify data gathered before the trigger should be preserved and used.

### Key Checkpoints

**1. After Turn 1 — Normal Clarify Start:**
TTT runs normal Clarify flow. Asks ≤2 questions to narrow the thesis. No Vibe it!! trigger yet — TTT should not preemptively switch to fast path.

**2. After Turn 2 — Mid-Flow Trigger Recognition:**
TTT recognizes "Vibe it!!" trigger mid-flow. Should save whatever Clarify data was gathered (thesis direction, platform = web, user = academic researchers), complete `clarification.md` with available info + stated assumptions, then switch to Vibe it!! mode. Should not restart Clarify or discard Turn 1 context.

**3. After Vibe It!! Completion — Full Artifact Generation:**
Same as Variant A checkpoint 2. All artifacts generated. Assumptions stated. No quality gates. State updated. The `clarification.md` should be richer than Variant A's because more user input was gathered before the trigger.

---

## Success Definition (Both Variants)

### Qualitative

- All artifact files generated (`clarification.md` through `coding_agent_prompt.md`)
- Assumptions stated explicitly in one block before generating — no silent assumptions
- No silent scope creep — features should be minimal (smallest thing that solves the job)
- Stack defaults used unless the product specifically needs something different
- Speed: Vibe it!! should complete noticeably faster than the full flow
- Vibe it!! does not skip `clarification.md` — it still produces one, just with more assumptions

### Rubric Expectations

| Dimension         | Expected | Rationale                                              |
|-------------------|----------|--------------------------------------------------------|
| coherence         | 3–4      | Assumptions may create minor internal tensions         |
| specificity       | 3–4      | Less user input → less specificity available            |
| relevance         | 3        | No real research conducted → assumption-based          |
| comprehensiveness | 4–5      | All sections should be present, even if assumption-based |
| actionability     | 4–5      | The whole point of Vibe it!! is a buildable spec quickly |

**Scoring note:** Lower scores on some dimensions are EXPECTED and acceptable for S4. The value of Vibe it!! is speed and completeness, not depth. A 3 on relevance is fine when no market research was conducted — that's the tradeoff the user chose.

---

S4 is the only scenario with two structurally different variants (immediate vs delayed trigger) rather than just domain variation. This tests whether TTT handles Vibe it!! correctly regardless of when in the conversation it's invoked.
