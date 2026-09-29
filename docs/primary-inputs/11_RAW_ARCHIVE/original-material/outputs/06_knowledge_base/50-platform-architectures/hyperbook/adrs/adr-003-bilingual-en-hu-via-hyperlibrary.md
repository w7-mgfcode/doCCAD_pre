# ADR-003: EN/HU bilingual structure via hyperlibrary, with an upstream Hungarian locale plan

## Status
Proposed (2026-08-12)

## Context
Hyperbook has no per-page translation framework; its bilingual model is one book per language composed by `hyperlibrary.json` with per-book `basePath` (verified: website/hyperlibrary.json — the project's own EN/DE docs). UI-chrome language support is limited to a typed union `de|en|fr|es|it|pt|nl` with only `en.json` and `de.json` string bundles shipped (packages/types/src/index.ts:44; packages/markdown/src/i18n.ts). Hungarian is not a supported UI locale; unsupported languages fall back to English strings, and the lunr search index falls back to English tokenization.

## Decision
Adopt a two-book layout from day one: `en/` (basePath `/`) and `hu/` (basePath `hu`), composed by a root `hyperlibrary.json` mirroring the upstream docs' pattern. Mirror directory structure between the trees and run a translation-drift check in CI (pattern: scripts/diffFolders.mjs from the upstream repo). In parallel: (a) submit an upstream PR adding `hu` to the `Language` union plus a `hu.json` locale (the i18n mechanism is a flat key-value JSON — small change); (b) until merged, run a post-build string-patch step that replaces known English chrome strings in the HU book's HTML output.

## Consequences
- Clean URLs (`/` and `/hu/`), independent navigation and search per language, no framework magic — consistent with anti-overengineering.
- Translation completeness is a process concern (CI drift check), not a platform guarantee; partially translated states are visible as missing pages, not mixed-language pages.
- The post-build patch is brittle across Hyperbook upgrades (string changes) — it is explicitly temporary, with the upstream PR as the real fix; success depends on the single maintainer's responsiveness.
- HU search quality is slightly degraded (English stemmer fallback); acceptable at target corpus size since lunr still substring/token matches Hungarian text.

## Alternatives
- Single mixed-language book with per-page `lang` frontmatter: rejected — no language switcher semantics, polluted navigation and search.
- Fork to add `hu` immediately: rejected — ADR-001/ADR-004 reserve forking as a last resort.
- Separate repos per language: rejected — breaks the single-source ecosystem and doubles CI.
