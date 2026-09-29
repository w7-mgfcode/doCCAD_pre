---
id: practice-bilingual-docs-en-hu
title: Bilingual Documentation (EN/HU) — Canonical Language plus Fallback
type: knowledge
category: best-practices
tags: [i18n, localization, hungarian, translation, docusaurus-i18n]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-12)
  - outputs/03_solution/content_architecture.md (§8)
  - outputs/01_products/docusaurus/ADRs/adr-003-i18n-en-hu-strategy.md
  - outputs/05_poc/VALIDATION_NOTES.md (§b, §h)
  - outputs/02_comparison/comparison.md (localization row)
confidence: HIGH
related: [pattern-canonical-generated-separation, pattern-hash-drift-detection, pattern-pr-gated-generation, framework-build-vs-buy-vs-host]
---

# Bilingual Documentation (EN/HU) — Canonical Language plus Fallback

**Summary** — Bilingual capability without bilingual fork drift: English is the single canonical authoring language; Hungarian lives as filesystem-mirrored copies under `i18n/hu/**` with automatic English fallback for every untranslated page. Translation is prioritized by audience value, generated content translates only after approval and on explicit trigger, and both locales build in one invocation so a partial-locale deploy is impossible.

## Core Logic

**EN-canonical + HU-fallback (AD-12).** The failure mode this prevents is fork drift — two language trees evolving independently until neither is authoritative. The rule set:

- EN is the authoring and canonical language; all governance (schemas, hashes, review) operates on EN content.
- HU lives in `i18n/hu/docusaurus-plugin-content-docs*/` mirroring file paths and ids exactly — Docusaurus's filesystem i18n means a translation is just a file copy in a parallel tree, PR-reviewed like everything else, with zero translation SaaS (Crowdin explicitly rejected at two locales).
- Untranslated pages fall back to EN automatically: the HU site is always *complete*, just partially translated. VERIFIED BY EXECUTION in 05_poc: the full build produced `build/` and `build/hu/` with the `hu` locale served entirely via English fallback, and `/hu/docs/overview/` returned HTTP 200 serving English content.
- Theme UI strings: Hungarian coverage upstream is ~50% (82 of 163 base keys in one bundle, some bundles missing [VERIFIED-REPO]); the gap is closed locally via `docusaurus write-translations`, tracked as a normal repo file (optionally upstreamed).

**Translation priority ordering.** Translate by reader value, not tree order: `00-overview`, `01-getting-started`, `02-user-manual` first; deep technical canon (architecture internals, ADRs) may *deliberately stay EN-only* — a recorded decision, not neglect. This concentrates translation effort where non-English readers actually land.

**Generated-content translation policy.** Generated pages are EN by default. HU variants are produced only on explicit trigger (contract `translate: hu`) and **only after the EN version is approved — never translate unapproved drafts**. This keeps the human gate singular: review happens once, on the canonical-language artifact; translation multiplies content, not governance. Bot-written HU content lands under the i18n mirror of `generated/**`, inside the same CI path gate.

**Build and deploy discipline.** CI builds both locales in one `docusaurus build` invocation (making a partial-locale deploy impossible) and the post-deploy smoke test hits `/` and `/hu/`. Build time roughly doubles with the second locale; mitigated by `future.faster` caching.

## Best Practices

1. **Pick one canonical language and hang all governance off it**, because hashes, schemas, and review gates must have a single source of truth per page — translations are derived artifacts.
2. **Use filesystem-mirrored i18n with automatic fallback**, because "always complete, partially translated" beats "translated but stale or missing" for every reader.
3. **Order translation by audience entry points**, because translation capacity is the scarcest resource in a solo-operated bilingual site.
4. **Never translate unapproved generated drafts**, because translating an artifact that may be rejected doubles waste and risks divergent review outcomes.
5. **Detect stale translations with the same hash mechanism as generated content** — store the canonical file's hash in the translated file's frontmatter — because translation drift is just another source→derivative dependency.
6. **Build all locales atomically**, because per-locale deploys eventually skew and skew is invisible until a reader hits it.

## Pitfalls

- Localization capability varied sharply across the platform field (Docusaurus/Mintlify/GitBook 4; MkDocs 3 via assembled plugins; Zensical 2 — *no multi-language content support yet*); treating i18n as a commodity feature would have been a selection error.
- Content duplication per locale is the accepted cost of filesystem i18n; the alternatives (two sites, or a translation SaaS) were rejected for broken shared navigation/search and SaaS coupling respectively.
- Theme-string gaps produce a jarring half-translated chrome even when content is translated — close the UI-string gap early; it is cheap and one-off.
- Custom frontmatter `id`/`slug` values must stay identical across locale copies, or the mirrored-path model silently breaks routing.

## Expert Notes

The elegant move is recognizing that translations are structurally the same problem as generated content: derived artifacts with a canonical source, needing provenance, staleness detection, and PR review — so the existing machinery (hash drift, path gates, PR flow) covers them with near-zero new architecture. AI translation fits the same mold: it is "another generate-into-files flow," PR-reviewed, provenance-marked — deferred until translation quality gates exist (a named Deferred item in the spine, not scope creep).

## Evidence & Further Reading

- `outputs/03_solution/content_architecture.md` §8 — the full translation strategy including priority order and the approved-first rule.
- `outputs/01_products/docusaurus/ADRs/adr-003-i18n-en-hu-strategy.md` — mechanism detail, theme-string coverage evidence, rejected alternatives.
- `outputs/05_poc/VALIDATION_NOTES.md` §b, §h — executed dual-locale build and `/hu/` fallback serving.
- `outputs/02_comparison/comparison.md` — localization scores across all six platforms.
