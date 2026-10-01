---
id: operations-monitoring-and-metrics
slug: /operations/monitoring-and-metrics
title: Operational Freshness & Drift Metrics
type: canonical
visibility: public
audience: [operator, architect]
owners: [operations]
sources: [.docs-manifest.json, impact.json]
related: [validation-drift-detection, operations-runbook-stale-views]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Operational Freshness & Drift Metrics

<!-- Archive mapping: Adapted from 05_DOCUMENTATION_DESIGN/documentation-process/automation_architecture.md §2 -->

Maintaining high documentation fidelity requires continuous measurement of repository freshness, drift ratios, and validation health.

## Core Operational Metrics

1. **Staleness Ratio**: The percentage of derived pages whose recorded `content_hash` mismatches the current on-disk canonical hash.
   ```text
   Staleness Ratio = (Count of Stale Derived Pages / Total Derived Pages) * 100%
   ```
2. **Canonical Coverage**: The ratio of canonical documents that have opted into automated derivation (`ai_generation.allowed: true`).
3. **Validation Pass Rate**: The percentage of CI validation runs that pass without schema, link, or hash violations.

## Automated Weekly Health Sweeps

Scheduled GitHub Actions workflows execute `scripts/detect_changes.py --all` weekly:
- Generates an updated `impact.json` report.
- Opens or updates an advisory GitHub issue summarizing any un-reconciled stale views.
- Triggers automated draft PRs for derived views whose contracts permit automatic maintenance.
