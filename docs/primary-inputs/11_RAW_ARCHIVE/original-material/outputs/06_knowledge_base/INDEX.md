---
id: kb-index
title: Knowledge Base Index — Documentation Platform & AI Docs Architecture Wiki
type: knowledge
category: index
tags: [index, map-of-content]
sources: [outputs/01_products/, outputs/02_comparison/, outputs/03_solution/, outputs/05_poc/]
confidence: HIGH
---

# Knowledge Base — GitHub-Native AI Documentation Ecosystem

A structured, cross-linked distillation of the full research and design corpus (six platform deep dives,
weighted comparison, target architecture, executed PoC). 31 pages + glossary. Every page carries frontmatter
(`id`, `tags`, `sources`, `confidence`, `related`) so both humans and LLMs can navigate, ingest and cite it.
Machine entry point: `llms.txt`. Evidence tags (`[VERIFIED-REPO]` etc.) are preserved from the source corpus.

## How to use this wiki

Start with **foundations** if you're new to docs-as-code; go straight to **platforms** for tool selection;
**patterns** and **best-practices** are the reusable engineering knowledge (independent of any platform
choice); **decision-frameworks** teach the methods used to decide, so you can rerun them on your own case.

## 00 — Foundations (basics)

| Page | What it teaches |
|---|---|
| [docs-as-code](00-foundations/docs-as-code.md) | The paradigm: Git as source of truth, PR as editorial gate, CI as quality gate — vs CMS/SaaS models |
| [static-site-generator-anatomy](00-foundations/static-site-generator-anatomy.md) | The 10-layer SSG model and how all six platforms map onto it |
| [markdown-mdx-frontmatter](00-foundations/markdown-mdx-frontmatter.md) | Markdown flavors, MDX-as-executable-content, frontmatter as metadata/provenance carrier |
| [mermaid-diagrams-as-code](00-foundations/mermaid-diagrams-as-code.md) | Diagrams-as-code rationale, rendering trade-offs, CI validation, syntax pitfalls |
| [i18n-models](00-foundations/i18n-models.md) | The localization models in the field + EN-canonical bilingual strategy |
| [search-models](00-foundations/search-models.md) | Build-time local index vs SaaS search vs vendor black box |

## 10 — Platforms (deep-dive distillations)

| Page | Verdict in one line | Score |
|---|---|---|
| [docusaurus](10-platforms/docusaurus.md) | Winner — structural canonical/generated separation, components, active core | 88.6 |
| [mintlify](10-platforms/mintlify.md) | Best AI surface, but vendor-locked build/serve plane | 85.0 |
| [mkdocs](10-platforms/mkdocs.md) | Simplest architecture; Material support cliff 2026-11-05 | 83.8 |
| [zensical](10-platforms/zensical.md) | Promising Rust+Python successor; pre-1.0, no plugin API yet | 76.4 |
| [hyperbook](10-platforms/hyperbook.md) | Education niche; bus factor 1; clever data+template mechanism | 76.0 |
| [gitbook](10-platforms/gitbook.md) | Polished SaaS; Git is a mirror, not the engine | 72.2 |
| [comparison-logic](10-platforms/comparison-logic.md) | How the decision was actually made — criteria, anchors, constraint vetoes | — |

## 20 — Architecture Patterns (reusable design logic)

[canonical-vs-generated-separation](20-patterns/canonical-vs-generated-separation.md) ·
[ai-in-ci-not-in-serving](20-patterns/ai-in-ci-not-in-serving.md) ·
[thin-provider-abstraction](20-patterns/thin-provider-abstraction.md) ·
[task-contracts](20-patterns/task-contracts.md) ·
[pr-gated-generation](20-patterns/pr-gated-generation.md) ·
[hash-based-drift-detection](20-patterns/hash-based-drift-detection.md) ·
[leveled-retrieval](20-patterns/leveled-retrieval.md) ·
[metadata-provenance-contract](20-patterns/metadata-provenance-contract.md)

Each pattern page: problem → structure → mechanics → the simpler alternative it beat → when NOT to use it.
Patterns proven by execution in the PoC are marked "VERIFIED BY EXECUTION in 05_poc".

## 30 — Best Practices (operational knowledge)

[ci-quality-gates](30-best-practices/ci-quality-gates.md) ·
[prompt-injection-defenses](30-best-practices/prompt-injection-defenses.md) ·
[github-actions-security](30-best-practices/github-actions-security.md) ·
[evidence-discipline](30-best-practices/evidence-discipline.md) ·
[bilingual-docs-en-hu](30-best-practices/bilingual-docs-en-hu.md)

## 40 — Decision Frameworks (expert methods)

[weighted-decision-model](40-decision-frameworks/weighted-decision-model.md) ·
[anti-overengineering-rules](40-decision-frameworks/anti-overengineering-rules.md) ·
[build-vs-buy-vs-host](40-decision-frameworks/build-vs-buy-vs-host.md) ·
[maintenance-risk-assessment](40-decision-frameworks/maintenance-risk-assessment.md)

## 50 — Platform Architecture Documentation (full research deliverables)

The complete, repository-grounded architecture documentation for each platform — the unabridged Solution
Architecture Documents (C4 L1–L3, sequences, deployment, security + threat model, operations, extensibility,
localization, AI suitability, risks, migration plan, verdict, Hungarian executive summary) plus per-platform
ADRs, runbooks, roadmaps and evidence logs. The `10-platforms` pages are the distilled profiles; these are
the full source documents.

| Platform | Docs |
|---|---|
| Mintlify | [index](50-platform-architectures/mintlify/README.md) · [full SAD](50-platform-architectures/mintlify/architecture.md) |
| GitBook | [index](50-platform-architectures/gitbook/README.md) · [full SAD](50-platform-architectures/gitbook/architecture.md) |
| Docusaurus | [index](50-platform-architectures/docusaurus/README.md) · [full SAD](50-platform-architectures/docusaurus/architecture.md) |
| MkDocs | [index](50-platform-architectures/mkdocs/README.md) · [full SAD](50-platform-architectures/mkdocs/architecture.md) |
| Zensical | [index](50-platform-architectures/zensical/README.md) · [full SAD](50-platform-architectures/zensical/architecture.md) |
| Hyperbook | [index](50-platform-architectures/hyperbook/README.md) · [full SAD](50-platform-architectures/hyperbook/architecture.md) |

## 90 — [Glossary](90-glossary.md)

~50 terms used across the corpus, each with a pointer to the page that treats it.

## Provenance

Distilled 2026-08-12 from the session corpus: `01_products/` (six repository-grounded SADs),
`02_comparison/` (weighted decision), `03_solution/` (target architecture + security + ADRs),
`05_poc/` (executed proof of concept), `04_validation/` (Gates A–F). No new research was performed for the
distillation; confidence levels are inherited from the underlying evidence.
