---
name: xiangxi-router
description: Shared skill router for Xiangxi repositories. Route ambiguous or strategic work through Grill Me before implementation, and prefer domain-specific skills when available.
---

Before executing a non-trivial request, classify it:

1. Routine and already specified: execute directly.
2. Ambiguous, strategic, high-impact, cross-system, data-sensitive, financial, permission-related, migration, deletion, or architecture work: invoke `grill-me` / `grilling` first.
3. If a repository-specific skill exists (for example `grill-xiangzu` or `grill-xiangda`), use it in addition to the generic grilling skill.

During grilling, retrieve facts from code, files, logs, databases, APIs, and connected tools rather than asking the user for facts that can be discovered. Ask the user only for decisions, priorities, trade-offs, authority, and business rules.

Execution gate: do not implement until unresolved decision branches are cleared, acceptance criteria are explicit, and the user confirms shared understanding.

This router is the common linkage layer across repositories. Keep shared behavior consistent; keep product-specific rules in product-specific skills.
