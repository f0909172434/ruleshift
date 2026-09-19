# RuleShift v1 measured results

The complete frozen Qwen3-4B 4-bit test ran **800/800 tasks** on Apple M5 (24 GiB unified memory). All 113 failed tasks remain in the denominator. No model, prompt, execution implementation or protocol was changed during the test.

| Memory strategy | Success | Rate | Tool calls | In-run rule read attempts | Total tokens |
|---|---:|---:|---:|---:|---:|
| None | 123/160 | 76.875% | 1,050 | 545 | 632,479 |
| Retrieval | 153/160 | 95.625% | 788 | 141 | 491,605 |
| TTL | 126/160 | 78.750% | 990 | 455 | 607,793 |
| Always refresh | 132/160 | 82.500% | 779 | 171 | 400,491 |
| Selective update | 153/160 | 95.625% | 835 | 178 | 493,886 |

## What this supports

The prespecified contrast, selective minus always refresh, is **+13.125 percentage points**, with the frozen paired-stream bootstrap 95% interval **[7.5, 18.125]** points over 20 schedule/seed streams. Selective also uses 56 more tool calls and 93,395 more tokens than refresh. This is a success/cost tradeoff, not an across-the-board improvement.

The simpler retrieval baseline is at least as compelling here: **the same 153 successes as selective, with 47 fewer tool calls, 37 fewer policy read attempts and 2,281 fewer tokens**. The experiment does not demonstrate a benefit from selective invalidation over retrieval. These strategies can all request fresh rules themselves; their names describe automatic memory handling, not a restriction on available tools.

Do not infer that stale memory is generally preferable or that refreshing rules causes failures. Prompt content, the number and placement of observations, repeated operations and model decisions differ. This experiment compares complete policies; it does not isolate their mechanisms causally.

## Dependence and uncertainty

The frozen primary analysis uses the protocol's 20 paired streams. The same five seeds recur across the four fixed schedules, so these 20 cases should not be treated as 20 independent samples from a broad task population. A separately labeled **post-run sensitivity analysis** resamples five seed blocks while retaining all four schedules. Enumerating all 3,125 ordered bootstrap resamples gives **[4.375, 18.75] percentage points**. One seed's average contrast is negative. Five seeds still provide weak population-level evidence; neither interval establishes generalization.

Per-schedule/domain counts and every failed record identifier appear in [diagnostics.json](../evidence/test-v1/diagnostics.json). These breakdowns are descriptive, not additional confirmatory discoveries.

## Failures and what they mean

Of the 113 failures, 93 have correct final business state but an incorrect decision or justification, 16 have both wrong state and decision, and four have wrong state despite a correct decision. These categories describe the evaluator's actual checks, not a causal error taxonomy.

For example, `multi-101-refresh`, zero-based task 2, changes the address successfully but finishes with `deny / already_changed`; the state is correct, but its final answer contradicts completion. `multi-202-selective`, task 7, denies for `too_old` while the applicable restriction is `opened`. A correct-looking denial is not accepted without a valid reason.

The recorded stale-consistent-error indicator is **zero for every strategy**. It is an observational check against the last visible policy, not proof that stale evidence never affected behavior. In particular, observations can be refreshed during a task. Recovery in the frozen report is first success after a change, not sustained adaptation; changed scopes that are never observed before the next boundary are retained as censored.

## Coverage and feedback limits found in independent review

Of 250 recovery entries, **75 (30%) contain zero affected tasks**. The fixed eight-task sequence does not revisit fulfillment after its later change, and does not revisit fulfillment or address changes after the recurring schedule restores their rules. Those entries remain censored; the experiment does not establish recovery in those unobserved domains.

All 28 refresh failures occur in address-change tasks with correct final state and wrong final decisions. This concentrates its deficit in one model/tool behavior and weakens an adaptation-specific interpretation of the aggregate contrast.

The world intentionally returns a concrete restriction reason with a blocked operation. That is allowed tool feedback, not hidden evaluator input, but it can let an agent correctly deny without refreshing memory. A future ablation should vary feedback specificity. The existing aggregate results alone do not establish how much this mechanism explains the retrieval/selective tie.

