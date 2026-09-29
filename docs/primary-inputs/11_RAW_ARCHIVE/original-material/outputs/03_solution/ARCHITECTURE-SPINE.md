---
title: Architecture Spine — GitHub-Native AI Documentation System
status: final
updated: 2026-08-12
method: bmad-architecture (spine distilled directly; memlog tooling unavailable in this environment)
---

# Architecture Spine

Paradigm: **docs-as-code, static-first, AI-in-CI**. One Git repository is the system of record; the
published site is a pure build artifact; AI is a generation plane that only writes through pull requests.
Everything below fixes the invariants that keep independently built parts (generation scripts, CI jobs,
components, content) from diverging. Rationale lives in `../02_comparison/` and `ADRs/`.

## Inherited Invariants (from mission + research)

- Git/GitHub is the primary source of truth; files over databases.
- AI must never be required to read/serve published documentation.
- AI-generated content must never silently become canonical.
- Operable by one capable engineer; every component must beat a simpler alternative.
- Bilingual EN/HU capability; Mermaid-as-code for all diagrams.

## Architecture Decisions

**AD-1 — Single repository, files only.**
Binds: all content, config, prompts, schemas, scripts, workflows. Prevents: split-brain between a docs DB
and Git. Rule: no runtime datastore; anything the system knows is a versioned file. `[ADOPTED]`

**AD-2 — Docusaurus v3.x is the publishing foundation.**
Binds: rendering, theming, i18n, search UI, Mermaid rendering. Prevents: per-team framework drift.
Rule: content targets Docusaurus MDX + frontmatter; `docusaurus build` (with `future.faster` flags) is the
sole production build; the build must pass with AI providers unreachable. Runner-up + revisit trigger: ADR-002.

**AD-3 — Two content planes, structurally separated.**
Binds: repository layout and plugin config. Prevents: generated content laundering into canon.
Rule: `docs/source/**` (canonical, human-owned) and `docs/generated/**` (derived, bot-authored) are separate
docs-plugin instances with separate sidebars, routes (`/docs`, `/views`), CODEOWNERS and CI gates. A generated
page may cite canonical pages; a canonical page never includes generated content.

**AD-4 — AI runs only in the generation plane (CI jobs + local CLI).**
Binds: all model calls. Prevents: AI in the serving path. Rule: model calls happen in GitHub Actions or a
developer's shell via `scripts/`; output lands as files in a bot branch; no server, no runtime endpoint.

**AD-5 — Thin provider abstraction, config-routed.**
Binds: every generation script. Prevents: provider lock-in and framework creep. Rule: one interface
(`complete(task, messages, opts) → text + usage`), one adapter per provider (Anthropic, Gemini, OpenAI,
OpenAI-compatible local), routing chosen from `ai.config.yaml` by task type with fallback chain; no agent
framework, no autonomous loops. Model names live in config only, never in code.

**AD-6 — Task contracts, not free-form prompting.**
Binds: what AI is allowed to produce. Prevents: unbounded generation. Rule: every generation job references
a named contract (`contracts/*.yaml`) defining inputs, allowed evidence, output schema, quality gates,
prohibited assumptions, persistence policy; prompts are versioned templates in `prompts/`.

**AD-7 — Retrieval is Level 1: deterministic file selection.**
Binds: how context is assembled. Prevents: premature vector infrastructure. Rule: context = files named in
the contract + frontmatter `sources`/`related` closure + repo grep. Decision boundary to Level 2/3 (index /
embeddings): corpus > ~1,500 pages OR measured grounding failures — recorded in ADR-006.

**AD-8 — Provenance is frontmatter; drift detection is hashes.**
Binds: metadata contract of every page. Prevents: unverifiable generated content and silent staleness.
Rule: canonical pages declare `id`, `type: canonical`, `sources`, `owners`; generated pages declare
`generated: true` + `generation:` block including `source_documents` with per-source content hashes.
CI recomputes hashes; mismatch ⇒ page flagged stale; only affected pages regenerate.

**AD-9 — Generated content persists only through pull requests.**
Binds: the write path. Prevents: unreviewed AI content going live. Rule: bot commits to `docs-gen/*`
branches; PR carries validation report; human approval required (branch protection); auto-merge never
enabled for generation PRs.

**AD-10 — Validation is deterministic-first.**
Binds: CI pipeline order. Prevents: AI judging AI as the only gate. Rule: lint → frontmatter schema →
internal links → Mermaid compile → build. AI-assisted checks (fact-consistency) are advisory labels, never
merge-blocking on their own.

**AD-11 — Interview/recruiter views are build-time artifacts.**
Binds: the career-layer features. Prevents: runtime AI dependency for readers. Rule: `<InterviewPrep>` and
recruiter pages render committed MDX/data from `docs/generated/`; regeneration is a CI job, not a request.

**AD-12 — i18n via Docusaurus filesystem locales; EN canonical.**
Binds: translation layout. Prevents: bilingual fork drift. Rule: EN is authoring language; HU lives in
`i18n/hu/**` mirroring IDs; HU gaps fall back to EN; generated pages translate on demand only.

**AD-13 — Search is build-time local index; SaaS optional.**
Binds: search UX. Prevents: mandatory third-party dependency. Rule: `@easyops-cn/docusaurus-search-local`
(or equivalent) in all modes; Algolia DocSearch optional in Mode B only.

**AD-14 — Deployment is static hosting; GitHub Pages default.**
Binds: delivery. Prevents: server sprawl / Kubernetes. Rule: `build/` deploys to GitHub Pages via Actions
(Mode B); identical artifact serves Mode A/C (any static server, incl. offline); no runtime backend exists.

**AD-15 — Untrusted-content boundary around model I/O.**
Binds: every generation script. Prevents: prompt injection becoming authority. Rule: repository content
enters prompts as delimited data, never as instructions; model output is parsed against the contract schema;
external links must match an allowlist or the PR is labeled for security review; secrets exist only as
GitHub Actions secrets / local env, never in context payloads.

## Deferred (named, not decided)

- Level 2+ retrieval implementation choice (index tech) — until AD-7 boundary trips.
- Runtime Q&A chat over docs — out of MVP scope entirely; would be an isolated service if ever built.
- Enterprise SSO / private-site auth — Harden phase, only if the site stops being public.
- Graph store for dependency mapping — manifest + frontmatter until provably insufficient.
- Automatic HU translation of generated pages — manual trigger until translation quality gates exist.

## Seed (true at cold start; code owns it after)

Docusaurus 3.x + Node ≥24.14; Python 3.11+ for pipeline scripts (stdlib + PyYAML + provider SDK-free HTTP);
repo layout per `content_architecture.md`; GitHub Actions for all automation; mermaid-cli for diagram
validation in CI.
