---
id: framework-maintenance-risk-assessment
title: Maintenance Risk Assessment — Judging Repo Health and Successor Dynamics
type: knowledge
category: decision-frameworks
tags: [repo-health, maintenance, bus-factor, eol, oss-risk]
sources:
  - outputs/01_products/mkdocs/repo_health.json
  - outputs/01_products/zensical/repo_health.json
  - outputs/01_products/docusaurus/repo_health.json
  - outputs/02_comparison/comparison.md ("MkDocs ecosystem in transition")
  - outputs/01_products/mkdocs/ADRs/adr-001-adopt-mkdocs-material-pinned-with-exit-plan.md
confidence: HIGH
related: [framework-build-vs-buy-vs-host, framework-weighted-decision-model, practice-evidence-discipline, framework-anti-overengineering-rules]
---

# Maintenance Risk Assessment — Judging Repo Health and Successor Dynamics

**Summary** — An OSS dependency's biggest risk is rarely its code; it is whether anyone will be maintaining it in two years. The corpus assessed this with a structured repo-health probe — release cadence, commit activity, contributor concentration (bus factor), security-support windows, and successor dynamics — collected per platform into `repo_health.json` with evidence tags. The MkDocs / Material / Zensical triangle is the case study: three healthy-looking projects whose combined signals produced a "conditional fallback only, with a dated exit" verdict that swung the platform decision.

## Core Logic

**Signals collected per project** (each with collection date and evidence provenance):

1. **Release cadence** — dates, not counts. MkDocs core: last release 2024-08-30, ~24 months stale at assessment. Docusaurus: steady minors (3.7.0 → 3.10.2 across 18 months) plus continuous canaries. Zensical: six releases in one month — fast, but alpha.
2. **Commit activity, qualified** — *what kind* of commits. Material was "active through 2026-08-09" yet the log shows only dependency bumps, security fixes, docs, and an EOL notice; last *feature* release a year prior. Activity without features is maintenance mode, whatever the commit graph looks like.
3. **Bus factor / contributor concentration** — MkDocs: historic maintainers stepped away (named, with years); community PRs sit unreviewed. Zensical: of the last 50 commits, two people dominate (~2 core devs). Even Docusaurus, with Meta backing and a large long-tail, gets "main risk: maintainer concentration" recorded honestly.
4. **Security-support windows** — the hardest signal available: Material's SECURITY.md declares public security support ends **2026-11-05** [VERIFIED-REPO] — a contractual-quality fact. Zensical's policy is latest-version-only fixes; MkDocs core has "unbounded response time to future CVEs."
5. **Successor dynamics** — Material's team announced Zensical and redirected effort to it; the successor is technically promising but pre-1.0, no plugin API, no multi-language content [VERIFIED-REPO @ v0.0.53]. A successor announcement is simultaneously a death notice for the predecessor and an immaturity notice for the replacement: "adopting either today means either a dated exit plan (MkDocs) or alpha churn (Zensical)."
6. **Ecosystem health separately** — satellite plugins (gen-files, mike, static-i18n, macros) were checked independently and found healthy; a dormant core can have a live ecosystem, and vice versa.

**Composite verdicts, with dates and triggers.** The signals compose into actionable decisions, not scores alone: MkDocs+Material — "adopt only version-pinned with a dated exit plan" before 2026-11-05; Zensical — "watch; revisit at 1.0 + plugin API + multi-language content" (the trigger is recorded in ADR-002 of the solution so it survives the decision). In the weighted model, this evidence forbade ignoring MkDocs' risk: "For MkDocs to overtake, its maintenance risk would have to be ignored, which the evidence forbids."

## Best Practices

1. **Read SECURITY.md and release dates before stars**, because a support-EOL date is verifiable and binding while popularity is a lagging indicator (MkDocs has 22k stars and a dormant core).
2. **Qualify activity by content** — features vs bumps vs docs — because maintenance-mode projects look alive in commit graphs.
3. **Count effective maintainers, not historical contributors**, because 367 all-time contributors can coexist with a bus factor of one.
4. **Turn risk into a dated exit or revisit trigger**, because "risky" is not actionable; "exit before 2026-11-05" and "revisit at 1.0 + plugin API" are.
5. **Record how each figure was obtained** — the repo_health files note that the GitHub API was blocked, so stars are page-displayed values — because evidence honesty (practice-evidence-discipline) applies to health data too.
6. **Assess the successor as its own candidate**, because inheriting the predecessor's community does not confer the predecessor's maturity.

## Pitfalls

- **Dormancy is not death, but it prices in**: MkDocs is functional and widely deployed; the risk is unbounded CVE response, which matters precisely because the platform sits in the build path.
- **Alpha velocity reads as health**: Zensical's weekly releases are genuine progress *and* upgrade churn with latest-only security fixes — both facts belong in the verdict.
- **Vendor-backed ≠ safe**: Docusaurus' Meta backing coexists with a named lead-maintainer concentration risk; record it even for the winner.
- **Checking the core but not the plugins** (or the reverse): the decision depended on the whole assembly — core, theme, and satellites — evaluated separately.

## Expert Notes

The transferable method is *falsifiable pessimism*: every risk claim is tied to a dated, cited artifact (a SECURITY.md line, a release timestamp, a shortlog count) so an optimist can check it and a future reader can re-run it. Note also how maintenance risk interacts with the other frameworks: it is the "host" column's counterpart to vendor lock-in (framework-build-vs-buy-vs-host), and it enters the weighted model not as a criterion but as evidence constraining scores and verdicts — which is why the 83.8-scoring "simplest architecture in the field" still could not win.

## Evidence & Further Reading

- `outputs/01_products/mkdocs/repo_health.json` — the richest example: dual-repo signals, named maintainer departures, composite verdict.
- `outputs/01_products/zensical/repo_health.json`, `outputs/01_products/docusaurus/repo_health.json` — successor and winner assessments.
- `outputs/02_comparison/comparison.md` — "The MkDocs ecosystem is in transition" synthesis; `outputs/02_comparison/decision_matrix.md` — how the evidence bound the decision.
- `outputs/01_products/mkdocs/ADRs/adr-001-adopt-mkdocs-material-pinned-with-exit-plan.md` — risk converted into an adoption contract.
