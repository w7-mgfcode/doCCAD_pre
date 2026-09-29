---
id: decisions-adr-006-retrieval-level1
slug: /decisions/adr-006-retrieval-level1
title: "ADR-006: Level-1 Deterministic Retrieval"
type: canonical
audience: [architect, developer]
owners: [architecture]
sources: [scripts/generate_page.py, scripts/generate_question.py]
related: [architecture-system-overview, architecture-ai-generation-plane]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# ADR-006: Level-1 Deterministic Retrieval

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-006-retrieval-level1.md -->

- **Status**: Accepted
- **Date**: 2026-08-12

## Context & Problem Statement
Vector databases with embedding pipelines (RAG) are frequently introduced into documentation projects prematurely. For moderate corpus sizes (fewer than 1,500 documents), embedding stores introduce non-deterministic retrieval, external SaaS dependencies, embedding version mismatches, and re-indexing lag.

## Decision
Adopt **Level-1 Deterministic Retrieval**:
- Assemble context strictly from:
  1. Files explicitly targeted by the generation invocation.
  2. Frontmatter dependency closure (`sources` repo paths + `related` document IDs, 1 hop).
  3. Stable keyword scanning over canonical files with deterministic tie-breaking.
- Impose strict context token budgeting.
- Only escalate to Level 2 (full-text index) or Level 3 (embeddings) if the canonical corpus exceeds ~1,500 pages or measured grounding failures demonstrate that keyword/closure retrieval is insufficient.
