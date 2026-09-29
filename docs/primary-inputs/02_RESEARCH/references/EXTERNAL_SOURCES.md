# Aggregated External Source Logs (REF-001..REF-006)

Concatenated per-platform `sources.md` evidence logs (originals preserved alongside the research and in RAW archive).


---

## REF-001 — mintlify source log

# Sources — Mintlify analysis

All accessed 2026-08-12. The primary evidence base is the **official docs source repository** `github.com/mintlify/docs` (MIT), which is the literal source of https://mintlify.com/docs — file paths below are cited as `[VERIFIED-OFFICIAL]` (official docs content) and, where repo mechanics themselves are the evidence (git history, config files), `[VERIFIED-REPO]`.

## Cloned repositories (shallow, /tmp)

| Repo | Path | What it evidenced |
|---|---|---|
| github.com/mintlify/docs | /tmp/mintlify-docs | Entire official docs corpus (~1500 files): docs.json schema & real-world config, navigation/languages structure, all feature docs below; LICENSE (MIT), CONTRIBUTING.md, git history (277 commits/30d; 235/300 recent commits by mintlify[bot]), gt.config.json + es/fr/zh trees (vendor's own translation pipeline), shipped OpenAPI specs (admin-openapi.json, analytics.openapi.json, discovery-openapi.json, static-export-openapi.json, openapi.json, asyncapi.yaml) |
| github.com/mintlify/starter | /tmp/mintlify-starter | Starter template: docs.json with $schema, AGENTS.md, MIT license |
| github.com/mintlify/components | /tmp/mintlify-components | Open-source MIT React/Tailwind component library; pnpm monorepo, Storybook, CHANGELOG v1.0.18 (2026-07-01), component inventory |
| github.com/mintlify/mint | clone attempt | 404/auth-required → CLI source repo is private [OBSERVED] |

## Key files inspected in /tmp/mintlify-docs (selection)

- `what-is-mintlify.mdx` — product model (repo/dashboard/site), build-on-push, Mermaid usage
- `docs.json` — real top-level config: theme, colors, navigation.languages (en/es/fr/zh), api, contextual, redirects, seo, integrations
- `organize/`: `navigation.mdx` (pages/groups/tabs/anchors/dropdowns/menus/languages/versions), `settings.mdx` ($ref splitting, mint.json upgrade), `settings-reference.mdx`, `settings-structure.mdx`, `settings-seo.mdx`, `settings-appearance.mdx` (8 themes), `settings-api.mdx`, `settings-integrations.mdx`, `hidden-pages.mdx`, `mintignore.mdx`, `pages.mdx`
- `components/mermaid-diagrams.mdx` — native Mermaid, ELK layout, zoom/pan controls, placement/actions props
- `components/*.mdx` — full built-in component inventory (30+)
- `create/reusable-snippets.mdx` — snippet system (.mdx/.md/.jsx imports, props, nesting); `create/redirects.mdx`, `create/changelogs.mdx`
- `customize/react-components.mdx` (inline/exported React with hooks), `custom-scripts.mdx` (CSS/JS, Tailwind v3), `custom-domain.mdx`, `themes.mdx`
- `ai/llmstxt.mdx` (auto llms.txt/llms-full.txt, .well-known, discovery headers, 100k-char cap), `ai/markdown-export.mdx` (.md suffix, Accept header, Visibility for agents, markdown.instructions), `ai/model-context-protocol.mdx` (search MCP at /mcp, tools, version/language filters, /authed/mcp), `ai/mintlify-mcp.mdx` (admin MCP at mcp.mintlify.com, OAuth, PR-only writes), `ai/skillmd.mdx` (auto skill.md, agentskills.io, A2A agent-card), `ai/contextual-menu.mdx`
- `assistant/index.mdx` (Pro+, credits, indexing behavior), `agent/index.mdx` (PR-based agent, review-process setting, branch-protection fallback), `automations/index.mdx` + `automations/reference.mdx` (trigger types, PR grouping, 500 runs/day)
- `deploy/github.mdx` (GitHub App, clone-out wizard), `preview-deployments.mdx` (Pro+, fork-PR exclusion, manual/API previews), `ci.mdx` (broken links, Vale, warning/blocking), `deployments.mdx` (manual redeploy, deletion), `monorepo.mdx`, `multi-repo.mdx` (Enterprise), `ghes.mdx`, `gitlab.mdx`, `gitlab-self-hosted.mdx`, `bitbucket.mdx`, `self-host.mdx` (Enterprise engagement; CDK/Helm; MongoDB/PostgreSQL/Redis/S3; 45–60 vCPU sizing; AI on own endpoint/BYO key), `export.mdx` (mint export, Enterprise, zip + serve.js), `authentication-setup.mdx` (password Pro+, OAuth/JWT Enterprise, groups), `csp-configuration.mdx`, `reverse-proxy.mdx`, `docs-subpath.mdx`
- `dashboard/`: sso, scim, roles (RBAC), audit-logs, session-security, network-access, security-contact — all Enterprise-gated
- `optimize/search.mdx` (boost, searchable, filters Enterprise), `optimize/seo.mdx` (JSON-LD @graph, sitemap, OG image gen), `guides/geo.mdx`
- `guides/internationalization.mdx` — supported language codes incl. **hu**; languages navigation; default language; duplicate-path warning
- `api/introduction.mdx` + `api/*` — REST surface: update trigger/status, preview trigger, automations trigger, agent jobs v2, assistant messages/search/page-content, analytics exports, deslop, static-export API; key types (mint_ admin, assistant, index), expiry, 10 keys/hour
- `search-index/*.mdx` — Mintlify Index (index.mintlify.com) cross-site retrieval MCP/API
- `cli/commands.mdx`, `cli/install.mdx` — mint dev/validate/broken-links/export/automations/index/add-domain/config
- `credits.mdx` — Pro contributes 10,000 credits/mo; add-ons 15k/$145, 40k/$370, 90k/$800; per-feature averages (assistant 23, translations 913, etc.); "Starter plan does not include AI features"
- `changelog.mdx` — Aug 7 2026 entry (Mintlify Index, private pages, faster previews) — release cadence evidence
- `editor/*.mdx` — web editor: branching/publishing, comments, suggestions, live preview, private pages; snippets unsupported in editor
- `help-center/openapi-url-fetch-fails-during-build.mdx` — documented failure mode

## Web fetches

| URL | What it evidenced |
|---|---|
| https://mintlify.com/pricing (fetched twice) | Tiers: Starter $0/mo (5 editor seats, custom domain, web editor, authentication, MCP server, API playground), Pro (unlimited editors; agent/assistant/automations/preview deployments/admin APIs; monthly/annual toggle — numeric price rendered client-side, not extractable), Enterprise contact-us (SSO/SCIM/RBAC, SLA, self-hosting, EU hosting, BYOK). 10,000/mo credits figure displayed (attribution to column ambiguous in fetch; credits.mdx confirms it belongs to Pro) [VERIFIED-OFFICIAL] |
| https://ferndesk.com/blog/mintlify-pricing (Dec 13 2025) | Third-party report: Pro $450/mo annual, $540 monthly, 10k credits included [OBSERVED — third-party, used with explicit labeling only] |
| https://github.com/mintlify/docs | 433 stars, 239 forks, 86 issues, 15 PRs, MIT [OBSERVED] |
| https://github.com/mintlify/components | 114 stars, 15 forks, 2 issues, MIT [OBSERVED] |
| https://github.com/mintlify/starter | 1.9k stars, 524 forks, MIT [OBSERVED] |
| https://github.com/mintlify/mint | 404 → private [OBSERVED] |

## npm registry (direct, allowed egress)

| Package | What it evidenced |
|---|---|
| registry.npmjs.org/mint | latest 4.2.797 published 2026-08-12; license Elastic-2.0; repository field → github.com/mintlify/mint (packages/mint); wraps @mintlify/cli 4.0.1400 |
| registry.npmjs.org/mintlify | same version/license; legacy alias package |

## Access limitations (honest scope)

- GitHub REST API and github.com HTML were session-gated in the analysis container; repo metadata was obtained via the web-fetch tool (rendered page values) instead. Git clone over HTTPS worked normally.
- mintlify.com was not reachable via in-container curl (egress policy); official pages were read through the web-fetch tool and, primarily, through the mintlify/docs source repo itself.
- Pro plan's exact price is rendered client-side on the official pricing page and could not be verified from official material; only a third-party figure is reported, labeled as such.
- Mintlify backend internals, search engine technology, AI model choices on hosted plans, uptime/SLA numbers, and compliance certifications: [UNKNOWN] — not claimed anywhere in this analysis.


---

## REF-002 — gitbook source log

# Sources — GitBook analysis (all accessed 2026-08-12)

## Official documentation (gitbook.com/docs) — [VERIFIED-OFFICIAL]

| URL | Evidenced |
|---|---|
| https://gitbook.com/docs/sitemap.md | Full docs IA; location of all feature pages |
| https://gitbook.com/docs/llms.txt | Machine-readable page index; exact URLs for Git Sync, OpenAPI, variants, API, search sections (also demonstrates llms.txt feature itself) |
| https://gitbook.com/docs/llms-full.txt (+ ?ask= queries) | Frontmatter fields (hidden, tags), Git Sync 5,000-page limit, 20-page import cap, 100MB file limit |
| https://gitbook.com/docs/docs-as-code/git-sync.md | Bidirectional sync definition; GitHub+GitLab; enterprise egress IPs; admin/creator-only setup; skill.md mention |
| https://gitbook.com/docs/docs-as-code/git-sync/enabling-github-sync.md | Setup flow; GitHub App repo-scoped permissions; branch selection; initial sync direction semantics ("GitBook is the source of truth" vs "GitHub branch is the source of truth"); live-edit locking; commit/change-request flow |
| https://gitbook.com/docs/docs-as-code/git-sync/content-configuration.md | .gitbook.yaml: root, structure.readme, structure.summary, redirects; SUMMARY.md format; sidebar titles; README-in-Git warning |
| https://gitbook.com/docs/docs-as-code/git-sync/commits.md | GITBOOK-{n} commit message format + customization; GitHub autolink references |
| https://gitbook.com/docs/docs-as-code/git-sync/monorepos.md | Project directories; per-section .gitbook.yaml; asset isolation across directories |
| https://gitbook.com/docs/docs-as-code/git-sync/github-pull-request-preview.md | Per-PR preview URLs; requirements; fork-PR previews off by default; authenticated-access exclusion |
| https://gitbook.com/docs/docs-as-code/git-sync/troubleshooting.md | Conflict behavior (new files created rather than merged); import-then-export ordering; README duplication; re-trigger procedures; SUMMARY.md registration requirement; protected-branch gitbook-com bypass; PRs don't create change requests; redirect rules |
| https://gitbook.com/docs/docs-as-code/gitbook-cli.md | @gitbook/cli: install, OAuth/PAT auth, commands, JSON output, agentic use, integration scaffolding |
| https://gitbook.com/docs/docs-as-code/gitbook-mcp.md | Write MCP server at mcp.gitbook.com/mcp; OAuth/PAT; change-request drafting; client support |
| https://gitbook.com/docs/getting-started/llm-ready-docs.md | .md page endpoints; llms.txt; llms-full.txt (includes hidden pages); per-site read MCP at /~gitbook/mcp; ?ask= mechanism |
| https://gitbook.com/docs/create-content/formatting/markdown.md | CommonMark-aligned syntax; hint custom syntax; Prism highlighting |
| https://gitbook.com/docs/create-content/blocks/mermaid-blocks.md | Native Mermaid blocks; ```mermaid round-trip via Git Sync; troubleshooting |
| https://gitbook.com/docs/create-content/openapi.md | Swagger 2.0 / OpenAPI 3.0 / 3.1; file or URL specs; Scalar-powered test-it; CORS requirement |
| https://gitbook.com/docs/create-content/version-control.md | Version history; diffs; rollback; revision preview URLs; change requests vs live edits vs Git Sync |
| https://gitbook.com/docs/create-content/searching-your-content.md | Quick Find keyword search; AI search with cited answers; cross-section scope |
| https://gitbook.com/docs/manage-your-site/site-structure/variants.md | Variants for versions/languages; language picker; slugs/canonical redirects; default variant |
| https://gitbook.com/docs/manage-your-site/site-structure/multilingual-sections.md | Localized titles per browsing language with fallback |
| https://gitbook.com/docs/collaborate/member-management/roles.md | Role ladder Guest→Admin; plan-gated roles; inheritance; billing per member |
| https://gitbook.com/docs/publish/publish-a-docs-site.md | Publish flow; public-by-default; audience modes; unpublish/delete |
| https://gitbook.com/docs/publish/seo.md | SSR pre-rendering; /sitemap-pages.xml; canonical URLs; OG tags; CDN; 301s |
| https://gitbook.com/docs/publish/adaptive-content.md | Claims-based segmentation; Ultimate-only |
| https://gitbook.com/docs/ai-for-your-readers.md | Assistant, AI search, connections, per-site MCP servers |
| https://gitbook.com/docs/gitbook-agent/overview.md | Agent capabilities; @gitbook invocation; styleguides; 10 msg/week free limit; OpenAI delivery, no training on customer data |
| https://gitbook.com/docs/developers/gitbook-api/quickstart.md | api.gitbook.com; bearer PATs; endpoint families incl. change requests, import/export, Ask endpoint |

## Official site / blog — [VERIFIED-OFFICIAL]

| URL | Evidenced |
|---|---|
| https://www.gitbook.com/pricing | Free $0; Premium $65/site/mo + $12/user; Ultimate $249/site/mo + $12/user; Enterprise custom; feature gating (custom domain, AI search, authenticated access, SAML, Git Sync IP allowlisting); translations add-on pricing; 14-day trials |
| https://www.gitbook.com/blog/gitbook-security-soc2-iso27001 | SOC 2 Type II + ISO/IEC 27001 (2023-09-29); security.gitbook.com trust center |

## Repository inspection — [VERIFIED-REPO]

| Source | Evidenced |
|---|---|
| Shallow clone of https://github.com/GitbookIO/gitbook (HEAD 7594a334, 2026-08-11) | README: "open source code used to render GitBook's published content"; GPL-3.0 LICENSE; "Legacy GitBook (deprecated)" section; monorepo packages (gitbook, react-contentkit, react-openapi, openapi-parser, react-math, expr, embed); packages/gitbook/package.json deps (@gitbook/api, @opennextjs/cloudflare, @opennextjs/aws, mermaid@^11.14.0, mermaid-zenuml, flexsearch, mcp-handler, @modelcontextprotocol/sdk, shiki, remark/rehype/mdast incl. mdast-util-frontmatter); src/routes (llms.ts, llms-full.ts, markdownPage.ts, markdownAsk.ts, sitemap.ts, robots.ts, openapi-proxy.ts); components (DocumentView, Search, AIChat, Adaptive, SiteAuth, PDF); src/lib/data/api.ts; .github/workflows (ci, deploy-production, publish) |
| Depth-200 clone log analysis of same repo | 177 commits in trailing 90 days; 10+ authors (Zeno Kapitein 47, Nolann B. 34, conico974 25, Greg Bergé 21, Samy Pessé 5, claude[bot] 4); last commit 2026-08-11 |
| https://github.com/GitbookIO/gitbook (web page) | 28.9k stars; ~4k forks; GPL-3.0; 46 open issues; not archived; latest visible release @gitbook/react-contentkit@0.7.7 (2025-10-15) |

## Historical (never presented as current architecture) — [HISTORICAL]

| Source | Note |
|---|---|
| Legacy GitBook toolchain / gitbook-cli (npm gitbook 3.x era) | Deprecated legacy OSS generator; acknowledged as deprecated in the current GitbookIO/gitbook README; used in this analysis only as a vendor-pivot risk prior. GitHub API access to gitbook-cli was blocked in this environment; deprecation evidenced via current repo README instead. |

## Gaps / negative findings

- GitHub org-level API listing blocked by environment proxy; per-repo web page used instead.
- gitbook.com/docs/account-management/plans.md and the SOC-2 help-center page returned 404 at their
  old paths (docs restructure); pricing and blog pages used instead.
- Not verifiable from public docs: sync failure webhooks, API rate limits, custom-frontmatter
  round-trip behavior, hreflang emission, AI-translation language list (Hungarian), production
  backend topology, SLAs — all marked [UNKNOWN] in the SAD.


---

## REF-003 — docusaurus source log

# Sources — Docusaurus analysis

All accessed 2026-08-12. Repository paths refer to the shallow clone of https://github.com/facebook/docusaurus at commit `3f483e80e326cc646b54b83d564b3f0c4881b9a6` (main, 2026-08-07), cloned to `/tmp/docusaurus`.

## Remote sources

| Source | What it evidenced |
|---|---|
| https://github.com/facebook/docusaurus (repo page, web fetch) | Stars 65.1k, forks 9.9k, 293 open issues, 106 open PRs, latest GitHub release v3.10.1 (2026-04-30), MIT + CC-BY-4.0 licenses, TypeScript 95.9%, "Used by 12.2k" |
| https://docusaurus.io/ (homepage, web fetch) | Advertised version v3.10 / docs at 3.10.2; positioning: MDX, React-based, localization, versioning, Algolia search |
| https://registry.npmjs.org/@docusaurus/core (npm registry JSON) | dist-tags (latest 3.10.2, canary 3.10.1-canary-6655), release timestamps: 3.7.0 2025-01-03, 3.8.0 2025-05-27, 3.9.0 2025-09-25, 3.10.0 2026-04-07, 3.10.1 2026-04-30, 3.10.2 2026-07-10 |
| Web search (facebook/docusaurus, 2026) | Existence of public v4 milestone (github.com/facebook/docusaurus/milestone/21), releases page, discussions |

Note: GitHub REST API (api.github.com) was blocked by the session egress proxy; repo-page figures were taken from the rendered GitHub UI instead. https://docusaurus.io/blog fetch was not approved in-session; release cadence was verified via npm timestamps instead.

## Repository files inspected (evidence per path)

| Path (relative to repo root) | What it evidenced |
|---|---|
| `lerna.json` | Monorepo version 3.10.1, pnpm client, fixed lockstep versioning, changelog label taxonomy |
| `package.json` (root) | pnpm workspace scripts; rspack/rsdoctor profiling scripts; Crowdin scripts for website i18n; Argos visual regression; per-locale build script |
| `packages/` (listing) | 38-package layout: core, mdx-loader, bundler, faster, content plugins, themes, utils, create-docusaurus |
| `packages/docusaurus/package.json` | v3.10.1; bin `docusaurus.mjs`; deps webpack ^5.106.2, react-router v5, tinypool; peer react ^19.2.5; engines node >=24.14; optional peer @docusaurus/faster |
| `packages/docusaurus-faster/package.json` | @rspack/core ^2.1.0, @swc/core, @swc/html, lightningcss — the 2026 faster-build stack |
| `packages/docusaurus-bundler/src/currentBundler.ts` | Bundler switch driven by `future.faster.rspackBundler`; webpack/rspack duality |
| `packages/docusaurus-types/src/config.d.ts` | FasterConfig flags (swcJsLoader, lightningCssMinimizer, mdxCrossCompilerCache, rspackBundler, rspackPersistentCache, ssgWorkerThreads, gitEagerVcs); FutureV4Config (fasterByDefault, mdx1CompatDisabledByDefault); VcsConfig abstraction; experimental hash router; onBrokenLinks/onBrokenAnchors/onBrokenMarkdownLinks severities |
| `packages/docusaurus-types/src/plugin.d.ts` | Plugin lifecycle contract: loadContent, contentLoaded, allContentLoaded, postBuild, configureWebpack, getThemePath, getPathsToWatch, extendCli, injectHtmlTags, translateContent |
| `packages/docusaurus-mdx-loader/src/processor.ts` | MDX pipeline: default remark plugins (headings, toc, transformImage, transformLinks, resolveMarkdownLinks, mermaid, admonitions, mdx1Compat), remark/rehype/recma extension points |
| `packages/docusaurus-mdx-loader/package.json` | @mdx-js/mdx ^3.1.1 (MDX v3) |
| `packages/docusaurus-mdx-loader/src/format.ts`, `frontMatter.ts` | md vs mdx format handling; frontmatter extraction |
| `packages/docusaurus-plugin-content-docs/src/frontMatter.ts` | Joi frontmatter schema (sidebar_position, sidebar_label, slug, tags, draft/unlisted via ContentVisibilitySchema, last_update) with `.unknown()` passthrough |
| `packages/docusaurus-plugin-content-docs/src/index.ts` | Multi-instance via options.id; per-instance CLI `docs:version:<id>`; per-instance data dirs |
| `packages/docusaurus-plugin-content-docs/src/sidebars/`, `src/versions/` | Autogenerated sidebar generator; snapshot versioning modules |
| `packages/docusaurus-plugin-sitemap/src/` | Sitemap generation (createSitemap/createSitemapItem, lastmod) |
| `packages/docusaurus-theme-mermaid/package.json` + `src/` | First-party Mermaid theme; mermaid >=11.14.0 peer; optional @mermaid-js/layout-elk; client lazy-load (loadMermaid.ts) |
| `packages/docusaurus-theme-classic/src/theme/` (69 components) | Swizzlable theme surface; MDXComponents/index.tsx global component mapping (incl. mermaid, admonition, Head); SiteMetadata (hreflang alternates); LocaleDropdownNavbarItem; EditThisPage; DocVersionBanner |
| `packages/docusaurus-theme-search-algolia/src/theme/` | First-party Algolia search UI (SearchBar, SearchPage, SearchTranslations); no local-search package exists in monorepo |
| `packages/docusaurus-theme-translations/locales/` | 36 locales incl. `hu`; HU coverage measured: theme-common.json 82/163 keys vs base |
| `packages/docusaurus/src/server/i18n.ts`, `packages/docusaurus-utils/src/i18nUtils.ts` | Locale resolution, Intl-based defaults, getPluginI18nPath filesystem layout |
| `packages/docusaurus/src/server/brokenLinks.ts` | Build-time broken link/anchor checking implementation |
| `packages/docusaurus/src/ssg/` (ssgExecutor.ts, ssgWorkerThread.ts, ssgEnv.ts) | SSG parallelization via tinypool worker_threads, worker recycling/memory notes, env tunables |
| `packages/docusaurus/src/commands/cli.ts` | CLI surface: build, swizzle, deploy, start, serve, clear, write-translations, write-heading-ids |
| `website/docusaurus.config.ts` | Dogfooding: future.v4 + faster with rspackBundler/rspackPersistentCache (~line 182-193); docs multi-instance `id: 'community'` (line 369); inline plugin definitions; DocSearch v3/v4 Ask AI config (~line 676-680); staging vs production locale sets |
| `.github/workflows/` (19 files) | CI battery: tests, tests-windows, tests-e2e, tests-swizzle, codeql-analysis, dependency-review, security-supply-chain, build-perf, lighthouse-report, argos, publish, continuous-releases |
| `LICENSE`, `LICENSE-docs` | MIT (code), CC-BY-4.0 (docs) |
| `README.md`, `CONTRIBUTING.md`, `AGENTS.md` | Positioning, contribution process, community links (Discord, Crowdin-based website localization) |
| Repo root (absence check) | No SECURITY.md present in clone |
| `git log -1` | HEAD 3f483e80e326, 2026-08-07, active dependency-bump traffic |


---

## REF-004 — mkdocs source log

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


---

## REF-005 — zensical source log

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


---

## REF-006 — hyperbook source log

# Sources — Hyperbook analysis (all accessed 2026-08-12)

## Repository (primary evidence base)

Cloned https://github.com/openpatch/hyperbook to /tmp/hyperbook (shallow, then history fetched with --filter=blob:none for contributor stats; HEAD dated 2026-08-11).

| Path | What it evidenced |
|---|---|
| README.md | Project purpose (interactive workbooks), package inventory, maintainer (Mike Barkmin / OpenPatch), Matrix community, no @hyperbook/toolkit package exists |
| LICENSE.md | MIT license, copyright Mike Barkmin 2021 |
| package.json, pnpm-workspace.yaml | pnpm monorepo, changesets release flow, website EN/DE diff script, no Next.js in current stack |
| packages/hyperbook/{index.ts,build.ts,dev.ts,incremental.ts,archive.ts} | CLI surface (new/dev/build), full static build to .hyperbook/out, lunr search index generation (build.ts:36-97), llms.txt generation (build.ts:283-412, 969-971), dev-only IncrementalBuilder with dependency tracking, WebSocket live reload (dev.ts:267-353), Node>=18 engines |
| packages/hyperbook/tests/incremental.test.ts | Incremental builder test coverage |
| packages/markdown/src/process.ts | Full remark/rehype pipeline; 40 directive plugins registered; shiki highlighting; KaTeX; allowDangerousHtml default false |
| packages/markdown/src/remarkDirective*.ts (40 files) | Verified element list: tabs, protect, mermaid, plantuml, excalidraw, geogebra, h5p, pyide, sqlide, webide, onlineide, multievent, textinput, learningmap, scratchblock, struktog, struktolab, blockflow, kirimoto, openscad, typst, abc-music, jsxgraph, alert, collapsible, slideshow, tiles, bookmarks, pagelist, term, qr, download, archive, embed, video, audio, youtube, unpack; no literal multiple-choice directive |
| packages/markdown/src/remarkDirectiveMermaid.ts | Dual mermaid syntax (fenced + directive), base64 payload, client-side render |
| packages/markdown/src/remarkDirectiveProtect.ts | protect = client-side gating; base64 password in data-toast; content in hidden div |
| packages/markdown/src/rehypeHtmlStructure.ts (lines ~200-280) | Emitted head metadata; verified defects: og:title uses value attr, keywords.join(""), html lang fallback "es", no canonical/sitemap/og:image |
| packages/markdown/src/i18n.ts + locales | UI i18n: only en.json and de.json bundles; English fallback |
| packages/markdown/assets/ | Per-directive JS/CSS assets incl. mermaid.min.js, lunr-adjacent search UI, store.js |
| packages/types/src/index.ts | hyperbook.json schema (search, llms, importExport, colors, fonts, scripts/styles, basePath, repo, cloud, elements config); Language union de|en|fr|es|it|pt|nl (no hu); frontmatter types incl. permaid, hide, virtual sections; HyperlibraryJson multi-book model |
| packages/fs/src/vfile.ts | Folder model (book/glossary/public/snippets/archives); .md.yml/.md.json data files requiring template; .md.hbs pages; dependency tracking for inlined snippets/templates; warning-only error handling (lines ~840-900) |
| packages/fs/src/handlebars.ts | ~20 Handlebars helpers (times, concat, case transforms, truncate, dateformat, rbase64, rfile...) |
| packages/create/package.json | create-hyperbook scaffolder |
| packages/web-component-excalidraw/package.json | React 19 web component packaged via r2wc — pattern for custom components via scripts |
| platforms/vscode/package.json | hyperbook-studio VS Code extension 0.54.0: activation, schema validation, snippets, preview |
| platforms/cloud/{README.md,Dockerfile,docker-compose.yml} | Optional self-hosted Express student-data backend, Docker/GHCR distribution — out of scope for target system |
| .github/workflows/changeset-version.yml | CI: changesets publish to npm, VS Code Marketplace + OpenVSX, GHCR cloud image; permissions surface |
| renovate.json | Automated dependency updates |
| website/hyperlibrary.json, website/en/**, website/de/** | Real EN/DE bilingual library config; docs corpus incl. elements/, hosting/{ghpages,glpages,vercel,custom}.md, advanced/ template demos |
| scripts/diffFolders.mjs (via package.json website:diff) | Translation drift detection pattern |
| git log/shortlog (full history) | First commit 2022-03-08; ~1010 human commits, 910+55 by maintainer, 2 external contributors x 1 commit; 220 commits in last 6 months |

## Web (secondary)

| URL | What it evidenced |
|---|---|
| https://github.com/openpatch/hyperbook (via web fetch) | Stars 74, forks 14, watchers 2, open issues 5, 1924 commits (2026-08-12) |
| https://github.com/openpatch/hyperbook/issues | 5 open issues, titles/dates incl. #350 OpenGraph Images (2022), #349 page/section password |
| https://registry.npmjs.org/hyperbook | Latest 0.104.0 published 2026-08-11T21:10Z; release timestamps showing 11 releases 2026-07-25..08-11 |
| https://hyperbook.openpatch.org/ | Official docs site (same content as website/ in repo; used for orientation) |
| https://github.com/openpatch/hyperbook-anywhere | Deployment starter template (search result; existence verified) |

Notes: GitHub REST API was blocked in this session; stars/forks/issues were observed via rendered pages and are marked [OBSERVED]. All code claims are [VERIFIED-REPO] from the local clone.
