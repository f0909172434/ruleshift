# Contributing

Small changes with explicit failure cases are welcome. Explain the behavior being fixed, supply a reproducible example, and state which evidence is affected.

Run `uv run pytest`, `uv run ruff check src tests`, `uv run ruff format --check src tests`, and `npm run build --prefix web`. UI changes should also be tried in the real browser on desktop and a narrow viewport, with keyboard focus and reduced motion considered.

Do not edit old experiment records, silently drop failures, use test results to tune the same claimed held-out comparison, or report the privileged oracle as model performance. A change to world semantics, prompts, budget, model, memory policy or evaluation requires a new output directory. Preserve source snapshots and the prior protocol. Report bug corrections explicitly, including effects on old claims.

Models receive only the explicit observation/tool/memory interface. Researcher snapshots, evaluator truth, future changes and seed metadata must not enter prompts. Add a regression test for any boundary change.

Keep CI independent of paid endpoints and large model downloads. Do not commit credentials, model weights, personal paths or unrelated local material. Contributors retain copyright in their work and submit code under Apache-2.0; synthetic authored data follows DATA_LICENSE.md.
