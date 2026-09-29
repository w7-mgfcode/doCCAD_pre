---
id: decisions-adr-003-canonical-generated-separation
slug: /decisions/adr-003-canonical-generated-separation
title: "ADR-003: Structural Separation of Canonical and Generated Knowledge"
type: canonical
audience: [architect, developer]
owners: [architecture]
sources: [docusaurus.config.ts, sidebars-source.ts, sidebars-generated.ts]
related: [architecture-content-planes, decisions-adr-005-pr-gated-generation]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# ADR-003: Structural Separation of Canonical and Generated Knowledge

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-003-canonical-generated-separation.md -->

- **Status**: Accepted
- **Date**: 2026-08-12

## Context & Problem Statement
AI generation must never launder unverified hallucinations into canonical engineering documentation. Merely using naming conventions or warning callouts is fragile and easily bypassed by editors or automated tools.

## Decision
Enforce a physical, structural separation using two distinct plugin instances:
1. **Canonical Plane**: Located in `docs/source/**`, served at route `/docs`. Only human PRs may touch this directory.
2. **Generated Plane**: Located in `docs/generated/**`, served at route `/views`. Automated generation tools write only here.
3. **Unidirectional Link Rule**: Generated views may cite canonical pages; canonical pages never cite generated views (except from a designated Views directory index).
