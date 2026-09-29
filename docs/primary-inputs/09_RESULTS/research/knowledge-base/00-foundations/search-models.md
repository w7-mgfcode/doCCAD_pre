---
id: foundation-search-models
title: Search Models for Docs Sites — Local Build-Time Index vs. SaaS vs. Black Box
type: knowledge
category: foundations
tags: [search, lunr, algolia, flexsearch, disco, build-time-index, saas, offline]
sources:
  - outputs/01_products/mkdocs/SAD_mkdocs.md           # lunr contrib search, lunr.hu.js
  - outputs/01_products/docusaurus/SAD_docusaurus.md   # Algolia first-party vs community local
  - outputs/01_products/zensical/SAD_zensical.md       # Disco engine, Rust index
  - outputs/01_products/hyperbook/SAD_hyperbook.md     # lunr, payload growth
  - outputs/01_products/mintlify/SAD_mintlify.md       # undisclosed engine, boost controls
  - outputs/01_products/gitbook/SAD_gitbook.md         # Quick Find + AI search
  - outputs/01_products/docusaurus/ADRs/adr-004-local-search-first-algolia-optional.md
confidence: HIGH
related: [foundation-ssg-anatomy, foundation-i18n-models, platform-docusaurus, platform-mkdocs, platform-zensical]
---

# Search Models for Docs Sites — Local Build-Time Index vs. SaaS vs. Black Box

