# TTT (To The T) - Complete System Architecture

## Document Purpose
This is the complete architecture specification for TTT, a product manager skill for vibe coders. Hand this to a coding agent (Cursor, Claude Code) to build the skill files, agent prompts, and file generation logic.

---

## 1. SYSTEM OVERVIEW

### What TTT Is
TTT is a product management layer for solo vibe coders. It sits upstream of coding. It answers: "What should we build, for whom, and why?" before a single line of code is written.

### Target User
Solo vibe coders who operate on momentum. They want to code, not write documents. TTT injects rigorous product thinking while protecting their momentum.

### How It Runs
TTT is a skill file installed in Claude Code, Cursor, or similar coding agents. The skill file contains the Choreographer prompt and instructions for spawning subagents.

### Core Value Propositions
1. Prevents building something nobody needs (market validation)
2. Prevents building too much (scope guard)
3. Prevents building without clarity (structured specification)
4. Respects momentum (Vibe it!! escape hatch)

---

## 2. AGENT ARCHITECTURE

### Overview
7 agents total. 1 Choreographer + 2 research subagents (parallel) + 4 specify subagents (parallel).

```
                          ┌─────────────────────┐
                          │    SKILL FILE        │
                          │  (entry point,       │
                          │   spawns             │
                          │   Choreographer)     │
                          └──────────┬──────────┘
                                     │
                          ┌──────────▼──────────┐
                          │   CHOREOGRAPHER      │
                          │                      │
                          │  - User interaction  │
                          │  - State management  │
                          │  - Phase transitions │
                          │  - Quality gates     │
                          │  - Gap assessments   │
                          │  - Scope guard       │
                          │  - File assembly     │
                          │  - Retry logic       │
                          │  - Pivot handling     │
                          │  - Progress updates  │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                                  │
           Phase 2: VALIDATE                  Phase 4: SPECIFY
           (2 parallel agents)               (4 parallel agents)
                    │                                  │
          ┌─────────┼─────────┐         ┌──────┬──────┼──────┬──────┐
          │                   │         │      │      │      │
   ┌──────▼──────┐  ┌────────▼───┐  ┌──▼──┐ ┌─▼──┐ ┌▼───┐ ┌▼────┐
   │   MARKET    │  │   USER     │  │PROD │ │TECH│ │DES │ │TEST │
   │ RESEARCHER  │  │ RESEARCHER │  │DET. │ │ARC.│ │ADV.│ │EVAL │
   └──────┬──────┘  └────────┬───┘  └──┬──┘ └─┬──┘ └┬───┘ └┬────┘
          │                   │         │      │     │      │
          ▼                   ▼         ▼      ▼     ▼      ▼
   market_research.md  user_research.md │  tech_arch  design  test_eval
                                     solution.md  .md    .md    .md
```

### Agent Responsibilities

#### Choreographer (runs in all phases)
- TALKS TO USER in Phases 1, 3, 5 and during pre-specify preference collection
- SPAWNS subagents in Phases 2 and 4
- VALIDATES all subagent outputs against quality gates
- MANAGES state via ttt_state.json
- ENFORCES scope guard (max 5 V1 features)
- RUNS gap assessments between phases
- RUNS spec completeness check after Phase 4
- HANDLES pivots (reassess what's still valid, re-run what's not)
- HANDLES retries (up to 3 per agent, with specific feedback)
- ASSEMBLES final files (coding_agent_prompt.md, blueprint.md, versions.md)
- SHOWS progress in natural language (never "Phase 2 of 5")
- HANDLES session resume from ttt_state.json
- HANDLES Vibe it!! (generate all remaining files with opinionated defaults)

#### Market Researcher (Phase 2, parallel with User Researcher)
- INPUT: clarification.md
- OUTPUT: market_research.md
- DOES: Porter's Five Forces, competitor SWOT, Business Model Canvas, whitespace analysis, timing assessment
- SOURCES: Reddit, YouTube, authentic articles, Wikipedia, research sites. Never flimsy blogs.
- DATA RULES: Mark data as weak where sources are soft. Do not use data where absent or very flimsy.

