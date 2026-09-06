---
name: xiangxi-router
description: Shared skill router for Xiangxi repositories. Route knowledge ingestion through the Xiangxi knowledge-ingest pipeline, ambiguous or strategic work through Grill Me before implementation, invoke governance for entropy reduction when available, and prefer domain-specific skills when available.
---

Before executing a non-trivial request, classify it:

1. Routine and already specified: execute directly.
2. Knowledge-ingestion work involving new documents/notes entering an Obsidian or Markdown vault, scanning an INBOX, preserving source evidence, classifying material, generating linked Markdown, or routing material into projects/knowledge/decisions: invoke `xiangxi-knowledge-ingest` when that Skill is installed in the current environment.
3. Knowledge-governance work involving cleanup, consolidation, duplicate rules, version conflicts, stale instructions, repeated prompts, overlapping skills, archive/deprecation decisions, or deciding whether recurring behavior should become a Skill: invoke `xiangxi-entropy-reducer` when that Skill is installed in the current environment.
4. If governance is required but `xiangxi-entropy-reducer` is not installed locally, do not pretend to call it. Mark the task as requiring Xiangxi governance and defer canonical cross-repository consolidation to the Xiangxi Skill Hub; continue only with safe local analysis that does not create a competing source of truth.
5. Ambiguous, strategic, high-impact, cross-system, data-sensitive, financial, permission-related, migration, deletion, or architecture work: invoke `grill-me` / `grilling` first.
6. If a repository-specific skill exists (for example `grill-xiangzu` or `grill-xiangda`), use it in addition to the generic skill above.
7. Create/assemble/repair a short video from approved text, images, footage, screenshots, or voiceover: invoke `shortvideo-factory` when installed.
8. Cross-platform publishing of already-approved text, images, or video: invoke `multipost-distribution` when installed. Do not use it for content generation or lead strategy.
9. If one request asks both to make a video and publish it, run `shortvideo-factory` first, then pass only the finished asset + approved title/caption + target platforms to `multipost-distribution`.

For ingestion that discovers duplicates, stale versions, or conflicting canonical rules, combine `xiangxi-knowledge-ingest` with `xiangxi-entropy-reducer`. Ingestion extracts and routes; governance decides KEEP / ADD / MERGE / REPLACE / ARCHIVE / DEPRECATE / PROMOTE_TO_SKILL.

Token discipline:
- Load only the Skill(s) needed for the current task.
- Reuse approved assets and decisions.
- Do not send full background or duplicate copy between Skills; pass minimal structured inputs.
- On failure, retry only the failed stage.

If governance work is also ambiguous or high-impact, combine `xiangxi-entropy-reducer` with `grill-me` / `grilling`: first locate existing facts and conflicts, then ask only for unresolved authority, trade-offs, scope, deletion, or business-policy decisions.

During ingestion, grilling, or governance, retrieve facts from files, code, logs, databases, APIs, and connected tools rather than asking the user for facts that can be discovered. Ask the user only for decisions, priorities, trade-offs, authority, and business rules.

Execution gate: do not implement high-impact or destructive changes until unresolved decision branches are cleared, acceptance criteria are explicit, and the user confirms shared understanding. Routine non-destructive ingestion or entropy reduction with a clear canonical destination may be executed directly.

This router is the common linkage layer across repositories. Keep shared behavior consistent; keep ingestion mechanics in `xiangxi-knowledge-ingest`; keep governance rules in `xiangxi-entropy-reducer`; keep product-specific rules in product-specific skills.
