# ADR-005: Generated-MDX contract — provenance frontmatter, global components, CI validation gate

## Status
Proposed (2026-08-12)

## Context
AI-generated MDX must be validated before publication and carry provenance. Docusaurus facts (repo-verified): the docs frontmatter schema is Joi-validated but allows unknown keys (`.unknown()` in `packages/docusaurus-plugin-content-docs/src/frontMatter.ts`), so custom metadata passes cleanly. MDX v3 (`@mdx-js/mdx ^3.1.1` via `docusaurus-mdx-loader`) is strict: stray `{`, `<`, or invalid JSX fails compilation. Theme components can be registered globally in the `MDXComponents` mapping (`packages/docusaurus-theme-classic/src/theme/MDXComponents/index.tsx`), removing import boilerplate from generated files. Build-time checks include frontmatter validation, MDX compile, and broken link/anchor detection (`packages/docusaurus/src/server/brokenLinks.ts`). MDX is executable code — generated JSX runs in readers' browsers.

## Decision
1. **Contract:** every generated file is `.mdx` with required frontmatter keys `ai_generated: true`, `source_ref` (canonical file path + git hash), `model`, `generated_at`, plus normal `title`/`description`/`sidebar_position`. A JSON Schema for this contract is enforced by a lint script in CI (Docusaurus validates shape; the ecosystem validates semantics).
2. **Components:** generators may only use an allow-listed set of components (`InterviewPrep`, theme built-ins like `Tabs`, `Admonition`, `Mermaid`). These are registered globally via a swizzle-wrapped `MDXComponents`; raw HTML/JSX outside the allow-list is rejected by an MDX-AST lint rule.
3. **Gate:** PR CI runs `docusaurus build` (both locales) with `onBrokenLinks`, `onBrokenAnchors`, `onBrokenMarkdownLinks` set to `throw`, plus the frontmatter/AST lints. No auto-merge: generated-content PRs require human review (MDX is executable).
4. A provenance banner is rendered on generated pages by a wrapped `DocItem` reading the `ai_generated` frontmatter.

## Consequences
- The platform's own build becomes the primary deterministic validation layer — no custom validator infrastructure to maintain for compile/link integrity.
- Generator prompts/templates must escape `{`/`<` in prose; expect and budget for a tail of MDX compile failures caught in CI, not production.
- The component allow-list keeps the XSS-equivalent risk of generated JSX bounded and reviewable.
- Full-site build per PR costs CI minutes; mitigated by persistent cache (ADR-001).

## Alternatives
- **Generate plain `.md` only:** maximally safe and portable but forfeits the `InterviewPrep` interactive component — rejected for derived views, allowed for simple pages.
- **Trust-and-render without AST lint:** simpler, but lets a prompt-injected `<script>`-like payload reach review unflagged; rejected.
- **Custom standalone validator service:** overengineering; the build plus lint scripts suffice for one engineer.
