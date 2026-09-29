---
id: platform-mkdocs
title: MkDocs + Material — Profile (83.8/100; Best Mechanics, Worst Trajectory)
type: knowledge
category: platforms
tags: [mkdocs, material, python, static-site-generator, maintenance-risk, eol, plugins]
sources:
  - outputs/01_products/mkdocs/SAD_mkdocs.md
  - outputs/01_products/mkdocs/scores.json
  - outputs/01_products/mkdocs/repo_health.json
  - outputs/01_products/mkdocs/ADRs/
  - outputs/02_comparison/decision_matrix.md
confidence: HIGH
related: [platform-zensical, platform-docusaurus, platform-comparison-logic, foundation-docs-as-code, foundation-i18n-models, foundation-search-models]
---

# MkDocs + Material — Profile (83.8/100; Best Mechanics, Worst Trajectory)

**Summary** — MkDocs is a small Python SSG whose architecture is "close to the theoretical minimum for a docs-as-code publishing layer" [VERIFIED-REPO]; with the Material theme and 4–6 ecosystem plugins it is mechanically the best-fitting, simplest foundation in the comparison. The decisive caveat is strategic, not technical: **MkDocs core is dormant (last release 1.6.1, 2024-08-30) and Material for MkDocs exits public security support on 2026-11-05** [VERIFIED-REPO: SECURITY.md] — under three months from the analysis date. Verdict: adopt only as a deliberately pinned, exit-ready foundation with a dated migration decision.

## Architecture Essence

~15 Python modules: click CLI (`mkdocs/commands/`), typed config validation (`mkdocs/config/`), file/nav/page model (`mkdocs/structure/`), Python-Markdown rendering, Jinja2 themes with `extends`/`custom_dir` inheritance, a **19-event plugin API** (`mkdocs/plugins.py`: `on_config`, `on_files`, `on_nav`, `on_page_markdown`… with `@event_priority` ordering), and bundled lunr.js search including `lunr.hu.js` [VERIFIED-REPO]. Layer map: Python-Markdown+pymdownx authoring / one YAML config / Python-Markdown parsing / single-process full-rebuild build / Jinja2 rendering / 19-event plugins + hooks / Material theme / lunr client search / plugin-assembled i18n / static-directory delivery.

Genuinely notable internals:

- **`hooks:`** — a single un-packaged Python file acts as a full plugin (`config/defaults.py:162`) [VERIFIED-REPO]. The analyst calls this "the anti-overengineering ideal": a 50-line `validate_frontmatter.py` enforces a metadata schema with zero packaging ceremony.
- **Per-file exposure controls** in core: `exclude_docs`, `draft_docs`, `not_in_nav`, plus a `validation:` block with per-category warning levels and `--strict` [VERIFIED-REPO] — a ready-made gate for AI-generated content.
- **Frontmatter safety**: `yaml.SafeLoader` in `utils/meta.py`; but `mkdocs.yml` itself supports `!!python/name:` tags — the *config* is code-equivalent and must be treated as trusted input [VERIFIED-REPO].
- Ecosystem completes the product: `mkdocs-gen-files` (virtual pages), `mkdocs-literate-nav`, `mike` (versioning on gh-pages), `mkdocs-static-i18n` — all actively released through 2026 [VERIFIED-OFFICIAL], unlike the core.

## Strengths

- **Simplest architecture in the field** — 5/5 (the only 5) on the 12% simplicity criterion: one Python process, one YAML, no JS toolchain (Material ships compiled assets), static output [VERIFIED-REPO].
- **Perfect Git alignment** (5/5, 15%): everything Git-tracked, `gh-deploy` built in, even deployed version history lives in Git via mike [VERIFIED-REPO].
- **Ideal substrate for external AI** (4/5, 15%): derived Markdown is just files; hooks + `--strict` make "fail the PR if AI output is malformed" one of the easiest wirings in the field — called "a genuine differentiator" [VERIFIED-REPO].
- **Hungarian support unusually complete**: Material `hu.html` UI pack + bundled `lunr.hu.js` stemmer + active static-i18n plugin [VERIFIED-REPO/-OFFICIAL] — assembled, but every part exists.
- **Mermaid-as-code with dual rendering**: same fence renders on GitHub and the site (superfences + Material runtime) [VERIFIED-REPO/-OFFICIAL].
- Free (BSD-2 + MIT), trivially self-hosted — 5/5 on both deployment and cost.

## Weaknesses & Risks

