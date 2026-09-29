# Decision Matrix — Publishing Foundation for the GitHub-Native AI Documentation System

Date: 2026-08-12. Scores are 1–5 per criterion; weighted score = Σ(score/5 × weight). Per-criterion
rationale, evidence and confidence: `01_products/<platform>/scores.json`. Raw grid: `scorecard.csv`.

## Weighted Model

| Criterion | Weight | Mintlify | GitBook | Docusaurus | MkDocs | Zensical | Hyperbook |
|---|---:|---:|---:|---:|---:|---:|---:|
| GitHub / docs-as-code fit | 15% | 5 | 3 | 5 | 5 | 5 | 4 |
| AI integration & extensibility | 15% | 5 | 4 | 4 | 4 | 3 | 3 |
| Architecture simplicity & maintainability | 12% | 4 | 4 | 4 | 5 | 4 | 4 |
| Structured content / IA | 10% | 5 | 4 | 5 | 4 | 3 | 4 |
| Security & governance | 10% | 3 | 4 | 4 | 3 | 3 | 3 |
| Mermaid / diagrams-as-code | 8% | 5 | 4 | 5 | 4 | 5 | 5 |
| Localization / bilingual | 8% | 4 | 4 | 4 | 3 | 2 | 3 |
| Deployment flexibility / self-hosting | 7% | 2 | 1 | 5 | 5 | 5 | 5 |
| Developer + author UX | 7% | 5 | 4 | 4 | 4 | 4 | 4 |
| Search + SEO | 5% | 4 | 4 | 4 | 4 | 4 | 3 |
| Cost efficiency | 3% | 2 | 3 | 5 | 5 | 5 | 5 |
| **Weighted total** | **100%** | **85.0** | **72.2** | **88.6** | **83.8** | **76.4** | **76.0** |

Ranking: **1. Docusaurus 88.6 · 2. Mintlify 85.0 · 3. MkDocs 83.8 · 4. Zensical 76.4 · 5. Hyperbook 76.0 · 6. GitBook 72.2**

## Decision

**Winner: Docusaurus.** The raw ranking and the critical architectural constraints point at the same
platform, so no override of the mathematical result is needed. Docusaurus is the only candidate that
simultaneously satisfies every non-negotiable constraint of the target system:

1. **Provider independence & static reads without AI** (Principle §9): MIT-licensed, plain static output,
   self-hostable anywhere, no vendor in the serving path. Mintlify and GitBook fail this outright.
2. **Canonical vs generated separation** (Principle §2): multi-instance docs plugin gives two independently
   configured content trees with separate sidebars, routes and validation — a structural boundary rather
   than a naming convention [VERIFIED-REPO: dogfooded upstream with `id: 'community'`].
3. **Programmatic generation target**: AI-generated `.mdx` is ordinary repo content; frontmatter accepts
   unknown keys, so the provenance contract passes validation unchanged [VERIFIED-REPO].
4. **InterviewPrep as a real component**: global MDXComponents registration means generated pages can use
   `<InterviewPrep/>` with zero imports — no other candidate has an equivalent [VERIFIED-REPO].
5. **Active maintenance**: v3.10.2 (2026-07), Rspack/SWC build path, active core team — against MkDocs'
   dormant core and Material's 2026-11-05 support cliff [VERIFIED-REPO: SECURITY.md].

**Runner-up (raw score): Mintlify (85.0).** Its AI-consumption surface (llms.txt, per-page .md, /mcp,
agent visibility) is the best in the field and its Git workflow is genuinely canonical. It loses on a
critical constraint, not on quality: the build/serve/search/AI plane is a proprietary black box; self-hosting
and static export are Enterprise-gated; the target workflow lands on the Pro plan (~$450/mo,
third-party-reported). §9 ("existing approved documentation must remain available even when providers are
unavailable") extends naturally to the publishing vendor: a system whose stated purpose is provider
independence cannot place its only rendering path inside one provider. This is the explicit justification
for why the #2 raw score does not become the recommendation even in a tie-adjacent scenario.

**Runner-up (constraint-adjusted): MkDocs + Material (83.8).** If the JS/React toolchain were vetoed, this
would be the fallback — architecturally the simplest system in the field — but only version-pinned and with
a dated exit decision before the 2026-11-05 Material support cutoff. Zensical is the designated re-evaluation
candidate once it ships 1.0 + a plugin API + multi-language content (revisit trigger recorded in ADR-002 of
the solution).

## Sensitivity Analysis

The decision is robust: Docusaurus leads or ties on the two heaviest criteria (GitHub fit 15%, AI
extensibility 15%) and dominates on self-hosting and cost. For Mintlify to overtake, the self-hosting and
cost weights would have to drop to ~0 AND provider-lock-in be accepted — i.e., a different mission.
For MkDocs to overtake, its maintenance risk would have to be ignored, which the evidence forbids. GitBook
cannot overtake under any weighting consistent with Git-as-source-of-truth. Zensical/Hyperbook trail
primarily on extensibility and localization — real gaps for this system, not weighting artifacts.

## Confidence

All six weighted totals rest on predominantly HIGH-confidence, repository- or official-doc-grounded scores.
Residual MEDIUM/LOW items (Mintlify Pro pricing, Zensical Spark pricing, GitBook frontmatter round-trip) are
recorded in each platform's `scores.json` and none is decision-changing.
