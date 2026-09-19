# Reproducing RuleShift

## Exact baseline

- Model: `mlx-community/Qwen3-4B-Instruct-2507-4bit`
- Revision: `50d427756c6b1b2fe0c0a10f67fbda1fc8e82c1b`
- Runtime: Python 3.12, MLX; dependency resolution in `uv.lock`.
- Original device: Apple M5, 24 GiB unified RAM, macOS arm64.
- Greedy decoding; 180 generated tokens per response; 16 response attempts and 12 tool calls per task; 1024 token memory budget.
- Four schedules, seeds 101/202/303/404/505, eight tasks, five memory policies.

Clone the repository and run the commands in the README from the repository root. The environment and evaluator run without MLX on other supported Python platforms; the only implemented model backend requires Apple Silicon. Installing the `mlx` extra on another platform does not provide an alternative backend.

The model download is content-version pinned. No `trust_remote_code` is enabled. Model weights are not redistributed with RuleShift. Network is needed for dependencies and the first weights download, not inference once cached. Reproducibility means deterministic world/replay and fixed inference settings; identical floating-point model outputs across hardware or future runtime versions are not guaranteed.

## Run and resume

Use a fresh output directory for a new experiment. Reuse exactly that directory to resume an interrupted run. The manifest binds the model revision, protocol, lockfile and five execution modules. Completed task rows are skipped by the runner. SQLite is canonical; each task also gets an atomic JSON export. If a crash happens between a database commit and its JSON export, use `ruleshift report RUN` to regenerate the complete canonical trajectory export. The runner does not reconstruct the missing individual task file automatically.

A failed or interrupted inference does not create a completed task. Restarting repeats that unfinished task from its prior boundary. A strategy's memory and world are restored from the last completed task. Do not edit the frozen execution modules or protocol and resume into the old directory: the runner rejects mismatched configuration.

The source archive records the execution code, initial report code, protocol and lockfile. Reports can be regenerated from the database; if reporting is corrected after a run, preserve the original source archive and document the correction.

## Reading evidence

- `manifest.json`: planned matrix, exact revision, hashes, runtime platform.
- `index.sqlite`: canonical task records.
- `STREAM/task-NN.json`: per-task readable export.
- `trajectories.jsonl.gz`: all records, including prompts, responses, memory, costs and replayable world snapshots.
- `metrics.jsonl`, `summary.csv`, `summary.json`: derived measurements, complete denominators, paired intervals and recovery censoring.
- `explorer.json`: compact researcher-view data for the web UI.
- `source/`: frozen execution files and protocol.

To replay a task: `uv run ruleshift replay RUN/STREAM/task-00.json`. This verifies recorded world transitions, not that rerunning a probabilistic computation generates identical tokens. Use the evidence audit script to check the entire matrix and every snapshot.

## Interpretation

There are 100 policy streams, but only 20 matched schedule/seed settings for the primary selective-versus-refresh contrast. Each stream contains eight dependent tasks. Bootstrap those 20 paired differences, not 800 task-level pseudo-replicates. Per-schedule estimates have only five seeds. The confidence interval describes variation in this small synthetic matrix; it is not a population guarantee.

Warmup uses three initial policy observations, identical across strategies; `none` discards them. Warmup construction, model load and first download are setup costs excluded from per-task totals. All policy-managed reads during evaluation are charged. Token totals sum actual model inputs/outputs; tool latency and inference latency are measured separately. These are local costs, not estimates of provider bills.

The 12 template names designate four variants per task family. They are not 12 independent domains or human-curated task datasets. Splits use distinct parameter combinations; some individual numeric values overlap across families/splits. Schedules are deterministic and short. Tools enforce policy, so an unsafe attempt can be blocked before state mutation. Success alone therefore does not establish safe autonomous behavior; inspect illegal attempts and costs too.

Recovery means first successful affected-scope task following a change, before the next same-scope change. A correct rejection counts as success; it need not prove that memory was updated. Stale-consistent errors are observational signals, not causal attribution.

`scenarios/retail.yaml` is a readable specification of the v1 scenario. The runner does not load arbitrary YAML scenarios. Add new worlds in code and create a new protocol/run rather than assuming editing YAML changes the experiment.

## Pilot history

`smoke-v1` was a development diagnostic. It exposed irrelevant tool timing in the prompt, which was removed before the fixed protocol/test. Preserve it as superseded diagnostic evidence, never combine it with confirmatory results. `smoke-v2` ran 16 development tasks; `validation-v1` ran 16 validation tasks. Neither belongs in the 800-task test denominator. Validation checked execution; test outcomes were not used to tune the prompt or strategies.