- **Material support cliff, date-certain**: maintenance mode since 2025-11-05 (team pivoted to Zensical); `SECURITY.md` fixes public security-update EOL at **2026-11-05**, with paid extended support offered [VERIFIED-REPO/-OFFICIAL]. Risk #1, likelihood "Certain (date fixed)".
- **Dormant core**: 1.6.1 since 2024-08-30; last master commits are doc fixes (2025-10-20); maintainer churn documented; unbounded CVE-response latency [VERIFIED-REPO/-OFFICIAL]. Security scored 3/5 mostly on this composite risk.
- **The adopted product is a composite** (core + theme + 4–6 plugins) and its risk profile is the composite's — "ecosystem archaeology" assembled from folk knowledge that stops evolving with Material frozen [INFERRED].
- **No multilingual model in core** — EN/HU is a three-part assembly, scored 3/5.
- **Full rebuilds only** (`--dirty` is an explicitly dev-only approximation) [VERIFIED-REPO]; raw HTML passes through Python-Markdown by default — sanitize AI output in a hook (threat T3).
- Build executes repo code (hooks, `!!python/name:`) — fork-PR CI must run without secrets (threat T2); Material loads Mermaid from unpkg by default — self-host via the privacy plugin (T4).

## When to Choose It / When Not To

**Choose it when**: the team is Python-literate and wants the minimum-complexity, maximum-control stack; validation/generation logic in plain Python (hooks) is the preferred extension model; a JS/React toolchain is unwanted — the decision matrix names it the constraint-adjusted fallback if React were vetoed. **Only** with pinned versions (`pip-compile` with hashes) and a dated exit decision before 2026-11-05 (migrate to Zensical, buy extended support, or fork).
**Avoid it when**: nobody will own the sustainability decision; you need first-class components in content (no MDX equivalent); you need native i18n; or adopting a security-frozen theme is a compliance non-starter.

## Weighted Score & Decision Drivers

**83.8/100** — rank 3 of 6. What kept it high: 5/5 on docs-as-code fit, architecture simplicity, self-hosting and cost. What kept it from winning: **security/governance 3/5 (10%)** — the analyst deliberately concentrated the maintenance risk there and in the critical-constraints list "rather than spread invisibly across criteria" (a scoring-hygiene pattern worth copying); plus localization 3/5 and Mermaid 4/5 (theme-supplied, not core). The decision matrix: "For MkDocs to overtake, its maintenance risk would have to be ignored, which the evidence forbids."

## Expert Notes

- The corpus's clearest lesson in **separating format risk from toolchain risk**: the content model (plain Markdown + frontmatter) is safe and portable regardless; only the toolchain has an EOL. That is why "pin everything and plan the exit" is coherent rather than reckless — a frozen static generator keeps working; it just stops getting patches.
- Keep generation and governance **in CI scripts, not MkDocs plugins**, explicitly to shrink exit cost (recommendation #2, #3) — the platform-agnostic-glue principle generalized.
- Build-time virtual generation (gen-files) is reserved for *mechanical* views only, because it bypasses PR review of rendered content; AI prose must be committed files (ADR-002) — a governance distinction finer than most teams make.
- Zensical reads `mkdocs.yml` natively, making MkDocs→Zensical the cheapest forward migration in the field — the two profiles should be read as one decision: see [zensical](zensical.md).
- Calendar governance: recommendation #9 literally says to *calendar* the re-evaluation (by 2026-10). Time-boxed risks deserve dated decisions, not standing worry.

## Evidence & Further Reading

- Full analysis: `outputs/01_products/mkdocs/SAD_mkdocs.md` (both repos cloned: mkdocs/mkdocs + squidfunk/mkdocs-material)
- Scores: `outputs/01_products/mkdocs/scores.json`; health: `repo_health.json` (core 22.3k★ dormant; Material 27.2k★ maintenance-mode, 9.7.7 2026-07-17)
- ADRs: adr-001 (adopt pinned + exit plan), adr-002 (committed Markdown, not build-time), adr-003 (static-i18n suffix EN/HU), adr-004 (Mermaid self-hosted runtime), adr-005 (hooks + strict CI governance)
- Successor analysis: [zensical](zensical.md); decision context: [comparison-logic](comparison-logic.md)
- Foundations: [docs-as-code](../00-foundations/docs-as-code.md), [i18n-models](../00-foundations/i18n-models.md), [search-models](../00-foundations/search-models.md)
