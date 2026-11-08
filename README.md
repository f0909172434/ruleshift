# RuleShift

RuleShift is a small simulated retail world for testing whether an agent's memory keeps up when business rules change. A local language model handles returns, shipments and address changes across a stream of tasks. Orders and stock persist between tasks, and the store's policies change partway through. A task counts as a success only if the model makes the correct decision and the world ends in the correct state.

[繁體中文](README.zh-TW.md) · [Protocol](docs/PROTOCOL.md) · [Research context](docs/CONTEXT.md) · [Reproduction](docs/REPRODUCING.md) · [Learning roadmap](docs/LEARNING.md)

[Live demo / 線上互動](https://chih-kai-wang.github.io/ruleshift/) · [Release evidence / 完整證據](https://github.com/Chih-Kai-Wang/ruleshift/releases)

![RuleShift interactive rule and memory laboratory](docs/assets/overview.png)

## What is here

- A deterministic retail world with validated tools, persistent state and snapshots. Any recorded run can be replayed exactly.
- An evaluator that scores the final world state against an independent specification. No language model acts as judge.
- Five memory strategies: none, retrieval, TTL, always refresh, and scoped refresh after a policy-block signal.
- A pinned local 4-bit Qwen3 4B model with fixed weights and greedy decoding on Apple Silicon.
- A paired 800-task protocol: four change schedules × five seeds × eight tasks × five strategies.
- A Traditional Chinese interactive workbench that shows the current rules, the memory the model actually observed, its real actions and their costs.

RuleShift is a pilot research instrument. It does not claim a novel algorithm, better general intelligence, production reliability or weight-based continual learning. A privileged reference agent checks that every task is solvable, and its successes are never reported as model performance.

## Try the world

Requires Python 3.12, [uv](https://docs.astral.sh/uv/) and Node.js 22+. The environment, tests and workbench do not need model weights or credentials.

```sh
git clone https://github.com/Chih-Kai-Wang/ruleshift.git
cd ruleshift
uv sync --frozen --extra dev
uv run ruleshift verify
npm ci --prefix web
npm run build --prefix web
uv run ruleshift serve --port 8765
```

Open <http://127.0.0.1:8765>. Read a policy, handle an order and advance time. At task four, compare the changed world with the policy you remembered. The workbench is a researcher view, so it shows ground truth that the model never receives. Its reference button runs the privileged reference agent, not the model.

## Run the model experiment

The current MLX backend requires Apple Silicon. The development machine had 24 GiB of unified memory. Allow roughly 3–4 GB for the model download and cache, plus runtime memory and experiment artifacts. Timing depends on the machine and concurrent workloads.

```sh
uv sync --frozen --extra dev --extra mlx
uv run ruleshift benchmark --smoke --output artifacts/runs/my-smoke
uv run ruleshift benchmark --output artifacts/runs/my-test
uv run ruleshift report artifacts/runs/my-test
```

The first model run downloads the pinned public model from Hugging Face. No paid endpoint, API key or remote model code is used. Running the same command again resumes at the next unsaved task. If you change the source, protocol, dependencies or run settings, use a new output directory. The report export includes every prompt, output and snapshot. The [reproduction details](docs/REPRODUCING.md) give the exact scope and limitations.

## SDK

```python
import json
from ruleshift.world import RuleShiftEnv, replay

env = RuleShiftEnv(schedule="recurring", split="dev")
env.reset(seed=17)
observation = env.start_task()  # explicit task boundary
observation, reward, terminated, truncated, info = env.step(
    {"tool": "read_policy", "args": {"scope": "returns"}}
)
print(json.loads(observation))
replay(env.snapshot())
```

`RuleShiftEnv` uses Gymnasium spaces and step tuples, but it exposes explicit task boundaries on purpose. You cannot drop it into a Gymnasium training loop that only calls reset and then step. The benchmark calls `start_task()` itself and evaluates the final state independently. Terminal rewards carry that independent score, and the runner recomputes it. The snapshot and restore APIs are for researchers and are never offered to the model as tools.

## Evidence and results

All **800/800** planned tasks ran, and the audit checked every one. The protocol asked whether scoped memory invalidation improves the success/cost tradeoff. Retrieval and selective both succeeded on **153/160** tasks (95.625%), and always refresh succeeded on **132/160** (82.5%). Selective cost more than retrieval for the same successes, so this pilot does **not** show a benefit from selective invalidation over the simpler baseline.

The prespecified contrast, selective minus refresh, is +13.125 percentage points, with a paired-stream bootstrap 95% interval of [7.5, 18.125]. The same five seeds are reused across schedules, which limits independence. A separately labeled seed-block sensitivity analysis gives [4.375, 18.75]. All 113 failures remain in the denominator.

[Full interpretation and limitations](docs/RESULTS.md) · [All strategies and costs](evidence/test-v1/summary.csv) · [Audit](evidence/test-v1/integrity.json) · [Frozen protocol](docs/PROTOCOL.md)

The release evidence archive holds every prompt, response and snapshot, plus the archived source. The local model experiment used no paid API.

## Development

```sh
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
npm run build --prefix web
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing evaluation behavior. The synthetic world only enforces which business actions are allowed. It is **not an operating-system sandbox**. The local workbench has no authentication and binds to loopback, so do not expose it as a public API.

Code is licensed under Apache-2.0. Authored synthetic task data and released experiment records are licensed under CC BY 4.0, subject to third-party rights. See [DATA_LICENSE.md](DATA_LICENSE.md) and [THIRD_PARTY.md](THIRD_PARTY.md). The project is not affiliated with DeepSeek, Qwen or any benchmark authors.

## What the results do not show

Two prompt and tool artifacts weigh heavily on these scores. The model sometimes loops on an invalid policy scope, and it sometimes repeats an address change that already succeeded. Because of this, the primary contrast does not isolate memory adaptation. The [review findings](docs/REVIEW.md) and [diagnostics](docs/RESULTS.md) give the counts.
