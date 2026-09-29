# ADR-001: Adopt MkDocs + Material as the publishing layer, version-pinned, with a dated exit plan

## Status
Proposed (decision must be revisited no later than 2026-10-15)

## Context
The target ecosystem needs a GitHub-native, static-first publishing layer for canonical Markdown + Mermaid + frontmatter, operable by one engineer, with AI-derived content generated in CI and never required at serve time. MkDocs (core) plus Material for MkDocs delivers the best mechanics for this: native frontmatter (`mkdocs/utils/meta.py`), 19-event plugin API plus single-file hooks (`mkdocs/plugins.py`, `config/defaults.py:162`), lunr search with Hungarian stemming (`mkdocs/contrib/search/lunr-language/lunr.hu.js`), Mermaid via superfences, and pure static output.

However, as of 2026-08-12: MkDocs core's last release is 1.6.1 (2024-08-30) with a dormant maintainer situation; Material for MkDocs is in maintenance mode (since 2025-11-05) with public security updates ending **2026-11-05** per its `SECURITY.md`, as the squidfunk team focuses on Zensical.

## Decision
Adopt MkDocs 1.6.1 + Material 9.7.x as the publishing layer **only under these conditions**:
1. All Python dependencies are pinned with hashes (pip-compile); upgrades are explicit, reviewed events.
2. Platform-specific logic is minimized: AI generation, validation orchestration, and deployment live in CI scripts; MkDocs-side logic is limited to thin hooks and configuration.
3. A dated re-evaluation checkpoint (2026-10-15) decides between: migrate to Zensical, purchase extended Material support, or freeze-and-fork.

## Consequences
- Immediate productivity: working pipeline in days, minimal moving parts, zero hosting cost.
- Accepted risk: after 2026-11-05 the theme has no public security support; the static-output model and pinned versions bound the exposure but do not eliminate it.
- The exit plan is a first-class deliverable, not an afterthought; content stays portable (plain Markdown + frontmatter + Mermaid fences).

## Alternatives
- **Zensical now**: same team, modern engine, reads `mkdocs.yml` — but younger and evaluated separately; adopting MkDocs pinned keeps that door open.
- **Docusaurus/Astro**: active maintenance but heavier JS toolchains, weaker single-file-hook ergonomics for a Python-centric one-engineer operation.
- **Hugo**: fast and maintained, but Go templating and weaker Python extensibility for the AI-validation hooks this ecosystem needs.
