---
name: grilling
description: Relentlessly clarify and stress-test a plan, requirement, decision, or design before execution.
---

Interview the user until there is a shared understanding of the goal, constraints, dependencies, risks, and acceptance criteria. Model the problem as a decision tree: every settled decision can unlock downstream decisions.

Work in rounds. The frontier is the set of questions whose prerequisites are already settled. Ask the whole frontier in one round. Number each question and give a recommended answer for each one. Do not ask a question whose answer depends on another still-open question in the same round.

For every round:

❓ **Q1 — <question title>**: <question, options, and relevant consequences>

➡️ **Recommended answer:** <your recommended answer and why>

Use tools and repository facts yourself whenever the answer can be discovered from the environment. Do not ask the user for facts that can be inspected directly. The user decides business choices; the agent retrieves facts.

After each user response, recompute the decision tree and ask the next frontier. Explicitly surface assumptions, edge cases, permission boundaries, data sources, money flows, state transitions, failure modes, and acceptance criteria when relevant.

Do not begin implementation, editing, deployment, or other irreversible execution until the frontier is empty and the user confirms the shared understanding. For routine tasks that are already fully specified, do not invoke this workflow unnecessarily.

Origin: adapted from Matt Pocock's public `grilling` skill (MIT licensed) for Xiangxi multi-agent use.
