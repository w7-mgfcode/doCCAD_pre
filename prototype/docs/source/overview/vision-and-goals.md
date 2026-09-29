---
id: overview-vision-and-goals
slug: /overview/vision-and-goals
title: Vision, Tenets & Bilingual Strategy
type: canonical
audience: [developer, architect, recruiter, user]
owners: [architecture]
sources: [package.json]
related: [overview-index, architecture-content-planes]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# Vision, Core Tenets & Bilingual Strategy

<!-- Archive mapping: Adapted from 01_PROJECT_KNOWLEDGE/VISION.md and REQUIREMENTS.md -->

## The DOCCAD Vision

DOCCAD envisions an engineering organization where documentation is not an afterthought, but an active, verifiable asset that continuously models reality.

```
Canonical GitHub Documentation -> Project Knowledge -> AI Processing ->
  { User Docs | Technical Architecture | Recruiter Views } -> Interview Preparation

User Question -> Retrieve Project Knowledge -> Analyze Context ->
  Generate Dedicated Page -> PR Review & Persistence
```

### What Exists Today vs Vision

To preserve transparency, DOCCAD maintains a strict distinction between what is designed, what is proven, and what is planned:
1. **Proven & Verified**: A static publishing framework (Docusaurus 3.x), two-plane structural separation, deterministic Level-1 retrieval, hash-based drift detection, task contracts, and complete offline generation via deterministic fixtures.
2. **Designed for Production**: The thin provider abstraction with adapters for Anthropic, Google Gemini, OpenAI, and local Ollama; GitHub Actions CI/CD workflows for PR-gated persistence.
3. **Deferred to Scale**: Vector database retrieval (Level 2/3), automatic translation of dynamic derived views, and enterprise SSO.

## The Six Non-Negotiable Tenets

1. **Files over Databases**: GitHub is the primary system of record. Every architectural decision, schema, prompt, and documentation page is a versioned file.
2. **AI in CI, Never in Serving**: Ordinary readers never interact with runtime AI models. Published pages are statically built HTML/JS assets with zero runtime LLM costs or single points of failure.
3. **Canonical Independence**: Canonical documentation can be built, published, and read even if every AI provider on earth is unreachable.
4. **Governed Derivation**: AI-generated views enter the repository solely through human-reviewed pull requests with provenance metadata.
5. **Deterministic Mechanical Drift**: Staleness is tracked through `sha256` content digests, not fragile timestamps or imprecise AI guesswork.
6. **Bilingual EN/HU Architecture**: English is the authoring and canonical language. Key landing, overview, and onboarding materials are localized into Hungarian (`hu`), with transparent indicators when deep technical specifications remain English.
