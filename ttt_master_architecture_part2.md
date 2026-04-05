# TTT Architecture Part 2: File Structures and Schemas

---

## 8. FILE STRUCTURES

### 8.1 ttt_state.json

Written by: Choreographer (after every phase transition, decision, pivot, retry)
Read by: Choreographer (on session resume, crash recovery, phase transitions)
Format: JSON (machine-parseable)

```json
{
  "version": "1.0",
  "product_thesis": "AI tool that helps indie YouTube creators turn long videos into Shorts",
  
  "current": {
    "phase": "define",
    "status": "in_progress",
    "substep": "scoping_v1_features",
    "progress_label": "Deciding what's v1 and what's later"
  },

  "phases": {
    "clarify": {
      "status": "complete",
      "completed_at": "2026-04-04T14:20:00Z",
      "output_files": ["clarification.md"]
    },
    "validate": {
      "status": "complete",
      "completed_at": "2026-04-04T14:45:00Z",
      "output_files": ["market_research.md", "user_research.md"],
      "agents_used": [
        {"name": "market_researcher", "attempts": 2, "final_status": "pass"},
        {"name": "user_researcher", "attempts": 1, "final_status": "pass"}
      ]
    },
    "define": {
      "status": "in_progress",
      "started_at": "2026-04-04T14:50:00Z",
      "output_files": [],
      "agents_used": []
    },
    "specify": {
      "status": "not_started",
      "output_files": [],
      "agents_used": []
    },
    "launch": {
      "status": "not_started",
      "output_files": [],
      "agents_used": []
    }
  },

  "decisions": [
    {
      "decision": "Target user narrowed to indie YouTube creators under 10K subs",
      "phase": "clarify",
      "timestamp": "2026-04-04T14:15:00Z",
      "source": "user"
    },
    {
      "decision": "Web app chosen over mobile. Creators work on laptops.",
      "phase": "clarify",
      "timestamp": "2026-04-04T14:18:00Z",
      "source": "assumption",
      "confidence": "medium"
    }
  ],

  "assumptions": [
    {
      "assumption": "English-only for v1",
      "confidence": "high",
      "made_in_phase": "clarify",
      "validated": false
    },
    {
      "assumption": "No mobile app for v1",
      "confidence": "medium",
      "made_in_phase": "clarify",
      "validated": true,
      "validated_by": "user confirmed in define phase"
    }
  ],

  "scope": {
    "v1_features": [
      "Upload long video and auto-detect highlight moments",
      "Generate 3 vertical Shorts with captions",
      "One-click export to YouTube"
    ],
    "v2_parking_lot": [
      {
        "feature": "Batch processing multiple videos",
        "reason": "Scope. Ship single-video first.",
        "added_in": "define"
      }
    ],
    "out_of_scope": [
      {
        "feature": "TikTok/Instagram export",
        "reason": "YouTube-only for v1 focus"
      }
    ]
  },

  "pivots": [
    {
      "pivot_number": 1,
      "timestamp": "2026-04-04T14:42:00Z",
      "from": "AI tool for creators",
      "to": "AI tool for indie YouTube creators to turn long videos into Shorts",
      "reason": "50+ generic creator tools. Whitespace in YouTube-specific short-form.",
      "files_invalidated": ["market_research.md"],
      "files_preserved": ["clarification.md"],
      "files_rewritten": ["market_research.md"]
    }
  ],

  "retry_history": [
    {
      "agent": "market_researcher",
      "phase": "validate",
      "attempt": 1,
      "timestamp": "2026-04-04T14:30:00Z",
      "failure_reason": "Only 1 direct competitor found. Minimum is 2.",
      "resolved": true,
      "resolution": "Re-ran with broader terms. Found 3 direct competitors."
    }
  ],

  "gap_assessments": {
    "define_to_specify": {
      "ran": true,
      "timestamp": "2026-04-04T15:10:00Z",
      "results": {
        "whitespace_alignment": "pass",
        "jtbd_alignment": "pass",
        "user_cohort_consistency": "pass",
        "timing_check": "pass",
        "scope_vs_competitor_weakness": "fail",
        "feature_job_mapping": "pass"
      },
      "failures_acknowledged": [
        {
          "check": "scope_vs_competitor_weakness",
          "detail": "No V1 feature directly targets competitor weakness",
          "user_response": "Acknowledged. Competing on UX simplicity instead."
        }
      ]
    },
    "spec_completeness": {
      "ran": false,
      "results": null
    }
  },

  "vibe_it": {
    "used": false,
    "triggered_at_phase": null,
    "assumptions_made": []
  },

  "session": {
    "last_active": "2026-04-04T14:55:00Z",
    "last_action": "User reviewing V1 feature list for scope cut",
    "next_action": "Finalize V1 features, collect build preferences, complete definition.md",
    "context_clear_recommended": false,
    "last_joke_category": null
  }
}
```

