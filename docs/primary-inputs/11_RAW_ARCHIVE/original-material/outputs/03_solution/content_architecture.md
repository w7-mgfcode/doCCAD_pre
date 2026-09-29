# Content Architecture — Taxonomy, Metadata, Conventions

Status: final · 2026-08-12 · Binds AD-1, AD-3, AD-8, AD-12 from `ARCHITECTURE-SPINE.md`.

## 1. Critique of the Proposed Starting Structure

The mission's draft taxonomy (16 numbered source dirs + generated/) is directionally right but has four
problems we fix here. First, `docs/source` vs `docs/generated` as a *naming* convention is too weak — in
Docusaurus we make it a *structural* boundary (two plugin instances, two route trees, two sidebars, separate
CODEOWNERS), so a generated file physically cannot appear under `/docs`. Second, several proposed categories
overlap (Development Manual vs Development Process; Operations vs Deployment vs Runbooks) — merged below with
one home per content type, because duplicate homes are how drift starts. Third, "Recruiter View", "Interview
Preparation" and "Generated Question Pages" are not categories of canonical knowledge — they are *audiences
of generated views*, so they live only under `generated/`. Fourth, diagrams need a canonical home with stable
paths (`docs/diagrams/`) so pages import them by reference and dependency mapping stays deterministic.

## 2. Final Taxonomy

```
docs/
├── source/                      # CANONICAL — human-owned, plugin instance "source", route /docs
│   ├── 00-overview/             # what the project is, problem, status; landing content
│   ├── 01-getting-started/      # install, first run, onboarding path (merges "Onboarding")
│   ├── 02-user-manual/          # end-user functionality
│   ├── 03-architecture/         # system views, boundaries, C4 narratives; links to diagrams/
│   ├── 04-development/          # dev manual: setup, workflow, conventions, contribution, AI/agent workflows
│   ├── 05-testing/              # test strategy, validation, quality gates
│   ├── 06-deployment/           # environments, release, infra
│   ├── 07-operations/           # operating model, monitoring, SOPs (merges "Operations")
│   ├── 08-security/             # security model, policies, threat model
│   ├── 09-troubleshooting/      # symptom→cause→fix articles
│   ├── 10-runbooks/             # step-by-step operational procedures (one procedure per file)
│   ├── 11-adr/                  # adr-NNN-slug.md, immutable once accepted
│   ├── 12-api/                  # API contracts, schemas, integration guides (merges "Integrations")
│   ├── 13-migration/            # migration guides
│   └── 14-knowledge-base/       # domain knowledge, glossary, FAQs that are human-verified
│
├── generated/                   # DERIVED — bot-authored via PR, plugin instance "generated", route /views
│   ├── recruiter/               # 30s / 2min / deep-dive evidence-linked profiles
│   ├── interview/               # <id>.interview.json + stub pages per opted-in canonical page
│   ├── questions/               # special-question pages, q-NNN-slug.mdx
│   ├── role-specific/           # senior-engineer view, beginner view, etc.
│   └── summaries/               # change summaries, migration summaries
│
└── diagrams/                    # CANONICAL .mmd sources, imported by reference
    ├── c4/  ├── sequence/  ├── workflows/  └── deployment/
```

Rationale for each directory is its one-line comment; a directory earns existence only with ≥2 planned pages,
otherwise content starts in the parent and splits later (anti-overengineering).

## 3. Canonical vs Generated Policy

Canonical: authored/approved by humans; the only admissible AI evidence; edited only by human PRs.
Generated: producible entirely from canonical sources + repo facts; deletable and regenerable at any time;
never cited as evidence by another generation task (no AI-citing-AI chains); readers always see a provenance
banner (rendered from frontmatter by the theme). Promotion path: if a generated page proves durably valuable
as canon, a human rewrites/adopts it into `source/` via normal PR — the frontmatter changes `type`, the
`generation` block is retained as `provenance_history`.

## 4. Naming Conventions

Files: `kebab-case.md(x)`; runbooks `rb-<verb>-<object>.md`; ADRs `adr-NNN-slug.md`; questions
`q-NNN-slug.mdx`; interview data `<canonical-id>.interview.json`. IDs: frontmatter `id` equals path-derived
slug, globally unique, never recycled. Headings: one `#` per page (title from frontmatter), start at `##`.

## 5. Metadata Schema (frontmatter contract)

Canonical (validated by `schemas/document.schema.json`):

```yaml
id: architecture-system-overview        # stable, unique
title: System Architecture
type: canonical
audience: [developer, architect]        # enum: developer|architect|operator|user|recruiter|interviewer
sources: [src/api/, pyproject.toml]     # repo paths this page documents (drift inputs)
owners: [architecture]
related: [adr-003, deployment-overview] # doc ids (link graph)
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-08-12
```

Generated (all canonical fields plus):

```yaml
type: generated
generated: true
generation:
  contract: GenerateRecruiterPage
  contract_version: 1
  prompt_version: recruiter.v1
  source_documents:
    - {id: architecture-system-overview, path: docs/source/03-architecture/system-overview.md, content_hash: sha256:...}
  repo_evidence: [pyproject.toml]
  provider: anthropic
  model: <from run config>
  generated_at: 2026-08-12T10:00:00Z
  approval_status: draft            # draft|in-review|approved  (approved is set by merge automation)
```

Improvements over the mission's draft: per-source `content_hash` (drift detection is mechanical),
`contract`/`contract_version` (traceable generation semantics), `repo_evidence` separated from
`source_documents` (docs vs code facts), and `confidence` dropped — a model's self-reported confidence is
not evidence and invites misplaced trust; the human review gate is the confidence mechanism.

## 6. Link Conventions

Internal links by relative file path (Docusaurus-validated at build; broken link ⇒ build failure = merge
block). Cross-plane: generated → canonical links use plain paths; canonical → generated links are forbidden
except from a dedicated "Views" index page (canon must not depend on derivables). External links in
generated content must match `config/link-allowlist.yaml` or the PR gets a security review label.

## 7. Diagram Conventions

Every diagram is Mermaid: fenced in-page for one-off illustrations, `.mmd` file under `docs/diagrams/` when
shared or referenced by `sources`. One diagram per file; file name states view type (`c4-l2-containers.mmd`).
CI compiles all of them (mermaid-cli); labels avoid `()[]{}`; dark/light handled by theme config, never
hard-coded colors. AI edits diagrams only through `UpdateMermaidDiagram` contract PRs.

## 8. Translation Strategy

EN is the authoring and canonical language (AD-12). HU lives in `i18n/hu/docusaurus-plugin-content-docs*/`
mirroring file paths and ids; untranslated pages fall back to EN automatically. Translation priority:
00-overview, 01-getting-started, 02-user-manual first; deep technical canon may stay EN-only deliberately.
Generated pages: EN by default; HU variants generated only on explicit trigger (contract `translate: hu`)
after the EN version is approved — never translate unapproved drafts. Theme UI strings: fill the ~50% HU gap
locally via `docusaurus write-translations` (tracked as a normal repo file).

## 9. Generated-Content Policy (summary; enforcement in automation_architecture.md)

Bot may create/update files only under `docs/generated/**` and `i18n/*/…/generated/**`; CI fails any
generation PR touching other paths. Every generated page: provenance frontmatter complete (schema-enforced),
all `source_documents` hashes current at merge time, evidence links resolve, no allowlist-violating external
links. Regeneration replaces the file wholesale (no AI-edits-AI diffs). Deletion of a canonical page ⇒ CI
flags all dependent generated pages for removal in the same PR.
