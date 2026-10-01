---
id: architecture-content-planes
slug: /architecture/content-planes
title: Two Content Planes — Canonical vs Generated
type: canonical
visibility: public
audience: [developer, architect]
owners: [architecture]
sources: [docusaurus.config.ts, sidebars-source.ts, sidebars-generated.ts]
related: [architecture-system-overview, decisions-adr-003-canonical-generated-separation]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# Two Content Planes — Canonical vs Generated

<!-- Archive mapping: Adapted from 05_DOCUMENTATION_DESIGN/information-architecture/content_architecture.md and ADR-003 -->

A foundational invariant of DOCCAD is the physical and architectural separation of documentation into two independent content planes.

## Why a Physical Separation is Necessary

In systems where human-authored documentation and AI-generated text coexist in the same folders, three dangerous failure modes occur:
1. **Silent Promotion**: Generated drafts gradually blend with verified engineering truth until engineers can no longer tell which paragraphs were human-verified.
2. **AI-on-AI Hallucination Feedback**: When an AI model gathers context from previous AI-generated text, subtle factual drift compounds into complete fantasy.
3. **Broken Accountability**: If an incident occurs due to an inaccurate runbook, it becomes impossible to determine whether an engineer or a model authored the instructions.

## The Two Planes in Docusaurus

DOCCAD resolves this by mounting two distinct `@docusaurus/plugin-content-docs` instances in `docusaurus.config.ts`:

```typescript
// Canonical plane (human-owned)
{
  id: 'source',
  path: 'docs/source',
  routeBasePath: 'docs',
  sidebarPath: './sidebars-source.ts',
}

// Generated plane (bot-authored via PR only)
{
  id: 'generated',
  path: 'docs/generated',
  routeBasePath: 'views',
  sidebarPath: './sidebars-generated.ts',
}
```

## Policy Rules

| Rule | Canonical Plane (`docs/source/`) | Generated Plane (`docs/generated/`) |
|---|---|---|
| **Author** | Human engineers only | Automated pipelines via PR |
| **Route Prefix** | `/docs/**` | `/views/**` |
| **Frontmatter Type** | `type: canonical` | `type: generated` (with `generation:` block) |
| **Admissibility as Evidence** | Sole admissible evidence for AI | Strictly forbidden as AI evidence |
| **Citations** | Never cites generated views | Cites canonical docs via plain links or `<EvidenceLink>` |
| **Drift Behavior** | Edits trigger hash changes | Recomputed hashes determine staleness |
