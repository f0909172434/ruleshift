# Web verification record

Checked on 2026-09-20 using the actual local browser, after production builds.

- Desktop homepage at 1280 px and mobile layout at 390 px: no document-level horizontal overflow. The large results table remains a deliberately scrollable region.
- Pointer hover: policy cards respond to pointer position; heading lens appears; buttons receive pointer-origin feedback.
- Dragging the authoritative ticket onto memory triggers transfer and updates memory with one charged teaching-demo read.
- Dropping outside memory leaves the remembered rule and query count unchanged.
- Enter activates the same update, including after a drag; a stale pointer flag was fixed.
- Reset during transfer cancels the pending update. Scenario changes reset the illustration.
- Time range supports keyboard input: restored A with remembered B exposes a false rejection.
- An out-of-date permissive memory attempts a blocked action; synchronized memory correctly rejects it.
- Reduced-motion preference disables card transforms, heading lens and decorative animation; updating remains usable.
- Local world: policy read, refund, finish, two privileged-reference tasks, task-four rule change and snapshot replay all operated through the actual page. Replay reconstructed the same world from ten events.
- Model replay separates actual model history, policy-managed observations, costs and success/failure. The teaching illustration is explicitly labeled as non-model.

The screenshots in `docs/assets/` are actual rendered pages. Native viewport emulation caused capture-only scaling artifacts in some attempts; those captures were discarded. Browser checks are recorded observations, not a claim of exhaustive device or assistive-technology coverage.

Static build was served separately without the API: its bundled 800-task dataset loaded, all five measured strategies matched the report, and strategy selection opened the matching replay. On the API-backed page, multi/101/refresh task 3 (one-based) showed the actual address change plus the recorded incorrect final decision. The extracted release passed all checksums and the complete portable audit.

Final post-review browser check: rebuilt local UI loads all 800 records; counters explicitly say query attempts and link to limitations. Selected refresh/multi/101, navigated to overview and back, and confirmed all selectors stayed unchanged. Local API was restarted with the initializing/corrupt-database fix. Final checks: 39 tests, Ruff and production build pass; portable extended audit verifies 800 records and 4,233 reconstructed prompts.
