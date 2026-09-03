---
name: grilling
description: Stress-test a plan, decision, requirement, or design by resolving the decision tree before execution.
---

Interview the user until there is shared understanding. Treat the problem as a decision tree: each decision may unlock downstream decisions.

Work in rounds. The frontier is the set of decisions whose prerequisites are already settled. Ask the whole frontier in one round. Number each question and include your recommended answer for each.

Do not ask the user for facts that can be obtained from the repository, tools, files, logs, or connected systems. Gathering facts is the agent's job; choosing among decisions is the user's job.

After each round, recompute the frontier. Do not ask a question whose answer depends on another unresolved question in the same round.

Use this skill for ambiguous, strategic, high-impact, or irreversible work. Do not use it for routine low-risk tasks whose requirements are already clear.

Do not implement, deploy, delete, migrate, or otherwise execute the plan until the frontier is empty and the user confirms the shared understanding.