---

### 8.2 clarification.md

Written by: Choreographer (Phase 1)
Read by: Market Researcher, User Researcher, Choreographer (all subsequent phases)

```markdown
# Clarification

## Product Thesis
[One line. Not a paragraph. One line.]

## Goal Type
Primary: [exactly one of: Engagement, Monetisation, Retention, Task Success]
Secondary: [optional, one of the above]
Success signal: [one measurable outcome for v1]

## Target User
Specificity score: [1-10, with justification]
Description: [As specific as possible]

## Platform
Choice: [web app | mobile app | desktop app | CLI | browser extension | agent | other]
Rationale: [Why this platform fits this user]

## Location/Market
Relevant: [yes/no]
If yes: [geographic or market context]

## Constraints
Build context: [0-to-1 | building on existing platform]
If existing platform: [name and what it does]
Builder profile: [solo vibecoder | small team | team with designers]
Timeline: [if any]
Tech comfort: [relevant tech skills or lack thereof]

## Assumptions Made
- "[assumption text]" (confidence: high/medium/low)
- "[assumption text]" (confidence: high/medium/low)
```

Quality gate: Product thesis = one sentence. Goal type = exactly one primary. Specificity score >= 6 to proceed. Platform has rationale. All assumptions listed.

---

### 8.3 market_research.md

Written by: Market Researcher subagent (Phase 2)
Read by: Choreographer (synthesis), User Researcher (context), all Phase 4 agents

```markdown
# Market Research

## Research Metadata
Sources used: [list of source types used]
Data confidence: [strong/moderate/weak]
Date of research: [timestamp]

## Industry Analysis (Porter's Five Forces)

### 1. Threat of New Entrants
- [point with evidence and source]
(minimum 1, maximum 4 points per force)

### 2. Bargaining Power of Suppliers
- [point with evidence and source]

### 3. Bargaining Power of Buyers
- [point with evidence and source]

### 4. Threat of Substitutes
- [point with evidence and source]

### 5. Industry Rivalry
- [point with evidence and source]

### Porter's Summary
[2-3 sentences. Is this an attractive industry to enter? Why or why not?]

## Competitor Analysis

### Direct Competitors

#### Competitor 1: [Name]
**What they do:** [one line]
**User base:** [size] (confidence: verified/estimated/unknown)
**Pricing:** [model and price points]
**SWOT:**
- Strengths: [1-3 points]
- Weaknesses: [1-3 points]
- Opportunities: [1-3 points]
- Threats: [1-3 points]

[Repeat for each direct competitor. Minimum 2, great is 3.]

### Indirect Competitors

#### Indirect 1: [Name]
**What they do:** [one line]
**Why indirect:** [how they partially solve the same problem]
**SWOT:** [same structure, can be briefer]

[Repeat for each indirect. Great is 2.]

(Total competitors: minimum 2 direct. Great: 3 direct + 2 indirect. Maximum 8 total.)

## Business Model Canvas

### Customer Segments
[Who pays, who uses]

### Value Propositions
[Core value delivered]

### Channels
[How the product reaches users]

### Customer Relationships
[Self-service, automated, personal]

### Revenue Streams
[How money is made, if applicable for v1]

### Key Resources
[What's needed to deliver the value]

### Key Activities
[What the product must do well]

### Key Partnerships
[External dependencies: APIs, platforms, data sources]

### Cost Structure
[Major costs for building and running]

## Whitespace Analysis

### Whitespace 1: [title]
Gap: [What competitors are ignoring]
Evidence: [User complaints, missing features, underserved segment with source]
Opportunity size: [large/medium/small with reasoning]

### Whitespace 2: [title]
[same structure]

### Whitespace 3: [title]
[same structure]

(Minimum 3. If fewer than 3 genuine whitespaces exist, state that explicitly.)

## Timing Assessment

### Supporting Trends
- [trend with evidence and source]

### Opposing Trends
- [trend with evidence and source]

### Timing Verdict
[Is now a good time? One paragraph with clear reasoning.]

## Data Confidence Notes
- "[data point]" -- [confidence note: estimated, stale, unverified]

## Sources
[Links and references used]
```

