---
id: decisions-adr-009-deployment-github-pages
slug: /decisions/adr-009-deployment-github-pages
title: "ADR-009: Static Deployment via GitHub Pages"
type: canonical
audience: [architect, operator]
owners: [architecture]
sources: [.github/workflows/docs-publish.yml, docusaurus.config.ts]
related: [architecture-system-overview, decisions-adr-002-docusaurus-foundation]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# ADR-009: Static Deployment via GitHub Pages

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-009-deployment-github-pages.md -->

- **Status**: Accepted
- **Date**: 2026-08-12

## Context & Problem Statement
Hosting dynamic documentation servers (e.g. Next.js SSR, custom backend APIs) requires maintaining running application containers, load balancers, and monitoring infrastructure. This expands the operational footprint and creates vulnerability to runtime exploitation.

## Decision
Deploy the documentation website as a **pure static build artifact** via **GitHub Pages** (or any static object bucket/CDN):
- Production deployment runs `docusaurus build` via GitHub Actions using OIDC tokens.
- No Node.js process, Python server, or database runs in the serving path.
- Offline and local reading use the exact same static build directory (`build/`).
