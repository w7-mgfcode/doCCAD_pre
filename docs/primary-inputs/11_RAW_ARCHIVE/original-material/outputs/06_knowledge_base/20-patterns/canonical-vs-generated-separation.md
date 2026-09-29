---
id: pattern-canonical-generated-separation
title: Canonical vs Generated Content — Structural Separation
type: knowledge
category: patterns
tags: [content-planes, provenance, docusaurus, governance, ai-content]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-3)
  - outputs/03_solution/ADRs/adr-003-canonical-generated-separation.md
  - outputs/03_solution/content_architecture.md (§1–3, §6, §9)
  - outputs/01_products/docusaurus/ADRs/adr-002-multi-instance-docs-for-canonical-vs-generated.md
  - outputs/04_validation/validation_report.md (Gate D, Gate F)
confidence: HIGH
related: [pattern-metadata-provenance-contract, pattern-pr-gated-generation, pattern-ai-in-ci-not-serving, practice-prompt-injection-defenses]
---

# Canonical vs Generated Content — Structural Separation

**Summary** — AI-derived documentation must never silently become authoritative. This pattern makes the boundary between human-owned canonical knowledge and AI-generated derived views *structural* — enforced by build tooling, routes, ownership and CI — rather than a folder-naming convention that anyone (or any bot) can quietly violate. It is the load-bearing anti-laundering control of the whole architecture.

## Core Logic

**Problem.** A docs system with an AI generation layer has two content classes with different trust levels. If the only thing distinguishing them is a directory name, a generated file can drift into the canonical tree, be cited as evidence by the next generation run, and launder hallucinations into "truth" (AI-citing-AI chains).

**Solution structure.** Two independent Docusaurus docs-plugin instances:

- Instance `source`: `docs/source/**`, route `/docs`, human CODEOWNERS, edited only by human PRs.
- Instance `generated`: `docs/generated/**`, route `/views`, bot-authored via PR, human approval enforced by branch protection.

Each plane has its own sidebar, its own route tree, and its own CI path gate: CI fails any generation PR touching paths outside `docs/generated/**` (and its i18n mirror). A generated file therefore *physically cannot* appear under `/docs`. Docusaurus dogfoods multi-instance docs upstream (`id: 'community'`) [VERIFIED-REPO], which is one reason it won the platform comparison.

**Mechanics.**
- Generated pages carry mandatory provenance frontmatter (`type: generated`, `generation:` block with source hashes — see pattern-metadata-provenance-contract) and render a visible "AI-generated content" provenance banner via the theme, so readers never mistake derived content for canon.
- Link direction is asymmetric: generated pages may cite canonical pages; canonical pages never link into `/views` except from one dedicated Views index (canon must not depend on derivables).
- Generated pages are never admissible evidence for another generation task — only canonical content is.
- **Promotion path**: when a generated page proves durably valuable, a human rewrites/adopts it into `docs/source/` via a normal PR; frontmatter `type` changes and the old `generation` block is retained as `provenance_history`. Promotion is a human act, never automation.
- Either plane can be rebuilt or deleted independently; generated content is always regenerable from sources.

VERIFIED BY EXECUTION in 05_poc: the two-instance config builds and serves `/docs/...` and `/views/...` routes (HTTP 200 smoke test), the interview page renders the provenance banner, and `validate_docs.py` reports "planes intact".

## Best Practices

1. **Make the boundary structural, not conventional** — separate plugin instances/route trees, because conventions are advisory and erode; structure is enforceable by CI.
2. **Enforce the boundary in CI as a path gate** on generation PRs, because the bot's write scope must be mechanical, not trusted.
3. **Render provenance visibly** (banner from frontmatter), because reader-facing honesty is part of the control, not decoration.
4. **Forbid AI-citing-AI**: contracts exclude generated pages as evidence, because error compounding is the failure mode separation exists to stop.
5. **Define an explicit promotion path** with retained `provenance_history`, because without one, useful generated content gets copy-pasted into canon untraceably.

## Pitfalls

- **Frontmatter-flag-only separation** (single tree + `generated: true`) was explicitly rejected: unenforceable at route/ownership level; a flag edit is a one-line laundering attack.
- **Separate repo for generated content** was rejected as complexity without governance gain at this scale: two repos to keep in sync, no additional enforcement.
- Two sidebars/configs to maintain is the accepted cost; cross-plane UX (e.g., embedding InterviewPrep alongside a canonical page's `/views` twin) needs the component layer.
- Deleting a canonical page without cleanup strands dependents: CI flags all dependent generated pages for removal in the same PR.

## Expert Notes

The simpler alternative this pattern beat is "one tree plus a naming convention," and the comparison work shows why the platform choice and this pattern are coupled: only platforms with genuine multi-instance or plugin-level separation (Docusaurus; MkDocs via plugins) can enforce it. GitBook was disqualified partly because its Git Sync normalizes exports, breaking the deterministic file identity this separation and its hash-based drift detection depend on. Note also that the separation is doing security work, not just editorial work: it bounds prompt-injection blast radius (T2/T11 in the threat model) because injected output can only ever land in `/views` behind a banner and a human gate.

## Evidence & Further Reading

- `outputs/03_solution/ADRs/adr-003-canonical-generated-separation.md` — decision, consequences, rejected alternatives.
- `outputs/03_solution/content_architecture.md` §1 (why naming is too weak), §3 (policy + promotion), §6 (link asymmetry), §9 (bot write scope).
- `outputs/02_comparison/decision_matrix.md` — multi-instance separation as a critical constraint in platform choice.
- `outputs/05_poc/docusaurus.config.ts`, `outputs/05_poc/scripts/validate_docs.py`, `outputs/04_validation/validation_report.md` Gate F — executed proof.
