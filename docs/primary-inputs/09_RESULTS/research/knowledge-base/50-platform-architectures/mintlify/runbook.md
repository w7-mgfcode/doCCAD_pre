# Operational Runbook — Mintlify (hosted plan)

Scope: operating the target ecosystem's docs on Mintlify's hosted platform with GitHub as canonical source. Backend internals are vendor-operated; this runbook covers everything the operator actually controls. Evidence: official docs (mintlify/docs repo, cloned 2026-08-12).

## 1. Install / Setup

### 1.1 Prerequisites
- Node.js v20.17.0+ (CLI requirement), a GitHub account/org, admin rights on the docs repo.
- Mintlify account (Starter is $0; Pro required for preview deployments, REST API, AI features).

### 1.2 Initial setup
1. Scaffold: copy `github.com/mintlify/starter` (MIT) or run onboarding; ensure the repo lives in YOUR org (avoid the Mintlify-hosted `mintlify-community` repo mode; if already there, use dashboard Git Settings → clone-out wizard).
2. Install the CLI: `npm i -g mint`. Verify with `mint --version`.
3. Local preview: `mint dev` in the directory containing `docs.json` (default http://localhost:3000).
4. Connect GitHub: dashboard → Git Settings → install the **Mintlify GitHub App**, scoped to *only* the docs repository. Requires org owner/admin approval.
5. Set the deployment branch (usually `main`); enable branch protection so all writes are PRs.
6. Custom domain: dashboard or `mint add-domain docs.example.com`; add the CNAME the dashboard shows. (Subpath hosting instead requires your own reverse proxy — more moving parts; prefer a subdomain.)
7. Configure `docs.json`: theme/colors/logo, navigation (use `$ref` splits), `seo`, `contextual.options`, `redirects`, `markdown.instructions`.
8. Add `.mintignore` for non-publishable files; add `.vale.ini` if using custom prose rules.
9. Pro only: enable CI checks (dashboard → Add-ons): broken links + Vale, choose Warning vs Blocking.
10. Generate an Admin API key (dashboard → API keys) for CI: store as GitHub Actions secret; set expiry; note keys are org-wide and server-side only.

### 1.3 Pipeline wiring (ecosystem-specific)
- PR validation Action: `npx mint validate` + `npx mint broken-links`.
- Derivation/translation Actions open PRs; previews build automatically for PRs against the deploy branch (Pro).
- Optional: `POST /api (update trigger)` after out-of-band spec changes; `preview/trigger` for custom branch previews.

## 2. Routine operations

| Task | How | Frequency |
|---|---|---|
| Publish content | Merge PR to deploy branch; App webhook triggers build | continuous |
| Verify deploy | Dashboard deployment status, or `GET update/status` API | per merge |
| Stuck deploy | Dashboard → manual "deploy" button (documented recovery for missed webhooks) | as needed |
| Review AI-derived PRs | GitHub PR + automatic preview URL + preview widget (changed-pages list) | per PR |
| Search tuning | Adjust `boost`/`searchable` frontmatter; monitor via search analytics API (Pro) | monthly |
| llms.txt / skill.md | Auto-generated; spot-check `/llms.txt`, `/skill.md` after large restructures (skill.md regeneration can take up to 24h) | after restructures |
| Archive mirror | Scheduled Action fetches `llms-full.txt`, `sitemap.xml`, all `.md` pages to `archive/` branch | weekly |
| EN/HU parity | Parity CI (file diff + staleness hashes) on every merge; translation PRs reviewed like any other | continuous |
| Credit usage (if Pro AI used) | Dashboard → Usage page; set/disable overages | monthly |
| Changelog watch | Subscribe to docs changelog RSS (`changelog.mdx` has `rss: true`) — platform changes are continuous and unversioned | weekly |

## 3. Upgrade

- **Platform:** vendor-managed, continuous, no operator action and no pinning on hosted plans. Risk handling: changelog RSS review + weekly fallback-SSG build as rendering canary + CI smoke test (fetch a few pages, assert key strings/status 200).
- **CLI:** `npm i -g mint@latest` in dev machines and pinned-with-renovate in CI. CLI versions update near-daily (npm shows same-day releases); pin in CI, refresh weekly.
- **docs.json schema:** validated against `https://mintlify.com/docs.json` schema; `mint validate` in CI catches breakage before merge. Legacy note: `mint.json` is deprecated in favor of `docs.json`; upgrade path documented (`organize/settings.mdx`).

## 4. Backup / Restore

**What Git covers (complete, canonical):** all MDX content, `docs.json` and `$ref` fragments, snippets, OpenAPI specs, images committed to the repo, `.mintignore`, `.vale.ini`, redirects. Restore = `git revert`/`git push` → automatic rebuild. Full-site rollback = revert the merge commit and push.

**What Git does NOT cover (dashboard/platform state) — record in an `ops/dashboard-state.md` file after every change:**
- Custom domain settings, Git connection/App installation, deployment branch choice.
- CI check add-on configuration (levels, enabled checks).
- API keys (recreate; never backed up by design).
- Authentication settings (passwords, OAuth/JWT config), MCP enablement for authed sites.
- Analytics history, assistant conversations, feedback data → export periodically via analytics REST API (Pro) if valued.
- Preview deployment history (ephemeral; recreate on demand).

**Disaster cases:**
- *Accidental deployment deletion:* irreversible (documented); recreate deployment, reconnect repo, replay `ops/dashboard-state.md`, re-add domain. Content is intact in Git.
- *Vendor unavailable:* serve the weekly fallback-SSG build; DNS cutover per §7.

## 5. Common failures + recovery

| Symptom | Likely cause | Recovery |
|---|---|---|
| Push merged but site unchanged | GitHub App missing/suspended on the repo, or webhook missed | Check Git Settings App status; reinstall if needed; dashboard manual deploy |
| Build fails | Invalid `docs.json`, broken MDX, OpenAPI URL unreachable during build (documented help-center case) | Run `mint validate`/`mint dev` locally to reproduce; for remote OpenAPI URLs, vendor docs suggest checking accessibility or vendoring the spec file into the repo |
| PR shows no preview | PR from a fork (previews intentionally unsupported), or not targeting deploy branch, or not on Pro | Push branch to main repo; retarget PR; verify plan |
| Broken-links check fails on links to ignored files | Links point at `.mintignore`d pages (documented behavior) | Remove links or un-ignore |
| Mermaid diagram renders poorly | Large diagram, default layout | Add ELK init directive; use zoom/pan controls default placement |
| Hungarian page 404s from switcher | `hu` tree missing that file, or path duplicated across languages | Parity CI should have caught it; add translation or temporarily drop page from `hu` navigation fragment |
| Search returns hidden/derived pages | `seo.indexing: "all"` set, or missing `searchable: false` | Fix frontmatter class defaults per ADR-002 |
| API 401/403 | Expired admin key (default 90-day expiry) | Rotate key; update CI secret; note 10 keys/hour org cap |
| Editor commit conflicts | Parallel branch edits | Normal Git resolution; editor supports branches — prefer branch-per-change |

## 6. Monitoring signals

- Deployment success/failure: dashboard + `GET update/status` (poll after CI-triggered updates).
- CI check outcomes on PRs (blocking gates).
- Uptime of the published site: external synthetic check on `/` and `/llms.txt` (also validates the AI surface).
- Search and traffic analytics via REST API (Pro): views, visitors, searches, feedback-by-page — watch for search-zero-result growth after restructures.
- Credit balance/overage state (only if Mintlify AI features are enabled).
- Fallback-SSG weekly build status (canary for MDX portability regressions).

## 7. Security ops

- **Least privilege:** GitHub App on the docs repo only; branch protection on deploy branch (also forces Mintlify's agent into PR mode — documented behavior).
- **Keys:** admin API keys server-side only, with expiry; rotate on personnel/tooling change; assistant keys are deployment-scoped.
- **Content injection review:** treat `docs.json` `integrations`/custom-scripts changes as security-sensitive PRs (sitewide JS execution); configure CSP per `deploy/csp-configuration.mdx`.
- **Admin MCP:** keep disconnected unless actively used; scope to one deployment; review every PR it opens.
- **Hidden pages are public-by-URL** — never park sensitive drafts there; use unmerged branches or `.mintignore`.
- **Exports:** `mint export --groups` bundles restricted pages unauthenticated (Enterprise feature) — control distribution.
- **DNS cutover drill (annual):** point the docs domain at the fallback host, confirm read-only service, revert. Document TTLs.
- Plan-tier note: dashboard SSO/RBAC/audit logs are Enterprise-only; on Starter/Pro, restrict dashboard membership to the operating engineer and use strong auth on the account.
