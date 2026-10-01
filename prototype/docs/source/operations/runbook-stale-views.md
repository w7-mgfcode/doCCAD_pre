---
id: operations-runbook-stale-views
slug: /operations/runbook-stale-views
title: "Runbook: Detecting & Resolving Stale Views"
type: canonical
visibility: public
audience: [operator, developer]
owners: [operations]
sources: [scripts/detect_changes.py, scripts/generate_page.py]
related: [validation-drift-detection, troubleshooting-generation-failures]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Runbook: Detecting & Resolving Stale Views

<!-- Archive mapping: Adapted from 05_DOCUMENTATION_DESIGN/documentation-process/automation_architecture.md §2 -->

This operational runbook explains how to diagnose, identify, and resolve stale derived views when canonical documentation or code sources are updated.

## Symptom

CI reports a drift warning or `scripts/validate_docs.py` fails with:
```
FAIL — 1 violation(s) (1 stale):
  - docs/generated/recruiter/project-overview.mdx: STALE — hash mismatch for
    docs/source/architecture/system-overview.md
    recorded sha256:4f8a...
    actual   sha256:7b2e...
```

## Diagnosis Procedure

Run the drift detection script in full scan mode:

```bash
python3 scripts/detect_changes.py --all
```

Review the printed regeneration plan in `impact.json`. It will indicate which canonical file changed and which contract-target pairs require regeneration:
```json
{
  "stale_generated": [
    {
      "id": "recruiter-project-overview",
      "path": "docs/generated/recruiter/project-overview.mdx",
      "contract": "GenerateRecruiterPage"
    }
  ]
}
```

## Remediation Procedure

Execute targeted regeneration using the command suggested in `impact.json`:

```bash
python3 scripts/generate_page.py \
  --contract GenerateRecruiterPage \
  --target architecture-system-overview
```

After regeneration, verify that provenance hashes match on disk:

```bash
python3 scripts/validate_docs.py
```

Commit the regenerated artifact in a pull request. Once merged, the staleness warning is resolved.
