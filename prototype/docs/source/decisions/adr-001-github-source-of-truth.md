---
id: decisions-adr-001-github-source-of-truth
slug: /decisions/adr-001-github-source-of-truth
title: "ADR-001: Git/GitHub as the Single Source of Truth"
type: canonical
visibility: public
audience: [architect, developer]
owners: [architecture]
sources: [.github/workflows/, .docs-manifest.json]
related: [architecture-system-overview, decisions-adr-003-canonical-generated-separation]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# ADR-001: Git/GitHub as the Single Source of Truth

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-001-github-source-of-truth.md -->

- **Status**: Accepted
- **Deciders**: Lead Product Engineer, Documentation Architect
- **Date**: 2026-08-12

## Context & Problem Statement
Documentation ecosystems frequently introduce external databases (PostgreSQL, MongoDB, vector databases) or headless CMS platforms to store content or metadata. This causes split-brain state: when code is refactored in a Git branch, the external database cannot be branched or rolled back in lockstep.

## Decision
Git/GitHub is the **sole system of record**. 
- All canonical documentation, derived views, task contracts, prompt templates, router configs, and schemas live as versioned files in the repository.
- There is no runtime database, CMS, or external datastore.
- Metadata and dependency mapping are stored in a versioned `.docs-manifest.json` file generated during CI.

## Consequences
- **Positive**: Atomic commits, branch-specific documentation previews, zero database hosting costs, and trivial disaster recovery (`git clone`).
- **Negative**: High-churn analytics or live collaborative editing require PR workflows rather than real-time sockets.
