# Operational Runbook — Hyperbook

Scope: operating a Hyperbook-based bilingual (EN/HU) documentation site with AI-derived content, run by one engineer. All paths cited were verified in the openpatch/hyperbook repository on 2026-08-12.

## 1. Install / Setup

Prerequisites: Node.js >= 18 (verified: packages/hyperbook/package.json engines), git. pnpm is only needed if building Hyperbook itself from source; consumers use npm/npx.

Initial project setup:

```bash
# scaffold (interactive)
npx create-hyperbook@latest
# or
npx hyperbook@0.104.0 new my-docs
```

Recommended repo layout (mirrors upstream website/):

```
hyperlibrary.json          # {"library":[{"src":"en","basePath":"/"},{"src":"hu","basePath":"hu"}]}
en/hyperbook.json          # name, language: "en", search: true, llms: true
en/book/ ...               # canonical + derived pages
en/glossary/  en/public/  en/snippets/  en/templates/  en/archives/
hu/...                     # mirrored tree
scripts/harden.mjs         # post-build SEO/guard script (ADR-004)
.github/workflows/deploy.yml
```

Pin the CLI: commit a `package.json` with `"hyperbook": "0.104.0"` (exact) and a lockfile; vendor the tarball (`npm pack hyperbook@0.104.0`) into release storage (ADR-001).

Local dev:

```bash
npx hyperbook dev          # dev server, WebSocket live reload, incremental rebuilds
npx hyperbook build        # full static build -> .hyperbook/out (library) / out dir
```

Editor: install the "Hyperbook" VS Code extension (publisher openpatch) for preview with the production renderer, snippets, and hyperbook.json schema validation.

