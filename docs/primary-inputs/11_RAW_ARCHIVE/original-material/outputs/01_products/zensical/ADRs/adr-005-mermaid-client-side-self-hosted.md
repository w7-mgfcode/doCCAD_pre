# ADR-005: Accept client-side Mermaid rendering, self-host the Mermaid bundle

## Status
Accepted (2026-08-12)

## Context
Mermaid-as-code is a canonical-content requirement. Zensical supports it out of the box exactly like Material for MkDocs: `pymdownx.superfences` registers a `mermaid` custom fence [VERIFIED-REPO: python/zensical/config.py default custom_fences; python/zensical/bootstrap/zensical.toml], and the theme detects `.mermaid` blocks and lazily loads `https://unpkg.com/mermaid@11/dist/mermaid.min.js`, applying light/dark theme variables [VERIFIED-REPO: zensical/ui src/assets/javascripts/components/content/mermaid/index.ts, index.css]. There is no build-time SVG rendering; diagrams require JavaScript in the reader's browser and depend on a third-party CDN by default.

## Decision
Accept client-side rendering (matches static-first: no AI, no server involved). Override the default by self-hosting a pinned mermaid@11 build via `extra_javascript`/template override so no third-party CDN is in the serving path and the renderer version is deterministic.

## Consequences
- Positive: zero build complexity; diagrams versioned as text in Git; theme-consistent styling in both palettes; works on any static host.
- Positive: removing unpkg eliminates an availability/tampering dependency and improves GDPR posture (roadmap's GDPR asset-downloading feature is not yet shipped [VERIFIED-OFFICIAL: roadmap]).
- Negative: no-JS readers and SEO crawlers see raw diagram source; diagram text is not in the search index; complex diagrams cost client CPU.
- Negative: pinning mermaid means tracking its releases ourselves; new syntax needs a manual bump.

## Alternatives
- Pre-render Mermaid to SVG in the AI/derived pipeline (mermaid-cli in CI) and commit SVGs: better SEO/no-JS, but adds a toolchain and breaks the "diagrams stay as code" reviewing ergonomics; keep as a later option for high-value pages.
- Keep default unpkg loading: acceptable functionally, rejected for provider-independence reasons.
