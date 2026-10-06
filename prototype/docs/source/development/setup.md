---
id: development-setup
slug: /development/setup
title: Local Development & Contribution Workflow
type: canonical
visibility: public
audience: [developer]
owners: [core]
sources: [package.json, scripts/validate_docs.py]
related: [getting-started-installation, development-contracts-and-schemas]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Local Development & Contribution Workflow

<!-- Archive mapping: Adapted from 09_RESULTS/implementation/poc/docs/source/development/setup.md and CONTRIBUTING.md -->

This document outlines the day-to-day development workflow for contributing canonical documentation, creating derived templates, and running local tests.

## Running the Dev Server

Start Docusaurus with hot reloading:

```bash
npm start
```

The site will be available at `http://localhost:3000/doCCAD_pre/`.

## Authoring Canonical Documentation

When adding or updating a canonical document:
1. Place the file under `docs/source/<category>/<slug>.md`.
2. Ensure required frontmatter fields are complete: `id`, `title`, `type: canonical`, `audience`, `owners`, `sources`, and `last_validated`.
3. Set `ai_generation.allowed: true` if this document is admissible as evidence for derived views.
4. Run validation before opening a PR:
   ```bash
   npm run validate
   ```

## Contribution Principles

- **Preserve Before Modifying**: Historical decisions and rationale should be superseded via new ADRs rather than silently deleted.
- **Never Commit Secrets**: API keys, credentials, and tokens must never appear in files or context payloads. Use `.env.example`.
- **Maintain Plane Integrity**: Do not place generated content in `docs/source/`.
