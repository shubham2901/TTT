#!/usr/bin/env python3
"""TTT Eval Harness — CLI tool for managing evaluation runs."""

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
SCENARIOS_DIR = EVALS_DIR / "scenarios"
RUNS_DIR = EVALS_DIR / "runs"
RUBRIC_PATH = EVALS_DIR / "rubric.md"
SCORECARD_PATH = EVALS_DIR / "scorecard.md"
PROMPTS_DIR = EVALS_DIR.parent / "prompts"

ARTIFACTS = [
    "clarification.md", "market_research.md", "user_research.md",
    "definition.md", "solution.md", "tech_architecture.md",
    "design_guideline.md", "test_eval.md", "coding_agent_prompt.md",
]
DIMENSIONS = ["coherence", "specificity", "relevance", "comprehensiveness", "actionability"]

# Per-artifact dimension weights from rubric.md v1.0.
# clarification.md has relevance=0 (first artifact, no upstream).
WEIGHTS = {
    "clarification.md":       [0.25, 0.30, 0.00, 0.25, 0.20],
    "market_research.md":     [0.15, 0.20, 0.20, 0.30, 0.15],
    "user_research.md":       [0.15, 0.20, 0.20, 0.30, 0.15],
    "definition.md":          [0.25, 0.25, 0.20, 0.15, 0.15],
    "solution.md":            [0.20, 0.20, 0.15, 0.20, 0.25],
    "tech_architecture.md":   [0.20, 0.15, 0.15, 0.20, 0.30],
    "design_guideline.md":    [0.20, 0.20, 0.15, 0.20, 0.25],
    "test_eval.md":           [0.15, 0.20, 0.15, 0.25, 0.25],
    "coding_agent_prompt.md": [0.25, 0.15, 0.15, 0.20, 0.25],
}
CROSS_FILE_PASSES = [
    "solution ↔ definition", "tech ↔ solution", "design ↔ solution",
    "test ↔ solution", "Global consistency",
]


def _weight(artifact: str, dim_idx: int) -> float:
    return WEIGHTS.get(artifact, [0.2] * 5)[dim_idx]


def get_rubric_version() -> str:
    if not RUBRIC_PATH.exists():
        return "unknown"
    for line in RUBRIC_PATH.read_text().splitlines():
        if "**Version:**" in line:
            return line.split("**Version:**")[1].strip()
    return "unknown"


def extract_opening(text: str) -> str:
    match = re.search(r'\*\*User:\*\*\s*"([^"]+)"', text)
    return match.group(1) if match else "(could not extract — check scenario file)"


def file_checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def prompt_int(label: str, lo: int = 1, hi: int = 5) -> int:
    while True:
        raw = input(f"  {label} ({lo}-{hi}): ").strip()
        try:
            val = int(raw)
            if lo <= val <= hi:
                return val
        except ValueError:
            pass
        print(f"  Enter a number between {lo} and {hi}.")