CI (GitHub Pages sketch):

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-node@v4        # node 20+
- run: npm ci
- run: npx hyperbook build 2>&1 | tee build.log
- run: node scripts/harden.mjs .hyperbook/out build.log   # fails on warnings/page-count drift
- uses: actions/upload-pages-artifact@v3
- uses: actions/deploy-pages@v4
```

Set `basePath` in hyperbook.json when hosting under a subpath (project Pages).

## 2. Routine Operations

- **Content change**: branch → edit `.md` (canonical) or merge AI PR of `.md.yml` (derived) → PR checks (schema validation, secret scan, build) → merge → CI rebuilds and deploys. Full rebuild each time; incremental builds exist only in the dev server (packages/hyperbook/incremental.ts), not in `hyperbook build`.
- **Adding a derived page type**: add `templates/<type>.md.hbs` + JSON Schema + CI validation entry; document the data contract for the AI layer (ADR-002).
- **Translation sync**: CI drift job compares `en/` vs `hu/` trees (pattern: upstream scripts/diffFolders.mjs); triage weekly.
- **Search/llms**: `"search": true` and `"llms": true` in hyperbook.json regenerate `search.js` and `llms.txt` on every build automatically — no separate ops.
- **Glossary**: add terms under `glossary/`; reference with `:t[Term]` in content.

## 3. Upgrade

Quarterly, or out-of-band for critical fixes:

1. Read CHANGELOGs of `hyperbook`, `@hyperbook/markdown`, `@hyperbook/fs` (per-package CHANGELOG.md, changesets-generated).
2. Bump pinned version in a branch; `npm ci`; build the smoke-test book that exercises every directive/config feature in use.
3. Visual diff of rendered smoke pages (manual or Playwright screenshots); verify `scripts/harden.mjs` still matches the emitted HTML head structure (upgrade is the moment it can break).
4. Re-vendor the new tarball; merge.

Rollback: revert the version-bump commit; CI rebuilds with the previous pinned version. Because output is fully static, the previously deployed artifact also remains valid — redeploy it directly if a bad build shipped.

## 4. Backup / Restore

**What Git covers (everything canonical):** all content, config, templates, snippets, public assets, CI workflows, the pinned generator version, and the harden script. A clone is a complete restore of the system of record.

**What Git does not cover:**
- The published artifact (rebuildable; optionally retain the last N Pages artifacts / `out/` archives for instant rollback without rebuilding).
- The vendored hyperbook tarballs if stored outside the repo — keep them in at least two locations (repo LFS or release assets + local).
- GitHub repo settings (branch protection, CODEOWNERS enforcement flags, Pages config, Actions secrets) — export/record them in a `docs/ops/settings.md`; there are no other secrets in this architecture.
- Reader-side state: bookmarks/protect-unlocks/textinput answers live in browser localStorage (import/export feature is user-facing, config `importExport`); by design nothing server-side to back up.

Restore drill (annually): fresh clone on a clean machine → `npm ci` → `npx hyperbook build` → serve `out/` locally → spot-check EN and HU books, search, one Mermaid page.

## 5. Common Failures + Recovery

| Symptom | Cause | Recovery |
|---|---|---|
| Page silently missing from site | `.md.yml` missing `template` key or template file absent — build logs a warning and continues (packages/fs/src/vfile.ts) | harden.mjs fails CI on log warnings/page-count drift; fix the data file or template |
| Build fails after dependency update | unpinned transitive or Node version change | restore lockfile/pinned version; rebuild |
| Directive renders as literal `:::name` text | typo in directive name or unsupported nesting; directives are compiled-in, no user registration | check spelling against packages/markdown/src/remarkDirective*.ts list; validate in VS Code preview |
| Mermaid diagram shows raw text | client JS blocked or mermaid asset missing from output (only shipped when directive detected) | confirm `directive-mermaid` assets in output; check browser console; ensure fenced block has `mermaid` language tag |
| Search returns nothing / stale | `search: false`, or search.js not redeployed | verify config; confirm search.js timestamp in output |
| Wrong links under subpath hosting | `basePath` missing/misconfigured | set `basePath` in hyperbook.json; rebuild |
| HU book shows German/English UI strings | expected: no `hu` locale upstream (packages/markdown/src/i18n.ts has en/de only) | post-build string patch (ADR-003) until upstream PR lands |
| lunr warns language invalid | configured language has no bundled lunr plugin — falls back to English (build.ts:62) | accept for HU, or ship custom stemmer via fork; cosmetic otherwise |
| `og:` previews broken on social/ATS | upstream og:title `value` attr bug; no og:image | harden.mjs rewrites meta tags (ADR-004) |
| npm install of pinned version fails (unpublished/compromised) | upstream supply-chain event | install from vendored tarball; initiate fork-readiness assessment |

## 6. Monitoring Signals

Minimal by design; watch:
- CI: build success, build duration trend, harden.mjs assertions (page count vs manifest, zero warnings, search.js size budget, sitemap present).
- Host: Pages/host uptime (external uptime check on `/` and `/hu/`), HTTP 404 rate if host exposes logs.
- Content: weekly translation-drift report; link checker (e.g., lychee) over `out/` in a scheduled workflow.
- Upstream: release feed of openpatch/hyperbook (watch releases only), open-issue spike, and a "6 months without commits" tripwire that triggers the fork-readiness decision (ADR-001).

## 7. Security Ops

- Keep `allowDangerousHtml: false`; PR linter enforces a directive whitelist on derived content (mdast parse via @hyperbook/fs).
- gitleaks (or equivalent) on every PR — AI-generated branches included (ADR-005).
- Never treat `protect` as access control — content and base64 password are in the served HTML (remarkDirectiveProtect.ts); policy: repo is public-equivalent.
- Dependabot/Renovate on the consumer repo for the pinned hyperbook version advisories; review upstream changelog for security notes at each upgrade window.
- GitHub org hygiene: branch protection on main, required checks, CODEOWNERS separating `*/book/` canonical vs derived dirs, Actions pinned by SHA, least-privilege workflow permissions (upstream's own workflow needs contents+packages write; yours needs only pages).
- No runtime security surface exists (static site); the optional Hyperbook Cloud backend is explicitly out of scope and not deployed.
