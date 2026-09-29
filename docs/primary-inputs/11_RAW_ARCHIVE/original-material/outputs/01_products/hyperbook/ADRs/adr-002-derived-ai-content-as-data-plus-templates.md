# ADR-002: AI-derived content is emitted as data files rendered by human-owned Handlebars templates

## Status
Proposed (2026-08-12)

## Context
The ecosystem separates canonical content (human-authored Markdown) from AI-derived views (recruiter pages, interview-prep sections). Hyperbook natively supports pages defined as `.md.yml` / `.md.json` data files that reference a `template` rendered from `templates/<name>.md.hbs` (verified: packages/fs/src/vfile.ts:840-900), with ~20 Handlebars helpers (packages/fs/src/handlebars.ts). This gives a structural boundary: data = what the AI says; template = how it is presented.

## Decision
All AI-generated derived pages are committed as `.md.yml` data files under dedicated directories (e.g. `book/interview/`, `book/recruiter/`), never as free-form Markdown. Presentation lives exclusively in version-controlled `.md.hbs` templates owned by the engineer (e.g. `templates/interview-prep.md.hbs`). CI validates every derived data file against a JSON Schema before merge, and CODEOWNERS requires human review on derived directories. Canonical content remains plain `.md` and is never written by the AI layer.

## Consequences
- PR diffs of AI output are structured YAML — semantically reviewable and machine-validatable, unlike prose diffs.
- Presentation changes (styling, layout, wording of chrome) never require regenerating AI content; regeneration never changes presentation.
- Incremental regeneration maps to file-level diffs: only changed `.md.yml` records are rewritten.
- Constraint accepted: templates are logic-light Handlebars (string helpers only); complex conditional presentation must be encoded in the data schema instead.
- Build-time template errors are console warnings, not hard failures (vfile.ts logs and continues), so CI must additionally assert expected page counts / grep build logs (see runbook).

## Alternatives
- AI writes full Markdown pages directly: rejected — mixes content and presentation, makes review and validation harder, increases prompt-injection surface for directives/HTML.
- External generator producing `.md` into the repo: kept as fallback; loses schema validation and the clean data/presentation split.
