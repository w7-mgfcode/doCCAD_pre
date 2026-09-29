---
id: validation-drift-detection
slug: /validation/drift-detection
title: Hash-Based Drift Detection & Targeted Regeneration
type: canonical
audience: [developer, architect, operator]
owners: [architecture]
sources: [scripts/detect_changes.py, .docs-manifest.json]
related: [validation-quality-gates, operations-runbook-stale-views]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# Hash-Based Drift Detection & Targeted Regeneration

<!-- Archive mapping: Adapted from 05_DOCUMENTATION_DESIGN/documentation-process/automation_architecture.md §2 and ADR-008 -->

Software documentation inevitably drifts as systems evolve. DOCCAD uses **mechanical content hashing** to detect drift automatically without requiring engineers to manually track every downstream derived view.

## How Content Hashing Works

1. When a derived page is generated (e.g. `docs/generated/recruiter/project-overview.mdx`), the generator computes the `sha256` hash of every canonical file consulted:
   ```yaml
   generation:
     source_documents:
       - id: architecture-system-overview
         path: docs/source/architecture/system-overview.md
         content_hash: sha256:e3b0c44...
   ```
2. When a pull request edits `docs/source/architecture/system-overview.md`, its byte sequence changes, resulting in a new `sha256` digest.
3. CI runs `scripts/detect_changes.py --all` to compare on-disk hashes against the recorded hashes in each derived page.
4. If a hash mismatch is detected, the page is flagged `STALE` in `impact.json`.

## Targeted vs Full-Corpus Regeneration

Full-corpus regeneration on every commit is expensive, wasteful, and noisy. DOCCAD adheres to the **Incrementality Rule**:
- Only the specific derived pages flagged as stale in `impact.json` are scheduled for regeneration.
- Unaffected derived views remain untouched, preserving stable Git history and minimizing AI compute costs.
- Full-corpus regeneration exists solely as an explicit manual trigger (`workflow_dispatch` with `confirm: all`).