#### User Researcher (Phase 2, parallel with Market Researcher)
- INPUT: clarification.md
- OUTPUT: user_research.md
- DOES: Maslow's needs, Reiss's 16 desires (pick 3-5), Seven Sins compulsions, JTBD with functional/emotional/psychological layers
- SOURCES: Same quality rules as market researcher

#### Product Detailer (Phase 4, parallel with other specifiers)
- INPUT: definition.md, market_research.md, user_research.md
- OUTPUT: solution.md
- DOES: User journeys (onboarding, activation, core loop, retention), feature specifications, edge cases, screen inventory, state definitions

#### Tech Architect (Phase 4, parallel)
- INPUT: definition.md (including build preferences)
- OUTPUT: tech_architecture.md
- DOES: Stack decisions with rationale, data models, API routes, external dependencies
- RULE: If user said "Take the best call", choose what's best for vibecoding, well-documented, extensible, scalable

#### Design Advisor (Phase 4, parallel)
- INPUT: definition.md (including design preferences), solution.md (screen inventory)
- OUTPUT: design_guideline.md
- DOES: UX philosophy, design references, layout, components, typography, color, spacing, states, responsive behavior
- NOTE: Design Advisor may need solution.md's screen inventory. Since Product Detailer runs in parallel, the Choreographer should pass the screen list from definition.md's V1 features as a proxy. Or run Product Detailer slightly before the others.

#### Test & Eval Generator (Phase 4, parallel)
- INPUT: definition.md, solution.md
- OUTPUT: test_eval.md
- DOES: Acceptance tests per feature, user journey tests, performance benchmarks, success evaluation criteria
- NOTE: Same dependency on solution.md as Design Advisor. Same resolution.

### Phase 4 Dependency Note
Product Detailer generates solution.md which Design Advisor and Test & Eval Generator ideally want as input. Two options:

Option A (simpler): Run Product Detailer first, then run Tech Architect + Design Advisor + Test & Eval Generator in parallel using its output. This is 2 waves: Wave 1 = Product Detailer, Wave 2 = other 3 in parallel.

Option B (faster but less precise): Run all 4 in parallel, giving Design Advisor and Test Eval the V1 feature list from definition.md instead of the full solution.md. Accept slightly less alignment. Choreographer catches gaps in the completeness check.

Recommendation: Option A. It's only slightly slower (one extra agent round) but produces much better aligned outputs. This matches GSD's wave execution pattern.

---

## 3. PHASE FLOWS

### Phase 1: CLARIFY
Handled by: Choreographer directly (no subagents)

```
Flow:
1. Check if user provided any input
   - If blank: Show a witty opener (rotate from joke bank), then "What are we building?"
   - If input exists: Start extracting

2. Extract from user input (do not re-ask what's already provided):
   a. Is this 0-to-1 or building on existing platform? (ASK FIRST)
   b. Core idea and why it should exist
   c. Target user (evaluate specificity 0-10)
   d. Platform (contextual: creators won't use CLI, devs won't use mobile)
   e. Location/market (only if contextually relevant)
   f. Builder constraints: vibecoder or team? Timeline? Tech comfort?

3. Ask maximum 2 questions per message. Lead with the most important.

4. Use analogies for ambiguous choices:
   "Are you imagining something configurable like Notion, or focused like Google Keep?"

5. For platform, be contextual:
   - Content creators -> web app or mobile app (not CLI, not extension)
   - Developer tools -> CLI or web app (rarely mobile)
   - Consumer social -> mobile first
   - Suggest with reasoning, let user override

6. Narrow to one-line thesis:
   Raw: "AI tool for creators"
   Narrowed: "AI tool that helps YouTube creators turn long videos into viral shorts"

7. Evaluate: Is user specificity >= 6? If not, ask more narrowing questions.

8. Write clarification.md
9. Write ttt_state.json (phase: clarify, status: complete)

10. Offer choice:
    "We have the basics. We can:
     1. Validate this against the market (recommended)
     2. Vibe it!! - I'll make all the calls and generate the full spec now
     What do you want to do?"
```

Progress labels during Phase 1:
- "Understanding what you want to build"
- "Narrowing down your idea"
- "Idea is clear. Ready to validate."

### Phase 2: VALIDATE
Handled by: Choreographer spawns Market Researcher + User Researcher in parallel