Quality gates: Porter's = all 5 forces, 1-4 points each. Competitors = min 2 direct, full SWOT 1-3 per factor. BMC = all 9 blocks. Whitespace = min 3 with evidence. Timing = both supporting and opposing.

---

### 8.4 user_research.md

Written by: User Researcher subagent (Phase 2)
Read by: Choreographer (synthesis), Define phase, all Phase 4 agents

```markdown
# User Research

## Research Metadata
Sources used: [list]
Data confidence: [strong/moderate/weak]
Date of research: [timestamp]

## User Profile
From clarification: [copy target user description]
Refined: [refinements based on research]

## Needs Analysis (Maslow's Hierarchy)

Only include levels that are relevant. Do not force-fit. Mark irrelevant levels explicitly.

### Physiological
[If relevant to the product. Otherwise: "Not directly relevant to this product."]

### Safety
[Financial security, health, stability needs the product touches]

### Love/Belonging
[Community, connection, peer recognition needs]

### Esteem
[Achievement, status, recognition, confidence needs]

### Self-Actualisation
[Creative fulfilment, mastery, purpose needs]

### Needs Summary
Primary need level: [which level the product primarily serves]
Secondary: [if applicable]

## Desires Analysis (Reiss's 16 Basic Desires)

Select 3-5 most relevant desires. Do not list all 16. Justify each.

### [Desire name, e.g., "Independence"]
Relevance: [How this desire connects to the product/user]
Intensity: [high/medium/low for this user segment]

### [Desire name]
Relevance: [explanation]
Intensity: [level]

### [Desire name]
[same structure]

(3-5 desires only. Each justified.)

## Compulsions Analysis (Seven Sins Framework)

Not all products have compulsion loops. Be honest if none apply.

### Applicable Compulsions
- **[Sin name]**: [how it manifests in user behavior]. Ethical note: [whether to leverage or avoid, and why]

### Not Applicable
[List sins that don't apply and briefly why]

## Jobs To Be Done

### Job 1: "[When I..., I want to..., so I can...]"

**Functional job:** [The practical task]
**Emotional job:** [How they want to feel]
**Psychological job:** [The deeper why]
**Current workaround:** [How they solve this today]
**Pain level of workaround:** [high/medium/low]

### Job 2: "[When I..., I want to..., so I can...]"
[same structure]

(Minimum 2 jobs, maximum 5. All three layers required for each.)

## User Behavior Patterns
[When do they do this task, how often, what triggers it, what tools they use now]

## Key Quotes / Evidence
- "[quote]" -- [source with link]
- "[quote]" -- [source with link]
(Minimum 2 sourced quotes)

## Assumptions
- "[assumption]" (confidence: high/medium/low)
```

Quality gates: Maslow's = 2+ levels with substance. Reiss = 3-5 justified. Compulsions = 1 or explicit none. JTBD = min 2 with all 3 layers. Quotes = min 2 sourced.

---

### 8.5 definition.md

Written by: Choreographer (Phase 3)
Read by: All Phase 4 subagents, Choreographer (for validation checks)

