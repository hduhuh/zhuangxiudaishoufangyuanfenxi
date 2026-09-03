---
name: verification
description: Verify that an implementation or analysis is backed by real data, correct state transitions, permissions, and reproducible evidence rather than UI appearance or assumed success.
---

# Verification

Before declaring work complete, verify the full path that matters:

1. **Source of truth** — identify the authoritative database, API, file, ledger, or repository state.
2. **Write path** — confirm the intended mutation actually persisted.
3. **Read path** — confirm downstream queries return the persisted truth, not fixtures, cache, fallback, or mock data.
4. **Permissions** — verify server-side authorization/RLS, not only front-end visibility.
5. **State transitions** — test success, failure, retry, cancellation, rollback, and duplicate action where relevant.
6. **Reconciliation** — compare summary totals with underlying detail rows when the feature aggregates data.
7. **Evidence** — capture concrete IDs, queries, logs, responses, or test outputs sufficient to reproduce the conclusion.

Do not mark a feature complete merely because a page renders or a button responds.
