# ADR-003: Bilingual EN/HU via dual-build until native i18n ships

## Status
Accepted (2026-08-12) — revisit when Zensical native i18n leaves the roadmap

## Context
The ecosystem must publish English and Hungarian views. Zensical's theme UI is translated into 69 languages including Hungarian [VERIFIED-REPO: zensical/ui src/partials/languages/hu.html], and `theme.language` is configurable [VERIFIED-REPO: python/zensical/config.py]. However, the mkdocs-static-i18n plugin is explicitly not yet supported (Tier-2 backlog) [VERIFIED-OFFICIAL: zensical.org/compatibility/plugins/], and native internationalization ("flexible content organization", "AI-powered translation workflows") is planned but unshipped [VERIFIED-OFFICIAL: zensical.org/about/roadmap/].

## Decision
Publish one site with two language trees built in two passes: `mkdocs.en.yml` (docs_dir=docs/en, site_url=.../en/, theme.language=en) and `mkdocs.hu.yml` (docs_dir=docs/hu, site_url=.../hu/, theme.language=hu), merged into one `site/` artifact by CI. Cross-language switching uses the theme's `extra.alternate` configuration (the alternate/language switcher exists in the UI [VERIFIED-REPO: zensical/ui src/assets/javascripts/integrations/alternate]). Hungarian content is a curated subset; untranslated pages link to the English canonical rather than being machine-stubbed.

## Consequences
- Positive: zero dependence on unsupported plugins; each build is a plain supported Zensical invocation; per-language search indexes come free (index is per-build, language-aware tokenization [VERIFIED-REPO: crates/zensical/src/structure/search.rs]).
- Negative: two builds double CI time (small at personal-site scale); no per-page fallback rendering — parity tracking is manual/AI-assisted; nav is maintained twice.
- Negative: hreflang/meta cross-links must be added via template override or extra config; verify output before relying on it for SEO [INFERRED].
- Migration: when native i18n ships, collapse to a single config; content layout `docs/en|docs/hu` was chosen to match the folder-per-language structure most i18n systems expect.

## Alternatives
- Single mixed-language site: poor reader UX, poor SEO signals.
- Stay on Material for MkDocs + mkdocs-static-i18n: works today but forfeits Zensical adoption; kept as documented fallback.
- Machine-translate everything to force parity: violates validation/review principles for derived content.
