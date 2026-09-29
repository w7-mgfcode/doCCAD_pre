# ADR-002: AI content generation runs entirely outside the Zensical build

## Status
Accepted (2026-08-12)

## Context
Zensical has no plugin API today: only search and offline are modeled as plugins in the Rust core ("Right now, this is only a small subset... We'll replace this with the module system in the near future" [VERIFIED-REPO: crates/zensical/src/config/plugins.rs]); a fixed set of MkDocs plugins is emulated via hardcoded shims [VERIFIED-REPO: python/zensical/config.py]. The module system with a Python API is roadmapped but unreleased [VERIFIED-OFFICIAL: zensical.org/about/roadmap/]. The target ecosystem requires derived AI views (recruiter pages, interview prep, role-specific docs) that are regenerated when sources change, validated, and PR-reviewed — and AI must not be needed to serve docs.

## Decision
The AI layer is a standalone generator (repo script/Action) that writes complete Markdown files with frontmatter into `docs/derived/**`, opens PRs, and never integrates with Zensical internals. Zensical is treated as a deterministic black-box renderer invoked as `zensical build --clean --strict` in CI. Incremental regeneration is implemented in the AI layer (hash source files → regenerate affected derived pages), not in the SSG.

## Consequences
- Positive: works today; immune to module-system delays; derived content is ordinary reviewable files in Git; fallback to Material for MkDocs unaffected.
- Positive: Zensical's built-in link/anchor validation plus `--strict` becomes the automated quality gate for machine output [VERIFIED-REPO: crates/zensical/src/config/validation.rs; main.py].
- Negative: no virtual pages — every derived page must physically exist in the repo (repo size growth; acceptable and even desired for reviewability).
- Negative: build cannot enrich pages at render time (e.g., cross-page computed indexes) without committing the computed output; the macros extension + data files cover simple cases [VERIFIED-REPO: python/zensical/extensions/macros.py].

## Alternatives
- Wait for the module system and write a Zensical module: blocks the project on an unshipped API.
- Use markdown-exec to compute content at build time: introduces build-time code execution and nondeterminism into CI; rejected except for trusted, trivial cases.
- Fork/patch Zensical: unacceptable maintenance load for one engineer.
