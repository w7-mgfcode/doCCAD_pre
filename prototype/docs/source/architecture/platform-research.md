---
id: architecture-platform-research
slug: /architecture/platform-research
title: Six-Platform Research & Evaluation
type: canonical
visibility: public
audience: [developer, architect]
owners: [architecture]
sources: [docusaurus.config.ts]
related: [architecture-system-overview, decisions-adr-002-docusaurus-foundation]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# Six-Platform Research & Evaluation

<!-- Archive mapping: Adapted from 02_RESEARCH/documentation-platforms/_comparison/ and 04_ARCHITECTURE/architecture-decisions/decision_matrix.md -->

During the initial architecture phase of DOCCAD, six leading documentation platforms were rigorously evaluated across 11 weighted criteria:

1. **Docusaurus 3.x** (Meta Open Source)
2. **Mintlify** (Commercial SaaS / Git sync)
3. **MkDocs + Material** (Python Docs-as-Code)
4. **Zensical** (Modern Static Docs)
5. **Hyperbook** (Interactive Book Framework)
6. **GitBook** (Hosted Docs SaaS)

## Weighted Scorecard Summary

| Rank | Platform | Total Score (/100) | Primary Strengths | Disqualifying Limitations |
|---|---|---|---|---|
| **1** | **Docusaurus 3.x** | **88.6** | Dual docs-plugin instances, React 19 component ecosystem, native offline build, local search | Requires Node.js toolchain |
| **2** | **Mintlify** | **85.0** | Polished default typography, built-in components | Closed SaaS hosting, lacks dual-plane separation |
| **3** | **MkDocs + Material** | **83.8** | Lightweight Python toolchain, excellent search, fast builds | Limited dynamic React component extensibility |
| **4** | **Zensical** | **76.4** | Clean Markdown support | Immature ecosystem, unproven multi-plane architecture |
| **5** | **Hyperbook** | **76.0** | Clean layout, good for structured tutorials | Rigid navigation taxonomy, limited search plugin support |
| **6** | **GitBook** | **72.2** | User-friendly WYSIWYG editor | Proprietary sync conflicts, high cost, SaaS dependency |

## The Selection Rationale

Docusaurus won primarily due to **Architectural Sovereignty**:
- It can be built completely offline inside an isolated container with zero outbound internet access.
- Its `@docusaurus/plugin-content-docs` supports multiple concurrent instances with separate route trees (`/docs` vs `/views`), providing physical enforcement of canonical vs derived content planes.
- Native React MDX enables rich interactive components like `<EvidenceLink>` and `<InterviewPrep>` without runtime server requirements.
