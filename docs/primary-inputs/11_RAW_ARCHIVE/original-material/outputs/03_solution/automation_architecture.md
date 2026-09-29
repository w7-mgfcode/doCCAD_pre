# Automation Architecture — Ingestion, Drift, CI/CD

Status: final · 2026-08-12 · Binds AD-8, AD-9, AD-10, AD-14. Diagrams: `diagrams/flow_git_change_to_docs.mmd`,
`diagrams/flow_publishing.mmd`.

## 1. GitHub Ingestion (mission §6)

Discovery is git-native — no crawler, no database. On every push/PR, `scripts/detect_changes.py` runs:

1. **Change set**: `git diff --name-status <base>...<head>`.
2. **Classification** (path rules, deterministic): canonical doc (`docs/source/**`), diagram
   (`docs/diagrams/**`), generated (`docs/generated/**`), doc-relevant code (paths appearing in any
   frontmatter `sources[]`), config/workflow, other.
3. **Metadata extraction**: parse frontmatter of changed docs; validate against schema.
4. **Dependency manifest**: `.docs-manifest.json` is rebuilt from all frontmatter (id → path, sources,
   related, derived pages) — a build artifact committed by CI to the repo (single JSON file; beat: graph DB,
   which adds a service for a query set answerable by one dict lookup).
5. **Impact analysis**: changed path → (a) canonical pages whose `sources[]` match (docs-drift suspects),
   (b) generated pages whose `source_documents[].path` match or whose hashes mismatch (stale set),
   (c) diagrams referenced by changed pages.
6. Output: `impact.json` — consumed by CI annotations and by the regeneration workflow.

Incrementality rule (mission §6): regeneration jobs receive the stale set and touch ONLY those artifacts.
Full-corpus regeneration exists solely as a manual `workflow_dispatch` with an explicit `confirm: all` input
(used e.g. after a prompt-version bump, which by design marks all dependents stale).

## 2. Drift Detection (mission §27)

Deterministic checks, in order of authority:
- **Generated staleness**: recompute sha256 of every `source_documents[].path` at HEAD; mismatch ⇒ label
  page stale in `impact.json`; scheduled weekly workflow opens/refreshes a single "stale views" issue and
  can auto-trigger regeneration PRs for pages whose contract allows it.
- **Code-vs-docs drift**: PR touches paths in some canonical page's `sources[]` but not the page ⇒ CI posts
  a `docs-drift-suspect` comment listing affected pages with checkboxes; merge is not blocked (authors may
  legitimately judge no doc change needed — blocking here was rejected as review theater).
- **Age report**: `last_validated` older than 180 days ⇒ advisory listing in the weekly issue.
- **AI-assisted classification** (optional, Phase 2): SummarizeRepositoryChange labels the *kind* of change
  to help reviewers; advisory only, never gating (AD-10).

Content hashes beat mtimes (git doesn't preserve them) and beat AI judgment (non-deterministic, unauditable)
as the primary signal.

## 3. CI/CD Pipelines (mission §28)

### docs-validate.yml — every PR (read-only, no secrets beyond GITHUB_TOKEN read)
markdownlint → frontmatter schema validation (`scripts/validate_docs.py`) → internal link check (via
`docusaurus build` broken-link failure) → Mermaid compile (mermaid-cli, sandboxed Chromium) → manifest
rebuild + impact/drift annotations → secrets scan (gitleaks) + pinned-action audit → `docusaurus build`
(both instances, both locales) → upload preview artifact. Human review → merge.

### docs-generate.yml — workflow_dispatch / issue-form / stale-trigger (has provider secrets, env-protected)
inputs: contract, target id(s) or question, privacy class → generation pipeline (ai_architecture.md §5) →
bot branch → PR with run report. Never triggered by `pull_request_target`; never runs on fork code
(security_architecture.md).

### docs-publish.yml — push to main
production `docusaurus build` → deploy to GitHub Pages (OIDC) → smoke test: HTTP 200 on /, /docs, /views,
search index file present, sampled deep links. Rollback = revert commit (build is deterministic from Git).

### Scheduled
weekly: hash sweep + stale-views issue + external link check (external links are not merge-blocking —
the web rots independently of PRs).

## 4. Preview Strategy

MVP: build artifact attached to the PR + local `npm run serve` instruction (zero infra). Phase 2 option:
per-PR preview deploys (Netlify/Cloudflare Pages free tier or Pages preview environments) — added only if
artifact-download friction actually bites (recorded simpler-alternative decision).

## 5. Workflow Security Posture (summary)

Least-privilege `permissions:` blocks per job; generation secrets only in a protected `ai` environment;
fork PRs get validation without secrets; all third-party actions pinned to commit SHAs; bot cannot approve
its own PRs; branch protection requires human review + green validate pipeline. Full model:
`security_architecture.md`.
