# Operational Runbook — GitBook (SaaS) as publishing tier

Scope: operating GitBook as the presentation layer of a GitHub-canonical docs ecosystem, one-way
Git→GitBook discipline (ADR-001). Platform internals are managed by GitBook; this runbook covers the
surface you own. All claims from official docs (gitbook.com/docs, accessed 2026-08-12) unless noted.

## 1. Install / Setup

There is nothing to install server-side. Setup is configuration:

1. Create org + site in app.gitbook.com; add sections/variants (EN default, HU variant per ADR-003).
2. Repo layout (monorepo project directories):
   - `docs/en/.gitbook.yaml`, `docs/en/README.md`, `docs/en/SUMMARY.md`, `docs/en/.gitbook/assets/`
   - `docs/hu/...` (same shape; assets duplicated — not shared across project directories)
   - `.gitbook.yaml` minimum: `root: ./` plus `structure.readme` / `structure.summary` if non-default;
     `redirects:` map old paths to `page.md` paths (no leading slashes).
3. Enable Git Sync per section: section header → Set up → GitHub Sync → install the GitBook GitHub
   App **scoped to the docs repo only** → pick repo + branch (`main`) → set Project directory
   (`docs/en` / `docs/hu`) → choose initial direction **GitHub → GitBook**.
   Note: enabling sync locks live edits; app changes would go through change requests — policy: none.
4. Roles: operator = Admin; everyone else Reader or uninvited. (Commenter/Reviewer need paid plans.)
5. Protected branch: allow the documented `gitbook-com` bypass only if app-side commits are ever
   expected; under ADR-001 do NOT grant bypass — sync export is unused.
6. Publish the site (Publish button); sites are public by default — confirm Audience setting.
7. Custom domain (Premium+): Settings → configure domain, add DNS record, verify HTTPS.
8. SEO: verify `/sitemap-pages.xml`, submit to Google Search Console.
9. LLM surfaces sanity check: `<site>/llms.txt`, any page + `.md`, `<site>/~gitbook/mcp`.
10. CLI for the operator: `npm i -g @gitbook/cli` (Node ≥18); `gitbook login` interactively or
    `gitbook auth --token <PAT>` in CI.

## 2. Routine operations

- **Content change (human or AI pipeline)**: PR to `main` touching `docs/**` → GitBook status check
  posts a per-PR preview URL (requires published site; viewer needs a GitBook account; fork PRs get
  no preview by default) → review → merge → sync imports the commit automatically.
- **New page**: file must be added to the corresponding `SUMMARY.md` in the same PR — unlisted files
  do not sync.
- **Renames/moves**: add a `redirects:` entry in `.gitbook.yaml`; old page must be deleted for the
  redirect to activate; GitBook also auto-301s app-side moves.
- **Weekly**: review GitBook changelog (changelog.gitbook.com) for behavior changes; check watchdog
  CI is green; check fallback build (ADR-004) is green.
- **Monthly**: API snapshot of app-side config (site settings, customization, redirects, roles,
  domains) via REST API into the repo (`ops/gitbook-config-snapshot.json`).

## 3. Upgrade

No platform upgrades exist for you to run (continuous SaaS). Upgrade surface you own:
- `@gitbook/cli` version in CI (pin, bump monthly).
- GitBook GitHub App permission changes — review when GitHub prompts.
- Watch changelog for Git Sync or Markdown-syntax changes; run the round-trip fidelity test
  (Section 6, F5) after any announced sync change.

## 4. Backup / Restore

**What Git covers (complete):** all page content as Markdown, `SUMMARY.md` structure, assets,
`.gitbook.yaml` config, redirects defined in-file, full history. This is the primary backup — no
extra job needed beyond normal repo protection.

**What Git does NOT cover:** app-side site settings (audience, customization/branding, in-app
redirects, custom domain binding), org membership/roles, variants/sections structure metadata,
analytics history, change-request history, GitBook version history. Cover via the monthly API
snapshot; domains and roles are also documented in the runbook repo for manual re-creation.

**Restore scenarios:**
- Bad content merged → revert the Git commit; sync re-imports the revert. (App-side rollback via
  Version history exists but violates ADR-001; use Git.)
- Section corrupted/sync wedged → disable Git Sync, re-enable with GitHub → GitBook initial
  direction to force a clean re-import from the repo.
- Site deleted → recreate site/sections from snapshot doc, re-enable sync (content restores from
  repo), re-bind domain, re-publish.

## 5. Common failures + recovery (per official troubleshooting)

| Failure | Symptom | Recovery |
|---|---|---|
| Import didn't run after merge | Site not updated | Push a trivial commit to re-trigger import |
| Export (app→Git) failed | Change request merged, no commit | Merge a small new change request to re-trigger full export (should not occur under ADR-001) |
| Sync installation broken | Persistent sync errors | Remove and reinstall the Git Sync integration |
| Duplicate README files | Two readme files in repo | Manage README only in Git; delete duplicates; never create readmes in UI |
| Frontmatter invalid | Page renders wrong / import issues | Lint YAML (whitespace/indentation); CI yamllint on `docs/**` |
| New page missing on site | File merged but absent | Check it is listed in `SUMMARY.md` |
| Redirect not firing | Old URL 404s | Remove leading slash in redirect key; ensure old page deleted |
| PR preview absent | No status check | Fork PR (default-off), unpublished site, or authenticated-access site |
| Protected branch blocks sync commits | Export errors | Grant `gitbook-com` bypass (only if bidirectional mode is ever enabled) |

## 6. Monitoring signals

- **F1 Sync freshness watchdog (CI, hourly or post-merge)**: compare repo HEAD SHA/timestamp vs the
  site's latest revision via REST API; alert if lag > 15 min. (No official failure webhook is
  documented.)
- **F2 Uptime**: external HTTP check on the published site + `/sitemap-pages.xml`.
- **F3 Policy guard**: alert on any commit to `main` matching `GITBOOK-*` (app-side edit occurred).
- **F4 Link/summary integrity**: CI checks every `docs/**/*.md` is referenced by a `SUMMARY.md` and
  internal links resolve.
- **F5 Round-trip fidelity probe (weekly)**: canary file with representative syntax + frontmatter;
  verify byte-stability across sync cycles.
- **F6 Search Console**: coverage/indexing regressions on the custom domain.

## 7. Security operations

- 2FA/SSO on the operator account; a second break-glass Admin stored offline.
- GitBook GitHub App restricted to the docs repo; review installation quarterly.
- PATs: created in developer settings, user-scoped — store in CI secrets, rotate quarterly, never in
  repo.
- Keep fork-PR previews disabled (default) — prevents malicious preview content under your domain.
- Audience review monthly: site must remain Public-by-intent; remember hidden pages are exposed via
  `llms-full.txt` and the site MCP server — never sync semi-confidential drafts.
- Enterprise-only: Git Sync IP allowlisting (published egress IPs) — not applicable at Premium tier.
- Incident: suspected account compromise → revoke sessions/PATs, uninstall GitHub App, site to
  private share-link mode, then investigate `GITBOOK-*` commits and app audit trail.