```
Flow:
1. Pre-check: Does research already exist?
   - If market_research.md AND user_research.md exist AND this is not a re-research after pivot:
     Skip to synthesis. Use existing research.
   - If one exists but not the other: Run only the missing agent.
   - If neither exists: Run both.
   - If pivot triggered re-research: Check ttt_state.json for which files were invalidated.
     Re-run only invalidated agents. Preserve valid files.

2. Spawn Market Researcher with input: clarification.md
   Spawn User Researcher with input: clarification.md
   (These run in parallel)

3. Receive Market Researcher output. Validate against quality gates:
   - Porter's: All 5 forces, each with 1-4 points? 
   - Competitors: Minimum 2 direct with full SWOT (1-3 per factor)?
   - Business Model Canvas: All 9 blocks filled?
   - Whitespace: Minimum 3 with evidence?
   - Timing: Both supporting and opposing trends?
   If FAIL: Retry with specific feedback. Max 3 retries.
   If PASS: Write market_research.md

4. Receive User Researcher output. Validate against quality gates:
   - Maslow's: At least 2 levels with substance?
   - Reiss: 3-5 desires selected and justified?
   - Compulsions: At least 1 or explicit "none apply"?
   - JTBD: Minimum 2 jobs, each with functional + emotional + psychological?
   - Current workaround for each job?
   If FAIL: Retry. Max 3 retries.
   If PASS: Write user_research.md

5. Synthesis (Choreographer does this internally, not a subagent):
   Read both research files. Evaluate:
   a. Does a USP or whitespace exist relative to competitors?
   b. Is timing favorable?
   c. Does the idea fit user needs, desires, and jobs?
   If all three YES: Proceed with confidence.
   If any NO: Identify what needs to change.

6. Present to user with 4 options:
   a. Build as-is (even if research suggests weakness)
   b. Pivot with refinement 1 (Choreographer suggests based on strongest whitespace)
   c. Pivot with refinement 2 (Choreographer suggests based on highest-pain JTBD)
   d. Pivot with refinement 3 (Choreographer suggests based on timing advantage)
   e. User's own direction

7. If user pivots:
   - Log pivot in ttt_state.json
   - Evaluate: same market or new market?
     - Same market, different angle: Update clarification.md. Add pivot addendum to research. Skip to Phase 3.
     - New market: Update clarification.md. Re-run research (Step 2) with new inputs.
   - Preserve unchanged files. Rewrite only what's invalidated.

8. Update ttt_state.json (phase: validate, status: complete)
```

Progress labels during Phase 2:
- "Researching the market and your target users"
- "Analyzing what the research means for your idea"
- "Here's what I found. Your call on direction."

### Phase 3: DEFINE
Handled by: Choreographer directly (no subagents)

```
Flow:
1. Read clarification.md, market_research.md, user_research.md

2. Define user cohort:
   - Start with clarification.md target user
   - Refine using user_research.md findings
   - If too broad: Narrow using research evidence. Take assumptions where confident.
   - Ask user ONLY for gaps. Do not re-ask what research already answered.

3. Define primary problem:
   - Identify from user_research.md: which JTBD has highest pain?
   - Cross-reference with market_research.md: which whitespace is largest?
   - Pick the intersection. One problem, not three.
   - Present to user for confirmation.

4. Define solution direction:
   - High-level approach. Not features yet. The strategic direction.
   - "We will build [approach] because [whitespace] + [timing] + [user pain]"

5. SCOPE GUARD - V1 Feature Selection:
   - Ask user: "What are the must-have features for v1?"
   - If user lists > 5: Force a cut.
     "That's [N] features. For a solo vibecoder, 5 is the ceiling for v1. 
      Which ones should we park for v2?"
   - For each feature: verify it maps to at least one JTBD
   - Features serving no job: Flag. "This doesn't connect to any user need 
     we found. Move to V2?"
   - Park deferred features in V2 section of definition.md AND versions.md

6. Collect build preferences (Choreographer asks, not a subagent):
   Tech preferences:
   - "Framework preference? Or should I pick the best option?"
   - "Backend? Database? Auth? Hosting?"
   - For each: accept user choice OR "Take the best call"
   
   Design preferences:
   - "I'll show you reference apps from your space. Which aesthetic matches your vision?"
   - Suggest 2-3 apps from the same industry based on research
   - "UI density: minimal, moderate, or dense?"
   - "What matters most: speed, beauty, information density, or simplicity?"
   
   Vibecoding context:
   - Confirm: solo or team, primary coding agent, ship timeline

7. Define success metric:
   - One measurable outcome for v1
   - Must be achievable and testable

8. Write definition.md

9. RUN GAP ASSESSMENT (Define-to-Specify):
   [See section 5.2 for full check]
   If gaps found: Present to user. Revise or acknowledge.

10. Update ttt_state.json (phase: define, status: complete)

11. Recommend context clear:
    "Good point to clear context before we generate the spec. 
     Everything is saved in files. Ready to continue?"
```

