# ADR-002: Docusaurus 3.x as the Documentation Framework

Status: Accepted · 2026-08-12

## Context
Six platforms were analyzed with equal depth and scored against 11 weighted criteria
(../../02_comparison/decision_matrix.md). Constraints: static-first, self-hostable, structural
canonical/generated separation, custom components, Mermaid, EN/HU, programmatic generation target.

## Decision
Adopt Docusaurus 3.x (weighted winner 88.6/100) with future.faster flags (Rspack, SSG workers), docs plugin
multi-instance (source→/docs, generated→/views), @docusaurus/theme-mermaid, local search plugin, filesystem
i18n (en, hu).

## Consequences
+ Structural content-plane separation; <InterviewPrep/> as a real MDX component; provenance frontmatter
  passes validation; active upstream.
- Node >=24.14 + React 19 toolchain; MDX v3 strictness means AI output must pass a build gate (this is a
  feature: deterministic validation); Mermaid renders client-side only.

## Alternatives
Mintlify (85.0): best AI-consumption surface, rejected — vendor build/serve plane, Enterprise-gated
self-host/export violate provider independence. MkDocs+Material (83.8): simplest architecture, rejected as
primary — Material public security support ends 2026-11-05, core dormant; remains the documented fallback.
Zensical (76.4): revisit trigger = 1.0 + plugin API + multi-language content. Hyperbook (76.0): education
niche. GitBook (72.2): Git is a mirror, not the engine.
