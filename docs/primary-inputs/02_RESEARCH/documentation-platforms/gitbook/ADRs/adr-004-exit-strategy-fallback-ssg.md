# ADR-004: Maintain a rehearsed exit path to a self-hostable static site generator

## Status
Proposed

## Context
GitBook's platform is proprietary SaaS with no self-hosting option [VERIFIED-OFFICIAL]. The only
open-source component is the GPLv3 published-site renderer, which renders content fetched from
api.gitbook.com and is not an offline generator [VERIFIED-REPO]. GitBook has previously deprecated
an entire toolchain (the legacy open-source GitBook, now marked deprecated in the current repo's
README) [HISTORICAL — used only as a risk prior]. The ecosystem's hard requirements include provider
independence and static-first serving. Mitigating asset: with Git Sync, the full content set already
lives in GitHub as Markdown + `SUMMARY.md` + `.gitbook.yaml` [VERIFIED-OFFICIAL].

## Decision
Keep a continuously-green fallback build in CI: a scripted converter transforms the repo
(`SUMMARY.md` → nav config; GitBook syntax `{% hint %}`, `{% tabs %}` → fallback-SSG equivalents;
fenced mermaid passes through) and builds the site with a self-hostable SSG. The fallback build runs
weekly and on converter changes; artifacts are retained. Custom domain DNS is documented so cutover
is a TTL away.

## Consequences
- Exit cost is bounded and measured (CI proves the conversion works today, not hypothetically).
- Small ongoing cost: the converter must track any new GitBook syntax the pipeline emits — bounded
  by ADR-005's restricted block palette.
- App-side configuration (redirects, customization, roles, domains) is not in Git; a monthly API
  export job snapshots it for the exit runbook.

## Alternatives
- **No exit rehearsal**: cheapest; rejected — concentrates vendor risk against a hard requirement.
- **Self-host the GPLv3 renderer**: rejected as an exit path — it still depends on the GitBook API,
  so it does not remove the vendor.
- **Dual-publish continuously**: rejected — permanent double maintenance violates
  anti-overengineering; a rehearsed cold standby suffices.
