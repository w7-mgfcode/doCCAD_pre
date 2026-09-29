# ADR-004: Local static search by default; Algolia DocSearch as optional upgrade

## Status
Proposed (2026-08-12)

## Context
The ecosystem is static-first and provider-independent: published docs must not depend on external runtime services. Docusaurus's first-party search is `@docusaurus/theme-search-algolia` (SearchBar/SearchPage in `packages/docusaurus-theme-search-algolia/src/theme`), a SaaS-backed crawler model with DocSearch v3/v4 support (including an optional "Ask AI" mode, seen in `website/docusaurus.config.ts` ~line 676-680). No first-party offline/local search package exists in the monorepo; the official docs point to community plugins (e.g. `@easyops-cn/docusaurus-search-local`) that build a static index at build time and serve it as a static asset.

## Decision
Adopt a community local-search plugin (pinned exact version, vetted package name) as the default search. Configure it to index both locales and both docs instances. Treat Algolia DocSearch as a documented, reversible upgrade path if corpus size or search quality demands it later.

## Consequences
- Search works fully offline/self-hosted; no API keys, no third-party runtime dependency, no index lag after deploys (index rebuilt with the site).
- Search quality and typo-tolerance are below Algolia's; acceptable at medium corpus scale.
- A community plugin adds a supply-chain and maintenance-risk surface not covered by Meta's release train — pin versions and watch its compatibility with Docusaurus minors (notably Rspack-path compatibility from ADR-001).
- If Algolia is adopted later: search-only API key ships client-side; crawler config and index become external state to operate.

## Alternatives
- **Algolia DocSearch from day one:** best UX, free program for eligible docs, but reintroduces SaaS coupling and crawl-lag; contradicts provider-independence default; kept as upgrade.
- **No search at MVP:** viable for a small corpus with good IA; rejected because interview-prep use implies lookup behavior.
- **Self-hosted search service (Typesense/Meilisearch):** adds a running server — violates static-first and one-engineer constraints; rejected.
