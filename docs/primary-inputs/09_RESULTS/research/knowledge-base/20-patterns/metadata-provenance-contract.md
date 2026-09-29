---
id: pattern-metadata-provenance-contract
title: Metadata & Provenance as a Frontmatter Contract
type: knowledge
category: patterns
tags: [frontmatter, provenance, metadata-schema, content-hash, trust]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-8)
  - outputs/03_solution/content_architecture.md (§5)
  - outputs/05_poc/schemas/document.schema.json, outputs/05_poc/docs/generated/recruiter/project-overview.mdx
  - outputs/04_validation/validation_report.md (Gate D)
confidence: HIGH
related: [pattern-hash-drift-detection, pattern-canonical-generated-separation, pattern-task-contracts, pattern-leveled-retrieval]
---

# Metadata & Provenance as a Frontmatter Contract

**Summary** — Every page's YAML frontmatter is a schema-validated contract, not decoration. Canonical pages declare identity, audience, the repo paths they document, and ownership; generated pages additionally carry a complete `generation` block naming the contract, prompt version, provider, and per-source content hashes. The frontmatter *is* the system's metadata database — queryable by scripts, enforceable by CI, and versioned with the content it describes.

## Core Logic

**Problem.** Provenance ("where did this content come from, and is it still current?") and dependency mapping ("what breaks if this file changes?") usually live in external systems that drift from the content. A files-only architecture (AD-1) needs both to live *in* the files.

**Solution structure.** Two schemas, one file (`schemas/document.schema.json`), CI-enforced on every PR.

Canonical:

```yaml
id: architecture-system-overview   # stable, unique, never recycled
title: System Architecture
type: canonical
audience: [developer, architect]   # enum incl. operator|user|recruiter|interviewer
sources: [src/api/, pyproject.toml]  # repo paths this page documents (drift inputs)
owners: [architecture]
related: [adr-003, deployment-overview]  # doc-id link graph
ai_generation: {allowed: true, derived_pages: [recruiter, interview]}
last_validated: 2026-08-12
```

Generated (all canonical fields plus):

```yaml
type: generated
generated: true
generation:
  contract: GenerateRecruiterPage
  contract_version: 1
  prompt_version: recruiter.v1
  source_documents:
    - {id: ..., path: docs/source/..., content_hash: sha256:...}
  repo_evidence: [pyproject.toml]
  provider: anthropic
  model: <from run config>
  generated_at: 2026-08-12T10:00:00Z
  approval_status: draft   # draft|in-review|approved (approved set by merge automation)
```

**Mechanics.** `sources[]` feeds drift suspects and L1 retrieval; `related[]` builds the link graph and retrieval closure; the manifest (`.docs-manifest.json`) is rebuilt from frontmatter, so metadata errors surface as CI failures, not silent gaps. The provenance block is stamped by the pipeline, never written by the model (the prompt says so explicitly: "do not fabricate one"). The theme renders the provenance banner from these fields.

**Design deltas vs the mission's draft schema** (each deliberate):
- **Per-source `content_hash`** added — drift detection becomes mechanical (pattern-hash-drift-detection). The rationale: mtimes don't survive git; AI judgment isn't auditable; bytes are.
- **`contract`/`contract_version`/`prompt_version`** added — generation semantics are traceable; a prompt bump marks dependents stale.
- **`repo_evidence` separated from `source_documents`** — docs sources vs deterministically-extracted code facts are different evidence classes.
- **Model self-`confidence` dropped** — "a model's self-reported confidence is not evidence and invites misplaced trust; the human review gate is the confidence mechanism."

VERIFIED BY EXECUTION in 05_poc: PoC pages carry real computed sha256 hashes; `validate_docs.py` validated 5 pages, 1 interview dataset, and 5 provenance hashes, and failed correctly when a hash was corrupted. Docusaurus accepting unknown frontmatter keys — so this contract passes framework validation unchanged — was a [VERIFIED-REPO] platform-selection criterion.

## Best Practices

1. **Schema-validate frontmatter in CI on every PR**, because a metadata contract that isn't enforced is a suggestion, and every downstream system (drift, retrieval, banners) consumes these fields.
2. **Keep `id` stable, unique, and never recycled**, because ids are the join key for `related`, the manifest, and derived-page naming (`<id>.interview.json`).
3. **Let the pipeline stamp provenance, never the model**, because the model attesting to its own provenance is circular.
4. **Set `approval_status: approved` only via merge automation**, because approval must be an event record, not an editable field.
5. **Derive aggregate views (manifest) from frontmatter rather than maintaining them**, because a second copy of the truth is a drift source.

## Pitfalls

- Dropping the `confidence` field is counterintuitive — most teams add it. The corpus's argument: it *invites misplaced trust*; keep human review as the trust mechanism and record objective facts (hashes, versions, provider) instead.
- `sources[]` hygiene is load-bearing: an empty or stale `sources` list silently blinds both drift detection and retrieval. The schema can require the field; only review can require it to be *right*.
- Frontmatter changes are content changes: adding a `slug` in the PoC changed canonical bytes and correctly staled every dependent hash — expect and embrace this.
- Don't overload `related[]` into a tagging free-for-all; it drives one-hop retrieval closure, so noisy relations bloat generation context.

## Expert Notes

This pattern is what makes "files over services" (AD-1) actually work: provenance, dependency graph, staleness, audience routing, and translation state are all queries over frontmatter — answered by a Python script in milliseconds, with the answers versioned alongside the content. The deep design rule visible in the `confidence` decision and the pipeline-stamped provenance: **record facts the machine can verify; leave judgments to the humans and mark where they happened** (`approval_status`, `last_validated`).

## Evidence & Further Reading

- `outputs/03_solution/content_architecture.md` §5 — both schemas plus the improvement rationale (including the dropped confidence field).
- `outputs/03_solution/ARCHITECTURE-SPINE.md` AD-8 — the invariant this pattern implements.
- `outputs/05_poc/schemas/document.schema.json`, `outputs/05_poc/docs/generated/recruiter/project-overview.mdx` — real schema and a real stamped page.
- `outputs/04_validation/validation_report.md` Gate D — "mandatory `generation:` frontmatter with per-source sha256 hashes; PoC pages carry real computed hashes; schema-enforced."
