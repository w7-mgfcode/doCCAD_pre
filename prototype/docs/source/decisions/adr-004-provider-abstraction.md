---
id: decisions-adr-004-provider-abstraction
slug: /decisions/adr-004-provider-abstraction
title: "ADR-004: Thin Provider Abstraction & Routing"
type: canonical
audience: [architect, developer]
owners: [architecture]
sources: [ai/provider.py, ai/router.py, ai.config.yaml]
related: [architecture-ai-generation-plane, decisions-adr-005-pr-gated-generation]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# ADR-004: Thin Provider Abstraction & Routing

<!-- Archive mapping: Adapted from 04_ARCHITECTURE/ADR/adr-004-provider-abstraction.md -->

- **Status**: Accepted
- **Date**: 2026-08-12

## Context & Problem Statement
Integrating commercial and local LLMs often leads to adopting heavy agent frameworks (LangChain, LiteLLM, CrewAI) that pull hundreds of transitive dependencies, obscure HTTP errors, and introduce non-deterministic loops.

## Decision
Define a single structural `Provider` protocol in Python:
- Implement lightweight (~40 line) REST adapters for Anthropic, Gemini, OpenAI, and local OpenAI-compatible endpoints (Ollama/vLLM), alongside a deterministic `FixtureProvider` for offline testing.
- Route models via declarative rules in `ai.config.yaml`.
- Enforce that tasks marked `privacy: private` never fall back to cloud providers.