```markdown
# Definition

## User Cohort
[Exact user. Maximum specificity. Refined from clarification + research.]

## Primary Problem
Statement: [One specific friction or struggle. One. Not three.]
Evidence: [Which JTBD, which need, which pain point from research]
Current workaround: [How they solve it today]
Why workaround fails: [Specific friction points]

## Solution Direction
Approach: [High-level strategic direction]
Why now: [Timing + whitespace from market research]
Why this user: [Why this cohort, not broader]

## Scope Guard

### V1 Features (maximum 5)
1. [Feature]: [one-line description]
2. [Feature]: [one-line description]
3. [Feature]: [one-line description]
(3-5 features. Each must map to a JTBD.)

### V2 Parking Lot
- [Feature]: [why v2, not v1] (added during: [phase])
- [Feature]: [why v2] (added during: [phase])

### Out of Scope
- [Feature]: [why excluded entirely]

## Build Preferences

### Tech Preferences
- Framework: [choice or "Take the best call"]
- Backend: [choice or "Take the best call"]
- Database: [choice or "Take the best call"]
- Auth: [choice or "Take the best call"]
- Hosting: [choice or "Take the best call"]

### Design Preferences
- Reference apps: [2-3 apps from same industry user wants to look like]
- UI density: [minimal/moderate/dense or "Take the best call"]
- Key UX priority: [speed | beauty | information density | simplicity]

### Vibecoding Context
- Solo or team: [from clarification]
- Primary coding agent: [Cursor | Claude Code | Windsurf | other]
- Ship target: [timeline if any]

## Success Metric
[One metric. Measurable. Time-bound if possible.]

## Assumptions
- "[assumption]" (confidence: high/medium/low)
```

Quality gates: User cohort specificity >= 7. Exactly one primary problem. V1 features <= 5. Every feature maps to a JTBD. V2 parking lot exists. Build preferences all filled. Success metric is measurable.

---

### 8.6 solution.md

Written by: Product Detailer subagent (Phase 4, Wave 1)
Read by: Design Advisor, Test & Eval Generator, Choreographer

```markdown
# Solution

## Core User Journeys

### Journey 1: Onboarding
1. [User action] -> [System response]
2. [User action] -> [System response]
Goal: [What successful onboarding looks like]
Time target: [How long this should take]

### Journey 2: Activation (First value moment)
[same structure]

### Journey 3: Core Loop
[same structure]

### Journey 4: Retention Loop
[same structure]

## Feature Specification (V1 only)

### Feature 1: [Name]
**User action:** [What the user does]
**System response:** [What happens]
**Edge cases:**
- [Edge case 1]: [How system handles it]
- [Edge case 2]: [How system handles it]
**Acceptance criteria:**
- [Criterion 1]
- [Criterion 2]

[Repeat for every V1 feature from definition.md. No extras.]

## Screen/View Inventory
- [Screen 1]: [purpose, key elements]
- [Screen 2]: [purpose, key elements]

## State Definitions
- Empty state: [What user sees with no data]
- Loading state: [What user sees during processing]
- Error state: [What user sees on failure]
- Success state: [What user sees on completion]

## V2 Parking Lot
[Carried from definition.md. Add any new ideas surfaced during detailing.]
- [Feature]: [why v2]
```

---

### 8.7 tech_architecture.md

Written by: Tech Architect subagent (Phase 4, Wave 2)
Read by: Choreographer, coding agent

```markdown
# Tech Architecture

## Stack Decision

### Frontend
Choice: [exact framework and version]
Rationale: [why, considering vibecoding + extensibility + docs]

### Backend
Choice: [framework]
Rationale: [why]

### Database
Choice: [DB]
Rationale: [why]

### Auth
Choice: [approach]
Rationale: [why]

### Hosting
Choice: [platform]
Rationale: [why]

### Key Libraries
- [Library]: [purpose]

## Data Models

### [Model name]
field_name: type (constraints)
field_name: type (constraints)

[Repeat for all models needed by V1 features]

## API / Route Structure
- [METHOD /path]: [purpose, input, output]

## External Dependencies
- [API/service]: [purpose, pricing note if relevant]

## Infrastructure Notes
[Setup instructions, env vars, deployment notes for coding agent]
```

---

### 8.8 design_guideline.md

Written by: Design Advisor subagent (Phase 4, Wave 2)
Read by: Choreographer, coding agent

