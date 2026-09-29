---
id: practice-evidence-discipline
title: Evidence Discipline — Tagged Claims and Calibrated Honesty
type: knowledge
category: best-practices
tags: [evidence, verification, research-method, honesty, confidence]
sources:
  - outputs/00_research/analysis_brief.md (evidence rules)
  - outputs/04_validation/validation_report.md (Gate A)
  - outputs/02_comparison/comparison.md, outputs/02_comparison/decision_matrix.md (Confidence)
  - outputs/01_products/*/sources.md, scores.json (structure)
confidence: HIGH
related: [framework-weighted-decision-model, framework-maintenance-risk-assessment, pattern-task-contracts, framework-build-vs-buy-vs-host]
---

# Evidence Discipline — Tagged Claims and Calibrated Honesty

**Summary** — Every factual capability claim in the research corpus carries an explicit evidence tag, invention of unverifiable facts is banned by a named list, and proprietary SaaS internals are treated as black boxes. This discipline is what made a six-platform comparison *decidable*: because every score's grounding and confidence is recorded, the final decision can state that no open evidence gap is decision-changing — and be checked.

## Core Logic

**The taxonomy.** Six mandatory tags, applied per claim:

- **`[VERIFIED-OFFICIAL]`** — current official docs/site.
- **`[VERIFIED-REPO]`** — inspected real repository files (with file-path citations).
- **`[OBSERVED]`** — observed behavior of public interfaces.
- **`[INFERRED]`** — reasoned from evidence, and labeled as such.
- **`[UNKNOWN]`** — honestly unknown; never silently filled.
- **`[HISTORICAL]`** — archived/outdated material, never presented as current architecture (e.g. GitBook's archived OSS repos).

**The never-invent list.** Banned outright: backend technologies, internal services, security controls, compliance claims, SLAs, unverified pricing numbers, benchmarks, adoption/customer counts. This list later reappears, almost verbatim, as the `prohibited` section of AI task contracts — the research rules became runtime generation rules.

**Proprietary-SaaS handling.** GitBook's current platform and Mintlify's backend are analyzed strictly through public interfaces and docs; internals are `[UNKNOWN]`, not guessed. Where evidence quality is mixed, it is labeled at point of use: Mintlify's Pro pricing is marked *third-party-reported* (the official page renders client-side); some GitHub star counts came from rendered pages because the REST API was blocked in-session — both facts flagged where used (Gate A).

**Confidence as data.** Every `scores.json` criterion carries `{score, rationale, evidence, confidence: HIGH|MEDIUM|LOW}`. Aggregated upward: each platform's total is labeled with overall evidence confidence, and residual MEDIUM/LOW items are enumerated in the decision matrix with the explicit finding that "none is decision-changing." Open gaps are *recorded, not hidden* — in `progress.json` and per-platform `scores.json`.

**Why calibrated honesty made the comparison decidable.** The brief demands equal analytical depth and warns: "Be honest about weaknesses; the comparison depends on calibrated honesty." If one analyst inflates and another hedges, weighted totals compare optimism, not platforms. Uniform tagging + per-score confidence made the six totals commensurable, let the sensitivity analysis test robustness meaningfully, and allowed hard findings to stand on verifiable citations — e.g. Material's 2026-11-05 support EOL `[VERIFIED-REPO: SECURITY.md]`, which drove the MkDocs verdict.

## Best Practices

1. **Tag at claim granularity, not document granularity**, because a document mixes verified and inferred content and the reader must know which is which.
2. **Prefer repository evidence over marketing**, and cite file paths, because docs describe intent while code describes reality — the brief explicitly refuses "credit for marketing claims" on self-hosting scores.
3. **Record `[UNKNOWN]` as a first-class answer**, because a labeled gap can be triaged for decision impact; an invented fact cannot.
4. **Attach confidence to every score and roll gaps up to the decision**, because the decision-maker needs to know not just the ranking but how much to trust it.
5. **Log evidence provenance operationally** (sources.md with access dates; how a number was obtained when the primary channel failed), because evidence collected under constraints must say so.
6. **Honesty about your own process too**: the validation report's Skill Usage Statement records which methodology parts could not run — self-applied evidence discipline.

## Pitfalls

- Date-sensitive facts rot: the security architecture deliberately refuses to restate provider retention windows because "citing a specific number here would rot silently" — instead it mandates verify-at-key-creation with a recorded check date. Distinguish facts that age from facts that don't.
- `[HISTORICAL]` mislabeled as current is the classic SaaS-analysis failure (archived GitBook OSS repos describe a product that no longer exists).
- Tagging is not free of judgment: `[OBSERVED]` star counts from rendered pages are weaker than API-exact values — the repo_health notes say so explicitly rather than upgrading the tag.
- Equal-depth parity matters: Gate B verified all six SADs at comparable word counts and identical deliverable sets, because an under-analyzed platform yields falsely confident scores.

## Expert Notes

The transferable insight is that evidence discipline is an *architecture input*, not just research hygiene: the target system institutionalizes the same rules for its AI (contracts prohibit unevidenced claims; a deterministic named-entity gate checks that every technology mentioned appears in evidence; `<EvidenceLink>` makes citations reader-visible). A team adopting this practice should expect its research standards to become its generation standards — design the taxonomy once, use it in both places.

## Evidence & Further Reading

- `outputs/00_research/analysis_brief.md` — the mandatory evidence rules and never-invent list.
- `outputs/04_validation/validation_report.md` Gate A — how the discipline was audited, including the honest residuals.
- `outputs/02_comparison/decision_matrix.md` (Confidence section) and `outputs/01_products/*/scores.json` — confidence-per-score in practice.
- `outputs/03_solution/ai_architecture.md` §4, §6 — the taxonomy's reincarnation as contract prohibitions and evidence gates.
