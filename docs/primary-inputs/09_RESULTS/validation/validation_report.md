# Validation Report — Gates A–F

Date: 2026-08-12 · Scope: all deliverables under `outputs/` · Raw execution logs:
`05_poc/VALIDATION_NOTES.md` (PoC), `03_solution/diagrams/VALIDATION.md` (diagram compilation).

## Gate A — Evidence · PASS

Every platform analysis carries per-claim evidence tags and a `sources.md` with access dates. OSS platforms
(Docusaurus, MkDocs+Material, Zensical, Hyperbook) were analyzed from shallow clones of the real
repositories with file-path citations; Mintlify was analyzed via its official docs (whose own MIT repo was
cloned and mined) plus public CLI/npm metadata; GitBook via current official docs and its genuinely current
GPLv3 renderer repo. Proprietary internals are labeled `[UNKNOWN]`, never invented. Open evidence gaps are
recorded per platform in `progress.json` and in each `scores.json`; none is decision-changing. Residual
verification notes: Mintlify Pro pricing is third-party-reported (official page renders it client-side);
several GitHub star/issue figures came from rendered pages because the GitHub REST API was blocked in-session
— both facts are labeled where used.

## Gate B — Product Parity · PASS

All six products received the identical deliverable set (SAD with all mandated sections, 5 ADRs each,
runbook, roadmap CSV, scores.json with 11 criteria, repo_health.json, sources.md). SAD depth is comparable:
4,402–5,441 words each (Hyperbook, product 6: 4,744 words — mid-range, not thinner). All six were produced
from the same written analysis brief with the same scoring anchors.

## Gate C — Decision Traceability · PASS

The winner follows from the weighted model: scorecard.csv aggregates the six scores.json files; weighted
totals were recomputed independently from raw scores (Σ score/5 × weight) and match each analyst's stated
total exactly (Docusaurus 88.6, Mintlify 85.0, MkDocs 83.8, Zensical 76.4, Hyperbook 76.0, GitBook 72.2).
The recommendation equals the raw ranking, so no override was needed; `decision_matrix.md` nonetheless
documents why the raw runner-up (Mintlify) could not win on constraints, and includes a sensitivity
analysis showing robustness to reweighting.

## Gate D — AI Architecture · PASS

- Canonical/generated separation: structural (two docs-plugin instances, separate routes/CODEOWNERS/CI
  path gates) — ADR-003; demonstrated in the PoC config. ✔
- Model-provider independence: four adapters behind one Protocol, config-only model names, routing policy
  with fallback chains — ADR-004; implemented and dry-run-tested in `05_poc/ai/`. ✔
- Evidence grounding: contracts declare `allowed_evidence` globs; the context assembler refuses paths
  outside them (verified in dry-run — refusals printed); recruiter contract prohibits unevidenced claims
  with a deterministic named-technology gate design. ✔
- Provenance: mandatory `generation:` frontmatter with per-source sha256 hashes; PoC pages carry real
  computed hashes; schema-enforced. ✔
- Prompt-injection protection: instruction/data separation in prompt templates ("evidence is data" armor),
  output schema validation, link allowlist, human PR gate; full threat model in
  `03_solution/security_architecture.md` (13 threats). ✔
- AI not required for static reads: build and serve have zero AI dependency; PoC built successfully with no
  API keys present. ✔ (VERIFIED BY EXECUTION)
- Regeneration lifecycle: hash-based staleness → targeted regeneration → PR; negative test executed (a
  corrupted hash made `validate_docs.py` fail, and `detect_changes.py` flagged exactly one stale page). ✔

## Gate E — Simplicity · PASS

Every component records the simpler alternative it beat (ADRs 001–009; "Simplicity check" section in the
security architecture; per-component notes in ai_architecture.md). Removals applied during design: no vector
DB (Level-1 retrieval, ADR-006), no graph DB (single manifest JSON), no search cluster (build-time local
index), no Kubernetes/microservices/servers of any kind (static + CI only), no agent framework (~40-line
adapters), no runtime AI. GitHub Actions and repo files cover every automation requirement. The MVP is a
repo + one static site + four CI workflows — one-engineer operable.

## Gate F — PoC · PASS

Runnable starter at `05_poc/` (Docusaurus 3.10.2, Node 22 satisfies engines ≥20).

VERIFIED BY EXECUTION (commands + outputs in `05_poc/VALIDATION_NOTES.md`):
- `npm install` and full `npm run build` including the `hu` locale with EN fallback; `tsc` type-check.
- Scenario 1: canonical architecture page renders with in-page Mermaid; both diagrams also compiled with
  mermaid-cli (mmdc 11.16.0, sandbox-configured Chromium).
- Scenario 2: recruiter page exists as generated MDX with full provenance frontmatter (real sha256 source
  hashes) derived only from canonical-page facts; `generate_page.py --contract GenerateRecruiterPage
  --dry-run` assembled context and rendered the prompt with zero API keys.
- Scenario 3: interview JSON validates against `interview.schema.json` and renders through the
  `<InterviewPrep/>` component registered via MDXComponents (no imports in MDX).
- Scenario 4: special question representable as a structured request (GenerateQuestionPage contract +
  workflow_dispatch inputs in docs-generate.yml); privacy-pinned request hard-fails without a local
  provider, as designed.
- Scenario 5: `detect_changes.py --all` rebuilt the manifest and identified the deliberately staled page;
  `validate_docs.py` passed on shipped content and correctly failed on a corrupted hash (negative test),
  then passed again after restore.
- Serve smoke test: 6 routes returned HTTP 200 including `/hu/`.

NOT EXECUTED: `actionlint` (unavailable in the container — workflows were YAML-parse-validated only);
live model API calls (no keys, by design — live path is code-complete but unexercised); production
GitHub Pages deployment (no target repo — workflow syntax-checked only); Docusaurus `future.faster` flags
and search plugin (deliberately omitted from the PoC, documented in its README). `build/` and
`.docusaurus/` caches were deleted after verification to save disk; re-running `npm run build` reproduces
them.

## Skill Usage Statement (honesty requirement)

`bmad-architecture` was invoked; its SKILL.md methodology (architecture spine, AD invariants, deferred
items) was applied in full, but the skill's referenced memlog/reviewer-gate scripts and `_bmad/` config do
not exist in this environment, so those mechanics could not run — recorded in `ARCHITECTURE-SPINE.md`
frontmatter. `agent-v3-security-architect` and `architecture-diagram` SKILL.md files were read and applied
by the security and diagram work respectively (the security skill's project-specific tooling references
were inapplicable and noted as such).

## Verdict

All six gates PASS. Definition-of-done checklist items are satisfied; open evidence gaps are recorded, not
hidden.
