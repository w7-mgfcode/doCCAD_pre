---
id: pattern-hash-drift-detection
title: Hash-Based Drift Detection and Incremental Regeneration
type: knowledge
category: patterns
tags: [drift, staleness, sha256, manifest, incremental-regeneration, determinism]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-8, AD-10)
  - outputs/03_solution/automation_architecture.md (§1–2)
  - outputs/03_solution/content_architecture.md (§5)
  - outputs/05_poc/scripts/detect_changes.py, outputs/05_poc/scripts/validate_docs.py, outputs/05_poc/.docs-manifest.json, outputs/05_poc/impact.json
  - outputs/04_validation/validation_report.md (Gate D, Gate F)
confidence: HIGH
related: [pattern-metadata-provenance-contract, pattern-task-contracts, pattern-pr-gated-generation, practice-ci-quality-gates]
---

# Hash-Based Drift Detection and Incremental Regeneration

**Summary** — Every generated page records a sha256 content hash of each source document it was derived from. CI recomputes those hashes at HEAD; any mismatch flags the page stale, and only the stale set regenerates. Staleness thereby becomes a mechanical, auditable fact instead of an opinion — the concrete embodiment of the system's deterministic-before-AI principle.

## Core Logic

**Problem.** Generated views silently rot as their sources change. Detecting this with modification times fails (git doesn't preserve mtimes); detecting it with AI judgment is non-deterministic and unauditable. Regenerating everything on every change is wasteful and floods reviewers.

**Solution structure.** Three cooperating mechanisms:

1. **Per-source hashes in provenance frontmatter.** Each generated page's `generation.source_documents[]` lists `{id, path, content_hash: sha256:...}` for every source. `validate_docs.py` recomputes hashes and fails on mismatch, reporting exactly which source drifted.
2. **Dependency manifest.** `.docs-manifest.json` is rebuilt from all frontmatter (id → path, `sources`, `related`, derived pages) — a single committed JSON file mapping source paths → dependent canonical docs → dependent generated pages. It beat a graph database: "a service for a query set answerable by one dict lookup."
3. **Impact analysis.** On every push/PR, `detect_changes.py` diffs (`git diff --name-status`), classifies changed paths by deterministic path rules, and emits `impact.json`: (a) canonical pages whose `sources[]` match changed code paths (docs-drift suspects), (b) generated pages whose `source_documents[].path` match or whose hashes mismatch (the **stale set**), (c) diagrams referenced by changed pages.

**Incremental regeneration.** Regeneration jobs receive the stale set and touch *only* those artifacts. Full-corpus regeneration exists solely as a manual `workflow_dispatch` with an explicit `confirm: all` — used e.g. after a prompt-version bump, which deliberately marks all dependents stale. A weekly scheduled sweep recomputes all hashes, maintains a single "stale views" issue, and can auto-trigger regeneration PRs where the contract allows.

**Deterministic-before-AI.** Content hashes beat AI judgment as the primary drift signal because they are reproducible and auditable; AI-assisted change classification (SummarizeRepositoryChange) is an optional advisory layer, never merge-blocking (AD-10). Code-vs-docs drift (code changed, doc didn't) posts a `docs-drift-suspect` checklist comment but does not block merge — blocking there was rejected as review theater, since authors may legitimately judge no doc change is needed.

VERIFIED BY EXECUTION in 05_poc: `detect_changes.py --all` rebuilt a 6-entry manifest; appending one byte to a source file produced `stale generated: 1` with a concrete regeneration plan (`GenerateRecruiterPage --target recruiter-project-overview`); corrupting 8 hex chars of a `content_hash` made `validate_docs.py` fail with the exact stale page and source named, then pass again after restore. During PoC hardening, adding `slug` frontmatter to canonical pages changed their bytes and forced recomputation of all dependent hashes — "exactly the drift the hash mechanism is for."

## Best Practices

1. **Hash content, not timestamps**, because git preserves bytes, not mtimes; hashes survive clones, rebases and CI checkouts.
2. **Store hashes in the artifact they protect** (the generated page's own frontmatter), because staleness must be checkable from the file alone, without external state.
3. **Rebuild the manifest from frontmatter every run**, because a hand-maintained dependency map is itself a drift source; derived state should be derived.
4. **Regenerate the stale set only**, because targeted PRs keep review load proportional to change — the property that keeps the human gate viable.
5. **Negative-test the mechanism** (corrupt a hash, expect failure), because a drift detector that never fires is indistinguishable from a broken one.

## Pitfalls

- Hash mismatch says *that* a source changed, not *whether the change matters* — a typo fix stales dependents just like a rewrite. Accepted: false-positive staleness costs one cheap regeneration; false-negative staleness costs credibility.
- Wholesale file replacement on regeneration is required (no AI-edits-AI diffs); incremental edits would break the "regenerable from sources at any time" invariant and bloat history.
- Manifest recall depends on frontmatter hygiene (`sources[]` filled in correctly) — which is why the frontmatter schema is CI-enforced.
- Deleting a canonical page must flag all dependents for removal in the same PR, or the manifest happily maps to ghosts.

## Expert Notes

The pattern only works because file identity is deterministic — a key reason GitBook was disqualified (its Git Sync normalizes exports, so bytes change without meaning changing) and a quiet argument for the whole files-over-services stance: sha256 over repo files is trivially correct, while hashing CMS/database state is a project. Note the layering: hashes handle generated-vs-source drift *mechanically*; the softer code-vs-docs drift gets human-judgment prompts; age reports (>180 days since `last_validated`) are purely advisory. Authority decreases as determinism decreases — by design.

## Evidence & Further Reading

- `outputs/03_solution/automation_architecture.md` §1 (ingestion + manifest + impact), §2 (drift checks in order of authority).
- `outputs/03_solution/content_architecture.md` §5 — `content_hash` in the provenance schema.
- `outputs/05_poc/VALIDATION_NOTES.md` §c–d — positive and negative executed proofs; `outputs/04_validation/validation_report.md` Gate D/F.
- `outputs/05_poc/scripts/detect_changes.py`, `outputs/05_poc/scripts/validate_docs.py` — reference implementation.
