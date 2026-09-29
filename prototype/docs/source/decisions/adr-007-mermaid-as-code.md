---
id: decisions-adr-007-mermaid-as-code
slug: /decisions/adr-007-mermaid-as-code
title: "ADR-007: Mermaid-as-Code with CI Compilation Gate"
type: canonical
audience: [architect, developer]
owners: [architecture]
sources: [docs/diagrams/, docusaurus.config.ts]
related: [architecture-system-overview, decisions-adr-002-docusaurus-foundation]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# ADR-007: Mermaid-as-Code with CI Compilation Gate

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-007-mermaid-as-code.md -->

- **Status**: Accepted
- **Date**: 2026-08-12

## Context & Problem Statement
Architecture diagrams stored as binary images (PNG, JPEG, draw.io XML) cannot be diffed, reviewed, or automatically updated in Git pull requests. Furthermore, image diagrams quickly drift from source code implementations.

## Decision
All system diagrams in DOCCAD are authored as **Mermaid-as-code**:
- Shared diagrams reside as `.mmd` files in `docs/diagrams/**`.
- One-off illustrations are authored as fenced ` ```mermaid ` code blocks directly in Markdown/MDX.
- CI validates diagrams using `@docusaurus/theme-mermaid` and `mermaid-cli` compilation gates.
- AI modifications to diagrams occur strictly through `UpdateMermaidDiagram` task contracts.
