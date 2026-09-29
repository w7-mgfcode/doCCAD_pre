---
id: pattern-leveled-retrieval
title: Leveled Retrieval — Deterministic First, Escalate on Evidence
type: knowledge
category: patterns
tags: [retrieval, context-engineering, rag, escalation-boundary, no-vector-db]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-7)
  - outputs/03_solution/ADRs/adr-006-retrieval-level1.md
  - outputs/03_solution/ai_architecture.md (§3)
  - outputs/04_validation/validation_report.md (Gate D, Gate E)
confidence: HIGH
related: [pattern-task-contracts, pattern-hash-drift-detection, framework-anti-overengineering-rules, pattern-thin-provider-abstraction]
---

# Leveled Retrieval — Deterministic First, Escalate on Evidence

**Summary** — Context for AI generation is assembled by four escalating levels: L1 deterministic file selection (adopted), L2 build-time full-text index, L3 embeddings, L4 hybrid+rerank. Only L1 is built at MVP; each escalation has a recorded, evidence-based trigger. The pattern replaces the reflex "add a vector DB for RAG" with an auditable pipeline that a human reviewer can fully reconstruct from the PR.

## Core Logic

**Problem.** Grounded generation needs relevant context, and the industry default is embeddings + vector store from day one. At a corpus of low hundreds of pages, that adds a service, an embedding pipeline, and a sync problem to answer queries that a dict lookup and grep already answer — while making grounding *less* auditable.

**Solution structure — Level 1 (adopted).** Context assembly is deterministic and ordered:

1. Files explicitly named by the contract invocation (e.g., the canonical page being transformed).
2. Frontmatter closure: the page's `sources[]` repo paths plus `related[]` docs, one hop.
3. Keyword expansion: capped `git grep -l` over `docs/source/` for contract-declared key terms.
4. Priority-ordered truncation to the task's context budget.

Every included file is listed in the PR run report, so grounding is reviewable by the human gate; and the assembler refuses any path outside the contract's `allowed_evidence` globs *before* any model call. VERIFIED BY EXECUTION in 05_poc: the dry run printed the evidence assembly, including refusals of in-closure-but-not-allowed files, accepted 3 evidence files, and rendered the full prompt with delimited evidence blocks — with zero API keys and no network.

**Explicit escalation boundaries (recorded in ADR-006, not built):**

- **L2 — build-time full-text index**, reusing the local search plugin's index: only when the corpus exceeds ~1,500 pages OR documented grounding failures accumulate (the grep step demonstrably missing relevant canon).
- **L3 — embeddings**: only after L2 *measurably* fails on retrieval quality. L3 requires a persisted index and would be the system's first "service-ish" component — hence deferred.
- **L4 — hybrid + rerank**: unjustifiable at this scale; out of scope.

Revisit requires evidence — collected failed-grounding examples — "not enthusiasm."

## Best Practices

1. **Start from contract-named files, not search**, because the task usually knows its primary evidence exactly; retrieval should fill gaps, not define scope.
2. **Use the metadata graph (`sources`/`related`) as the retrieval index**, because it's already CI-schema-enforced and doubles as the drift-detection manifest — one structure, two jobs.
3. **List every context file in the run report**, because auditable grounding is what makes human review of AI output meaningful.
4. **Write the escalation trigger down at adoption time** (corpus size + measured failure), because otherwise the upgrade happens on mood, and un-building infrastructure is much harder than adding it.
5. **Cap and truncate by priority**, because a deterministic budget beats silent context overflow — what got cut is knowable.

## Pitfalls

- **Vector DB at MVP** was rejected explicitly: service + embedding pipeline + sync problem for queries grep already answers, plus lost auditability. Gate E's validation confirms "no vector DB" as an applied removal.
- **Full-corpus-in-context** was also rejected: cost aside, "it dulls grounding discipline" — if the model sees everything, nobody can say what a claim is grounded in.
- L1 recall is bounded by metadata hygiene and grep literality (synonyms/paraphrases are missed). Mitigations: CI-enforced frontmatter schema; contract-declared key terms. When these measurably fail, that *is* the L2 trigger — log the failures instead of patching around them.
- Reusing the search plugin's index for L2 is the intended cheap path; building a bespoke index first would skip a level.

## Expert Notes

The deep insight is that retrieval sophistication and reviewability trade off directly: every level up makes "why did the model see this file?" harder to answer, and this system's trust story depends on that answer being easy (run report + human PR gate). Leveling also converts an architecture argument into a measurement question — the team never has to debate "should we do RAG?"; it has to check "are we >1,500 pages, or do we have documented grounding failures?" That reframing is the anti-overengineering discipline (framework-anti-overengineering-rules) applied to the most hype-prone component in the stack. Note the boundary numbers are honest estimates, not magic: the point is that *some* concrete boundary is recorded and owned by an ADR, so escalation is a decision with a paper trail.

## Evidence & Further Reading

- `outputs/03_solution/ADRs/adr-006-retrieval-level1.md` — decision, boundary, rejected alternatives.
- `outputs/03_solution/ai_architecture.md` §3 — the four-step L1 algorithm and escalation ladder.
- `outputs/05_poc/VALIDATION_NOTES.md` §e — executed dry-run of the assembler; `outputs/05_poc/scripts/generate_page.py`.
- `outputs/04_validation/validation_report.md` Gate E — "no vector DB (Level-1 retrieval, ADR-006)" listed among applied removals.