Progress labels during Phase 3:
- "Defining exactly who this is for"
- "Narrowing down the core problem"
- "Deciding what's in v1 and what's later"
- "Getting your build and design preferences"
- "Problem, user, and solution are locked. Ready to specify."

### Phase 4: SPECIFY
Handled by: Choreographer spawns subagents in 2 waves

```
Flow:
1. Read definition.md (this is the single source of truth for all subagents)

2. Wave 1: Spawn Product Detailer
   Input: definition.md, market_research.md, user_research.md
   Output: solution.md
   Wait for completion. Validate output:
   - Every V1 feature has a specification entry?
   - User journeys cover onboarding, activation, core loop, retention?
   - Edge cases identified for each feature?
   - Screen inventory present?
   - All 4 states defined (empty, loading, error, success)?
   If FAIL: Retry with feedback. Max 3.

3. Wave 2: Spawn in parallel:
   a. Tech Architect
      Input: definition.md
      Output: tech_architecture.md
   
   b. Design Advisor
      Input: definition.md, solution.md (from Wave 1)
      Output: design_guideline.md
   
   c. Test & Eval Generator
      Input: definition.md, solution.md (from Wave 1)
      Output: test_eval.md

4. Validate each Wave 2 output against quality gates.
   Retry failed agents (max 3 each).

5. RUN SPEC COMPLETENESS CHECK:
   [See section 5.3 for full check]
   Fix automatically where possible. Flag to user where judgment needed.

6. Choreographer assembles remaining files:
   - coding_agent_prompt.md (references all output files, build order, rules)
   - blueprint.md (file manifest, connections, reading order)
   - versions.md (changelog, V2 parking lot, scope changes)

7. Present to user:
   "Spec is complete. Here's what was generated: [file list]
    You can review any file and request changes, or hand 
    coding_agent_prompt.md to your coding agent and start building."

8. Update ttt_state.json (phase: specify, status: complete)
```

Progress labels during Phase 4:
- "Detailing the product flows and features"
- "Building out the technical architecture, design system, and test plan"
- "Checking everything fits together"
- "Spec is ready. You can start building."

### Phase 5: LAUNCH (Optional)
Handled by: Choreographer directly

```
Flow:
1. Offer as optional:
   "Spec is done. Want to map out a launch plan, or start building?"

2. If user wants launch plan:
   - Distribution: where first 100 users come from
   - Infrastructure: hosting, monitoring
   - Metrics: 30-day and 90-day targets
   - V2 triggers: what signals to build next version

3. Write launch.md
4. Update ttt_state.json (phase: launch, status: complete)
```

Progress labels during Phase 5:
- "Planning how to reach your first users"
- "Launch plan is ready."

---

## 4. VIBE IT!! MECHANICS

### When Available
- After Phase 1 (Choreographer offers it explicitly)
- Anytime mid-flow (user types "Vibe it!!")

### Flow
```
1. User triggers "Vibe it!!"
2. Choreographer checks ttt_state.json: what files exist?
3. For every missing phase, Choreographer generates files directly.
   NO subagents. Speed over depth.

4. State assumptions using these heuristics:

   Market: Pick the angle with least competition and clearest 
   timing tailwind. Prefer niches over broad markets.

   User: Pick the most specific cohort where the problem is 
   most acute. Narrower is better.

   Problem: Pick the job with highest pain in the current 
   workaround. Manual + hating it = the problem.

   Solution: Pick the smallest thing that fully solves the 
   primary job. One feature done perfectly.

   Stack defaults: Next.js + Supabase + Tailwind + shadcn/ui
   (unless product needs something else)

   Design defaults: Minimal, fast, one-column layout.
   References: Linear (productivity), Stripe (dev tools), 
   Cal.com (scheduling)

5. Present all assumptions in one block before generating.
6. Generate all remaining files sequentially.
7. No quality gates. No retries.
8. Write ttt_state.json with vibe_it.used: true and all assumptions logged.
9. All files are editable. User can revise any file after.
```