```markdown
# Design Guidelines

## UX Philosophy
[2-3 principles. Specific to this product. Not generic.]

## Design References
- Primary: [App] -- [what to borrow: layout, typography, color, interaction]
- Secondary: [App] -- [what to borrow]

## Layout
### Primary View
[Main screen layout description]

### Secondary Views
[Other key views]

## Component Patterns
- [Component]: [description, states, interaction]

## Typography Scale
[Sizes, weights, fonts]

## Color System
[Primary, secondary, accent, semantic]
[Dark mode: yes/no/later]

## Spacing System
[Base unit, scale]

## Key States
- Empty: [visual approach]
- Loading: [approach: skeleton/spinner/progressive]
- Error: [approach: inline/toast/modal]
- Success: [approach]

## Responsive Behavior
[Adaptation rules, breakpoints, mobile considerations]
```

---

### 8.9 test_eval.md

Written by: Test & Eval Generator subagent (Phase 4, Wave 2)
Read by: Choreographer, coding agent

```markdown
# Test Cases and Evaluation Criteria

## Acceptance Tests

### Feature 1: [Name]
| Test ID | Scenario | Input | Expected Output | Priority |
|---------|----------|-------|-----------------|----------|
| T1.1 | Happy path | [input] | [expected] | Must |
| T1.2 | Edge case | [input] | [expected] | Must |
| T1.3 | Error case | [input] | [expected] | Should |

[Repeat for every V1 feature]

## User Journey Tests
| Journey | Steps to verify | Success criteria |
|---------|----------------|-----------------|
| Onboarding | [steps] | [criteria] |
| Activation | [steps] | [criteria] |
| Core Loop | [steps] | [criteria] |
| Retention | [steps] | [criteria] |

## Performance Benchmarks
- [Metric]: [target]

## V1 Success Evaluation
Metric: [from definition.md]
How to measure: [method]
Target: [number]
Timeline: [when to evaluate]

## What Good Looks Like
[Qualitative success description]

## What Failure Looks Like
[Failure modes to watch for]
```

---

### 8.10 coding_agent_prompt.md

Written by: Choreographer (Phase 4, after all subagents complete)
Read by: User's coding agent (Cursor, Claude Code, etc.)

```markdown
# Coding Agent Prompt

You are building [product thesis].

## Read These Files First
1. solution.md
2. tech_architecture.md
3. design_guideline.md
4. test_eval.md

## Stack
[Copied from tech_architecture.md]

## Folder Structure
[Proposed project structure]

## Build Order
1. [First: project init, DB setup]
2. [Second: data models]
3. [Third: core feature end-to-end]
[Ordered by dependency]

## Rules
- Follow design_guideline.md for all UI
- Implement all states: empty, loading, error, success
- Write tests matching test_eval.md
- Do not build features not in solution.md V1
- If unclear, check definition.md before asking

## V2 Parking Lot (Do NOT build)
[From definition.md + versions.md]
```

---

### 8.11 blueprint.md

Written by: Choreographer (Phase 4, final assembly)

```markdown
# Blueprint

## Product
[One-line thesis]

## File Manifest
| File | Purpose | Generated in Phase |
|------|---------|-------------------|
| ttt_state.json | Session state and progress | All phases |
| clarification.md | Idea clarity and constraints | Phase 1 |
| market_research.md | Industry and competitive analysis | Phase 2 |
| user_research.md | User needs and jobs analysis | Phase 2 |
| definition.md | User, problem, solution, scope | Phase 3 |
| solution.md | Product flows and features | Phase 4 |
| tech_architecture.md | Stack and data models | Phase 4 |
| design_guideline.md | UX and visual rules | Phase 4 |
| test_eval.md | Acceptance criteria and eval | Phase 4 |
| coding_agent_prompt.md | Day 0 prompt for coding agent | Phase 4 |
| launch.md | Distribution and metrics | Phase 5 (optional) |
| versions.md | Changelog and pivot history | All phases |

## How Files Connect
clarification.md -> market_research.md + user_research.md (parallel input)
Both research files -> definition.md (Choreographer synthesizes)
definition.md -> solution.md (Wave 1)
solution.md + definition.md -> tech_architecture.md + design_guideline.md + test_eval.md (Wave 2, parallel)
All Phase 4 files -> coding_agent_prompt.md (Choreographer assembles)

## Reading Order
1. clarification.md
2. market_research.md
3. user_research.md
4. definition.md
5. solution.md
6. tech_architecture.md + design_guideline.md
7. test_eval.md
8. coding_agent_prompt.md
```

