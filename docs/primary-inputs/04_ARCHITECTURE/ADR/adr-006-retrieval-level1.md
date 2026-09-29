# ADR-006: Level-1 Deterministic Retrieval with Explicit Escalation Boundary

Status: Accepted · 2026-08-12

## Context
Grounded generation needs relevant context. Options range from file selection (L1), full-text index (L2),
embeddings (L3), hybrid+rerank (L4). Corpus at MVP: low hundreds of pages.

## Decision
L1: contract-named files + frontmatter sources/related closure (one hop) + capped git grep expansion +
priority truncation. Every included file is listed in the PR run report. Escalation to L2 (reuse the search
plugin's build-time index) only when corpus > ~1500 pages OR documented grounding failures accumulate; L3
only after L2 measurably fails; L4 out of scope.

## Consequences
+ Auditable, reproducible context; zero retrieval infrastructure; grounding reviewable by humans.
- Recall limited by metadata hygiene (mitigated: frontmatter schema is CI-enforced) and grep literality.

## Alternatives
Vector DB at MVP rejected: a service + embedding pipeline + sync problem to answer queries a dict lookup and
grep already answer at this scale. Full-corpus-in-context rejected (cost, and it dulls grounding discipline).
