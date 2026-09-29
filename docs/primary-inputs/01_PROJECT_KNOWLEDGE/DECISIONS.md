# Decision Register  [EXPLICIT — all decisions have artifact evidence]

Canonical decision documents live in 04_ARCHITECTURE/ADR/ and 04_ARCHITECTURE/architecture-decisions/.

| ID | Decision | Evidence artifact |
|---|---|---|
| DEC-001 | Docusaurus 3.x selected as publishing foundation (88.6/100); Mintlify raw runner-up rejected on provider-independence; MkDocs constraint-adjusted fallback with dated exit | architecture-decisions/decision_matrix.md |
| DEC-002 | GitHub repository as single source of truth, no runtime datastore | ADR/adr-001-github-source-of-truth.md |
| DEC-003 | Docusaurus with future.faster, multi-instance docs plugin | ADR/adr-002-docusaurus-framework.md |
| DEC-004 | Structural canonical/generated separation (two plugin instances, /docs vs /views) | ADR/adr-003-canonical-generated-separation.md |
| DEC-005 | Thin provider abstraction, config-routed, no AI framework | ADR/adr-004-provider-abstraction.md |
| DEC-006 | Generated content persists only through human-approved PRs | ADR/adr-005-generated-content-via-pr.md |
| DEC-007 | Level-1 deterministic retrieval with explicit escalation boundary (~1,500 pages) | ADR/adr-006-retrieval-level1.md |
| DEC-008 | Mermaid-as-code with CI compilation gate | ADR/adr-007-mermaid-as-code.md |
| DEC-009 | Build-time/CI-time AI over runtime AI | ADR/adr-008-build-time-ai.md |
| DEC-010 | Static deployment, GitHub Pages default, Modes A/B/C on one artifact | ADR/adr-009-deployment-github-pages.md |

Method-level decisions (recorded in the respective documents): weighted scoring with constraint override
rule (decision_matrix.md); evidence-tag taxonomy (02_RESEARCH per-platform SADs); deterministic-before-AI
validation ordering (05_DOCUMENTATION_DESIGN/documentation-process/automation_architecture.md).
