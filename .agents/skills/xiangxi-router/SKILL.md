---
name: xiangxi-router
description: Shared skill router for Xiangxi repositories. Route knowledge ingestion, automated INBOX events, Miaoda-to-GitHub source synchronization, governance, strategic work, and product-specific execution to the appropriate Xiangxi Skills.
---

# Xiangxi Router

Before executing a non-trivial request, classify it.

1. **Routine and fully specified**: execute directly.
2. **Manual knowledge ingestion** involving new documents/notes entering an Obsidian/Markdown vault, scanning an INBOX, preserving source evidence, classifying material, generating linked Markdown, or routing material into projects/knowledge/decisions: invoke `xiangxi-knowledge-ingest`.
3. **Automatic knowledge watcher event** (`KNOWLEDGE_INBOX_NEW_FILE`) or requests to auto-process a configured knowledge INBOX: invoke `xiangxi-knowledge-ingest` + `xiangxi-knowledge-ingest-v1-5`.
4. **Knowledge governance** involving cleanup, consolidation, duplicate rules, version conflicts, stale instructions, repeated prompts, overlapping skills, archive/deprecation decisions, or Skill promotion: invoke `xiangxi-entropy-reducer` when available.
5. **Miaoda first migration / initial backup**: invoke `miaoda-migration`.
6. **Miaoda later release synchronization, export ZIP watcher events (`MIAODA_EXPORT_READY`), source diffing, secret scanning, Git branch/commit/push/PR, or keeping a Miaoda GitHub repo current**: invoke `miaoda-github-sync`.
7. **Ambiguous, strategic, high-impact, cross-system, data-sensitive, financial, permission-related, deletion, or architecture work**: invoke `grill-me` / `grilling` before destructive implementation.
8. **Repository-specific work**: add the domain Skill when available, e.g. `grill-xiangzu`, `grill-xiangda`.
9. **Short video creation/repair**: invoke `shortvideo-factory` when installed.
10. **Cross-platform publishing of approved content**: invoke `multipost-distribution` when installed.

## Combined routing

- Knowledge ingestion that discovers duplicates/stale/conflicting canonical rules: `xiangxi-knowledge-ingest` -> `xiangxi-entropy-reducer`.
- Automatic INBOX event: `xiangxi-knowledge-ingest` -> `xiangxi-knowledge-ingest-v1-5`; add governance only when needed.
- Miaoda sync with ambiguous project identity, secret risk, destructive overwrite, or unclear source authority: `miaoda-github-sync` -> governance/grilling as appropriate.
- A request that both modifies project code and syncs it must preserve Git discipline: test -> diff -> secret scan -> branch -> commit -> push -> PR.

## Token discipline

- Load only the Skills needed for the current task.
- Reuse approved assets, hashes, paths, decisions, and canonical notes.
- Pass minimal structured inputs between Skills.
- Retry only the failed stage.

## Fact retrieval discipline

During ingestion, governance, code sync, or grilling, retrieve discoverable facts from files, code, logs, databases, APIs, Git history, and connected tools. Ask the user only for decisions, priorities, authority, trade-offs, or business rules that cannot be discovered.

## Execution gates

Do not implement high-impact or destructive changes until unresolved decision branches are cleared. Routine non-destructive ingestion, watcher job creation, safe source archiving, no-change detection, and non-conflicting branch/PR creation may proceed directly.

Never pretend:

- a watcher event means ingestion succeeded;
- a Miaoda publish means GitHub already contains the latest source;
- a screenshot is source code;
- an external reference is a system rule;
- a draft is canonical truth.

This router is the common linkage layer across repositories. Keep ingestion mechanics in the ingestion Skills, Miaoda code-sync mechanics in `miaoda-github-sync`, governance in `xiangxi-entropy-reducer`, and product business rules in product-specific Skills.
