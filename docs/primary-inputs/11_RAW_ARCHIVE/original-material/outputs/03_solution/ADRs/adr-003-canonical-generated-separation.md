# ADR-003: Structural Separation of Canonical and Generated Content

Status: Accepted · 2026-08-12

## Context
AI-derived pages must never silently become authoritative. A naming convention (a folder) is advisory only;
a structural boundary is enforceable.

## Decision
Two docs-plugin instances: `source` (docs/source, route /docs, human CODEOWNERS) and `generated`
(docs/generated, route /views, bot-authored but human-approved PRs). CI fails any generation PR touching
paths outside docs/generated/** and its i18n mirror. Generated pages carry mandatory provenance frontmatter
and a rendered provenance banner. Canonical pages never link into /views except from one Views index.
Promotion to canon = human rewrite via normal PR, retaining provenance_history.

## Consequences
+ Laundering is structurally impossible; audiences see clearly labeled derived content; either plane can be
  rebuilt/deleted independently.
- Two sidebars/configs to maintain; cross-plane UX needs the component layer (accepted).

## Alternatives
Single tree + frontmatter flag rejected (unenforceable at the route/ownership level). Separate repo for
generated content rejected (two repos to keep in sync — complexity without governance gain at this scale).
