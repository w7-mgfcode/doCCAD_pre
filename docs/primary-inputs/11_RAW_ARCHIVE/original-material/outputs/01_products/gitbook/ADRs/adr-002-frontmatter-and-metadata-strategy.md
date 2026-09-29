# ADR-002: Keep machine metadata in sidecar files, use only documented frontmatter

## Status
Proposed

## Context
The ecosystem encodes provenance and regeneration metadata (source hashes, generator version,
derived-view type) in frontmatter. GitBook documents a limited frontmatter vocabulary: `hidden`,
`tags` (including primary-tag objects), and page description [VERIFIED-OFFICIAL]. Behavior of
arbitrary custom frontmatter keys across a GitBook round-trip is undocumented [UNKNOWN]; because
GitBook parses Markdown into its internal block model and re-serializes on export, unknown keys are
at risk of being dropped or reordered whenever any app-side or sync-side rewrite occurs.

## Decision
Pages carry only GitBook-documented frontmatter (`hidden`, `tags`, description). All pipeline
metadata lives in sidecar JSON files under a directory outside the `.gitbook.yaml` `root` (e.g.
`/meta/**.json`), keyed by page path. Derived pages are marked with a `tags` entry (e.g.
`ai-derived`) so provenance is visible in the published site without depending on custom keys.
A one-day fidelity spike (round-trip a file with custom keys) is run before adoption; if custom keys
provably survive, this ADR may be relaxed for non-critical metadata only.

## Consequences
- Regeneration logic joins pages to metadata via path, adding a small indirection.
- Sidecar files are invisible to GitBook (outside `root`), so they can never be corrupted by sync.
- Renames must update the sidecar key — enforced by a CI link check.

## Alternatives
- **Custom frontmatter everywhere**: simplest, rejected until fidelity is proven; silent metadata
  loss would corrupt incremental regeneration.
- **Metadata in a database**: rejected — violates anti-overengineering and Git-canonical rules.
- **HTML comments in page body**: fragile under block-model normalization; rejected.
