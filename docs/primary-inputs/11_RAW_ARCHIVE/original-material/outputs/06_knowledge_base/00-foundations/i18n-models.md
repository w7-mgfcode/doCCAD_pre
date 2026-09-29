---
id: foundation-i18n-models
title: Localization Models for Docs Platforms — Five Patterns and the EN-Canonical Strategy
type: knowledge
category: foundations
tags: [i18n, localization, bilingual, hungarian, translation, en-canonical]
sources:
  - outputs/01_products/docusaurus/SAD_docusaurus.md   # filesystem locale copies, HU 82/163
  - outputs/01_products/mkdocs/SAD_mkdocs.md           # static-i18n plugin assembly
  - outputs/01_products/gitbook/SAD_gitbook.md         # language variants
  - outputs/01_products/zensical/SAD_zensical.md       # "not yet" + dual-build workaround
  - outputs/01_products/hyperbook/SAD_hyperbook.md     # hyperlibrary multi-book, no HU locale
  - outputs/01_products/mintlify/SAD_mintlify.md       # directory-per-locale, hu supported
  - outputs/01_products/docusaurus/ADRs/adr-003-i18n-en-hu-strategy.md
confidence: HIGH
related: [foundation-ssg-anatomy, platform-docusaurus, platform-mkdocs, platform-zensical, platform-hyperbook]
---

# Localization Models for Docs Platforms — Five Patterns and the EN-Canonical Strategy

**Summary** — The six-platform field exhibits every localization architecture that exists in practice: filesystem locale copies (Docusaurus, Mintlify), plugin-assembled multilingual builds (MkDocs + static-i18n), SaaS language variants (GitBook), structural multi-book composition (Hyperbook), and simply "not yet" (Zensical). Two separate layers must be localized — content and UI chrome — and platforms routinely support one without the other. For a bilingual EN/HU site run by one engineer, the corpus converges on an EN-canonical strategy: English is the source of truth, Hungarian is a derived, drift-monitored translation.

## Core Logic

