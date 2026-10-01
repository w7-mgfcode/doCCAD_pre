---
id: validation-quality-gates
slug: /validation/quality-gates
title: Deterministic CI Quality Gates
type: canonical
visibility: public
audience: [developer, operator, architect]
owners: [core]
sources: [scripts/validate_docs.py, .github/workflows/docs-validate.yml]
related: [validation-drift-detection, generation-pipeline-lifecycle]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Deterministic CI Quality Gates

<!-- Archive mapping: Adapted from 05_DOCUMENTATION_DESIGN/documentation-process/automation_architecture.md §3 -->

In DOCCAD, all verification gates are **deterministic-first** (AD-10). Automated AI-evaluating-AI checks are advisory at best; only mechanical, provable tests can block a pull request.

## The CI Validation Pipeline

When a PR is opened or updated, `scripts/validate_docs.py` runs the following sequential checks:

```
+-------------------------------------------------------------+
| 1. Frontmatter Schema Check (document.schema.json)           |
+-------------------------------------------------------------+
                              | PASS
+-------------------------------------------------------------+
| 2. Plane Boundary Integrity (/docs vs /views segregation)   |
+-------------------------------------------------------------+
                              | PASS
+-------------------------------------------------------------+
| 3. Unique Document ID Check                                 |
+-------------------------------------------------------------+
                              | PASS
+-------------------------------------------------------------+
| 4. Interview Dataset Validation (interview.schema.json)     |
+-------------------------------------------------------------+
                              | PASS
+-------------------------------------------------------------+
| 5. Provenance Hash Verification (sha256 matches disk)       |
+-------------------------------------------------------------+
                              | PASS
+-------------------------------------------------------------+
| 6. Path Traversal & Containment Check                       |
+-------------------------------------------------------------+
                              | PASS
+-------------------------------------------------------------+
| 7. Safe MDX Inspection (no raw script tags / eval)          |
+-------------------------------------------------------------+
                              | PASS
+-------------------------------------------------------------+
| 8. Docusaurus Build & Broken Link Gate (onBrokenLinks: throw)|
+-------------------------------------------------------------+
```

## Failure Consequences
- Any gate failure exits with code `1` and prints the offending file, line number, and rule violation.
- In GitHub Actions, a failing gate blocks branch merging via protected branch rules.
