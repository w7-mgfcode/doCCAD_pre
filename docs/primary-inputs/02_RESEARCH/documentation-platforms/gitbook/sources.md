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
