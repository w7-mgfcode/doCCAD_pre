# Operational Runbook — Docusaurus (v3.10.x)

Scope: operating the target ecosystem's Docusaurus site (canonical + generated docs instances, EN/HU, static hosting). Single-operator oriented. Repo facts verified against facebook/docusaurus clone at commit `3f483e80e326` (2026-08-07).

## 1. Install / Setup

Prerequisites: Node >= 24.14 (hard requirement — `engines` in `@docusaurus/core` package.json), a package manager (pnpm recommended; upstream uses pnpm), Git.

```bash
# scaffold (TypeScript variant)
npx create-docusaurus@latest site classic --typescript
cd site

# add faster stack (ADR-001)
pnpm add @docusaurus/faster

# pin node
echo "24" > .nvmrc
```

Key config (`docusaurus.config.ts`):
- `future: { v4: true, faster: true }`
- `onBrokenLinks: 'throw'`, `onBrokenAnchors: 'throw'`, `markdown: { hooks: { onBrokenMarkdownLinks: 'throw' } }` (site-level severities; see `packages/docusaurus-types/src/config.d.ts`)
- `i18n: { defaultLocale: 'en', locales: ['en', 'hu'] }`
- Two docs instances (`@docusaurus/plugin-content-docs` with `id: 'generated'` for the second) — ADR-002
- Themes: `@docusaurus/theme-mermaid` (+ `markdown: { mermaid: true }`), local search plugin (pinned) — ADR-004

Local dev: `pnpm docusaurus start` (hot reload, default locale only). To preview HU: `pnpm docusaurus start --locale hu`.

## 2. Routine Operations

- **Publish content:** merge PR to main → CI runs `docusaurus build` → deploy `build/` to hosting. No manual steps.
- **Full local check before big changes:** `pnpm docusaurus build && pnpm docusaurus serve`.
- **Add a generated view:** AI pipeline writes MDX into `generated/`, opens PR; CI gate per ADR-005; human review; merge.
- **Update translations:** `pnpm docusaurus write-translations --locale hu` after adding new theme components/plugins; fill new keys in `i18n/hu/**.json`.
- **Clear caches** (after weird build behavior): `pnpm docusaurus clear` (removes `.docusaurus` and bundler caches).
- **Dependency updates:** weekly/monthly Dependabot PRs; merge patch bumps if CI green; hold minors for a read of the Docusaurus changelog (`/changelog` on docusaurus.io).

## 3. Upgrade Procedure (Docusaurus minor, e.g. 3.10 → 3.11)

1. Read release notes / changelog for breaking-change and swizzle-affecting labels.
2. Branch; bump all `@docusaurus/*` packages to the same version (they are lockstep-versioned — Lerna fixed versioning).
3. `pnpm docusaurus clear && pnpm docusaurus build` (both locales build by default).
4. Diff-check swizzled/wrapped components (keep an inventory file listing them; upstream source lives in `packages/docusaurus-theme-classic/src/theme/`).
5. Visual spot-check: home, one canonical doc, one generated view, one HU page, one Mermaid page, search.
6. Merge; deploy; smoke-test.

Node major upgrades: only when Docusaurus `engines` demands or LTS forces it; change `.nvmrc` + CI image together.

## 4. Backup / Restore

- **Covered by Git (everything that matters):** all content (`docs/`, `generated/`, `i18n/`), config, sidebars, custom components, lockfile. Restore = `git clone` + `pnpm install --frozen-lockfile` + build. The GitHub repo (plus any mirror) is the backup.
- **NOT in Git — regenerable, no backup needed:** `build/` output, `.docusaurus/` codegen, bundler persistent cache, `node_modules`, local-search index (rebuilt each build).
- **NOT in Git — needs export if used:** Algolia crawler config and index (if ADR-004 upgrade taken) — keep crawler config JSON committed in-repo; index is regenerable by re-crawl. Hosting config (custom headers/redirect rules) — keep as code (`netlify.toml`/nginx conf) in the repo.
- **Restore drill:** quarterly, build from a fresh clone on a clean machine/container; confirms lockfile + Node pin still reproduce the site.

