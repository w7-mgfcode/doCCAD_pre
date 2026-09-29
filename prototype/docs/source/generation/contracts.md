---
id: generation-contracts
slug: /generation/contracts
title: Task Contracts Catalog
type: canonical
audience: [developer, architect]
owners: [architecture]
sources: [contracts/GenerateRecruiterPage.yaml, contracts/GenerateInterviewPrep.yaml, contracts/GenerateQuestionPage.yaml]
related: [generation-pipeline-lifecycle, development-contracts-and-schemas]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Task Contracts Catalog

<!-- Archive mapping: Adapted from 06_AI_DOCUMENTATION/model-strategy/ai_architecture.md §4 -->

DOCCAD provides a catalog of pre-configured task contracts governing distinct documentation transformations:

| Contract Name | Target Purpose | Primary Inputs | Output Artifact | Persistence |
|---|---|---|---|---|
| **`GenerateRecruiterPage`** | Produce recruiter-focused profiles | Audience depth (`30s`, `2min`, `deep`) | `docs/generated/recruiter/*.mdx` | PR |
| **`GenerateInterviewPrep`** | Generate technical interview cards | Canonical doc ID | `docs/generated/interview/*.interview.json` | PR |
| **`GenerateQuestionPage`** | Answer user questions with citations | Question text, audience, privacy | `docs/generated/questions/q-*.mdx` | PR |
| **`GenerateTroubleshootingGuide`** | Map error symptoms to runbook fixes | Error message / symptom scope | `docs/generated/troubleshooting/*.mdx` | PR |
| **`GenerateArchitectureManual`** | Compile deep technical manuals | Architecture subsystem scope | `docs/generated/manuals/*.mdx` | PR |
| **`UpdateMermaidDiagram`** | Propose architecture diagram updates | Diagram path + change intent | `docs/diagrams/*.mmd` | PR |

## Contract Invariant Rules
- Every contract mandates a `prohibited` section forbidding fabricated metrics or ungrounded claims.
- Every contract enforces `allowed_evidence` restrictions.
- All persistent outputs require a reviewed PR before inclusion in canonical release builds.
