---
id: platform-comparison-logic
title: How the Six-Platform Comparison Was Decided — Weights, Anchors, Constraints, Sensitivity
type: knowledge
category: platforms
tags: [decision-matrix, weighted-scoring, scoring-anchors, sensitivity-analysis, constraints, methodology]
sources:
  - outputs/02_comparison/decision_matrix.md
  - outputs/02_comparison/comparison.md
  - outputs/02_comparison/scorecard.csv
  - outputs/00_research/analysis_brief.md      # scoring anchors + evidence rules
  - outputs/01_products/*/scores.json          # per-criterion rationale/evidence/confidence
confidence: HIGH
related: [platform-docusaurus, platform-mintlify, platform-mkdocs, platform-gitbook, platform-zensical, platform-hyperbook, foundation-docs-as-code]
---

# How the Six-Platform Comparison Was Decided — Weights, Anchors, Constraints, Sensitivity

**Summary** — Six analysts scored six platforms against the same 11 weighted criteria on a 1–5 anchor scale, producing weighted totals out of 100 (Docusaurus 88.6 › Mintlify 85.0 › MkDocs 83.8 › Zensical 76.4 › Hyperbook 76.0 › GitBook 72.2). The final decision was **not** "highest number wins": the weighted model ranked, a layer of non-negotiable constraints vetoed, and a sensitivity analysis proved the result robust. This page distills that machinery so it can be reused.

## Core Logic

**The 11 weighted criteria** (weights sum to 100, encoding the target ecosystem's priorities):

| Criterion | Weight | Why this weight |
|---|---:|---|
| GitHub / docs-as-code fit | 15 | Git-as-single-source is the system's first principle |
| AI integration & extensibility | 15 | The system's purpose: derived views via an external AI layer |
| Architecture simplicity & maintainability | 12 | One-engineer, anti-overengineering hard rule |
| Structured content / IA | 10 | Canonical/derived separation needs structural support |
| Security & governance | 10 | AI-generated content raises the review bar |
| Mermaid / diagrams-as-code | 8 | Hard content-format requirement |
| Localization / bilingual EN-HU | 8 | Hard product requirement |
| Deployment flexibility / self-hosting | 7 | Provider-independence enforcement |
| Developer + author UX | 7 | Adoption friction |
| Search + SEO | 5 | Necessary, but commoditized at this scale |
| Cost efficiency | 3 | Personal-scale budget, lowest stake |

**Scoring anchors** (applied identically by all analysts, from the shared brief): **5** = best-in-class, native, no workarounds · **4** = strong, minor gaps · **3** = workable with documented workarounds/plugins · **2** = significant friction or partial lock-in · **1** = unsuitable/blocked. Formula: `weighted_score = Σ(score/5 × weight)`, range 0–100. Two anti-inflation rules for SaaS: score docs-as-code fit against *true* Git-as-single-source operation, and self-hosting against *actual* options — "do not give credit for marketing claims." (This is why GitBook's real Git Sync still scored 3, and Mintlify's Enterprise-only self-host scored 2.) Every score carries rationale, evidence pointers and a HIGH/MEDIUM/LOW confidence in the platform's `scores.json`.

**Why raw score ≠ automatic winner.** The model is deliberately two-layered:

1. *Weighted ranking* orders the field and forces analysts to be explicit about trade-offs.
2. *Critical constraints* — non-negotiable system principles — veto regardless of total. The worked example is Mintlify: 85.0, ties or beats the winner on both 15% criteria, yet is rejected because principle §9 ("approved documentation must remain available even when providers are unavailable") extends to the publishing vendor — "a system whose stated purpose is provider independence cannot place its only rendering path inside one provider." The matrix records this as "the explicit justification for why the #2 raw score does not become the recommendation even in a tie-adjacent scenario." Conversely, Docusaurus needed no override: "the raw ranking and the critical architectural constraints point at the same platform." A weighted sum smooths over vetoes; the constraint layer un-smooths them.

**The sensitivity analysis** stress-tests the decision instead of just asserting it:

- *Docusaurus is robust*: it leads or ties on the two heaviest criteria (15% + 15%) and dominates self-hosting and cost — no plausible re-weighting flips it.
- *Mintlify overtakes only if* self-hosting and cost weights drop to ~0 **and** provider lock-in is accepted — "i.e., a different mission." Weight changes that large aren't tuning; they are a different project.
- *MkDocs overtakes only if* its maintenance risk is ignored, "which the evidence forbids" (Material EOL 2026-11-05 is date-certain [VERIFIED-REPO]).
- *GitBook cannot overtake* under any weighting consistent with Git-as-source-of-truth — a structural, not numerical, exclusion.
- *Zensical/Hyperbook* trail on extensibility and localization — "real gaps for this system, not weighting artifacts" — i.e., the model was checked for artifacts and cleared.

**Confidence accounting.** All six totals rest on predominantly HIGH-confidence, repo- or official-doc-grounded scores; residual MEDIUM/LOW items (Mintlify Pro pricing, Zensical Spark pricing, GitBook frontmatter round-trip) are enumerated and individually shown to be non-decision-changing.

## Best Practices

1. **Fix weights and anchors before scoring** (the brief predates all six analyses) — post-hoc weights rationalize; pre-committed weights decide.
2. **Keep a constraint layer separate from the weighted layer** and write down which principles are vetoes — otherwise a strong score in the wrong architecture wins by arithmetic.
3. **Score against verified operation, not claims**; attach evidence and confidence to every cell so disagreements resolve to sources, not opinions.
4. **Run the sensitivity analysis and publish it** — "what would have to change for #2 to win" is the most persuasive sentence in the whole comparison.
5. **Record concentrated risks as named critical constraints** rather than diffusing them across criteria (the MkDocs pattern) — it keeps scores comparable and risks visible.
6. **Give losers dispositions, not just ranks**: reject-with-reason (Mintlify, GitBook), conditional fallback (MkDocs), watch-with-trigger (Zensical at 1.0 + plugin API), niche (Hyperbook). A comparison's output is a policy, not a leaderboard.

## Pitfalls

- **Averaging away a veto** — GitBook scores 4 on six criteria and is still last *and* disqualified; without the constraint layer it would look like a mid-field option.
- **Criteria that don't discriminate**: Mermaid (five platforms at 4–5) and cost (four at 5) barely moved the ranking — they matter as *gates*. Localization (2–4 spread) and extensibility actually separated the field. Check spread when choosing criteria.
- **Popularity as proxy**: the renderer repo's 28.9k stars are inherited from a deprecated product [INFERRED]; Hyperbook's 74 stars coexist with daily maintenance. The method used commit/contributor/release evidence instead.
- **Tie-adjacent totals implying interchangeability**: Zensical (76.4) and Hyperbook (76.0) are 0.4 apart with *completely different* risk shapes (alpha surface vs. bus factor 1). Totals compress; read the constraint lists.

## Expert Notes

- The weight vector *is* the requirements document, compressed: 30% on Git-fit + AI-extensibility says "this is an AI-augmented docs-as-code system"; 3% on cost says "money is not the scarce resource, engineer attention is." Reading weights as requirements is the fastest way to audit someone else's matrix.
- The two 15% criteria pulled in opposite directions across the field (hosted platforms won AI surface, OSS won Git fit) — a deliberate tension that forced the constraint layer to do the final arbitration. Good matrices *create* the hard question; they don't hide it.
- Equal analytical depth was mandated ("this platform must be analyzed as deeply as every other") — the honest-weakness rule ("the comparison depends on calibrated honesty") is what makes cross-analyst scores comparable at all.

## Evidence & Further Reading

- The matrix itself: `outputs/02_comparison/decision_matrix.md`; master table + field findings: `outputs/02_comparison/comparison.md`; raw grid: `outputs/02_comparison/scorecard.csv`
- Anchors, weights, evidence rules: `outputs/00_research/analysis_brief.md`
- Per-cell rationale/evidence/confidence: `outputs/01_products/<platform>/scores.json`
- Profiles: [docusaurus](docusaurus.md) · [mintlify](mintlify.md) · [mkdocs](mkdocs.md) · [zensical](zensical.md) · [hyperbook](hyperbook.md) · [gitbook](gitbook.md)
