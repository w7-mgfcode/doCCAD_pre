# ADR-005: Content governance via single-file MkDocs hooks + strict builds in CI, not packaged plugins

## Status
Proposed

## Context
The ecosystem mandates validation of both canonical and AI-derived content (frontmatter schema, link integrity, EN/HU parity, sanitization of generated HTML) with anti-overengineering as a hard rule. MkDocs offers three mechanisms: packaged plugins (entry-point `mkdocs.plugins`), the `hooks:` config option (`mkdocs/config/defaults.py:162`) which loads plain Python files as ad-hoc plugins with the full 19-event API, and the built-in `validation:`/`--strict` machinery (`defaults.py:169-199`: nav.omitted_files, nav.not_found, absolute_links; plus links validation) with `exclude_docs`/`draft_docs`/`not_in_nav` exposure controls.

## Decision
1. All custom validation ships as **single-file hooks** in `hooks/` (e.g. `validate_frontmatter.py`, `check_i18n_parity.py`, `sanitize_derived.py`) registered under `hooks:` in `mkdocs.yml` — no packaging, no publishing, versioned with the content they validate.
2. Frontmatter schema (required keys per page type: `title`, `lang`, `audience`, `generated`, `source_hash`, …) is validated in `on_page_markdown`/`on_files`; violations log warnings that `--strict` escalates to build failure.
3. CI runs `mkdocs build --strict` as a required PR status check; deploy jobs run the same command — one code path.
4. Derived content sanitization (strip script tags / raw HTML from `docs/derived/**`) runs in a hook so it cannot be bypassed by a forgotten CI step.
5. Packaged plugins are reserved for third-party functionality (i18n, gen-files, literate-nav); we author no in-house packaged plugin unless a hook demonstrably cannot do the job.

## Consequences
- Governance logic is ~100–200 lines of reviewable Python living in the docs repo; a one-engineer team can maintain it.
- Hooks execute arbitrary code at build time: CODEOWNERS must protect `hooks/` and `mkdocs.yml`, and fork PRs must build without secrets.
- Coupling to the MkDocs plugin API means a future platform migration rewrites these hooks (bounded cost: they are small and logic-centric).

## Alternatives
- **In-house packaged plugin**: reusable across repos but adds packaging/release overhead for one repo — rejected (overengineering).
- **Standalone CI scripts only (no hooks)**: platform-agnostic but duplicates MkDocs' file/nav model and can drift from what the build actually sees — partially rejected; CI scripts remain for AI generation, hooks own build-coupled validation.
