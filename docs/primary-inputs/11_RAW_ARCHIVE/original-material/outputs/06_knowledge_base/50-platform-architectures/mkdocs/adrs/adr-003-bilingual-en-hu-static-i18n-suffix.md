# ADR-003: Bilingual EN/HU via mkdocs-static-i18n suffix strategy with CI parity checks

## Status
Proposed

## Context
MkDocs core has no multilingual site model — `mkdocs/localization.py` only localizes theme chrome. The proven ecosystem answer is `mkdocs-static-i18n` (v1.3.1, 2026-02-20, actively maintained), which builds one site per locale from suffixed files (`page.md` / `page.hu.md`) or per-locale folders, integrates with Material's language switcher, and works with Material's 69 UI translations including `partials/languages/hu.html`. Core search bundles `lunr.hu.js` for Hungarian stemming; Material's search plugin accepts `lang: [en, hu]`.

English is the primary/complete locale; Hungarian coverage will be partial initially and may lag.

## Decision
1. Use `mkdocs-static-i18n` with the **suffix** strategy: `index.md` (EN, default) and `index.hu.md` (HU) side by side — translations stay adjacent to their source in diffs and PRs.
2. Configure fallback to English for untranslated pages (plugin default behavior), so the HU site is never broken, only partially English.
3. Material `theme.language` per locale plus search `lang: [en, hu]` for correct UI strings and stemming.
4. A CI hook reports EN/HU parity (pages missing `.hu.md`, and `.hu.md` files whose EN source changed after their last update, via frontmatter `translated_from_hash`); warnings, not build failures, to avoid blocking canonical work.
5. AI-assisted translation drafts follow ADR-002: generated `.hu.md` files arrive as PRs with provenance frontmatter.

## Consequences
- Fully static bilingual output with language switcher and Hungarian search stemming; no external translation service required.
- Doubled build output and some config duplication (nav titles per locale).
- Dependency on a third-party plugin (small, vendorable Python; fork feasible if abandoned).

## Alternatives
- **Two separate MkDocs projects (en/, hu/)**: no plugin dependency but duplicated config, no switcher integration, worse cross-linking — rejected.
- **Material Insiders-style multi-language via projects plugin**: more moving parts, Material is frozen — rejected.
- **Single mixed-language site**: poor UX and SEO (no hreflang pairs) — rejected.