**Model 1 — Filesystem locale copies (Docusaurus; Mintlify's variant of it).** Default-locale content lives in `docs/`; translations are full file copies under `i18n/<locale>/...` (Docusaurus) or a mirrored `hu/` tree (Mintlify). UI strings come from theme translation bundles (`write-translations` extraction in Docusaurus). Each locale builds as a separate site variant, roughly doubling build time for two locales [VERIFIED-REPO Docusaurus; INFERRED on timing]. Locale dropdown and hreflang alternates are built in [VERIFIED-REPO]. Cost: content duplication per locale; benefit: no SaaS, no plugin, everything in Git. Docusaurus's known gap: upstream Hungarian theme strings are only ~50% complete (82/163 keys in `theme-common.json`), closable locally in hours via `write-translations` [VERIFIED-REPO].

**Model 2 — Plugin-assembled (MkDocs).** Core MkDocs has *no* multilingual site model — only theme-chrome locales [VERIFIED-REPO]. Bilingual capability is assembled from three parts: `mkdocs-static-i18n` (per-language builds from `page.md`/`page.hu.md` suffixes, language switcher), Material's 69-language UI packs (including `hu.html`), and lunr's bundled Hungarian stemmer (`lunr.hu.js`) [VERIFIED-REPO/-OFFICIAL]. It works and is proven, but it is a composite you configure and maintain by hand — scored 3/5, "workable with documented workarounds," not native.

**Model 3 — Language variants (GitBook).** Each section gets per-language variants with a language picker; each variant can sync from its own monorepo directory (`docs/en`, `docs/hu`) [VERIFIED-OFFICIAL]. AI auto-translation is a paid add-on (Hungarian availability [UNKNOWN]); a Git-managed HU tree sidesteps the question. Caveats: assets are not shared across section directories, and hreflang emission is undocumented [VERIFIED-OFFICIAL/UNKNOWN].

**Model 4 — Structural multi-book (Hyperbook).** `hyperlibrary.json` composes one *book per language* under one site with per-book `basePath` — used by Hyperbook's own EN/DE docs, including a `diffFolders` script that detects untranslated drift between trees [VERIFIED-REPO]. Structurally clean; but UI chrome supports only `de|en|fr|es|it|pt|nl` with just `en`/`de` string bundles shipped — **no Hungarian**: HU readers get English chrome unless a small `hu.json` locale is contributed upstream or patched post-build [VERIFIED-REPO].

**Model 5 — "Not yet" (Zensical).** Theme UI translations are strong (69 languages *including* Hungarian) but multi-language *content* is unsupported: mkdocs-static-i18n is explicitly incompatible and native i18n is an unchecked roadmap item [VERIFIED-OFFICIAL]. The workaround is the classic dual build: two configs building into `/en/` and `/hu/` subpaths, wired together with the theme's `extra.alternate` switcher [VERIFIED-REPO for the switcher; INFERRED workflow]. Scored 2/5 — the lowest localization score in the field.

**The EN-canonical strategy.** Every ADR-003 in the corpus (one per platform) lands on the same logic: with one engineer and an AI translation pipeline, symmetric bilingual maintenance is unaffordable and drift is inevitable. Therefore: (1) English content is canonical — the only tree humans must keep correct; (2) Hungarian is a *derived artifact*, produced by the AI layer as another generate-into-files pipeline, reviewed via PR like any generated content; (3) CI enforces parity mechanically (file-tree diffs, per-file source hashes, missing-counterpart checks — Hyperbook's `diffFolders`, MkDocs hook-based parity checks, Mintlify tree-diff recommendation); (4) UI-chrome gaps are closed once, locally (Docusaurus HU strings) or upstream (Hyperbook `hu.json`). This turns i18n from a second authoring burden into one more instance of the derived-content machinery the ecosystem already has.

## Best Practices

1. **Localize both layers deliberately** — content *and* UI chrome are separate systems; verify each (Hyperbook passes structurally, fails chrome; Zensical the reverse).
2. **Declare one canonical locale and make every other locale generated** — it converts translation into the ecosystem's existing derive→PR→validate loop.
3. **Wire drift detection into CI from day one** (tree parity + source hashes) — silent EN/HU divergence is the highest-likelihood bilingual risk on every platform's risk table.
4. **Never expose a language switcher before parity checks pass** — a switcher to missing pages is worse than no switcher (Mintlify recommendation #6).
5. **Verify hreflang/SEO emission per platform** — built-in for Docusaurus, plugin-provided for MkDocs, undocumented for GitBook [UNKNOWN]; missing hreflang silently splits search ranking across locales.

## Pitfalls

- **"Supports 69 languages" claims describe chrome, not content** (Zensical, Material) — the exact inversion of what a bilingual site needs.
- **Hungarian is a minority-language stress test**: partially translated upstream bundles (Docusaurus 82/163), absent locale unions (Hyperbook), unknown auto-translation coverage (GitBook). Minor locales expose gaps that `fr`/`de` never would — test *your* locale, not *a* locale.
- **Per-locale build multiplication**: filesystem models roughly double build time and CI minutes per added locale [INFERRED, corpus-consistent]; fine at two locales, a scaling term beyond.
- **Asset duplication** in directory-per-locale models (GitBook verified limitation; Mintlify nav must be duplicated per language, mitigated by `$ref` splitting).

## Expert Notes

- Localization was weighted only 8%, yet it produced the field's widest score spread (2–4) — it is one of the least-commoditized capabilities in the docs-platform space, unlike Mermaid (all 4–5). When shortlisting platforms, i18n discriminates; Mermaid does not.
- The dual-build workaround (Zensical) is older than most i18n plugins and still perfectly serviceable at two locales — the analysts treated missing native i18n as a *cost*, not a veto, precisely because the workaround is low-tech and exit-friendly.
- Treating translations as derived AI content has a governance dividend: provenance frontmatter (`source_ref`, source hash) makes "which EN revision is this HU page translated from?" a queryable fact rather than tribal knowledge.

## Evidence & Further Reading

- Per-platform Localization sections: `outputs/01_products/*/SAD_*.md` (§Localization)
- EN/HU strategy ADRs: `outputs/01_products/docusaurus/ADRs/adr-003-i18n-en-hu-strategy.md`, `outputs/01_products/mkdocs/ADRs/adr-003-bilingual-en-hu-static-i18n-suffix.md`, `outputs/01_products/zensical/ADRs/adr-003-bilingual-dual-build.md`, `outputs/01_products/hyperbook/ADRs/adr-003-bilingual-en-hu-via-hyperlibrary.md`, `outputs/01_products/gitbook/ADRs/adr-003-bilingual-monorepo-layout.md`, `outputs/01_products/mintlify/ADRs/adr-003-bilingual-en-hu-strategy.md`
- Related: [ssg anatomy](static-site-generator-anatomy.md), [search-models](search-models.md) (Hungarian stemming), platform profiles under `../10-platforms/`