**Summary** — Documentation search comes in three architectures: a build-time local index executed client-side (lunr, flexsearch, Zensical's Disco), an external SaaS index queried at runtime (Algolia DocSearch), and vendor-undisclosed engines inside hosted platforms (Mintlify, GitBook). For a small team on a static-first, provider-independent stack, the corpus's decision logic is unambiguous: start with a local build-time index, keep SaaS as an opt-in upgrade — search is the one subsystem where a "worse" engine wins on architecture.

## Core Logic

**Model A — Build-time local index, client-side execution.** At build, the generator extracts per-section text into a JSON index shipped as a static asset; the browser loads it (usually in a web worker) and queries locally. Verified implementations: MkDocs core bundles lunr.js with language stemmers **including Hungarian** (`lunr.hu.js`) and a worker-based client [VERIFIED-REPO]; Material re-skins the same static-index model; Hyperbook builds a lunr index with position metadata for highlighting [VERIFIED-REPO]; Zensical builds its index *in Rust* and queries it with **Disco**, the team's new engine — which currently ships as a minified, source-pending blob [VERIFIED-REPO]; GitBook's OSS renderer even keeps a client-side flexsearch path [VERIFIED-REPO]. Properties: zero infrastructure, zero cost, works offline and on any static host, no external dependency in the read path, index regenerates automatically on every build. Limits: relevance is lunr-grade rather than Algolia-grade; the index payload grows linearly with the corpus and is downloaded by every searching visitor — fine at hundreds of pages, a budget item beyond ~1–2k [INFERRED, consistent across SADs].

**Model B — SaaS index (Algolia DocSearch).** Docusaurus's only first-party search is `theme-search-algolia`: a crawler indexes the published site on a schedule and browsers query Algolia's API [VERIFIED-REPO]. Free for eligible open-source docs [VERIFIED-OFFICIAL, program terms MEDIUM confidence]. Properties: best-in-class relevance and UX, optional "Ask AI" layer. Costs: an external runtime dependency in the read path, crawler-based index lag behind deploys, API keys to manage, and SaaS coupling in an otherwise self-contained system.

**Model C — Vendor-undisclosed.** Mintlify's search engine is documented nowhere — no Algolia/Typesense reference exists in the official docs [UNKNOWN]; the operator's controls are frontmatter `boost` multipliers, `searchable: false`, and analytics APIs [VERIFIED-OFFICIAL]. GitBook ships built-in Quick Find keyword search plus AI Search with citations (Premium+), non-configurable, no bring-your-own-index [VERIFIED-OFFICIAL/UNKNOWN]. Properties: zero effort, decent quality; but quality is untunable beyond the exposed knobs and unswappable — risk #7 in the Mintlify table: "a black box you cannot tune… accept residual opacity."

**Decision logic for small teams** (from Docusaurus ADR-004 and the recommendation sections):

1. If provider independence / self-hosting / offline capability is a requirement → **Model A**, full stop. It is the only model with no external service in the read path, satisfying "AI (and any vendor) must not be required to serve docs" by construction.
2. If corpus is small-to-medium (≤ low thousands of pages) → Model A's relevance is adequate and its payload acceptable; the Algolia upgrade is a *later* option that requires no content changes (crawler-based, decoupled from build).
3. Adopt Model B only when relevance complaints are real and measured, and the SaaS coupling is consciously accepted; use scoped keys (search-only key client-side, crawler key server-side) — CI-secret-leakage is a named threat in the Docusaurus threat model.
4. Model C is not a choice but a consequence of choosing a hosted platform; if adopted, actively use the exposed controls (`boost`, `searchable`, analytics) and accept the ceiling.
5. On keyword-vs-AI search: baseline keyword search must work without AI (GitBook's Quick Find does, satisfying static-first even there [VERIFIED-OFFICIAL]); AI search layers are additive UX, never load-bearing.

## Best Practices

1. **Default to local search; document Algolia as the upgrade path** — the reverse migration (SaaS → local) means adopting a community plugin under time pressure; the forward one is config-only (Docusaurus recommendation #6).
2. **Match the stemmer to the locale**: enable `lang: [en, hu]` where supported — MkDocs bundles `lunr.hu.js` [VERIFIED-REPO]; Hyperbook's bundled set is [UNKNOWN] for HU (English tokenization substring-matches HU "tolerably"). Un-stemmed minority-language search silently underperforms.
3. **Budget the index**: track the search asset's size in CI and predefine an escape hatch — Hyperbook's plan names Pagefind (runs over static HTML, zero platform coupling) as the swap-in when lunr's payload exceeds budget.
4. **Pin community search plugins by exact name and version** — Docusaurus's local search lives in community packages, and typosquatting of exactly such plugins is threat #6 in its threat model.
5. **On hosted platforms, encode ranking intent in frontmatter** (`boost`, `searchable: false` for derived pages) so derived/AI content doesn't outrank canonical pages [VERIFIED-OFFICIAL: Mintlify].

## Pitfalls

- **Assuming first-party = local.** Docusaurus's first-party search is Algolia SaaS; local search is community-plugin territory [VERIFIED-REPO by absence] — the opposite of what most adopters expect.
- **Index lag on crawler-based SaaS**: search results trail deploys; fresh pages are findable by URL but not by query until the next crawl.
- **Unauditable client code**: Zensical's Disco ships minified without published source, executing in every reader's browser — mitigated by same-origin serving, flagged until the promised OSS release lands [VERIFIED-REPO].
- **Shipping the index to users who never search**: lazy-load the index on first search focus (MkDocs does [VERIFIED-REPO]); eager loading taxes every page view.
- **Diagrams and client-rendered content are invisible to build-time indexes** — see [mermaid-diagrams-as-code](mermaid-diagrams-as-code.md).

## Expert Notes

- Search is where "best tool" and "right architecture" diverge most cleanly: Algolia is objectively the better engine, and the corpus still recommends against starting with it — because the evaluation optimizes for *system properties* (independence, determinism, zero ops) over *component quality*. This is the single most transferable decision pattern in the whole comparison.
- The search criterion carried only 5% weight and the field scored 3–4 across the board — search quality is commoditized at small scale; search *architecture* is what differentiates.
- Post-build indexers (Pagefind) are a fourth micro-model worth knowing: they index the emitted HTML, so they are platform-agnostic by construction — the ideal escape hatch and a useful migration constant across SSG changes.

## Evidence & Further Reading

- Decision record: `outputs/01_products/docusaurus/ADRs/adr-004-local-search-first-algolia-optional.md`
- Implementations: `outputs/01_products/mkdocs/SAD_mkdocs.md` (§Search, search sequence diagram), `outputs/01_products/zensical/SAD_zensical.md` (§Search — Disco), `outputs/01_products/hyperbook/SAD_hyperbook.md` (§Search)
- SaaS/black-box models: `outputs/01_products/docusaurus/SAD_docusaurus.md` (§Search), `outputs/01_products/mintlify/SAD_mintlify.md` (§Search), `outputs/01_products/gitbook/SAD_gitbook.md` (§Search)
- Related: [ssg anatomy](static-site-generator-anatomy.md), [i18n-models](i18n-models.md)
