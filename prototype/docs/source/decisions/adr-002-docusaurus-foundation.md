---
id: decisions-adr-002-docusaurus-foundation
slug: /decisions/adr-002-docusaurus-foundation
title: "ADR-002: Docusaurus 3.x as the Publishing Foundation"
type: canonical
visibility: public
audience: [architect, developer]
owners: [architecture]
sources: [package.json, docusaurus.config.ts]
related: [architecture-platform-research, decisions-adr-003-canonical-generated-separation]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# ADR-002: Docusaurus 3.x as the Publishing Foundation

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-002-docusaurus-framework.md -->

- **Status**: Accepted
- **Score**: 88.6/100 (Weighted 11-criterion evaluation)
- **Date**: 2026-08-12

## Context & Problem Statement
DOCCAD requires a modern static documentation framework supporting multi-instance documentation plugins (to segregate `/docs` from `/views`), React 19 component extensibility, offline static compilation, local search, and bilingual i18n (`en` and `hu`).

## Decision
Adopt **Docusaurus 3.x** as the primary publishing framework.
- Configure `@docusaurus/plugin-content-docs` for canonical docs (`/docs`) and derived views (`/views`).
- Integrate `@easyops-cn/docusaurus-search-local` for build-time offline search indexing.
- Use `@docusaurus/theme-mermaid` for diagrams as code.

## Revisit Trigger
If Docusaurus build times exceed 10 minutes on corpora over 5,000 pages, evaluate adopting `@docusaurus/faster` (Rspack compiler) or migrating to MkDocs+Material via our documented exit plan.