def cmd_new(args):
    scenario_path = SCENARIOS_DIR / f"{args.scenario_id}.md"
    if not scenario_path.exists():
        print(f"Error: scenario not found at {scenario_path}")
        sys.exit(1)

    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    run_dir = RUNS_DIR / f"{args.scenario_id}-{stamp}"
    run_dir.mkdir(parents=True)

    shutil.copy2(scenario_path, run_dir / "scenario.md")
    if SCORECARD_PATH.exists():
        shutil.copy2(SCORECARD_PATH, run_dir / "scorecard.md")

    metadata = {
        "scenario_id": args.scenario_id,
        "variant": args.variant,
        "created_at": datetime.now().isoformat(),
        "rubric_version": get_rubric_version(),
    }
    (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    opening = extract_opening(scenario_path.read_text())
    print(f"Run initialized: {run_dir}")
    print(f'\nOpening message:\n  "{opening}"')
    print(f"\nFollow the scenario script in {run_dir}/scenario.md")


def cmd_collect(args):
    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        print(f"Error: run directory not found at {run_dir}")
        sys.exit(1)

    artifact_root = Path("ttt")
    if not artifact_root.exists():
        raw = input("ttt/ not found. Enter artifact root path: ").strip()
        artifact_root = Path(raw)
        if not artifact_root.exists():
            print(f"Error: {artifact_root} does not exist")
            sys.exit(1)

    arts_dir = run_dir / "artifacts"
    arts_dir.mkdir(exist_ok=True)

    count = 0
    for f in sorted(artifact_root.iterdir()):
        if f.is_file() and f.suffix in (".md", ".json"):
            shutil.copy2(f, arts_dir / f.name)
            count += 1

    state_file = artifact_root / "ttt_state.json"
    if state_file.exists():
        shutil.copy2(state_file, run_dir / "state_snapshot.json")

    raw = input("Paste transcript file path (or press Enter to paste directly): ").strip()
    if raw:
        src = Path(raw)
        if src.exists():
            shutil.copy2(src, run_dir / "transcript.md")
        else:
            print(f"Warning: {src} not found — skipping transcript")
    else:
        print("Paste transcript below. End with a line containing only 'END':")
        lines = []
        for line in sys.stdin:
            if line.strip() == "END":
                break
            lines.append(line)
        (run_dir / "transcript.md").write_text("".join(lines))

    versions = {}
    if PROMPTS_DIR.exists():
        for p in sorted(PROMPTS_DIR.glob("*.md")):
            versions[p.name] = file_checksum(p)
    (run_dir / "prompt_versions.json").write_text(json.dumps(versions, indent=2) + "\n")

    print(f"Artifacts collected: {count} files")


def cmd_score(args):
    run_dir = Path(args.run_dir)
    arts_dir = run_dir / "artifacts"
    if not arts_dir.exists():
        print(f"Error: no artifacts directory in {run_dir}")
        sys.exit(1)

    present = [a for a in ARTIFACTS if (arts_dir / a).exists()]
    if not present:
        print("No recognized artifacts found in artifacts/.")
        sys.exit(1)

    results = {}
    all_pass = True
    print(f"\nScoring {len(present)} artifacts. Refer to evals/rubric.md for anchor text.\n")

    for artifact in present:
        print(f"── {artifact} ──")
        scores = {}
        for i, dim in enumerate(DIMENSIONS):
            w = _weight(artifact, i)
            if w == 0.0:
                scores[dim] = {"score": None, "weight": 0.0, "notes": "N/A"}
                continue
            s = prompt_int(dim)
            notes = input("  Notes (optional): ").strip()
            scores[dim] = {"score": s, "weight": w, "notes": notes}
            if s < 3:
                all_pass = False
        modes_raw = input("  Failure modes observed (comma-separated, or Enter for none): ").strip()
        failure_modes = [m.strip() for m in modes_raw.split(",") if m.strip()] if modes_raw else []
        weighted = sum(d["score"] * d["weight"] for d in scores.values() if d["score"] is not None)
        results[artifact] = {"scores": scores, "weighted_score": round(weighted, 2), "failure_modes": failure_modes}
        print(f"  Weighted score: {weighted:.2f}\n")

    print("── Cross-File Alignment ──")
    cross_file = {}
    for pass_name in CROSS_FILE_PASSES:
        s = prompt_int(pass_name)
        notes = input("  Notes (optional): ").strip()
        cross_file[pass_name] = {"score": s, "notes": notes}
        if s < 3:
            all_pass = False

    cross_avg = sum(p["score"] for p in cross_file.values()) / len(cross_file)
    artifact_agg = sum(r["weighted_score"] for r in results.values()) / len(results)
    overall = artifact_agg * 0.7 + cross_avg * 0.3
    passed = all_pass and overall >= 3.0

    output = {
        "rubric_version": get_rubric_version(),
        "artifacts": results,
        "cross_file_alignment": cross_file,
        "aggregate_score": round(artifact_agg, 2),
        "cross_file_average": round(cross_avg, 2),
        "overall_score": round(overall, 2),
        "pass": passed,
    }
    (run_dir / "scores.json").write_text(json.dumps(output, indent=2) + "\n")
    _write_scorecard(run_dir, output)

    print(f"\n{'=' * 40}")
    print(f"Artifact aggregate: {artifact_agg:.2f}  Cross-file: {cross_avg:.2f}  Overall: {overall:.2f}")
    print(f"Pass/Fail: {'PASS' if passed else 'FAIL'}")
    print(f"Scores → {run_dir / 'scores.json'}  Scorecard → {run_dir / 'scorecard.md'}")


def _write_scorecard(run_dir, data):
    meta_path = run_dir / "metadata.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    L = [
        "# TTT Eval Scorecard", "",
        f"**Run ID:** {run_dir.name} | **Scenario:** {meta.get('scenario_id', '?')} {meta.get('variant') or ''}".rstrip(),
        f"**Evaluator:** _(fill in)_ | **Rubric version:** {data['rubric_version']} | **Date:** {datetime.now().strftime('%Y-%m-%d')}",
    ]
    for artifact, info in data["artifacts"].items():
        L += ["", f"## {artifact}", "| Dimension | Score (1–5) | Notes |", "|-----------|-------------|-------|"]
        for dim in DIMENSIONS:
            d = info["scores"].get(dim, {})
            sc = "N/A" if d.get("score") is None else str(d["score"])
            L.append(f"| {dim.capitalize()} | {sc} | {d.get('notes', '')} |")
        modes = ", ".join(info.get("failure_modes", [])) or "none"
        L.append(f"**Weighted:** {info['weighted_score']:.2f} | **Failure modes:** {modes}")
    L += ["", "## Cross-File Alignment", "| Pass | Score (1–5) | Notes |", "|------|-------------|-------|"]
    for pn, info in data["cross_file_alignment"].items():
        L.append(f"| {pn} | {info['score']} | {info.get('notes', '')} |")
    L.append(f"**Cross-file average:** {data['cross_file_average']:.2f}")
    L += [
        "", "## Summary",
        f"**Artifact aggregate:** {data['aggregate_score']:.2f} | **Cross-file:** {data['cross_file_average']:.2f} | **Overall:** {data['overall_score']:.2f}",
        f"**Pass/Fail:** {'PASS' if data['pass'] else 'FAIL'}",
        "", "### Strengths", "-", "", "### Weaknesses", "-",
        "", "### Failure modes observed", "-", "", "### Evaluator notes", "-",
    ]
    (run_dir / "scorecard.md").write_text("\n".join(L) + "\n")


