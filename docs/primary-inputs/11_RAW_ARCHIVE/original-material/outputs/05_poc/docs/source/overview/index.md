---
id: overview
slug: /overview
title: Project Overview
type: canonical
audience: [developer, architect, user]
sources: [docusaurus.config.ts, package.json, scripts/, ai/]
owners: [maintainer]
related: [architecture-system-overview, development-setup]
ai_generation:
  allowed: true
  derived_pages: [recruiter]
last_validated: 2026-08-12
---

## What this is

This site is the proof of concept for a **GitHub-native AI documentation system**: a
single Git repository is the system of record, the published site is a static build
artifact, and AI participates only as a *generation plane* that writes derived pages
through pull requests. No AI service is involved in serving or reading the published
documentation.

## What the PoC actually contains

The PoC is deliberately small. It ships:

- A Docusaurus 3 site with **two structurally separated content planes**: canonical
  human-owned pages under `docs/source/` (this plane, served at `/docs`) and
  AI-derived pages under `docs/generated/` (served at `/views`). The separation is
  enforced by two independent docs-plugin instances, not by naming convention.
- A **provider abstraction** in `ai/`: one `complete()` interface with four thin HTTP
  adapters (Anthropic, Gemini, OpenAI, and a local OpenAI-compatible endpoint) and a
  config-driven router with privacy pinning and fallback chains.
- **Task contracts** in `contracts/` and versioned prompt templates in `prompts/`
  that bound what generation jobs may read and produce.
- **Pipeline scripts** in `scripts/`: frontmatter/schema validation, change-impact
  detection via content hashes, and the contract-driven generation pipeline.
- **CI workflows** in `.github/workflows/` for deterministic validation on PRs and
  human-triggered generation runs.

## What the PoC does not do

Honest limitations: there is no search index, no deployed instance, no Hungarian
translations yet (the `hu` locale builds and falls back to English), and no live
generation run is included in the repository — the generation pipeline is
demonstrated in `--dry-run` mode so the PoC works without any API keys.

## Status

Proof of concept. Every claim on the generated pages under `/views` is derived from
the canonical pages in this plane and is traceable through frontmatter provenance.
