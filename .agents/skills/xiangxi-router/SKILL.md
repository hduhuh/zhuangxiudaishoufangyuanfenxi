---
name: xiangxi-router
description: Shared skill router for Xiangxi repositories. Route knowledge ingestion, public-web/social intelligence, model selection, automated INBOX events, Miaoda-to-GitHub synchronization, governance, strategic work, creative production, and product-specific execution to the appropriate Xiangxi Skills.
---

# Xiangxi Router

Before executing a non-trivial request, classify it.

1. **Routine and fully specified**: execute directly.
2. **Manual knowledge ingestion** involving new documents/notes entering an Obsidian/Markdown vault, scanning an INBOX, preserving source evidence, classifying material, generating linked Markdown, or routing material into projects/knowledge/decisions: invoke `xiangxi-knowledge-ingest`.
3. **Automatic knowledge watcher event** (`KNOWLEDGE_INBOX_NEW_FILE`) or requests to auto-process a configured knowledge INBOX: invoke `xiangxi-knowledge-ingest` + `xiangxi-knowledge-ingest-v1-5`.
4. **Knowledge governance** involving cleanup, consolidation, duplicate rules, version conflicts, stale instructions, repeated prompts, overlapping skills, archive/deprecation decisions, or Skill promotion: invoke `xiangxi-entropy-reducer` when available.
5. **Experience distillation / turning cases into reusable rules, SOPs, decision trees or new Skills**: invoke `xiangxi-distill`, then `xiangxi-entropy-reducer` before promoting a new canonical Skill.
6. **Normal public web research / website extraction / official pages / bank products / operator websites / policy pages**: invoke `crawl4ai-web-intelligence` for collection, then `research`/`verification`/`decision` as needed.
7. **Social-platform intelligence** involving Xiaohongshu, Douyin, Bilibili, Zhihu, Weibo or similar public social content: invoke `mediacrawler-social-intelligence`, respecting platform/legal boundaries.
8. **Miaoda first migration / initial backup**: invoke `miaoda-migration`.
9. **Miaoda later release synchronization, export ZIP watcher events (`MIAODA_EXPORT_READY`), source diffing, secret scanning, Git branch/commit/push/PR, or keeping a Miaoda GitHub repo current**: invoke `miaoda-github-sync`.
10. **Ambiguous, strategic, high-impact, cross-system, data-sensitive, financial, permission-related, deletion, or architecture work**: invoke `grill-me` / `grilling` before destructive implementation.
11. **Repository-specific work**: add the domain Skill when available, e.g. `grill-xiangzu`, `grill-xiangda`.
12. **Short video creation/repair**: invoke `shortvideo-factory`; when OpenMontage is available and appropriate, use `openmontage-adapter` as the production-engine adapter.
13. **Cross-platform publishing of approved content**: invoke `multipost-distribution` when installed.
14. **Visual style standardization / hand-drawn illustration / reusable style IDs / visual prompt packs**: invoke `handdraw-style`.
15. **Explain a difficult concept through an analogy, fable or story before formal explanation**: invoke `story-explain`.
16. **Choose among approved LLM/image/video models after the execution channel is known**: invoke `model-router`. `openclaw-execution-router` decides terminal/automation/Agent first; `model-router` selects the model only when a model is needed.
17. **Find mature self-hosted/open-source software before building from scratch**: invoke `opensource-scout`.
18. **Product/brand naming, slogan, English name, logo direction or naming shortlist**: invoke `brand-builder`.
19. **Create or refactor a formal Prompt/Agent/Skill instruction**: apply `prompt-framework`; if derived from real operational experience, run `xiangxi-distill` first.
20. **旧房/出租房/公寓轻改、奶油风改造、改造效果图、装修BOM、工程量、同物料去重、每SKU 6–8家中国平台比价、采购清单、2万元内改造预算控制、到货验收与实际成本回填**: invoke `xiangxi-renovation-brain` when installed.

