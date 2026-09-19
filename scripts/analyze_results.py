"""Descriptive diagnostics; does not change the frozen report or primary estimand."""

from __future__ import annotations

import argparse
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    root = args.run
    with gzip.open(root / "trajectories.jsonl.gz", "rt") as f:
        records = [json.loads(line) for line in f]
    summary = json.loads((root / "summary.json").read_text())
    if not summary["complete"]:
        raise SystemExit("Only analyze the completed matrix")
    groups = defaultdict(list)
    failures = []
    for r in records:
        groups[(r["policy"], r["schedule"], r["score"]["scope"])].append(r)
        if not r["score"]["success"]:
            state, decision = r["score"]["state_ok"], r["score"]["decision_ok"]
            failures.append(
                {
                    "stream": r["stream"],
                    "task_index": r["task_index"],
                    "classification": "decision_only"
                    if state
                    else "state_only"
                    if decision
                    else "state_and_decision",
                    "stale_consistent": r["stale_consistent_error"],
                    "last_action": r["history"][-1]["action"] if r["history"] else None,
                    "observed_errors": dict(
                        Counter(h["result"]["error"] for h in r["history"] if "error" in h["result"])
                    ),
                }
            )
    breakdown = [
        {
            "policy": key[0],
            "schedule": key[1],
            "scope": key[2],
            "n": len(rows),
            "successes": sum(r["score"]["success"] for r in rows),
            "policy_reads": sum(r["cost"]["policy_reads"] for r in rows),
            "tool_calls": sum(r["cost"]["tool_calls"] for r in rows),
        }
        for key, rows in sorted(groups.items())
    ]
    # Same seed is reused across schedules. Secondary sensitivity resamples the
    # five seed blocks while retaining all four fixed schedules within each block.
    # This is deliberately separate from the frozen 20-stream primary report.
    pairs = summary["paired_comparison"]["pairs"]
    by_seed = defaultdict(list)
    for row in pairs:
        by_seed[row["seed"]].append(row["success_difference"])
    values = np.array([np.mean(by_seed[s]) for s in sorted(by_seed)])
    # Enumerate all ordered resamples: five seeds => 5**5 = 3125, no RNG variation.
    import itertools

    bootstrap = np.array([np.mean(v) for v in itertools.product(values, repeat=len(values))])
    sensitivity = {
        "label": "Post-run seed-block sensitivity; not a replacement for the frozen primary analysis",
        "unit": "seed, retaining all four fixed schedules",
        "n_seeds": len(values),
        "seed_mean_differences": dict(zip(map(str, sorted(by_seed)), values.tolist(), strict=True)),
        "mean_success_difference": float(values.mean()),
        "percentile_95_interval": np.quantile(bootstrap, [0.025, 0.975]).tolist(),
        "limits": "Only five seeds. Repeated deterministic templates and fixed schedules limit population inference.",
    }
    output = {
        "breakdown": breakdown,
        "failures": failures,
        "failure_counts": dict(Counter(r["classification"] for r in failures)),
        "seed_block_sensitivity": sensitivity,
        "max_recorded_mlx_peak_gib": max(r["cost"]["peak_memory_bytes"] for r in records) / 2**30,
        "summed_task_wall_seconds": sum(r["cost"]["wall_seconds"] for r in records),
        "summed_model_seconds": sum(r["cost"]["model_seconds"] for r in records),
    }
    reads, errors, mechanisms, recovery_types = {}, {}, Counter(), {}
    capped = [r for r in records if r["cost"]["tool_calls"] == 12]
    for policy in sorted({r["policy"] for r in records}):
        selected = [r for r in records if r["policy"] == policy]
        attempted = [
            h
            for r in selected
            for h in r["history"]
            if isinstance(h["action"], dict) and h["action"].get("tool") == "read_policy"
        ]
        reads[policy] = {
            "attempts": len(attempted),
            "successful_observations": sum("policy" in h["result"] for h in attempted),
            "errors": dict(Counter(h["result"]["error"] for h in attempted if "error" in h["result"])),
        }
        errors[policy] = dict(
            Counter(h["result"]["error"] for r in selected for h in r["history"] if "error" in h["result"])
        )
        events = [e for e in summary["recovery"] if e["policy"] == policy]
        recovery_types[policy] = {
            "never_observed": sum(e["affected_tasks_observed"] == 0 for e in events),
            "observed_events": sum(e["affected_tasks_observed"] > 0 for e in events),
            "observed_without_success": sum(
                e["affected_tasks_observed"] > 0 and e["censored"] for e in events
            ),
        }
    for r in records:
        if r["score"]["success"]:
            continue
        last = r["history"][-1]["action"]
        if r["cost"]["tool_calls"] == 12:
            category = (
                "budget_exhausted_with_unknown_scope"
                if r["history"][-1]["result"].get("error") == "unknown_scope"
                else "budget_exhausted_duplicate_change"
            )
        elif isinstance(last, dict) and last.get("args", {}).get("reason") == "already_changed":
            category = "duplicate_change_then_wrong_denial"
        elif isinstance(last, dict) and last.get("args", {}).get("decision") == "complete":
            category = "false_completion"
        else:
            category = "invalid_denial_reason"
        mechanisms[category] += 1
    output["post_review_diagnostics"] = {
        "read_accounting": reads,
        "tool_error_categories": errors,
        "failure_pattern_counts": dict(mechanisms),
        "recovery_censoring": recovery_types,
        "unknown_scope_affected_tasks": sum(
            any(h["result"].get("error") == "unknown_scope" for h in r["history"]) for r in records
        ),
        "budget_capped_tasks": len(capped),
        "budget_capped_task_tokens": sum(
            r["cost"]["prompt_tokens"] + r["cost"]["completion_tokens"] for r in capped
        ),
        "limits": "Post-run descriptive patterns, not causal attributions; all frozen results retained.",
    }
    destination = Path(__file__).resolve().parents[1] / "evidence" / "test-v1"
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "diagnostics.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    from package_evidence import write_checksums

    write_checksums(destination)
    print(json.dumps({k: v for k, v in output.items() if k not in ["breakdown", "failures"]}, indent=2))


if __name__ == "__main__":
    main()
