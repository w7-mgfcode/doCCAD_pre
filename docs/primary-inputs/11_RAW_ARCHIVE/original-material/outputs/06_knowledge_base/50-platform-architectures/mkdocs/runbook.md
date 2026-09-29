# Operational Runbook — MkDocs + Material stack (target ecosystem)

Scope: one-engineer operation of the MkDocs 1.6.1 + Material 9.7.x publishing layer for the GitHub-native, AI-augmented docs ecosystem. Date: 2026-08-12.

## 1. Install / Setup

```bash
# Python 3.11+ recommended; use a venv
python -m venv .venv && source .venv/bin/activate
pip install pip-tools
# requirements.in (pin the world):
#   mkdocs==1.6.1
#   mkdocs-material==9.7.7
#   mkdocs-static-i18n==1.3.1
#   mkdocs-gen-files==0.6.1
#   mkdocs-literate-nav==0.6.3
#   pymdown-extensions>=10.2
#   # optional: mike==2.2.0 (only if versioning is needed)
pip-compile --generate-hashes requirements.in
pip-sync requirements.txt
mkdocs new .        # scaffolds mkdocs.yml + docs/index.md
```

Key `mkdocs.yml` blocks (evidence: Material repo `mkdocs.yml` and `docs/reference/diagrams.md`):

```yaml
theme:
  name: material
  language: en
  custom_dir: overrides          # Jinja partials, e.g. InterviewPrep block
markdown_extensions:
  - admonition
  - attr_list
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
plugins:
  - search:
      lang: [en, hu]
  - i18n:
      docs_structure: suffix
      languages:
        - locale: en
          default: true
          name: English
        - locale: hu
          name: Magyar
hooks:
  - hooks/validate_frontmatter.py
  - hooks/check_i18n_parity.py
  - hooks/sanitize_derived.py
validation:
  links: {absolute_links: warn, unrecognized_links: warn}
extra_javascript:
  - assets/javascripts/mermaid.min.js   # self-hosted, pinned
```

Local preview: `mkdocs serve` (livereload; full rebuild per change). Drafts: `mkdocs serve --dirty` for speed (nav may be stale — never for CI).

## 2. Routine operations

- **Author loop**: edit Markdown → `mkdocs serve` → PR → CI `mkdocs build --strict` status check → review → merge → auto-deploy.
- **AI derivation loop** (outside MkDocs): CI job detects changed canonical sources (compare `source_hash` frontmatter), calls provider, writes `docs/derived/**.md` + frontmatter provenance, opens PR. Same strict build gates it.
- **Deploy**: GitHub Actions Pages workflow — `mkdocs build` → `actions/upload-pages-artifact` (site/) → `actions/deploy-pages`. Avoid laptop `mkdocs gh-deploy` (works — `mkdocs/commands/gh_deploy.py` — but bypasses CI gates).
- **Search**: nothing to operate; `search_index.json` is rebuilt every build and served statically.
- **Weekly**: review Dependabot/OSV alerts; check EN/HU parity report artifact from CI.

## 3. Upgrade procedure

Given the maintenance freeze, upgrades are rare and deliberate:
1. Read changelogs (Material releases are security/dependency bumps only since 9.7.0).
2. Bump in `requirements.in`, `pip-compile --generate-hashes`, build locally, diff `site/` output spot-checks (search, mermaid, language switcher).
3. PR the lockfile change; CI must pass strict build for both locales.
4. Never upgrade to a hypothetical MkDocs 2.x without a dedicated migration spike (breaking changes announced but unreleased as of 2026-08).
5. Mermaid runtime: upgrading `assets/javascripts/mermaid.min.js` is an explicit PR; test all diagram types used.

## 4. Backup / restore

**What Git already covers** (no separate backup needed): all content, config, hooks, theme overrides, CI workflows; deployed-site history if using `mike` (site versions are commits on `gh-pages`); PR history of AI generations.

