---
id: troubleshooting-generation-failures
slug: /troubleshooting/generation-failures
title: Troubleshooting Generation Failures & Degradation
type: canonical
audience: [developer, operator]
owners: [operations]
sources: [ai/router.py, scripts/generate_page.py]
related: [operations-runbook-stale-views, architecture-ai-generation-plane]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Troubleshooting Generation Failures & Degradation

<!-- Archive mapping: Adapted from 06_AI_DOCUMENTATION/model-strategy/ai_architecture.md §9 -->

When automated generation jobs fail in CI or local CLI execution, use this guide to identify the root cause and apply appropriate fixes.

## Common Failure Scenarios

### 1. `PrivacyRoutingError`: Local Provider Disabled
- **Symptom**: CLI exits with `PrivacyRoutingError: Task is privacy: private but local provider is disabled...`
- **Cause**: The task is flagged `privacy: private`, but `ai.config.yaml` has `providers.local.enabled: false`.
- **Remediation**:
  - For offline local testing, start a local OpenAI-compatible endpoint (e.g. `ollama run llama3`) and set `providers.local.enabled: true` in `ai.config.yaml`.
  - In demo mode, use the deterministic `fixture` provider.
  - **Do NOT** change task privacy to `public` merely to force execution through cloud APIs.

### 2. Schema Validation Errors on Model Output
- **Symptom**: `ContractViolation: Output invalid after one repair retry: missing required 'audience'`
- **Cause**: The model emitted malformed frontmatter or omitted a mandatory field.
- **Remediation**:
  - The pipeline automatically performs one repair retry appending the validator error trace.
  - If it fails repeatedly, verify that the prompt template in `prompts/` explicitly demonstrates the required YAML frontmatter structure.

### 3. Missing Canonical Evidence
- **Symptom**: `ContractViolation: No canonical page with id '<id>' under docs/source/`
- **Cause**: The requested target ID does not exist or was renamed without updating task references.
- **Remediation**: Check `prototype/docs/source/` for the correct document `id` and update your generation command arguments.

### 4. Broken Link Gate (`onBrokenLinks: throw`)
- **Symptom**: `docusaurus build` fails with `Docusaurus found broken links`.
- **Cause**: A markdown document references an invalid relative path or missing doc ID.
- **Remediation**: Correct the relative path or ensure explicit `slug:` frontmatter is set for the target page.
