# Sources — Zensical analysis (all accessed 2026-08-12)

## Repositories inspected (shallow clones)

- **https://github.com/zensical/zensical** → cloned to /tmp/zensical at commit 21824d2 (v0.0.53, 2026-08-04), depth 50.
  Files inspected and what they evidenced:
  - `LICENSE.md` — MIT license
  - `SECURITY.md` — vuln reporting process, 3-day ack, latest-version-only fixes
  - `README.md` — positioning, Spark offering, Discord/Docker/PyPI badges
  - `Cargo.toml` / `Cargo.lock` — Rust workspace (crates/*), Rust 1.86 / edition 2024, deps: minijinja 2.19, pyo3 0.29 abi3-py310, zrx 0.0.26 (crates.io), ariadne, tungstenite
  - `pyproject.toml` / `uv.lock` — maturin build, Python >=3.10 deps (click, jinja2, markdown, pygments, pymdown-extensions, pyyaml, tomli, deepmerge), PyPI classifier "Development Status :: 3 - Alpha", CLI entry point
  - `python/zensical/main.py` — CLI commands build/serve/new; config discovery zensical.toml → mkdocs.yml → mkdocs.yaml; --clean, --strict; "Build project in Rust runtime, calling back into Python"
  - `python/zensical/config.py` — mkdocs.yml + TOML parsing, material.extensions namespace remap, theme entry-points + inheritance, repo_url/edit_uri GitHub defaults, plugin conversion (search, offline, mike shim), _shim_* for autorefs/mkdocstrings/macros/glightbox/markdown-exec, watched_files, hashes for rebuild triggering
  - `python/zensical/markdown/render.py` — Python-side Markdown rendering, full-YAML frontmatter parsing, "working on moving the entire rendering chain to Rust"
  - `python/zensical/extensions/` — macros (jinja2, subprocess), search, links, emoji, glightbox, autorefs, mkdocstrings extensions
  - `python/zensical/bootstrap/` — `zensical new` template: zensical.toml (default features, superfences mermaid fence), GitHub Pages workflow docs.yml
  - `python/zensical/.gitignore` — templates dir gitignored (theme bundled from ui repo)
  - `crates/zensical/src/workflow.rs` — zrx stream/barrier build pipeline; module-system migration comment (April 2026)
  - `crates/zensical/src/workflow/cached.rs` — hash-keyed cache, "preliminary implementation"
  - `crates/zensical/src/config/plugins.rs` — only search + offline plugins in Rust core, "only a small subset ... replace with the module system"
  - `crates/zensical/src/config/validation.rs` — link/anchor/footnote validation options
  - `crates/zensical/src/structure/search.rs` — Rust search index build, language + separator config, nav-path/tags in items
  - `crates/zensical-serve/src/` — HTTP dev server, websocket middleware; `crates/zensical-watch/` — watcher
  - `.github/workflows/` (build/check/commit/docker/release) — multi-platform wheels, artifact attestations
  - `Dockerfile` — python:3.14-alpine build image
  - `python/tests/` — unit + integration tests
  - `git log/tag/shortlog` — release cadence (v0.0.48–53 Jul–Aug 2026), contributor concentration (Donath, Mazzucotelli)

- **https://github.com/zensical/ui** → cloned to /tmp/zui (v0.0.24, MIT).
  - `src/partials/languages/` — 69 UI translations incl. `hu.html` (Hungarian strings verified)
  - `src/assets/javascripts/components/search/client/README.md` — Disco search engine shipped minified, OSS release "expected early 2026" (still unreleased at collection)
  - `src/assets/javascripts/components/content/mermaid/index.ts` + `index.css` — lazy-load of `https://unpkg.com/mermaid@11/dist/mermaid.min.js`, `--md-mermaid-*` theming
  - `src/assets/javascripts/integrations/alternate` — language switcher integration
  - `src/` — base.html, 404.html, sitemap.xml, redirect.html templates

- **https://github.com/zensical/zrx** — existence/public access verified via `git ls-remote` (HEAD c052078); differential engine published on crates.io as zrx 0.0.26 (per Cargo.lock). Not deep-dived.
- **github.com/zensical/disco** — not accessible (private or nonexistent); Disco source availability [UNKNOWN].

## Official web (zensical.org)

- https://zensical.org/ — positioning, generator meta tag v0.0.53
- https://zensical.org/about/roadmap/ — Foundation done (Rust runtime, differential builds, parallelization); Feature Parity in progress; Module system / Disco vector search / Versioning / i18n / Component system planned
- https://zensical.org/compatibility/ — mkdocs.yml native support, identical Markdown dialect/HTML/URLs, MiniJinja adjustment note, 4-phase plan
- https://zensical.org/compatibility/plugins/ — supported: mkdocstrings, macros, glightbox, autorefs, markdown-exec, mike; NOT yet: awesome-nav, redirects, minify, blog, tags, social, i18n
- https://zensical.org/docs/get-started/ — install via pip/uv/conda/Docker; "written in Rust and Python"
- https://zensical.org/docs/setup/basics/ — zensical.toml primary format, mkdocs.yml natively read, core options, TOML rationale
- https://zensical.org/docs/community/faqs/ — Material maintenance 12 months from 2025-11-05; mkdocs.yml read indefinitely; module system top priority; differential builds/caching claims; CommonMark + Python-optional future; Spark = support only, no paid features
- https://zensical.org/spark/tiers/ — attempted; page content did not render (pricing [UNKNOWN])
- https://zensical.org/sitemap.xml, /docs/, /search/search_index.json, /docs/migrate/ — attempted, empty/404 (noted as access gaps)

## GitHub web (via fetch)

- https://github.com/zensical/zensical — stars 4.6k, forks 103, watchers 24, open issues 9, "Used by 948", Rust 61.4% / Python 38.2%, MIT
- https://github.com/zensical/zensical/releases — recent release notes v0.0.42–v0.0.46 (page lagged git tags at collection time)

## Announcement / ecosystem

- https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/ — launch announcement: MkDocs "unmaintained since August 2024", "supply chain risk"; ZRX differential engine; "4 to 5x faster" repeated builds; Material maintenance mode; Sponsors → Spark transition
- https://github.com/squidfunk/mike — fork of mike "that works with Zensical" (versioning path) [OBSERVED via search result title]
- Web search results (star count corroboration, migration articles, Talk Python episode #542) — context only, not used for factual claims

## Access limitations recorded

- GitHub REST API blocked in this session (session-scoped repo policy) — repo metrics taken from rendered GitHub page + clone instead; full-history contributor count [UNKNOWN]
- img.shields.io, repos.ecosyste.ms blocked by egress policy
- Spark pricing page and docs SPA-rendered pages not retrievable — pricing and some docs details [UNKNOWN]
