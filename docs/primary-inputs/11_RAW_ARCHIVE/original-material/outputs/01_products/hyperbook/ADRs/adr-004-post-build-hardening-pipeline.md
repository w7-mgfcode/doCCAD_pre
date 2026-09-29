# ADR-004: Post-build hardening pipeline over static output (SEO, security, guards)

## Status
Proposed (2026-08-12)

## Context
Verified gaps in Hyperbook's emitted output: no sitemap.xml, no robots.txt, no canonical links, no og:image; `og:title` uses an invalid `value` attribute instead of `content`; `keywords` are joined without separators; `<html lang>` falls back to `"es"` (packages/markdown/src/rehypeHtmlStructure.ts:200-280). There are also no CSP headers/meta and no build-failure signal when a template is missing (warnings only). The published site is recruiter-facing, so discoverability and link previews matter.

## Decision
Introduce a single post-build Node script (`scripts/harden.mjs`, target <150 lines) that runs in CI between `hyperbook build` and deploy, operating only on the static output directory. It: (1) generates `sitemap.xml` and `robots.txt` from the emitted HTML files; (2) rewrites head metadata — fixes `og:title`, adds `og:image`, canonical URLs, correct `keywords`, correct `lang` per book; (3) injects a CSP meta tag appropriate to the directives actually used; (4) fails the build if page count deviates from the committed manifest or if the Hyperbook build log contained template/directive warnings. Fixes with upstream value (og:title bug, sitemap) are also submitted as upstream PRs so the script can shrink over time.

## Consequences
- SEO and link-preview quality reach professional baseline without forking the generator.
- The script is coupled to Hyperbook's HTML structure and must be re-verified at each pinned-version upgrade (covered by the ADR-001 smoke-test workflow).
- CI gains hard failure modes for silent degradation (missing pages, template errors) that the platform itself does not provide.
- Keeps the "AI not required to serve" and static-first invariants: the pipeline is deterministic Node with no external services.

## Alternatives
- Fork Hyperbook and fix rehypeHtmlStructure directly: rejected while upstream is responsive; higher permanent cost (ADR-001).
- Accept SEO defects: rejected — recruiter discoverability is a primary business goal.
- Full custom head via `allowDangerousHtml` page HTML: rejected — per-page manual work, error-prone.