**What Git does NOT cover**:
- The Python environment: covered by hash-pinned `requirements.txt` (in Git) + PyPI availability. Mitigation for PyPI disappearance of frozen packages: keep a `wheels/` mirror artifact (one-time `pip download -r requirements.txt -d wheels/` stored as a release asset).
- GitHub repo settings (branch protection, Pages config, secrets): document in `docs/ops/settings.md`; secrets (AI provider keys) live in a password manager, not Git.
- The rendered `site/` directory: disposable — always reproducible from source; do not back up.

**Restore**: clone repo → recreate venv from lockfile (or wheels mirror) → `mkdocs build` → redeploy. RTO ≈ minutes.

## 5. Common failures + recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| `Config value 'plugins': The "i18n" plugin is not installed` | venv drift / missing dep | `pip-sync requirements.txt` |
| Strict build fails: `Doc file contains a link ... not found` | broken relative link (often in AI-derived page) | fix link or regenerate; this is the gate working as designed |
| Warnings about pages not in nav | new file not added to `nav:`/literate-nav | add to nav or mark under `not_in_nav:` |
| Mermaid blocks show as plain code | superfences custom fence missing/mis-indented in `mkdocs.yml` | restore the `custom_fences` block; verify `!!python/name:` tag intact |
| Diagrams blank on site | self-hosted mermaid.min.js path wrong or JS error | check browser console; verify `extra_javascript` path; re-pin file |
| Hungarian search returns poor results | search `lang` missing `hu` | set `plugins.search.lang: [en, hu]` (core copies `lunr.hu.js` automatically) |
| HU site shows English UI strings | `theme.language` not set per-locale in i18n plugin | set `language: hu` in the hu locale block |
| `mkdocs serve` slow on large corpus | full rebuild per change (by design) | use `--dirty` locally; scope preview with `exclude_docs` |
| gh-pages deploy shows stale site | Pages cache or workflow deployed wrong artifact | re-run deploy job; verify artifact contents; hard-refresh |
| Build works locally, fails in CI | unpinned transitive dep or Python version mismatch | hash-pinned lockfile + pin Python version in workflow |
| YAML error on `!!python/name:` | config loaded by a non-MkDocs YAML parser (e.g. custom tooling) | only parse `mkdocs.yml` via mkdocs config loader |

## 6. Monitoring signals

- CI: strict-build pass rate on PRs; build duration trend (creeping corpus growth).
- Warning counts in build logs (MkDocs logs counts; treat new warning classes as regressions).
- Link-check job (external links) — scheduled weekly, not per-PR.
- Host: GitHub Pages availability (status.github.com); uptime ping on the public URL.
- Security: Dependabot/OSV alerts on the lockfile; calendar alarm for **2026-11-05 Material EOL** and the 2026-10-15 exit-decision checkpoint (ADR-001).
- Content governance: EN/HU parity report; count of derived pages whose `source_hash` no longer matches canonical sources (staleness metric).

## 7. Security operations

- Pin everything with hashes; no `latest` anywhere (including GitHub Actions — pin by SHA).
- Fork PRs build without secrets; AI provider keys only in the generation workflow, never in build/deploy jobs.
- CODEOWNERS on `mkdocs.yml`, `hooks/`, `overrides/`, `.github/workflows/` (code-equivalent surfaces: hooks run arbitrary Python at build time; `!!python/name:` tags make the config code-adjacent).
- Sanitization hook strips active HTML from `docs/derived/**` (AI output treated as untrusted input until reviewed).
- Pre-deploy artifact scan: secret scan + `grep` for internal hostnames in `site/`.
- Serve-time hardening at the host: CSP headers (self + inline styles needed by Material), no third-party origins after Mermaid self-hosting.
- After 2026-11-05 (Material EOL): monitor GitHub advisories on mkdocs-material manually; any published vulnerability triggers the ADR-001 exit decision immediately.
