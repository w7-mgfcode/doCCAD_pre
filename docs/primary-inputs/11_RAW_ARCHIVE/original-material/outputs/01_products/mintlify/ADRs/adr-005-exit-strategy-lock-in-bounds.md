# ADR-005: Exit strategy and lock-in bounds

## Status
Proposed (2026-08-12)

## Context
Mintlify's content model is portable (MDX in our Git repo, MIT-licensed component library available on npm), but three lock-in surfaces exist: (1) `docs.json` navigation/config semantics, (2) Mintlify-specific MDX components used in pages, (3) hosted-only capabilities (search, assistant, previews, llms.txt generation). Static export of the rendered site is Enterprise-only, and the hosted plan offers no build-artifact ownership. The ecosystem's hard rule is that Git remains canonical and the platform must be replaceable by one engineer within days.

## Decision
- **Component discipline:** pages may use Mintlify components only via local snippet wrappers (`snippets/*.jsx|mdx`, e.g. `InterviewPrep`, `RoleCard`). A CI grep forbids direct use of a curated deny-list of Mintlify-only components outside `snippets/`.
- **Conservative MDX:** derived-content generators emit CommonMark + Mermaid + frontmatter + wrapped snippets only; no inline React in generated pages.
- **Fallback renderer:** a minimal SSG config (kept in-repo, CI-built weekly) renders the corpus read-only; wrappers have plain fallback implementations there. DNS cutover to the fallback is documented in the runbook and rehearsed once.
- **Continuous archival:** a scheduled Action fetches `llms-full.txt`, `sitemap.xml`, and every page's `.md` endpoint into an `archive/` branch — an official, always-current plaintext mirror requiring no plan tier.
- **Config portability:** navigation lives in `$ref`-split JSON fragments with a documented mapping script to the fallback SSG's sidebar format.
- Exit is triggered by defined tripwires: sustained price increase beyond budget, removal of free-tier custom domains, deprecation of `.md`/llms.txt surfaces, or repeated unannounced rendering regressions.

## Consequences
- Exit cost is bounded to: navigation mapping (scripted), wrapper reimplementation (a handful of files), search/assistant replacement (accept degradation initially).
- Slightly constrained authoring (wrapper indirection, conservative MDX in generated pages) — an acceptable tax for reversibility.
- The weekly fallback build doubles as a rendering-regression canary for canonical Markdown.

## Alternatives
- **No discipline, full component usage everywhere:** best short-term authoring speed; exit becomes a page-by-page rewrite — rejected.
- **Enterprise static export as the exit mechanism:** ties reversibility to the most expensive tier — rejected.
- **Avoiding Mintlify components entirely:** maximally portable but discards much of the platform's value (cards, tabs, steps, API components); wrappers capture most value at low exit cost.
