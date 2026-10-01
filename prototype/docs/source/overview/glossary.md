---
id: overview-glossary
slug: /overview/glossary
title: DOCCAD Architectural Glossary
type: canonical
visibility: public
audience: [developer, architect, recruiter, user]
owners: [architecture]
sources: [schemas/document.schema.json]
related: [overview-index, architecture-content-planes]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# DOCCAD Architectural Glossary

<!-- Archive mapping: Adapted from 09_RESULTS/research/knowledge-base/90-glossary.md -->

A reference glossary of core concepts, architectural terms, and acronyms used throughout the DOCCAD documentation platform.

| Term | Definition in DOCCAD |
|---|---|
| **Canonical Plane** | The human-authored, peer-reviewed collection of engineering truth residing under `docs/source/` and served at `/docs`. It is the only admissible evidence for generation. |
| **Derived Plane** | The collection of audience-specific views (recruiter profiles, interview prep, question answers) generated from canonical evidence under `docs/generated/` and served at `/views`. |
| **Level-1 Retrieval** | Deterministic context assembly combining explicit file targets, frontmatter dependency closures, and deterministic keyword grep. |
| **Task Contract** | A declarative YAML specification (`contracts/*.yaml`) defining the allowed evidence, output schema, quality gates, and prohibited assertions for an AI task. |
| **Mechanical Drift** | Discrepancy between the `sha256` content hash of a source document recorded at generation time and the current hash of that file on disk. |
| **PR-Gated Persistence** | The architectural rule that automated AI generators may only commit to candidate branches and open pull requests, never merging directly to default branches. |
| **Simulated Approval** | A local demonstration mechanism tracking review decisions in `demo_reviews.json` (`approved-for-demo`) without setting production approval status. |
| **Docs-as-Code** | The philosophy of storing documentation in the same version-control repositories as source code, using the same linters, reviews, and release workflows. |
