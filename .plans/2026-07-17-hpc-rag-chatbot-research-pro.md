Title: Research Pro rubric for an HPC RAG chatbot
Status: Draft
Owner: agent-llm
Reviewers: n/a
Issues: n/a
Scope: repo-wide
Risk: low

# Context & Problem

The cloud GPU milestone plan defines how to automate technical iteration, but it does not fully
answer the product question: what makes a RAG chatbot viable for academic HPC users? The acceptance
set already covers Slurm, Amarel, support/policy, and safety questions. Research Pro should refine
that rubric with external evidence from academic HPC support documentation, public support patterns,
and examples of AI assistants or self-service workflows used by research computing centers.

This research should run in parallel with cloud setup/download time. It must not block the first
Vast smoke milestone, and it must not require private OARC tickets or raw ServiceNow exports.

# Goals / Non-goals

Goals:

- Define viable user-facing capabilities for an HPC RAG chatbot.
- Identify common academic HPC support categories that should be represented in the corpus and
  acceptance tests.
- Define refusal, uncertainty, and escalation behavior for unsafe or under-supported questions.
- Propose production-readiness metrics that complement the existing acceptance harness.
- Identify missing acceptance categories before HPC promotion.

Non-goals:

- Do not ingest private Rutgers/OARC support tickets.
- Do not create new corpus files under `docs/`.
- Do not replace the existing acceptance harness.
- Do not make product decisions that require privileged Rutgers policy context without human review.

# Research Prompt

Use ChatGPT Deep Research / Research Pro with this objective:

```text
Research what capabilities, safety behaviors, and benchmark metrics define a viable RAG chatbot for
academic HPC users. Focus on university research computing / OARC-like support contexts, including
Slurm, account access, storage, software modules, GPU jobs, data transfer, troubleshooting, support
escalation, and policy-sensitive questions.

Use official or primary sources first: university HPC documentation, research computing support
pages, Slurm documentation, and public service-desk guidance. Use secondary sources only for
context. Do not infer Rutgers-specific policy unless it appears in Rutgers/OARC public material.

Output:
1. A prioritized support-category taxonomy for an HPC chatbot.
2. A viable-product rubric with must-have, should-have, and later capabilities.
3. Refusal and escalation rules for secrets, private ticket data, unsupported cluster-specific
   claims, unsafe commands, billing/allocation policy, and ambiguous user requests.
4. A benchmark plan that maps categories to acceptance questions and metrics.
5. Gaps in the current 18-question acceptance set.
6. Recommended additions to acceptance tests before HPC promotion.
7. Source URLs for every concrete claim.
```

# Output Contract

Save the extracted Research Pro report to:

```text
project_docs/research_pro/2026-07-17-hpc-rag-chatbot-product-rubric.md
```

If normalized JSON is extracted, save it next to the Markdown report:

```text
project_docs/research_pro/2026-07-17-hpc-rag-chatbot-product-rubric.json
```

The Markdown report should include:

- executive summary;
- source-priority notes;
- support-category taxonomy;
- viable-product rubric;
- refusal/escalation policy;
- benchmark and acceptance-test recommendations;
- gaps against `data/evaluation/acceptance/rag_v1_questions.jsonl`;
- source URLs.

# Implementation Plan

- [ ] Start Research Pro in a fresh ChatGPT conversation using the prompt above.
- [ ] Poll read-only until the report is complete; do not send follow-up prompts unless the user
  explicitly asks.
- [ ] Extract Markdown and JSON artifacts through the existing Research Pro extraction workflow.
- [ ] Save outputs under `project_docs/research_pro/`, not `docs/`.
- [ ] Compare findings against the existing acceptance categories:
  `slurm_basics`, `amarel_access`, `support_policy`, `negative_safety`, and
  `attachment_optional`.
- [ ] Convert gaps into proposed acceptance-test additions or a follow-up implementation plan.
- [ ] Use the rubric as an input gate before HPC promotion.

# Testing Strategy

Research output is reviewed rather than unit-tested. Acceptance criteria:

- The report cites official or primary sources for concrete recommendations.
- The report does not include or request private ServiceNow ticket data.
- The report separates generic HPC guidance from Rutgers/OARC-specific facts.
- The report maps recommendations to measurable acceptance or benchmark checks.
- The report identifies which gaps are required before HPC promotion versus later improvements.

# Rollout & Telemetry

This research informs the cloud benchmark loop and the final HPC promotion decision. It does not
change runtime behavior by itself. Any recommended code, corpus, or acceptance-test changes should
be implemented in separate focused plans or pull requests.

# Risks & Mitigations

- Risk: Research Pro overgeneralizes from other institutions to Rutgers/OARC.
  - Mitigation: require source labels and separate generic HPC guidance from local policy.
- Risk: research recommends using private ticket data.
  - Mitigation: keep private ticket data out of scope and require public/prepared-source paths only.
- Risk: the rubric becomes too broad for the first production gate.
  - Mitigation: classify capabilities as must-have, should-have, or later.
- Risk: cloud iteration proceeds before the product rubric is ready.
  - Mitigation: allow Milestone 1 smoke to proceed, but require the rubric before HPC promotion.

# Security & Privacy

Research Pro should use public information only. Do not paste private tickets, API keys, raw
ServiceNow exports, user identifiers, cluster secrets, hidden prompts, or unpublished Rutgers/OARC
policy into ChatGPT. The output belongs under `project_docs/research_pro/` because it is a
project-facing research artifact, not RAG corpus material.

# Docs to Update

After the report is extracted and reviewed, update the relevant plan or architecture docs with only
the accepted product rubric and benchmark changes. Do not duplicate large report sections in
`README.md`.

# Rollback Plan

If the research report is low quality or not useful, mark this plan `Abandoned`, leave cloud
milestones unchanged, and draft a narrower prompt focused on acceptance-test gaps only.

# Decision Log

- 2026-07-17: Track Research Pro separately from cloud GPU execution so it can run in parallel.
- 2026-07-17: Require Research Pro findings before HPC promotion, but not before the one-hour Vast
  smoke test.
- 2026-07-17: Store research outputs in `project_docs/research_pro/`, not `docs/`.
