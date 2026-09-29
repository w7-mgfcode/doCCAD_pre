# ADR-004: Mermaid via pymdownx.superfences client-side rendering, with self-hosted mermaid.js

## Status
Proposed

## Context
Canonical docs use Mermaid-as-code in fenced blocks, which GitHub renders natively in the repo view. On the published site, the de-facto MkDocs standard is `pymdownx.superfences` with a `mermaid` custom fence (`format: pymdownx.superfences.fence_code_format`), leaving the diagram source intact in HTML as `<pre class="mermaid">`, rendered client-side by Material's integration — which lazy-loads `mermaid@11` from the unpkg CDN unless a `mermaid` global already exists (`src/templates/assets/javascripts/components/content/mermaid/index.ts:72` in the mkdocs-material repo). Alternatives exist that render at build time (mkdocs-mermaid2 variants, Kroki server) producing SVG.

CDN loading conflicts with self-hosting/provider-independence goals and is a supply-chain exposure; build-time SVG adds toolchain weight (Node/puppeteer or an external Kroki service).

## Decision
1. Keep Mermaid sources as plain fenced blocks in canonical Markdown (dual rendering: GitHub + site, zero duplication).
2. Configure `pymdownx.superfences` custom fence exactly as Material documents (`docs/reference/diagrams.md`).
3. **Self-host** the Mermaid runtime: pin a `mermaid.min.js` copy in `docs/assets/javascripts/` loaded via `extra_javascript` (or use Material's `privacy` plugin to mirror external assets at build time), eliminating the unpkg dependency.
4. Do not adopt build-time SVG rendering initially; revisit only if client-side rendering causes measurable problems (print/PDF export, very large diagrams).

## Consequences
- Diagrams remain reviewable code in PRs; one source renders in repo and site.
- No third-party CDN at serve time; Mermaid version is pinned and upgraded deliberately.
- Client-side rendering means diagrams need JS (acceptable: search already does) and are invisible to naive SEO crawlers (acceptable: diagrams are not the SEO payload).

## Alternatives
- **Default CDN loading**: simplest but violates self-hosting and adds tampering/outage risk — rejected.
- **Kroki/build-time SVG**: static images without JS, but adds a service or headless-browser build dependency — rejected as overengineering for now.
