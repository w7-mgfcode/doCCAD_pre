# ADR-002: Isolation and lifecycle of AI-derived content within the Mintlify site

## Status
Proposed (2026-08-12)

## Context
Derived views (recruiter pages, interview-prep, special-question pages, role-specific docs) are generated from canonical pages by an external AI pipeline and must be: visibly separated from canonical content, PR-reviewed, incrementally regenerated, and individually controllable for search/SEO exposure. Mintlify provides the needed primitives but no built-in "derived content" concept: explicit `docs.json` navigation, `.mintignore` exclusion, `hidden: true` frontmatter (unlisted but public-by-URL), `searchable`/`boost` search controls, `noindex`/`seo.indexing` crawler controls, and arbitrary extra frontmatter keys.

## Decision
- Directory convention: canonical content under `docs/`, derived content under `derived/<view-type>/...` (mirrored per locale, e.g. `hu/derived/...`).
- Every derived page carries provenance frontmatter written by the pipeline: `generated: true`, `source_paths`, `source_hash`, `generated_at`, `pipeline_version`. Regeneration is triggered only when `source_hash` of the canonical inputs changes (incremental).
- Navigation: derived views appear only in dedicated tabs/groups in `docs.json`, which the pipeline updates programmatically and validates with `mint validate` in CI before opening the PR.
- Exposure defaults per class: recruiter/role pages indexed normally; interview-prep pages `boost: 0.5`; experimental views `hidden: true` + `searchable: false` until promoted. `hidden` is treated as "unlisted", never as access control.
- Working files, prompts, and intermediate artifacts are covered by `.mintignore` and/or live outside the docs path so they never publish.
- All derived changes flow through PRs with automatic Mintlify preview deployments as the review surface.

## Consequences
- Clean canonical/derived separation is enforced by convention + CI, reviewable in every PR diff.
- The pipeline must manipulate `docs.json` (JSON with published schema); `$ref` splitting per section keeps those diffs small and mergeable.
- Provenance keys are ignored by the renderer (only known frontmatter keys are consumed), so they ride along harmlessly; a platform change to strict frontmatter validation would require a prefix rename — low risk, monitored via changelog.
- Reviewers get rendered previews (Pro plan dependency).

## Alternatives
- **Separate Mintlify deployment for derived content:** stronger isolation, but doubles cost and navigation/domain complexity.
- **Mintlify multi-repo composition (Enterprise):** repo-level separation under one site; rejected on plan cost.
- **Hidden-pages-only publication:** insufficient — hidden pages are public-by-URL and invisible in navigation, defeating the purpose of curated derived views.