---

## 5. VALIDATION SYSTEMS

### 5.1 Quality Gates (per agent output)

Applied by Choreographer after receiving each subagent's output. If gate fails, retry with specific feedback. Max 3 retries per agent. After 3 failures, surface to user.

#### Market Researcher Quality Gates
- Porter's Five Forces: All 5 forces present, each with 1-4 points
- Competitors: Minimum 2 direct with full SWOT (1-3 points per factor per competitor). 3 direct + 2 indirect is great. Max 8 total.
- Business Model Canvas: All 9 blocks filled
- Whitespace: Minimum 3, each with evidence
- Timing: Both supporting and opposing trends present
- Data confidence notes present for any estimated/stale data

#### User Researcher Quality Gates
- Maslow's: At least 2 levels addressed with substance
- Reiss: 3-5 desires selected and justified
- Compulsions: At least 1 applicable or explicit "none apply" with reasoning
- JTBD: Minimum 2 jobs, each with functional + emotional + psychological
- Current workaround described for each job
- Key quotes/evidence section has at least 2 sourced quotes

#### Product Detailer Quality Gates
- Every V1 feature from definition.md has a specification entry
- User journeys: onboarding + activation + core loop + retention all present
- Edge cases: at least 1 per feature
- Screen inventory lists all distinct views
- All 4 states defined (empty, loading, error, success)

#### Tech Architect Quality Gates
- Stack: every layer has a choice with rationale
- "Take the best call" entries have clear reasoning for the choice made
- Data models cover all entities needed by V1 features
- API routes map to features
- External dependencies listed with purpose

#### Design Advisor Quality Gates
- UX philosophy: 2-3 principles, specific to this product (not generic)
- Design references match user's stated preferences
- Layout described for primary view
- Typography, color, spacing systems defined
- All 4 states have visual approach

#### Test & Eval Generator Quality Gates
- Every V1 feature has at least 1 happy path + 1 edge case test
- User journey tests cover all 4 journeys from solution.md
- Success metric from definition.md is referenced and measurable
- Performance benchmarks present

### 5.2 Define-to-Specify Gap Assessment

Run by Choreographer after Phase 3 completes, before spawning Phase 4 agents.

```
Check 1: WHITESPACE ALIGNMENT
- Read market_research.md whitespace section
- Read definition.md problem statement
- Does the problem target at least one identified whitespace?
- FAIL: "Your problem doesn't address any market whitespace."

Check 2: JTBD ALIGNMENT
- Read user_research.md JTBD section
- Read definition.md primary problem
- Does the problem map to the highest-pain job?
- FAIL: "You're solving a lower-pain job. Job [X] has higher pain."

Check 3: USER COHORT CONSISTENCY
- Read user_research.md user profile
- Read definition.md user cohort
- Is defined cohort subset of or identical to researched user?
- FAIL: "Definition broadened the user beyond what was researched."

Check 4: TIMING CHECK
- Read market_research.md timing verdict
- If unfavorable: does definition.md address opposing trends?
- FAIL: "Timing concerns not addressed in solution direction."

Check 5: SCOPE VS COMPETITOR WEAKNESS
- Read definition.md V1 features
- Read market_research.md competitor SWOT weaknesses
- Do V1 features exploit at least one competitor weakness?
- FAIL: "No V1 feature targets a competitor weakness."

Check 6: FEATURE-JOB MAPPING
- For each V1 feature: does it serve at least one JTBD?
- FAIL: "Feature [X] maps to no user job. Why is it in V1?"

Resolution: Present all failures to user. User can revise definition.md 
or acknowledge risks. Log decisions in ttt_state.json.
```

### 5.3 Spec Completeness Check

Run by Choreographer after all Phase 4 subagents complete, before presenting to user.

