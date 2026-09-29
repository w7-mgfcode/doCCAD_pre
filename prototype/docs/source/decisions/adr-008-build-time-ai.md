---
id: decisions-adr-008-build-time-ai
slug: /decisions/adr-008-build-time-ai
title: "ADR-008: Build-Time/CI-Time AI over Runtime AI"
type: canonical
audience: [architect, developer, operator]
owners: [architecture]
sources: [scripts/generate_page.py, docusaurus.config.ts]
related: [architecture-ai-generation-plane, decisions-adr-009-deployment-github-pages]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# ADR-008: Build-Time/CI-Time AI over Runtime AI

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-008-build-time-ai.md -->

- **Status**: Accepted
- **Date**: 2026-08-12

## Context & Problem Statement
Integrating live conversational AI chat widgets on documentation websites creates non-deterministic reader experiences, high API token costs, latency spikes, and real-time prompt injection vulnerabilities.

## Decision
Confine all AI generation to **Build-Time / CI-Time**:
- AI processes canonical evidence and produces static Markdown/MDX or structured JSON during offline CLI runs or CI pipelines.
- The published site renders pre-computed, human-reviewed static artifacts.
- Readers experience zero-latency static page loads with 100% deterministic content.
