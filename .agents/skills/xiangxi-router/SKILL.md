---
name: xiangxi-router
description: Shared skill router for Xiangxi repositories. Route ambiguous or strategic work through Grill Me before implementation, invoke governance for entropy reduction when available, and prefer domain-specific skills when available.
---

Before executing a non-trivial request, classify it:

1. Routine and already specified: execute directly.
2. Knowledge-governance work involving cleanup, consolidation, duplicate rules, version conflicts, stale instructions, repeated prompts, overlapping skills, archive/deprecation decisions, or deciding whether recurring behavior should become a Skill: invoke `xiangxi-entropy-reducer` when that Skill is installed in the current environment.
3. If governance is required but `xiangxi-entropy-reducer` is not installed locally, do not pretend to call it. Mark the task as requiring Xiangxi governance and defer canonical cross-repository consolidation to the Xiangxi Skill Hub; continue only with safe local analysis that does not create a competing source of truth.
4. Ambiguous, strategic, high-impact, cross-system, data-sensitive, financial, permission-related, migration, deletion, or architecture work: invoke `grill-me` / `grilling` first.
5. If a repository-specific skill exists (for example `grill-xiangzu` or `grill-xiangda`), use it in addition to the generic skill above.

If governance work is also ambiguous or high-impact, combine `xiangxi-entropy-reducer` with `grill-me` / `grilling`: first locate existing facts and conflicts, then ask only for unresolved authority, trade-offs, scope, deletion, or business-policy decisions.

During grilling or governance, retrieve facts from code, files, logs, databases, APIs, and connected tools rather than asking the user for facts that can be discovered. Ask the user only for decisions, priorities, trade-offs, authority, and business rules.

Execution gate: do not implement high-impact or destructive changes until unresolved decision branches are cleared, acceptance criteria are explicit, and the user confirms shared understanding. Routine non-destructive entropy reduction with a clear canonical source may be executed directly.

This router is the common linkage layer across repositories. Keep shared behavior consistent; keep governance rules in `xiangxi-entropy-reducer`; keep product-specific rules in product-specific skills.