```
Check 1: FEATURE COVERAGE
- Every V1 feature in definition.md has entry in solution.md?
- Every V1 feature has acceptance tests in test_eval.md?
- Every V1 feature appears in at least one user journey?
- FIX: Flag missing entries. Retry relevant agent.

Check 2: SCOPE LEAK DETECTION
- Every feature in solution.md is in definition.md V1 list?
- No user journey references unlisted capabilities?
- FIX: Remove leaked features. Move to V2 parking lot.

Check 3: TECH-FEATURE ALIGNMENT
- Every data model used by at least one feature?
- Every API route serves at least one feature?
- FIX: Remove orphaned models/routes.

Check 4: DESIGN COVERAGE
- Every screen in solution.md has design guidance?
- All 4 states defined in design_guideline.md?
- FIX: Flag missing screens to Design Advisor (retry if needed).

Check 5: BUILD PREFERENCE COMPLIANCE
- Tech stack matches definition.md preferences?
- Design references match stated preferences?
- FIX: Flag mismatches to user.

Check 6: TEST COMPLETENESS
- Every feature has happy path + edge case test?
- Success metric from definition.md is in test_eval.md?
- FIX: Flag gaps. Retry Test Eval agent.

Check 7: CODING AGENT PROMPT INTEGRITY
- References all output files?
- Build order respects tech dependencies?
- V2 parking lot matches definition.md + versions.md?
- FIX: Choreographer fixes directly (it assembles this file).

Check 8: CROSS-FILE CONSISTENCY
- Product thesis consistent across clarification.md, definition.md, coding_agent_prompt.md?
- User cohort consistent across all files?
- V1 feature list identical in definition.md, solution.md, coding_agent_prompt.md?
- FIX: Standardize to definition.md as source of truth.
```

---

## 6. OPERATIONAL MECHANICS

### 6.1 Retry Logic

```
Pattern (applied to every subagent call):

1. Spawn agent with inputs
2. Receive output text
3. Run quality gates against output
4. If PASS:
   - Write output to file
   - Update ttt_state.json (agent status: pass, attempts: N)
   - Proceed
5. If FAIL:
   - Increment retry counter
   - Log failure reason in ttt_state.json retry_history
   - If attempt < 3:
     Re-spawn agent with SAME inputs PLUS feedback:
     "Your output failed validation. Issues:
      - [specific gap 1]
      - [specific gap 2]
      Regenerate the full output addressing these gaps."
   - If attempt = 3:
     Surface to user:
     "I couldn't get deep enough research on [topic] after 3 attempts.
      This might mean [interpretation]. Can you help with [specific ask]?"
     User provides input -> Add to agent inputs -> One final retry
   - If still failing: Proceed with best output so far.
     Flag weak sections in ttt_state.json.
     Note in blueprint.md: "[file] has known gaps in [section]."
```

### 6.2 Scope Guard

```
Enforcement points:

1. Phase 3 (Define) - Feature selection:
   - V1 features capped at 5 maximum
   - If user proposes > 5: Force cut with explanation
   - Each feature must map to at least one JTBD
   - Features serving no job: Flag and suggest V2

2. Phase 4 (Specify) - Output validation:
   - Scope leak detection in completeness check
   - Any feature in solution.md not in definition.md V1: Remove
   - Any capability in user journeys not backed by V1 feature: Strip
   - Moved items go to V2 parking lot in versions.md

3. User-initiated additions:
   - If user asks to add a feature during Phase 4:
     "We have [N] V1 features. Adding this means cutting something else, 
      or it goes to V2. Which do you prefer?"
   - Never silently expand scope
```

### 6.3 Session Resume

```
On session start or context clear:

1. Check: does ttt_state.json exist in the working directory?

2. If NO: Fresh start.
   Check for blank input handling (joke + "What are we building?")

3. If YES: Read ttt_state.json
   Extract:
   - current.phase, current.status, current.substep
   - current.progress_label
   - session.last_action, session.next_action
   - List of files_generated across all phases
   
   Read the most recent output file for context.
   
   Greet user:
   "[progress_label]. Last time: [last_action]. 
    Next: [next_action]. Ready to continue?"
   
   User confirms -> Continue from next_action
   User wants to revisit -> Offer specific options based on phase
```

### 6.4 Progress Visibility

