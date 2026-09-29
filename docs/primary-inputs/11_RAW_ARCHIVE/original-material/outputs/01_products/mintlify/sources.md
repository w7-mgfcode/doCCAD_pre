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