# ── compare ──────────────────────────────────────────────────────────────


def cmd_compare(args):
    dir1, dir2 = Path(args.run_dir_1), Path(args.run_dir_2)
    scores = []
    for d in (dir1, dir2):
        p = d / "scores.json"
        if not p.exists():
            print(f"Error: scores.json not found in {d}"); sys.exit(1)
        scores.append(json.loads(p.read_text()))
    s1, s2 = scores
    if s1.get("rubric_version") != s2.get("rubric_version"):
        print(f"Warning: rubric version mismatch — {s1.get('rubric_version')} vs {s2.get('rubric_version')}\n")
    all_arts = sorted(set(list(s1["artifacts"]) + list(s2["artifacts"])))
    print(f"{'Artifact':<26} {'Dimension':<20} {'Run 1':>6} {'Run 2':>6} {'Delta':>6}")
    print("-" * 66)
    for art in all_arts:
        a1 = s1["artifacts"].get(art, {}).get("scores", {})
        a2 = s2["artifacts"].get(art, {}).get("scores", {})
        for dim in DIMENSIONS:
            v1 = a1.get(dim, {}).get("score")
            v2 = a2.get(dim, {}).get("score")
            if v1 is None and v2 is None:
                continue
            v1s, v2s = (str(v1) if v1 is not None else "-"), (str(v2) if v2 is not None else "-")
            delta = ""
            if v1 is not None and v2 is not None:
                d = v2 - v1
                delta = f"+{d}" if d > 0 else str(d) if d < 0 else "0"
            print(f"{art:<26} {dim:<20} {v1s:>6} {v2s:>6} {delta:>6}")
    print("-" * 66)
    for label, key in [("Aggregate", "aggregate_score"), ("Cross-file", "cross_file_average"), ("Overall", "overall_score")]:
        print(f"{label:<26} {'':20} {s1[key]:>6.2f} {s2[key]:>6.2f} {s2[key] - s1[key]:>+6.2f}")
    print(f"{'Pass/Fail':<26} {'':20} {'PASS' if s1['pass'] else 'FAIL':>6} {'PASS' if s2['pass'] else 'FAIL':>6}")


def main():
    parser = argparse.ArgumentParser(
        prog="harness.py",
        description="TTT Eval Harness — manage evaluation runs",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="Initialize a new eval run")
    p_new.add_argument("scenario_id", help="Scenario ID (e.g. s1-clear-idea)")
    p_new.add_argument("--variant", default=None, help="Scenario variant (e.g. a, b)")

    p_collect = sub.add_parser("collect", help="Collect artifacts into run bundle")
    p_collect.add_argument("run_dir", help="Path to run directory")

    p_score = sub.add_parser("score", help="Score a completed run")
    p_score.add_argument("run_dir", help="Path to run directory")

    p_compare = sub.add_parser("compare", help="Compare two scored runs")
    p_compare.add_argument("run_dir_1", help="First run directory")
    p_compare.add_argument("run_dir_2", help="Second run directory")

    args = parser.parse_args()
    commands = {
        "new": cmd_new,
        "collect": cmd_collect,
        "score": cmd_score,
        "compare": cmd_compare,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
