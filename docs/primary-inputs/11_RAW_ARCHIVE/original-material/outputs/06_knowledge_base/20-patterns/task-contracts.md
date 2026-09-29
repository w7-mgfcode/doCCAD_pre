---
id: pattern-task-contracts
title: Task Contracts — Bounded Generation Instead of Free-Form Prompting
type: knowledge
category: patterns
tags: [contracts, prompting, quality-gates, schema, generation-governance]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-6)
  - outputs/03_solution/ai_architecture.md (§4–6)
  - outputs/05_poc/contracts/GenerateRecruiterPage.yaml (and siblings)
  - outputs/05_poc/prompts/recruiter.md
  - outputs/04_validation/validation_report.md (Gate D)
confidence: HIGH
related: [pattern-thin-provider-abstraction, pattern-hash-drift-detection, pattern-metadata-provenance-contract, practice-prompt-injection-defenses, practice-evidence-discipline]
---

# Task Contracts — Bounded Generation Instead of Free-Form Prompting

**Summary** — Every AI generation job references a named, versioned YAML contract that defines what the task may read, what it must produce, which deterministic gates its output must pass, and what it is explicitly forbidden to say. Contracts turn "prompting" from an art into a governed interface: unbounded generation becomes structurally impossible, and prompt changes propagate as tracked staleness rather than silent behavior drift.

## Core Logic

**Problem.** Free-form prompting has no enforceable boundary on inputs (the model sees whatever the script happens to include), no output guarantee, and no change management — editing a prompt silently changes every future page while already-published pages claim the same provenance.

**Solution structure.** Contracts live in `contracts/*.yaml`, versioned and schema-validated. Each defines:

- **`inputs`** — typed parameters (e.g. `target: doc_id`, `depth: enum[30s, 2min, deep-dive]`).
- **`allowed_evidence`** — path globs; the context assembler *refuses* any file outside them before any model call. VERIFIED BY EXECUTION in 05_poc: the dry run printed refusals for `scripts/*.py` and `ai/*.py`, which were in the target's sources closure but outside `allowed_evidence`.
- **`output`** — format and location, plus an output schema (JSON Schema for structured outputs like `interview.schema.json`; MDX outputs validated by frontmatter schema + Docusaurus build).
- **`quality_gates`** — deterministic checks that must pass: frontmatter schema valid, every claim carries an evidence link, evidence links resolve, no external links outside the allowlist, source hashes current, `docusaurus build` passes.
- **`prohibited`** — an explicit list, e.g. for the recruiter contract: invented metrics/user counts/performance numbers, technologies not present in evidence, achievements or adoption claims, seniority adjectives, security guarantees, any statement without a canonical evidence link. The prohibited list is injected into the prompt *and* enforced where checkable (a named-entity gate verifies every technology token appears in the deterministic fact list or cited canon — a script, not AI judgment).
- **`model_requirements`** — structured-output need, minimum context — consumed by the router.
- **`persistence`** — always `pr` except advisory tasks (e.g. DetectDocumentationDrift persists nothing; it only annotates CI).

**Prompt versioning.** Prompts are Markdown templates in `prompts/`, referenced by version (`prompt_version: recruiter.v1`) and stamped into every generated page's provenance. Changing a prompt bumps the version, which *by design marks all dependent pages stale* — regeneration is then a deliberate, reviewable act (full-corpus regeneration requires a manual `workflow_dispatch` with `confirm: all`).

The catalog covers nine tasks (recruiter page, interview prep, question page, troubleshooting guide, architecture manual, developer guide, Mermaid update, change summary, drift detection) — each with its own evidence scope and output shape.

## Best Practices

1. **Enforce `allowed_evidence` in the assembler, not the prompt**, because a refusal before the model call is deterministic; an instruction to the model is a request.
2. **Write the prohibited list explicitly per task**, because generic "don't hallucinate" instructions are unenforceable — a named list can be gated (named-entity check) and reviewed.
3. **Version prompts and propagate staleness**, because provenance that names `prompt_version: v1` must actually mean v1 produced the page.
4. **Treat contracts and prompts as code** — CODEOWNERS, review, CI schema validation — because they steer the AI and are therefore part of the attack/quality surface.
5. **Keep persistence policy inside the contract**, because "where output is allowed to land" is a property of the task, not the caller.

## Pitfalls

- The simpler alternative — free-form prompts per script — is exactly what contracts beat: it forks routing/gating logic per script and leaves no audit trail of what the model was allowed to see.
- Contracts do not remove hallucination; they bound it and make it detectable. A schema-valid, allowlist-clean but wrong page still reaches human review — which is why AD-9 forbids auto-merge (residual risk of T2/T11, accepted with eyes open).
- Over-broad `allowed_evidence` globs quietly recreate free-form prompting; scope them per task (recruiter: canonical docs + `package.json` + `ai.config.yaml`, nothing else).
- Advisory tasks must stay advisory: drift classification labels help reviewers but never gate merges (AD-10).

## Expert Notes

A contract is where the system's honesty rules become machine-checkable. Note the division of labor: deterministic facts (languages, frameworks) are extracted from lockfiles/manifests *by script*, and the model may only use technologies appearing in that fact list or cited canon — the model narrates, the pipeline attests. This is the same evidence discipline the research phase applied to itself (practice-evidence-discipline), turned into runtime enforcement.

## Evidence & Further Reading

- `outputs/03_solution/ai_architecture.md` §4 (contract fields + full catalog table), §5 (pipeline), §6 (recruiter gates).
- `outputs/05_poc/contracts/GenerateRecruiterPage.yaml`, `GenerateInterviewPrep.yaml`, `GenerateQuestionPage.yaml` — concrete, runnable contracts.
- `outputs/05_poc/VALIDATION_NOTES.md` §e — evidence-refusal transcript (dry run, zero keys).
- `outputs/04_validation/validation_report.md` Gate D — "contracts declare `allowed_evidence` globs; the context assembler refuses paths outside them (verified in dry-run)".