## Accounting and reproducibility

Three shared initial policy observations are setup, excluded from in-run read totals. Every additional policy-managed read is charged against the same 12-call task budget. Tokens are tokenizer-measured recorded input/output counts, not a provider bill or an independent retokenization by the audit.

Summed task wall time is about **88.0 minutes**; this excludes model download/loading and other setup. Recorded MLX peak allocation is **2.812 GiB**, not total process or device memory. Concurrent machine workload can affect timing.

The full audit verified all **800 matrix cells**, replayed **23,332 events including repeated snapshot prefixes**, recomputed scores and reconciled histories, model actions and costs. Exported summaries match the frozen report recomputed from trajectories. Replay checks deterministic world semantics; it does not rerun neural inference.

[Machine-readable report](../evidence/test-v1/summary.json) · [Integrity record](../evidence/test-v1/integrity.json) · [Reproduction](REPRODUCING.md) · [Protocol](PROTOCOL.md)

## Next experiment

Treat this run as the preserved v1 pilot. A new protocol should use more independently generated worlds, additional models, longer streams, independently varied observation placement, and targeted tests of false rejection when permissive rules return. Those are future studies; this release does not claim to have run them. Do not tune against this test set and relabel the revised scores as held-out results.

## Post-review diagnostics: prompt and tool artifacts

These are descriptive analyses of the preserved run, not preregistered causal tests. The tool description uses the literal placeholder `returns|fulfillment|changes`; the model sometimes copies it instead of choosing one scope. There are **873 `unknown_scope` calls across 350 tasks** (none 382, TTL 363, retrieval 64, selective 56, refresh 8). Of 56 tasks that exhaust the 12-call budget, 52 end in invalid-scope loops and four in duplicate-change loops. All 56 fail and together consume **456,270 tokens, 17.4% of the 2,626,254 total**. That token percentage covers all 56 tasks, not only the 52 invalid-scope cases.

All **28 refresh failures** successfully change the address, repeat `change_order`, receive `already_changed`, then wrongly finish with denial. Selective succeeds on 26 of these paired cells. The primary contrast is therefore heavily influenced by a repeated-operation and final-answer failure pattern; it does **not isolate memory adaptation**. Retrieval and selective have identical failure sets.

The 113 failures partition descriptively into 52 budget-exhausted invalid-scope loops, 28 duplicate-change/wrong-denial cases, 18 invalid denial reasons, four budget-exhausted duplicate-change loops, and 11 false completions. These observed sequences do not prove a unique underlying cause.

The frozen `policy_reads` field counts **attempts**, including errors:

| Strategy | Read attempts | Successful observations |
|---|---:|---:|
| None | 545 | 163 |
| Retrieval | 141 | 77 |
| TTL | 455 | 92 |
| Always refresh | 171 | 163 |
| Selective update | 178 | 122 |

Selective uses 37 more attempts and obtains 45 more successful observations than retrieval; the comparison does not reverse when successful observations are counted. The frozen `illegal_attempts` field includes all tool errors, including malformed arguments, and is not a pure measure of unsafe business actions.

Each strategy has 15 structurally unobserved recovery entries and 35 observed entries. Among observed entries, those with no success before the next boundary are none 13, TTL 14, refresh 2, retrieval 1, selective 1. The all-zero stale-consistent indicator is especially limited for no-memory and always-refresh strategies by construction.

The extended audit additionally reconstructs **4,233 prompts** and all memory transitions, and reconciles timers and recorded MLX peaks. This is not independent tokenization or neural inference. See [extended audit](../evidence/test-v1/extended-audit.json) and [review adjudication](REVIEW.md).

A v2 study should replace the ambiguous schema placeholder, explicitly handle successful idempotent operations, vary feedback specificity, and ensure post-change domain coverage. Such changes require a fresh frozen protocol and new evaluation worlds. They must not be applied retrospectively to improve v1 scores.
