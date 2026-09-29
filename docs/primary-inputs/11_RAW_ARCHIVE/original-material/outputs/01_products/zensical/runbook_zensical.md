# Operational Runbook — Zensical (v0.0.x, collected 2026-08-12)

Scope: operating Zensical as the static publishing layer of a GitHub-native docs ecosystem, single engineer.

## 1. Install / Setup

### Local
```bash
python -m venv .venv && source .venv/bin/activate   # or: uv add --dev zensical
pip install "zensical==0.0.53"                      # PIN the exact version (ADR-004)
zensical new .                                       # scaffolds zensical.toml, docs/, GH Pages workflow
# or, for an existing MkDocs project: nothing — zensical reads mkdocs.yml natively
zensical serve -o                                    # live preview, websocket reload, differential rebuilds
```
Config discovery order: `zensical.toml` → `mkdocs.yml` → `mkdocs.yaml` (repo: python/zensical/main.py). Requires Python ≥ 3.10; prebuilt wheels for Linux/macOS/Windows incl. musl (repo: .github/workflows/build.yml). Conda-forge and Docker (`zensical/zensical`, build-only, not for hosting) also exist.

### CI (GitHub Pages)
Use the workflow Zensical scaffolds (repo: python/zensical/bootstrap/.github/workflows/docs.yml):
checkout → setup-python → `pip install zensical` → `zensical build --clean` → upload-pages-artifact(`site`) → deploy-pages, with `pages: write` + `id-token: write` OIDC permissions. Harden it: pin the zensical version, add `--strict`.

## 2. Routine Operations

- **Build:** `zensical build --clean --strict` in CI. `--strict` aborts on warnings (link/anchor validation). Local iteration: plain `zensical build` reuses the on-disk cache.
- **Preview:** `zensical serve -a localhost:8000`. Watches docs, config, theme overrides, snippet/macro sources automatically (repo: config.py `watched_files`).
- **Content ops:** all content changes flow through Git PRs; the generator has no state outside the repo and its disposable cache.
- **Versioned releases (if used):** deploy with the squidfunk/mike fork; Zensical honors `MIKE_DOCS_VERSION` (repo: config.py mike shim).
- **Bilingual site:** run the EN and HU builds sequentially, merge outputs into one artifact (see ADR-003).

## 3. Upgrade Procedure (monthly)

1. Read the changelog: https://zensical.org/docs/changelog/ (releases land several times/month).
2. Branch, bump the pin, `zensical build --clean --strict`.
3. Diff spot-check: homepage, one page per template type, search overlay, one Mermaid page, both languages.
4. Merge; the deploy workflow republishes. Rollback = revert the pin commit.
Note: only the latest version receives security fixes (repo: SECURITY.md) — do not skip months repeatedly.

## 4. Backup / Restore

- **Covered by Git:** everything canonical — Markdown, frontmatter, Mermaid sources, config, theme overrides, CI workflows, the derived AI content (committed via PR). Restore = `git clone` + CI run.
- **NOT covered by Git:** the build cache (disposable; recreated by `--clean` build), the published `site/` artifact (recreated deterministically; optionally retained as Actions artifacts), GitHub repo settings (Pages config, branch protection — export/document them), and any Spark/support account state.
- **Restore drill:** fresh clone on a clean machine + `pip install` pinned version + `zensical build` must produce a working site; rehearse quarterly together with the Material-fallback job (ADR-004).

## 5. Common Failures + Recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| `No config file found in the current folder` | CI working dir wrong or config not committed | Pass `-f path/to/mkdocs.yml`; check checkout path |
| Build fails only with `--strict` | AI-generated page has invalid link/anchor/footnote | Fix the page; this is the intended quality gate (validation.rs checks) |
| `Docs directory does not exist` / `site_dir must be within project root` | config paths wrong after refactor | Fix `docs_dir`/`site_dir`; both must live inside the project root (config.py validation) |
| Template override errors after upgrade | MiniJinja is stricter than Jinja2; theme partials changed pre-1.0 | Re-sync override against the current bundled templates; compatibility page documents "minor adjustments for MiniJinja" |
| Stale content in output | cache edge case (caching is self-described "preliminary", workflow/cached.rs) | `zensical build --clean`; report reproducible cases upstream |
| Mermaid diagrams not rendering | CDN blocked (default loads mermaid@11 from unpkg) or syntax error | Self-host mermaid (ADR-005); check browser console |
| Serve reload loop | watching a directory that the build writes to | Remove overlap between `watch` paths and `site_dir`/`custom_dir` (a v0.0.42 fix addressed one such loop) |
| Unsupported plugin in mkdocs.yml silently ignored / feature missing | plugin not in supported set | Check zensical.org/compatibility/plugins/; only search, offline, mike, mkdocstrings, autorefs, macros, glightbox, markdown-exec are handled today |

## 6. Monitoring Signals

- CI: build exit code (strict mode), build duration trend (regression = cache/perf issue), deploy job success.
- Content: count of validation warnings in non-strict local builds trending to zero.
- Availability: static-host uptime (GitHub Pages status) — nothing else runs.
- Upstream health: release cadence at github.com/zensical/zensical/releases; announcement blog/Discord for module-system and i18n landings; SECURITY.md channel (hello@zensical.org) advisories.
- Drift: quarterly fallback build (Material for MkDocs) still green (ADR-004).

## 7. Security Ops

- Pin exact versions with hashes; verify wheel provenance via GitHub artifact attestations (build.yml).
- Fork PRs: build without secrets; never enable markdown-exec/macros on untrusted input (build-time code execution).
- Keep the single supported (latest) version within one month (SECURITY.md latest-only fix policy).
- Serve all JS (incl. Mermaid, Disco search worker) from own origin; no third-party runtime calls.
- Report suspected Zensical vulnerabilities privately to hello@zensical.org (3-business-day ack per SECURITY.md); never in public issues.
- Review the dependency delta on every upgrade (`uv.lock`/`Cargo.lock` upstream; your own requirements lock locally).