## 5. Common Failures + Recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Build fails: "Error: MDX compilation failed ... Unexpected character" | AI-generated or authored MDX with unescaped `{` or `<` (MDX v3 strictness) | Fix/escape the character; harden generator template; the failing file path is printed |
| Build fails on broken links/anchors | `onBrokenLinks: 'throw'` caught a bad href after content moved | Fix link or add redirect via `@docusaurus/plugin-client-redirects`; do not downgrade severity |
| Frontmatter validation error naming a Joi rule | Key with wrong type (e.g. `sidebar_position: "3"`) | Fix type; schema at `plugin-content-docs/src/frontMatter.ts` documents allowed keys |
| Stale/odd output after upgrade or cache flag change | Persistent cache inconsistency | `docusaurus clear`, rebuild; if only on Rspack path, temporarily set `rspackPersistentCache: false` and report upstream |
| OOM / CI worker crash on build | Corpus grew; SSG worker memory | Increase CI RAM/Node heap (`NODE_OPTIONS=--max-old-space-size=4096`); SSG worker count/recycling is env-tunable (`packages/docusaurus/src/ssg/ssgEnv.ts`) |
| Mermaid diagram renders as code block | `markdown.mermaid` not enabled, theme missing, or diagram syntax error | Verify `@docusaurus/theme-mermaid` in `themes` + `markdown: {mermaid: true}`; test diagram at mermaid.live |
| HU page 404s while EN works | Deploy of partial locale build or missing translated file (translated pages require the file copy under `i18n/hu/...`) | Rebuild all locales in one job; untranslated pages 404 by design — either copy EN file as placeholder or accept EN-only for that page |
| Search returns nothing after deploy | Local-search index asset missing from deploy, or (Algolia) crawler lag/misconfig | Confirm index files in `build/`; for Algolia check crawler run logs |
| `docusaurus start` fine, `build` fails | SSR-unsafe code (browser globals at module scope) in a custom/swizzled component | Guard with `ExecutionEnvironment.canUseDOM` / `<BrowserOnly>`; build error names the route |

## 6. Monitoring Signals

- **CI:** build duration trend (cache regressions show here), build success rate, broken-link failure frequency (content hygiene signal).
- **Post-deploy smoke:** HTTP 200 on `/`, `/hu/`, one generated view, `sitemap.xml`; string-match a known phrase to catch blank-hydration pages.
- **Uptime:** external ping on the hosting URL (hosting-layer concern; site itself is static).
- **Web:** Lighthouse (perf/SEO) monthly or in CI (upstream ships `lighthouse-report.yml` as a pattern); Search Console for index coverage + hreflang errors.
- **Supply chain:** Dependabot alerts on the repo; `pnpm audit` in CI as non-blocking signal.
- **Upstream health:** watch Docusaurus GitHub releases feed; note deprecations of enabled `future` flags.

## 7. Security Ops

- Frozen lockfile installs in CI (`pnpm install --frozen-lockfile`); no floating tags.
- Scoped tokens: deploy token limited to the site target; if Algolia adopted, search-only key in client config, admin/crawler key only in CI secrets.
- Branch protection on `main`; required CI checks (build + lints); human review mandatory for `generated/**` (MDX is executable — enforce with CODEOWNERS).
- Serving-layer headers (CSP without `unsafe-eval` is generally feasible for a static Docusaurus site — verify against hydration and mermaid; HSTS; X-Content-Type-Options) configured at hosting.
- Quarterly: dependency prune, review swizzle inventory, restore drill (see 4), rotate deploy tokens.
- Incident: a compromised published site is remediated by re-deploying from a clean CI build of a known-good commit — static output makes rollback trivial (`git revert` + rebuild).
