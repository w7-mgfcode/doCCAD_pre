# Sources — MkDocs analysis (all accessed 2026-08-12)

## Repositories (shallow clones, primary evidence)

- https://github.com/mkdocs/mkdocs → cloned to `/tmp/mkdocs` (master, HEAD commit dated 2025-10-20). Evidenced:
  - Package layout: `mkdocs/{commands,config,structure,themes,contrib/search,livereload,utils}`, `plugins.py`, `theme.py`, `localization.py`
  - Plugin event API: `mkdocs/plugins.py` (19 `on_*` events, `event_priority` at line 426, `CombinedEvent` at line 460, `BasePlugin` at line 58)
  - Hooks + validation + exposure config: `mkdocs/config/defaults.py` (hooks line 162, Validation class lines 169-199, exclude_docs/draft_docs/not_in_nav lines 51-57)
  - Frontmatter parsing: `mkdocs/utils/meta.py` (`get_data`, `yaml.SafeLoader` line 67)
  - Markdown pipeline: `mkdocs/structure/pages.py` (`markdown.Markdown(extensions=...)` line 268)
  - Search: `mkdocs/contrib/search/` (`__init__.py` lunr language detection, `search_index.py`, `templates/search/{lunr.js,main.js,worker.js}`, `prebuild-index.js`, `lunr-language/lunr.hu.js` among 29 language files)
  - i18n: `mkdocs/localization.py` (babel-based theme-chrome locale only)
  - Theme engine: `mkdocs/theme.py` (Jinja2 dirs, `custom_dir`, `extends` inheritance line 146)
  - Livereload: `mkdocs/livereload/__init__.py` (watchdog polling observer, rebuild condition)
  - Dirty builds: `mkdocs/commands/build.py` lines 147-199, 249-270
  - gh-deploy: `mkdocs/commands/gh_deploy.py`; dependency `ghp-import` in `pyproject.toml:42`
  - Deps/entry points/license: `pyproject.toml` (deps lines 35-50, entry points lines 79-88), `LICENSE` (BSD-2-Clause, Tom Christie)
  - CI: `.github/workflows/{ci,autofix,deploy-release,docs}.yml`; tests in `mkdocs/tests/`
  - Commit history: `git log` (release 1.6.1 on 2024-08-30; only doc/CSS fixes afterward, last 2025-10-20)

- https://github.com/squidfunk/mkdocs-material → cloned to `/tmp/mkdocs-material` (master, HEAD 2026-08-09). Evidenced:
  - `SECURITY.md` (committed 2026-07-06): public security updates end **2026-11-05**; extended support offered
  - Maintenance-mode commit stream 2025-11 → 2026-08 (dependency bumps, "Prepare 9.7.7 release" 2026-07-17, "Disabled MkDocs 2.0 warning")
  - Built-in plugins: `material/plugins/{blog,group,info,meta,offline,optimize,privacy,projects,search,social,tags,typeset}`
  - Search plugin internals: `material/plugins/search/plugin.py` (lang config lines 67-70, pipeline/fields line 247)
  - Mermaid integration: `mkdocs.yml:163-167` (superfences custom fence), `docs/reference/diagrams.md`, `src/templates/assets/javascripts/components/content/mermaid/index.ts` (loads mermaid@11 from unpkg unless global present, line 72)
  - i18n: `material/templates/partials/languages/` (69 files incl. `hu.html`)
  - `pyproject.toml` (mkdocs>=1.6,<2 requirement in requirements.txt:24; recommended plugin extras lines 57-63; MkDocs plugin/theme entry points)
  - `LICENSE` (MIT, Martin Donath)

## Official web sources

- https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/ — Zensical announcement: Material enters maintenance mode, ≥12 months critical fixes, MkDocs core characterized as unmaintained supply-chain risk, Zensical reads mkdocs.yml. [VERIFIED-OFFICIAL]
- https://github.com/squidfunk/mkdocs-material/issues/8523 — "End of life on November 5, 2026" issue: what continues/stops during maintenance mode. [VERIFIED-OFFICIAL]
- PyPI JSON API (pypi.org/pypi/<pkg>/json) — latest versions and upload dates: mkdocs 1.6.1 (2024-08-30), mkdocs-material 9.7.7 (2026-07-17), mkdocs-macros-plugin 1.5.0 (2025-11-13), mkdocs-gen-files 0.6.1 (2026-03-16), mkdocs-literate-nav 0.6.3 (2026-03-16), mike 2.2.0 (2026-04-14), mkdocs-static-i18n 1.3.1 (2026-02-20). [VERIFIED-OFFICIAL]
- https://github.com/topics/mkdocs?o=desc&s=stars — star counts: mkdocs/mkdocs 22.3k, squidfunk/mkdocs-material 27.2k. [OBSERVED]

## Secondary/community sources (context, cross-checked)

- https://docsio.co/blog/mkdocs-material — 2026 review: maintenance-mode dates, 9.7.0 as last feature release (2025-11-11), 9.7.6 maintenance notice, star/contributor counts. [OBSERVED — third-party, cross-checked against repo]
- https://fpgmaas.com/blog/collapse-of-mkdocs/ — maintainer history of mkdocs core (waylan, oprypin departures; unreviewed PRs; ecosystem fragmentation incl. Zensical). [OBSERVED — third-party commentary, treated as context not fact where uncorroborated]
- Web search results (2026-08-12) surfacing the above, including Material blog archive pages. Additional search-result links not directly relied upon: https://github.com/squidfunk/mkdocs-material/releases, https://squidfunk.github.io/mkdocs-material/blog/, https://docsio.co/blog/docusaurus-vs-mkdocs.

## Not verified / gaps

- GitHub REST API stats (exact open-issue counts, fork counts) — API blocked in this environment; star counts taken from topics listing instead.
- mkdocs-macros / gen-files / literate-nav / mike / static-i18n repository internals — verified via PyPI metadata only, not cloned (health asserted from release dates).
- Community forks (MaterialX, ProperDocs) — mentioned in secondary sources only; not inspected. [UNKNOWN depth]
- MkDocs 2.0 plans — referenced in official Zensical announcement and a disabled warning in Material's repo; no public release artifacts exist. [UNKNOWN]
