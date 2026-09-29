---
id: framework-weighted-decision-model
title: Weighted Decision Model — 11 Criteria, Anchored Scores, Constraint Override
type: knowledge
category: decision-frameworks
tags: [decision-making, scoring, weights, sensitivity-analysis, platform-selection]
sources:
  - outputs/00_research/analysis_brief.md (scores.json shape, anchors)
  - outputs/02_comparison/decision_matrix.md
  - outputs/02_comparison/comparison.md, outputs/02_comparison/scorecard.csv
  - outputs/04_validation/validation_report.md (Gate C)
confidence: HIGH
related: [practice-evidence-discipline, framework-build-vs-buy-vs-host, framework-maintenance-risk-assessment, framework-anti-overengineering-rules]
---

# Weighted Decision Model — 11 Criteria, Anchored Scores, Constraint Override

**Summary** — The platform decision was made with a weighted scoring model: 11 criteria with fixed percentage weights, 1–5 scores with written anchors, weighted total = Σ(score/5 × weight) on a 0–100 scale, confidence recorded per score — plus the explicit rule that hard constraints can override the arithmetic. Applied to six platforms it produced Docusaurus 88.6 > Mintlify 85.0 > MkDocs 83.8 > Zensical 76.4 > Hyperbook 76.0 > GitBook 72.2, with the ranking independently recomputed and a sensitivity analysis proving robustness.

## Core Logic

**Criteria and weights** (fixed before scoring, derived from the mission): GitHub/docs-as-code fit 15%, AI integration & extensibility 15%, architecture simplicity & maintainability 12%, structured content/IA 10%, security & governance 10%, Mermaid/diagrams-as-code 8%, localization/bilingual 8%, deployment/self-hosting 7%, dev+author UX 7%, search+SEO 5%, cost efficiency 3%. Weights encode mission priorities — the two 15% criteria are the system's reason to exist.

**Anchored 1–5 scores.** Anchors were published in the shared brief so six parallel analysts scored commensurably: 5 = best-in-class, native, no workarounds; 4 = strong, minor gaps; 3 = workable with documented workarounds/plugins; 2 = significant friction or partial lock-in; 1 = unsuitable/blocked. Anti-inflation instructions were explicit (score SaaS self-hosting "against actual self-host options — do not give credit for marketing claims").

**Arithmetic.** `weighted_score = Σ(score/5 × weight)`, 0–100. Gate C recomputed all six totals independently from the raw `scores.json` files and matched every analyst's stated total exactly — the arithmetic is auditable, not decorative.

**Confidence per score.** Every criterion records `{rationale, evidence, confidence: HIGH|MEDIUM|LOW}`. Residual MEDIUM/LOW items (Mintlify Pro pricing, Zensical Spark pricing, GitBook frontmatter round-trip) were enumerated and individually assessed as not decision-changing — turning "how sure are we?" into a checkable claim.

**When constraints override math.** The model's stated epistemology: "The weighted model guides; constraints decide." Mintlify scored #2 (85.0) yet was rejected on a critical constraint — its build/serve/AI plane is vendor-locked, violating provider independence — and the matrix documents *why the #2 raw score could not win even in a tie-adjacent scenario*. Conversely, no override was actually needed: the winner led both the ranking and the constraint check, and the matrix notes the constraint set alone would have selected Docusaurus regardless.

**Sensitivity analysis.** The decision was stress-tested against reweighting: Mintlify overtakes only if self-hosting and cost weights drop to ~0 *and* lock-in is accepted ("i.e., a different mission"); MkDocs overtakes only by ignoring evidence-forbidden maintenance risk; GitBook "cannot overtake under any weighting consistent with Git-as-source-of-truth."

## Best Practices

1. **Fix criteria, weights, and anchors before anyone scores**, because post-hoc weights are rationalization with extra steps.
2. **Write scoring anchors and anti-inflation rules**, because multi-analyst scores are only comparable if 4 means the same thing everywhere.
3. **Record rationale, evidence, and confidence per score**, because a bare number cannot be audited or revisited.
4. **Recompute totals independently**, because transcription errors in decision matrices are common and corrosive.
5. **Name the hard constraints separately from the weights**, because a constraint is not a heavy weight — it is a veto, and burying vetoes in weights hides them.
6. **Run a sensitivity analysis**, because a decision that flips under mild reweighting isn't a decision; it's a coin toss with paperwork.

## Pitfalls

- **Weights that sum to a story, not a mission**: the 3% on cost is honest (all OSS candidates are free; cost barely discriminates) — resist weighting criteria by how interesting they are.
- **Score inflation on marketing claims** — the exact failure the brief pre-empted for SaaS self-hosting scores.
- **Letting the runner-up's strengths blur the veto**: Mintlify's AI surface was genuinely best-in-field; the matrix credits it fully *and* rejects it — both honesty and decisiveness, on the record.
- **Skipping the "no override needed" statement**: recording that math and constraints agreed is what makes the traceability gate (Gate C) checkable later.

## Expert Notes

The model's real product is not the number — it's the *decidability*. Because every score is evidenced and confidence-tagged (practice-evidence-discipline), disagreement collapses to specific, checkable claims ("does GitBook round-trip frontmatter byte-faithfully?") instead of vibes. And the constraint-override rule prevents the classic weighted-matrix pathology of a high-scoring option that fails a must-have. Use the ranking to order candidates, the constraints to disqualify them, and the sensitivity analysis to know whether you actually decided anything.

## Evidence & Further Reading

- `outputs/02_comparison/decision_matrix.md` — full model, decision, both runners-up, sensitivity analysis, confidence.
- `outputs/00_research/analysis_brief.md` — scores.json schema, anchors, weighting.
- `outputs/02_comparison/scorecard.csv` + `outputs/01_products/*/scores.json` — raw grid and per-score evidence.
- `outputs/04_validation/validation_report.md` Gate C — independent recomputation and traceability audit.
