# TTT Eval Protocol

Step-by-step guide for running a TTT evaluation. Use alongside `harness.py`.

---

## Prerequisites

- Python 3.10+ available
- TTT installed in a test project (Cursor or Claude Code)
- Scenario file selected from `evals/scenarios/`
- Rubric version noted (see header of `evals/rubric.md`)

---

## Step 1: Initialize the Run

```bash
python evals/harness.py new <scenario-id> [--variant <variant>]
```

Creates `evals/runs/{scenario}-{date}/` containing:
- Scenario script copy for reference
- Blank scorecard template
- Metadata (scenario, variant, rubric version, timestamp)

The harness prints the opening message. Copy it for Step 2.

## Step 2: Execute the Scenario

1. Open your agent (Cursor or Claude Code) in the test project.
2. Start TTT with the opening message from Step 1.
3. Follow the scripted turns (Turn 2, Turn 3 as specified in the scenario).
4. After scripted turns, continue as a reasonable user.
5. Complete the full run through Specify (or as far as TTT gets).
6. Watch for key checkpoints listed in the scenario — note which are hit.

## Step 3: Capture the Conversation

1. Copy the full conversation transcript from your agent.
2. Save it as a text file (you'll provide the path in Step 4).
3. Note any checkpoint observations and choices you made after scripted turns.

## Step 4: Collect Artifacts

```bash
python evals/harness.py collect <run-dir>
```

The harness will:
- Copy TTT artifacts from `ttt/` into the run bundle
- Copy `ttt_state.json` snapshot
- Prompt for your transcript (file path or paste)
- Record prompt file versions (SHA-256 checksums)

## Step 5: Score the Run

```bash
python evals/harness.py score <run-dir>
```

For each artifact in the bundle:
- Score each dimension 1–5 using `evals/rubric.md` anchor text as reference
- Add optional notes for diagnostic detail
- Record failure modes observed (from taxonomy or new)

After per-artifact scoring:
- Score 5 cross-file alignment passes (solution↔definition, tech↔solution, design↔solution, test↔solution, global)
- Review computed aggregates and pass/fail result

## Step 6: Record Observations

Open the scorecard at `<run-dir>/scorecard.md`:

- Add evaluator notes (surprises, patterns, context)
- Record failure modes with specific evidence
- Note which scenario checkpoints were hit or missed
- Flag any issues for prompt iteration

## Step 7: Compare Runs (Optional)

```bash
python evals/harness.py compare <run-dir-1> <run-dir-2>
```

Use after revising prompts and re-running a scenario:
- Dimension-by-dimension comparison with deltas
- Highlights improvements (+) and regressions (-)
- Flags rubric version mismatches between runs

---

## Evaluation Principles

- **Score AFTER the full run.** Don't score during the conversation.
- **Play the role naturally.** Don't optimize for high scores — play the scenario persona.
- **Be honest about failure modes.** The goal is finding weaknesses to fix, not proving quality.
- **Use rubric anchor text.** Score against the anchors in `evals/rubric.md`, not your intuition.
- **When in doubt, score 3.** "Partially meets" with notes beats an uncertain 4 or 2.
- **Document everything.** Checkpoint hits, unexpected behaviors, your choices — future you needs this.
