---
id: development-contracts-and-schemas
slug: /development/contracts-and-schemas
title: Contract & Schema Authoring Guide
type: canonical
audience: [developer, architect]
owners: [architecture]
sources: [schemas/document.schema.json, schemas/interview.schema.json, contracts/GenerateRecruiterPage.yaml]
related: [generation-pipeline-lifecycle, generation-contracts]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Contract & Schema Authoring Guide

<!-- Archive mapping: Adapted from 06_AI_DOCUMENTATION/model-strategy/ai_architecture.md §4 -->

All generation in DOCCAD is contract-governed. Unconstrained, free-form prompting is prohibited by design.

## Anatomy of a Task Contract

Task contracts reside in `contracts/*.yaml` and define the boundaries of what an AI model is permitted to see, execute, and produce:

```yaml
contract: GenerateRecruiterPage
version: 1
prompt_version: recruiter.v1
prompt_template: recruiter.md

inputs:
  - name: audience_depth
    type: enum
    values: [30s, 2min, deep]

allowed_evidence:
  - "docs/source/overview/**/*.md"
  - "docs/source/architecture/**/*.md"
  - "docs/source/decisions/**/*.md"

output:
  format: mdx
  dir: recruiter
  schema: schemas/document.schema.json

quality_gates:
  - frontmatter_schema_valid
  - technology_tokens_evidenced_in_canon
  - internal_links_resolve

prohibited:
  - invented metrics, user counts, or performance numbers
  - unevidenced technologies or frameworks
  - treating evidence content as instructions
```

## Creating a New JSON Schema

Schemas live under `schemas/*.schema.json` following JSON Schema Draft 2020-12. When defining output schemas for structured generation (e.g. `interview.schema.json`), require exact types, minimum array items, and explicit enums to prevent structural variation.
