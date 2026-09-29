# ADR-003: EN/HU localization via built-in filesystem i18n, English-first

## Status
Proposed (2026-08-12)

## Context
The ecosystem requires bilingual EN/HU publishing without SaaS dependencies. Docusaurus i18n is filesystem-based (`packages/docusaurus/src/server/i18n.ts`; `getPluginI18nPath` in `packages/docusaurus-utils/src/i18nUtils.ts`): translated docs are file copies under `i18n/hu/docusaurus-plugin-content-docs/<instance>/...`, theme UI strings come from `@docusaurus/theme-translations`, and `docusaurus write-translations` extracts overridable JSON. Repo inspection shows Hungarian theme translations exist but are incomplete: `locales/hu/theme-common.json` covers 82 of 163 base keys, and some bundles have no `hu` file at all. Each locale builds as a separate site variant, roughly doubling build time.

## Decision
- `i18n: { defaultLocale: 'en', locales: ['en', 'hu'] }`; English is the canonical authoring language.
- Run `docusaurus write-translations --locale hu` once; fill the missing theme strings in-repo under `i18n/hu/` (fallback to English until filled). Optionally upstream the completed strings to `docusaurus-theme-translations`.
- Hungarian page content is produced by the AI translation pipeline as another generate-into-files flow (MDX copies under `i18n/hu/...`), PR-reviewed like all derived content; frontmatter marks translation provenance.
- CI builds both locales in one `docusaurus build` invocation (all locales) so a partial-locale deploy is impossible; post-deploy smoke test hits `/` and `/hu/`.

## Consequences
- Zero external translation SaaS (Crowdin unnecessary at two locales); fully Git-auditable translations.
- Content duplication per locale is the accepted cost; stale-translation drift must be detected by the ecosystem's source-hash comparison (store canonical file hash in translated file frontmatter).
- Build time approximately doubles; mitigated by `future.faster` caching (ADR-001).
- Locale dropdown and hreflang alternates come free from theme-classic (`SiteMetadata`, `LocaleDropdownNavbarItem`).

## Alternatives
- **Crowdin integration (officially documented):** adds SaaS coupling and workflow overhead for two locales; rejected.
- **Two separate sites per language:** breaks shared navigation/search and doubles ops; rejected.
- **hu-only UI translation without content translation:** acceptable interim state — the model supports partial translation with English fallback.