---

### 8.12 versions.md

Written by: Choreographer (on every pivot, scope change, phase completion)

```markdown
# Version History

## Current: v0.1 (In Progress)

### Changelog
- [date] Phase 1 complete. Thesis: "[thesis]"
- [date] Phase 2 complete. Pivot from "[old]" to "[new]". Reason: [why]
- [date] Phase 3 complete. [N] v1 features, [M] parked for v2.
- [date] Phase 4 complete. Spec generated.

### V2 Parking Lot
- [Feature]: [reason for deferral] (added in [phase])

### Scope Changes
- [date]: "[Feature]" moved v1 -> v2. Reason: [reason]
```

---

### 8.13 launch.md (Optional, Phase 5)

Written by: Choreographer

```markdown
# Launch Plan

## Distribution
- Channel 1: [approach, expected yield for first 100 users]
- Channel 2: [approach, expected yield]

## Infrastructure
[Hosting, domain, monitoring, error tracking]

## Metrics
### 30-day targets
- [Metric]: [target]

### 90-day targets
- [Metric]: [target]

## V2 Triggers
- [Signal that it's time to build v2]
```

---

## 9. WHAT'S REMAINING TO BUILD

After reading these two files, a coding agent needs to build:

### Must Build (Core Skill)
1. **Skill file (SKILL.md)** - The entry point that describes TTT to the coding agent runtime and contains or references the Choreographer prompt
2. **Choreographer agent prompt** - The full system prompt with all phase logic, quality gates, gap assessments, scope guard rules, retry logic, progress labels, pivot handling, Vibe it!! heuristics, blank input handling, and interaction rules
3. **Market Researcher agent prompt** - System prompt with Porter's, SWOT, BMC, whitespace, timing instructions and source quality rules
4. **User Researcher agent prompt** - System prompt with Maslow's, Reiss, Seven Sins, JTBD instructions and source quality rules
5. **Product Detailer agent prompt** - System prompt for user journeys, feature specs, edge cases, screen inventory, states
6. **Tech Architect agent prompt** - System prompt for stack decisions, data models, API routes, "Take the best call" heuristics
7. **Design Advisor agent prompt** - System prompt for UX philosophy, references, layout, typography, color, spacing, states
8. **Test & Eval Generator agent prompt** - System prompt for acceptance tests, journey tests, benchmarks, success criteria
9. **File generation templates** - Logic for creating each output file with proper structure
10. **Quality gate validation logic** - Checks that run after each agent returns output
11. **Gap assessment logic** - Define-to-Specify check and Spec Completeness check
12. **ttt_state.json management** - Read/write/update logic for state persistence

### Should Build (Important but not blocking)
13. **Session resume flow** - Reading ttt_state.json and reconstructing context on new session
14. **Retry orchestration** - The retry-with-feedback loop, max 3 attempts, user escalation
15. **Pivot handling flow** - Narrow vs broad pivot detection, file invalidation, selective re-research
16. **Context clear recommendations** - When and how to suggest clearing context

### Build Later
17. **Quick mode** - Targeted updates to individual files without full re-run
18. **Config/settings** - Toggle agents, change research depth, model profiles
19. **GSD bridge command** - Convert TTT outputs to GSD-compatible format
20. **Joke bank** - Rotating witty openers for blank input (can start with a few hardcoded)

### Not Defined Yet (Needs Future Design)
21. **How the skill file triggers the Choreographer** - Depends on target runtime (Claude Code skill format vs Cursor rules vs other)
22. **Subagent spawning mechanism** - Exact syntax for spawning subagents in the target runtime
23. **Web search integration for research agents** - How research agents access web search (runtime-dependent)
24. **File write permissions and directory structure** - Where TTT writes its files relative to the user's project
25. **Error handling for runtime-specific failures** - What happens if the runtime doesn't support subagents
