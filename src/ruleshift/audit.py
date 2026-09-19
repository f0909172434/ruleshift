"""Read-only evidence checks, independent of the experiment runner."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sqlite3
from pathlib import Path

from ruleshift.agents import parse_action
from ruleshift.scoring import evaluate
from ruleshift.world import Action, digest, replay


def audit(root: Path, require_complete: bool = True) -> dict:
    root = Path(root)
    manifest = json.loads((root / "manifest.json").read_text())
    config = manifest["config"]
    source = root / "source"
    names = ("world.py", "scoring.py", "agents.py", "experiment.py", "store.py")
    archived_hash = digest({name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in names})
    if archived_hash != config["implementation_hash"]:
        raise ValueError("Archived execution source does not match manifest")
    for name, field in (("PROTOCOL.md", "protocol_hash"), ("uv.lock", "dependency_lock_hash")):
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != config[field]:
            raise ValueError(f"Archived {name} does not match manifest")
    # Replaying with a different implementation would not audit the frozen semantics.
    live = Path(__file__).parent
    if any((live / name).read_bytes() != (source / name).read_bytes() for name in names):
        raise ValueError("Use the archived execution version to audit this run")
    database = sqlite3.connect(f"file:{root / 'index.sqlite'}?mode=ro", uri=True)
    try:
        records = [
            json.loads(row[0])
            for row in database.execute("SELECT payload FROM tasks ORDER BY stream,task_index")
        ]
    finally:
        database.close()
    expected = set(
        itertools.product(config["schedules"], config["seeds"], config["policies"], range(config["tasks"]))
    )
    actual = [(r["schedule"], r["seed"], r["policy"], r["task_index"]) for r in records]
    if len(set(actual)) != len(actual) or set(actual) - expected:
        raise ValueError("Duplicate or unexpected matrix cells")
    if manifest["planned_tasks"] != len(expected):
        raise ValueError("Manifest planned count does not match matrix")
    missing = expected - set(actual)
    if require_complete and missing:
        raise ValueError(f"Incomplete matrix: {len(missing)} missing tasks")
    event_count = 0
    for r in records:
        snap = r["snapshot"]
        replay(snap)
        event_count += len(snap["events"])
        if evaluate(snap["task_start"], snap["state"]) != r["score"]:
            raise ValueError(f"Score mismatch in {r['stream']}:{r['task_index']}")
        if (
            snap["state"]["schedule"],
            snap["state"]["seed"],
            snap["state"]["split"],
            snap["state"]["task_index"],
        ) != (r["schedule"], r["seed"], config["split"], r["task_index"]):
            raise ValueError("Record identity does not match world")
        history, responses, cost = r["history"], r["responses"], r["cost"]
        current_events = [e for e in snap["events"] if e["kind"] == "tool" and e["index"] == r["task_index"]]
        if len(history) != len(current_events) or len(history) != cost["tool_calls"]:
            raise ValueError("Tool cost/history mismatch")
        for h, e in zip(history, current_events, strict=True):
            # Valid actions are canonicalized with optional args={} by the world.
            try:
                canonical = (
                    Action.model_validate_json(h["action"]).model_dump()
                    if isinstance(h["action"], str)
                    else Action.model_validate(h["action"]).model_dump()
                )
            except ValueError:
                canonical = h["action"]
            if canonical != e["action"]:
                raise ValueError("History action differs from replayed action")
            if h["result"] != e["observation"]["result"]:
                raise ValueError("Recorded tool result differs from replayed observation")
        if len(responses) != sum(h["origin"] == "model" for h in history):
            raise ValueError("Response/action count mismatch")
        model_actions = [h["action"] for h in history if h["origin"] == "model"]
        if model_actions != [parse_action(response["text"]) for response in responses]:
            raise ValueError("Model text does not match recorded actions")
        for key in ("prompt_tokens", "completion_tokens"):
            if cost[key] != sum(response[key] for response in responses):
                raise ValueError(f"Incorrect {key} total")
        if cost["policy_reads"] != sum(
            isinstance(h["action"], dict) and h["action"].get("tool") == "read_policy" for h in history
        ):
            raise ValueError("Incorrect policy read count")
        if cost["illegal_attempts"] != sum("error" in h["result"] for h in history):
            raise ValueError("Incorrect illegal-attempt count")
        if cost["tool_calls"] > config["tool_budget"] or len(responses) > 16:
            raise ValueError("Budget exceeded")
    return {
        "verified": True,
        "complete": not missing,
        "records": len(records),
        "planned": len(expected),
        "missing": len(missing),
        "replayed_events_including_shared_prefixes": event_count,
        "source_and_protocol_verified": True,
        "scores_and_costs_recomputed": True,
        "scope": "World replay and recorded accounting; does not rerun neural inference or prove novelty.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(args.path, not args.allow_partial), indent=2))


if __name__ == "__main__":
    main()
