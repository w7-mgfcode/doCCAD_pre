# Rejected Alternatives  [EXPLICIT — each recorded in an evidence artifact]

Platform level: **Mintlify** (raw runner-up 85.0) — vendor build/serve plane, Enterprise-gated self-hosting
and static export violate provider independence (decision_matrix.md). **GitBook** (72.2) — internal block
model, not Git, is the operational source of truth; normalized exports break deterministic provenance.
**MkDocs+Material** (83.8) — kept only as constraint-adjusted fallback: Material public security support
ends 2026-11-05, core dormant. **Zensical** (76.4) — pre-1.0, no plugin API, no multi-language content;
revisit trigger recorded. **Hyperbook** (76.0) — education-oriented; bus factor 1; no HU UI locale.

Architecture level (with the ADR recording each): Git+database hybrid and SaaS-mirror models (ADR-001);
single-tree naming-convention separation and separate-repo separation for generated content (ADR-003);
LangChain/LiteLLM-style frameworks, single-provider hard-coding, autonomous multi-agent orchestration
(ADR-004); auto-merge, direct-commit, and ephemeral-only persistence of generated content (ADR-005);
vector database at MVP and full-corpus-in-context (ADR-006); PlantUML and binary diagram formats (ADR-007);
runtime AI generation and per-page hybrid hydration (ADR-008); own server at MVP and Kubernetes (ADR-009);
model self-reported confidence as a provenance field (content_architecture.md §5); blocking merges on
docs-drift suspicion (automation_architecture.md §2 — rejected as review theater).
