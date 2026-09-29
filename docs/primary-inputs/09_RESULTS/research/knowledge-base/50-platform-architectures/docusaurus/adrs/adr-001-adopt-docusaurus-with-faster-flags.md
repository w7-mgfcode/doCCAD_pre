# ADR-001: Adopt Docusaurus 3.10.x with `future.v4` and `future.faster` enabled

## Status
Proposed (2026-08-12)

## Context
The ecosystem needs a static-first publishing foundation for canonical Markdown and AI-generated MDX views, operable by one engineer, with Mermaid, EN/HU i18n, and custom React components. Docusaurus 3.10.x (npm latest 3.10.2, 2026-07-10) is actively maintained by Meta OSS. Build performance historically relied on webpack 5; since the `@docusaurus/faster` package, Rspack, SWC, Lightning CSS, persistent caching, and SSG worker threads are available behind `future.faster` flags (`packages/docusaurus-types/src/config.d.ts`), and v4 behavior is previewable via `future.v4` (`fasterByDefault`, `useCssCascadeLayers`, `mdx1CompatDisabledByDefault`). The upstream website dogfoods `rspackBundler: true` and `rspackPersistentCache: true` (`website/docusaurus.config.ts`).

## Decision
Adopt Docusaurus at the current 3.10.x minor. Enable `future: { v4: true, faster: true }` from the first commit. Add `@docusaurus/faster` as a dependency. Pin Node 24.x (engines require >=24.14) in `.nvmrc` and CI. Upgrade only on minor releases after reading the changelog's breaking-change labels.

## Consequences
- Best available build times (persistent cache benefits warm CI builds) and early detection of v4 incompatibilities while they are opt-in.
- Slightly higher exposure to newer subsystems (Rspack path is less battle-tested than webpack); fallback is flipping flags off without content changes.
- `mdx1CompatDisabledByDefault` means MDX v1 leniencies are off — generated and authored content must be MDX-v3-clean from day one (aligned with ADR-005 validation gate).
- Node 24 requirement constrains CI images and any shared tooling.

## Alternatives
- **Stay on webpack defaults:** safer but slower builds; still inherits the v4 migration debt later.
- **Docusaurus v2:** EOL-track, React 18-era; rejected.
- **Other SSGs (Astro Starlight, Next.js/Nextra, Hugo):** evaluated by sibling analyses; Docusaurus chosen here for first-party Mermaid, multi-instance docs, and docs-focused IA out of the box.
