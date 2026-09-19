# Compact evidence index

This directory contains summaries and diagnostics, not the full trajectory/source bundle.
`SHA256SUMS` verifies only the files present here. Run `shasum -a 256 -c SHA256SUMS`
in this directory to check them.

For the complete 800-record audit, download and extract `ruleshift-test-v1.tar.gz`
from the GitHub release. `archive.sha256` names that download, which is not stored
in this directory. The extracted bundle has its own complete SHA256SUMS and source/.
From the matching source checkout, run `uv run ruleshift audit /path/to/ruleshift-test-v1 --exported`.

See ../../docs/RESULTS.md for interpretation and limitations. The frozen report,
raw recorded outcomes and execution source were not changed after review.
