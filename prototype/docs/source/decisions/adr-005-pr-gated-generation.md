---
id: decisions-adr-005-pr-gated-generation
slug: /decisions/adr-005-pr-gated-generation
title: "ADR-005: Generated Content Persists Only via Pull Requests"
type: canonical
visibility: public
audience: [architect, developer, operator]
owners: [architecture]
sources: [.github/workflows/docs-generate.yml]
related: [architecture-content-planes, decisions-adr-003-canonical-generated-separation]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# ADR-005: Generated Content Persists Only via Pull Requests

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-005-generated-content-via-pr.md -->

- **Status**: Accepted
- **Date**: 2026-08-12

## Context & Problem Statement
Automated generation pipelines should not write directly to the default repository branch (`main`). Direct automated commits bypass peer review, risk breaking static builds, and undermine human ownership.

## Decision
Generated content persists **strictly through GitHub pull requests**:
- Automated jobs push to ephemeral `docs-gen/<contract>-<target>` branches.
- PRs carry full automated validation reports (schema, link check, hash verification).
- GitHub branch protection requires human review approval before merging into `main`. Auto-merge is strictly disabled for generation PRs.
