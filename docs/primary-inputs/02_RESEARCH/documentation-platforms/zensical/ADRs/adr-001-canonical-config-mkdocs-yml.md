# ADR-001: Keep mkdocs.yml as the canonical configuration format

## Status
Accepted (2026-08-12)

## Context
Zensical reads three config files, in discovery order `zensical.toml`, `mkdocs.yml`, `mkdocs.yaml` [VERIFIED-REPO: python/zensical/main.py]. The team recommends `zensical.toml` for new projects but commits to reading `mkdocs.yml` "indefinitely" and to shipping conversion tooling when the formats diverge [VERIFIED-OFFICIAL: zensical.org/docs/community/faqs/]. Zensical is pre-1.0 (v0.0.53, PyPI classifier Alpha) with a ~2-person core team; the fallback platform, Material for MkDocs, consumes only `mkdocs.yml` and is committed to maintenance "at least 12 months" from 2025-11-05. The TOML syntax itself changed as recently as v0.0.53 ("update zensical.toml to TOML 1.1 syntax", commit 94ceb07).

## Decision
The ecosystem's docs repo keeps a single `mkdocs.yml` as the canonical, reviewed configuration. We do not create a `zensical.toml` until Zensical reaches 1.0 or until a required feature is TOML-only.

## Consequences
- Positive: one-line rollback to `mkdocs build` with Material for MkDocs if Zensical stalls or breaks; config remains readable by the entire MkDocs tool ecosystem (linters, editors, migration tools).
- Positive: avoids tracking pre-1.0 TOML schema churn.
- Negative: we forgo TOML's stricter typing and any future TOML-only options; Zensical docs examples increasingly use TOML, adding a small translation burden.
- Neutral: Zensical maps Material namespaces automatically (`material.extensions` → `zensical.extensions`) [VERIFIED-REPO: config.py compatibility shim], so the YAML needs no edits.

## Alternatives
- Adopt `zensical.toml` now: cleaner config, but burns the exit path and tracks an unstable schema.
- Maintain both files: guaranteed drift; violates single-source rule.