```
The Choreographer maintains natural language progress labels.
Never show "Phase 2 of 5" or "Step 3/7".
Always show what's happening in human terms.

Progress states and their labels:

CLARIFY:
- "Understanding what you want to build"
- "Narrowing down your idea"  
- "Idea is clear. Ready to validate."

VALIDATE:
- "Researching the market and your target users"
- "Analyzing what the research means for your idea"
- "Here's what I found. Your call on direction."

DEFINE:
- "Defining exactly who this is for"
- "Narrowing down the core problem"
- "Deciding what's v1 and what's later"
- "Getting your build and design preferences"
- "Problem, user, and solution are locked. Ready to specify."

SPECIFY:
- "Detailing the product flows and features"
- "Building out the technical architecture, design system, and test plan"
- "Checking everything fits together"
- "Spec is ready. You can start building."

LAUNCH:
- "Planning how to reach your first users"
- "Launch plan is ready."

Show at the start of each Choreographer message, naturally woven in.
Not as a header. Not as a status bar. As part of the conversation.

Example: "We've validated your idea and the market looks promising. 
Now I'm narrowing down exactly who we're building for."
```

### 6.5 Pivot Handling

```
When user chooses to pivot:

1. Log in ttt_state.json:
   - Increment pivot_count
   - Add to pivots array: from, to, reason, timestamp

2. Evaluate pivot scope:
   
   NARROW PIVOT (same market, different angle):
   - Update clarification.md (product thesis, possibly user)
   - Keep market_research.md, add "Pivot Addendum" section
   - Keep user_research.md (user is the same or similar)
   - Invalidate definition.md (will be rewritten in Phase 3)
   - Skip back to Phase 3
   
   BROAD PIVOT (different market or different user):
   - Update clarification.md substantially
   - Invalidate market_research.md (re-run Market Researcher)
   - Invalidate user_research.md (re-run User Researcher)
   - Re-enter Phase 2 with updated clarification.md
   
   USER-DIRECTED PIVOT (user gives specific new direction):
   - Choreographer assesses: is this narrow or broad?
   - If unclear, ask: "Is this the same audience with a different 
     product, or a completely different direction?"
   - Route accordingly

3. Preserve unchanged files. Rewrite only invalidated files.
4. Log in versions.md: what changed, why, which files affected
5. Update ttt_state.json with files_invalidated, files_preserved, files_rewritten
```

### 6.6 Context Management

```
Choreographer should recommend context clearing at these points:

1. After Phase 2 completes (research done, written to files):
   "Research is saved. Good point to clear context before we 
    move to defining the product."

2. After Phase 3 completes (definition locked):
   "Definition is locked. I recommend clearing context before 
    we generate the spec. Everything is in files."

3. After any pivot that triggers re-research:
   "We're re-researching with the new direction. Clear context 
    so I have fresh space for the new research."

On resume after clear: Choreographer reads ttt_state.json + 
relevant files to reconstruct working context.
```

### 6.7 Blank Input Handling

```
If user starts with no input, rotate through joke categories:

Categories (rotate, never repeat within session):
1. Philosophically Funny
2. Quirky & Weird  
3. Vibe-it Chaos
4. Sarcastic (But Gentle)

After joke, always end with: "So - what are we building?"

Store last_joke_category in ttt_state.json to avoid repeats.
```

---

## 7. INTERACTION RULES

### Question Rules
- Maximum 2 questions per message
- Lead with the most important question
- Never a wall of questions
- Do not ask if user already provided the information
- Use analogies for ambiguous choices
- Every menu has an open-ended escape option: "Or tell me something else entirely"

### Assumption Rules
- Every assumption stated immediately and clearly
- Confidence levels: high, medium, low
- Never let an assumption silently shape output
- Assumptions logged in ttt_state.json
- User can challenge any assumption at any time

### Honesty Rules
- If data is weak, say so: "This is from 2023. Treat as directional."
- If research fails, say so: "Couldn't find strong data here."
- If an idea is weak, say so: "This space is crowded. Here's what might work instead."
- Signal confidence on every claim: well-established vs directional vs estimated

### Tone Rules
- Plain language. No jargon without explanation.
- No padding. Every word earns its place.
- Opinionated. Challenge weak ideas with evidence.
- Respect the user's time over TTT's own completeness.