## Combined routing

- Web market research: `crawl4ai-web-intelligence` -> `research` -> `verification` -> `decision`.
- Social demand/competitor research: `mediacrawler-social-intelligence` -> `research` -> domain Skill -> `decision`.
- Experience-to-asset loop: operational result -> `xiangxi-distill` -> `xiangxi-entropy-reducer` -> human approval when high impact -> canonical Skill.
- Skill authoring: `xiangxi-distill` (when source is experience) -> `prompt-framework` -> tests -> GitHub canonical version.
- Short video flow: `shortvideo-factory` -> `openmontage-adapter` (optional engine) -> `shortvideo-factory` validation -> `multipost-distribution`.
- Visual asset flow: domain brief -> `handdraw-style` -> image-generation engine -> verification/brand review.
- Concept communication: domain decision/model -> `story-explain` -> formal explanation; never replace the formal conclusion with the story.
- Model selection: `openclaw-execution-router` -> if Agent/LLM needed, `model-router` -> selected provider/model.
- Open-source procurement: `opensource-scout` -> `verification` -> Adopt / Extend / Build decision.
- Brand creation: business positioning -> `brand-builder` -> availability verification before any claim of registrability.
- Knowledge ingestion that discovers duplicates/stale/conflicting canonical rules: `xiangxi-knowledge-ingest` -> `xiangxi-entropy-reducer`.
- Automatic INBOX event: `xiangxi-knowledge-ingest` -> `xiangxi-knowledge-ingest-v1-5`; add governance only when needed.
- Miaoda sync with ambiguous project identity, secret risk, destructive overwrite, or unclear source authority: `miaoda-github-sync` -> governance/grilling as appropriate.
- A request that both modifies project code and syncs it must preserve Git discipline: test -> diff -> secret scan -> branch -> commit -> push -> PR.
- Renovation full-flow requests: `xiangxi-renovation-brain`; add `research` for public supplier/product evidence and `verification` for links, specs, prices, budget formulas, and delivery acceptance when available.
- Renovation requests that change structural scope, exceed approved budget materially, or introduce high-risk electrical/plumbing work: `xiangxi-renovation-brain` -> `grill-me`/`grilling` before implementation.

## Token discipline

- Load only the Skills needed for the current task.
- Reuse approved assets, hashes, paths, decisions, canonical notes, verified SKUs, supplier records, and prior actual-cost data.
- Pass minimal structured inputs between Skills.
- Retry only the failed stage.

## Fact retrieval discipline

During ingestion, governance, code sync, market research, social intelligence, renovation sourcing, or grilling, retrieve discoverable facts from files, code, logs, databases, APIs, Git history, public product pages, public websites, and connected tools. Ask the user only for decisions, priorities, authority, trade-offs, dimensions that truly require site measurement, or business rules that cannot be discovered.

## Execution gates

Do not implement high-impact or destructive changes until unresolved decision branches are cleared. Routine non-destructive ingestion, public-data research, watcher job creation, safe source archiving, no-change detection, non-conflicting branch/PR creation, and non-structural renovation planning may proceed directly.

Never pretend:

- a watcher event means ingestion succeeded;
- a Miaoda publish means GitHub already contains the latest source;
- a screenshot is source code;
- an external reference is a system rule;
- a draft is canonical truth;
- a crawler result is automatically verified truth;
- a social-media sample represents the whole market;
- a model router can expose or store API secrets;
- an estimated renovation price is a live marketplace quote;
- an APP search keyword is a direct product URL;
- two photos of the same room require duplicate physical procurement.

This router is the common linkage layer across repositories. Keep ingestion mechanics in ingestion Skills, web/social collection in intelligence Skills, Miaoda code-sync mechanics in `miaoda-github-sync`, creative engine adapters separate from business rules, renovation/design/procurement mechanics in `xiangxi-renovation-brain`, governance in `xiangxi-entropy-reducer`, and product business rules in product-specific Skills.
