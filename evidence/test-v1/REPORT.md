# Experiment report

Completed: **800 / 800** tasks.

Model: `mlx-community/Qwen3-4B-Instruct-2507-4bit`

| Policy | Success | Tool calls | Policy reads | Total tokens |
|---|---:|---:|---:|---:|
| none | 123/160 | 1050 | 545 | 632479 |
| refresh | 132/160 | 779 | 171 | 400491 |
| retrieval | 153/160 | 788 | 141 | 491605 |
| selective | 153/160 | 835 | 178 | 493886 |
| ttl | 126/160 | 990 | 455 | 607793 |

Selective − refresh: 0.131; paired-stream bootstrap 95% CI [0.075, 0.181], n=20 streams.

## Interpretation boundaries

Frozen-weight, synthetic-retail, single-model pilot. Not a production or general-intelligence claim.
All model failures remain in the denominator. Warmup evidence is shared; policy-managed reads are charged.
The stale-evidence indicator is an observational consistency check, not a causal attribution.
Full prompts, responses, world snapshots and replayable actions are in trajectories.jsonl.gz.
