# ADR-001: Adopt Mintlify as a hosted, replaceable presentation layer over a Git-canonical corpus

## Status
Proposed (2026-08-12)

## Context
The ecosystem requires GitHub as the single source of truth (Markdown + Mermaid + frontmatter), PR-reviewed derived AI content, static-first serving, and operability by one engineer. Mintlify offers true Git-as-source operation (GitHub App sync, deploys on push, web editor that commits back to Git), native Mermaid with ELK layout, PR preview deployments, CI checks, and the strongest AI-consumption surface available (llms.txt, per-page `.md`, MCP server, skill.md) — all verified from the official docs repo. However, its build/serve plane is proprietary SaaS: no self-serve static export (Enterprise-only `mint export`), no build plugins, continuous unversioned platform updates, and self-hosting only as an Enterprise engagement with a heavy infrastructure footprint.

## Decision
Adopt Mintlify as the presentation/publishing tier, under an explicit "replaceable tier" discipline:
- The GitHub repo we own is the only content store; the Mintlify GitHub App is installed on that repo only; the deploy branch is protected so all changes (human, external AI pipeline, or Mintlify's own agent) arrive as PRs.
- Content stays conservative MDX: standard Markdown + Mermaid + frontmatter wherever possible; Mintlify-specific components only through locally defined snippet wrappers.
- No structural dependency on Mintlify's built-in AI (see ADR-004); no plan to self-host (footprint contradicts the anti-overengineering rule).
- A minimal fallback SSG configuration lives in the same repo and is rehearsed once, proving the corpus renders outside Mintlify.

## Consequences
- Near-zero operations: vendor runs build, CDN, search, SEO plumbing; the engineer's effort concentrates on content and the derivation pipeline.
- Presentation-layer lock-in is accepted and bounded: exit cost = navigation rebuild + component wrapper rewrites, not content migration.
- Serving depends on vendor availability; mitigated by Git canonicity, periodic `.md`/`llms-full.txt` archival, and the fallback SSG.
- The practical review workflow (PR previews, admin API) requires the Pro plan; budget accordingly.
- Rendering behavior can change under us (continuous vendor deploys); changelog monitoring and CI smoke checks are required.

## Alternatives
- **Self-hosted SSG (Docusaurus/Astro Starlight/MkDocs):** full control and zero SaaS dependence, but the engineer inherits hosting, search, previews, and AI-surface work that Mintlify provides out of the box.
- **GitBook:** hosted competitor; weaker docs-as-code depth and different lock-in profile.
- **Mintlify Enterprise self-host:** removes vendor-serving dependence but adds MongoDB/PostgreSQL/Redis/K8s operations — disproportionate for one engineer.
