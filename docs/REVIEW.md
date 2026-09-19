# Independent review and adjudication — v0.1.0

Two requested external reviewers evaluated methodology and code after completion of the 800-task frozen run:

- **Antigravity / Gemini 3.8 Flash High**: highest thinking option exposed by its native model selector. Reviewed code and methodology, ran tests, audit and reference checks.
- **DeepSeek Harness / DeepSeek-V41-Flash (`deepseek-flash`), `max` reasoning**: isolated per-run settings, reviewed both methodology and code; independently reconstructed 4,233 prompts and recomputed scores and statistics.

These reviews are model-assisted checks, not peer review or a guarantee of correctness. Raw local review transcripts are not published. Findings were checked against trajectories and implementation before adoption.

## Resolved engineering findings

- Compact evidence previously inherited checksums for files not included in that subset. Its checksums now cover exactly its own files.
- API experiment discovery now distinguishes initializing SQLite databases from corrupt/unavailable ones, without falsely reporting corrupt data as zero completed tasks.
- Portable auditing reads gzip without creating a database, validates summaries, reconstructs prompts and memory transitions, and checks recorded timing/peak accounting.
- Replay filters survive navigation; a fresh clone can load bundled evidence even with the API online. Download lifecycle, keyboard activation after dragging, reset during transfer and mobile timeline labels were repaired.

The frozen world, agents, scoring, experiment, store, report, protocol and dependency lock remain unchanged. All 113 failed tasks and original scores remain intact.

## Findings retained as v1 limitations

The invalid-scope prompt artifact (873 calls), 52 invalid-scope budget failures, repeated-operation pattern in all 28 refresh failures, read-attempt semantics, 75 structurally unobserved recovery entries, and dependent seed design are disclosed in [RESULTS.md](RESULTS.md). Fixing the prompt/tool contract requires a new study, not rewriting this run. The nominal response-attempt cap is clarified in [REPRODUCING.md](REPRODUCING.md).

## Adjudication

Refresh has eight invalid-scope calls, not four. Distinguishing successful reads from attempts does not reverse selective versus retrieval cost: selective has 37 more attempts and 45 more successful observations. Concrete business restriction feedback is an allowed observation, not access to hidden evaluator state. It may support a correct denial without memory refresh, but the current data does not identify its causal contribution. Reviewer statements implying causal certainty, general superiority or full production readiness were not adopted.

## Verification boundary

39 automated tests pass. The full deterministic audit verifies all 800 matrix cells; the extended audit reconstructs 4,233 prompts and memory transitions. Neither audit reruns the neural model or independently retokenizes it. Browser interaction checks are recorded in [WEB-VERIFICATION.md](WEB-VERIFICATION.md). The release archive retains its original checksum; supplementary diagnostics and the extended audit have separate repository checksums.
