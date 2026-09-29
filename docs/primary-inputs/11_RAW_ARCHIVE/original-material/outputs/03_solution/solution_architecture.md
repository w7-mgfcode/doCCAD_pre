# MEGOLDÁS — GitHub-Native AI Documentation System
## Solution Architecture Document

Status: final · Date: 2026-08-12 · Method: bmad-architecture spine (`ARCHITECTURE-SPINE.md`) distilled into
this SAD; diagrams in `diagrams/` (all compile-validated); security detail in `security_architecture.md`;
content model in `content_architecture.md`; AI plane in `ai_architecture.md`; automation in
`automation_architecture.md`; decisions in `ADRs/`.

## 1. Executive Summary

This architecture turns one GitHub repository into a governed documentation ecosystem. Canonical knowledge —
architecture docs, ADRs, runbooks, development guides, Mermaid diagrams — is human-owned Markdown/MDX under
`docs/source/`. An AI generation plane, running exclusively in GitHub Actions and a local CLI, transforms
that canonical evidence into derived views (recruiter pages, interview-prep sections, special-question pages)
under `docs/generated/`, always through schema-validated task contracts, always landing as pull requests that
a human approves. **Docusaurus 3.x** (weighted winner, 88.6/100 across six platforms) builds both planes into
one static site with first-party Mermaid, filesystem EN/HU i18n, local search and a custom `<InterviewPrep>`
component. AI providers (Claude, Gemini, OpenAI, local/Ollama) sit behind a ~200-line adapter interface
routed by a YAML policy; the published site never depends on any of them. Drift detection is deterministic:
generated pages record content hashes of their sources; CI flags and regenerates only what changed. The
whole system is files, one static site, and CI jobs — operable by one engineer.

## 2. HU: Vezetői összefoglaló

Ez az architektúra egyetlen GitHub repository-ból épít szabályozott dokumentációs ökoszisztémát. A kanonikus
tudás — architektúra-leírások, ADR-ek, runbookok, fejlesztői útmutatók, Mermaid-diagramok — ember által
karbantartott Markdown a `docs/source/` alatt. Az AI-generáló réteg kizárólag GitHub Actions-ben és helyi
CLI-ben fut: a kanonikus bizonyítékokból származtatott nézeteket készít (toborzói oldalak, interjú-felkészítő
szekciók, kérdés-oldalak) a `docs/generated/` alá — mindig sémával validált feladat-szerződéseken keresztül,
mindig pull requestként, amelyet ember hagy jóvá. A publikáló alap a **Docusaurus 3.x** (a hat platform
súlyozott összevetésének győztese, 88,6/100): beépített Mermaid, fájlrendszer-alapú angol/magyar i18n, helyi
kereső, és egyedi `<InterviewPrep>` komponens. A modellek (Claude, Gemini, OpenAI, helyi) vékony adapter
mögött, YAML-szabályzattal routolva érhetők el; a publikált oldal egyikőjüktől sem függ. Az elavulás-észlelés
determinisztikus: a generált oldalak tárolják forrásaik tartalom-hash-eit, a CI csak a változás által
érintett oldalakat generálja újra. A teljes rendszer fájlokból, egy statikus oldalból és CI-feladatokból áll
— egyetlen mérnök által üzemeltethető.

## 3. Problem Statement

Project knowledge lives in code and scattered docs; keeping documentation current, audience-appropriate
(developer vs recruiter vs interviewer) and trustworthy is manual and unreliable. Existing platforms either
lock content into SaaS (GitBook, Mintlify) or provide no AI-derived-view lifecycle at all (pure SSGs).
Needed: Git-canonical docs with a controlled AI transformation layer that cannot corrupt canon, cannot
fabricate claims, and is never required just to read the docs.

## 4. Goals

Git as single source of truth; structural canonical/generated separation; evidence-grounded AI views
(recruiter, interview, special questions); provider-independent model access incl. local; deterministic
drift detection and incremental regeneration; PR-gated persistence with provenance; static publishing with
Mermaid, EN/HU, search; one-engineer operability.

## 5. Non-goals

Runtime AI chat over docs (deferred, isolated if ever built); enterprise identity/SSO (Harden-phase option);
multi-repo knowledge federation; WYSIWYG editing for non-technical authors; real-time collaboration;
replacing code review or engineering judgment.

## 6. Architectural Principles

P1 Files over services. P2 Static-first: readers never wait on AI. P3 AI writes only through PRs. P4
Deterministic checks before AI judgment. P5 Contracts over prompts. P6 Provenance on every derived artifact.
P7 Provider independence, local-capable. P8 Every component must beat a simpler alternative (recorded per
component). P9 One engineer can operate, debug and evolve the whole system.

## 7. Chosen Documentation Foundation

**Docusaurus 3.x** with `future.faster` (Rspack, SSG worker threads) and `future.v4` rehearsal flags.
Multi-instance docs plugin: instance `source` → `/docs`, instance `generated` → `/views`.
First-party `@docusaurus/theme-mermaid`; `@easyops-cn/docusaurus-search-local`; filesystem i18n (`en`, `hu`).

## 8. Why It Won

Highest weighted score (88.6/100) AND sole platform passing every critical constraint: repo-files-only
content model [VERIFIED-REPO]; multi-instance docs plugin gives structural (not conventional)
canonical/generated separation, dogfooded upstream [VERIFIED-REPO]; frontmatter accepts unknown keys so the
provenance contract passes validation [VERIFIED-REPO]; global MDXComponents lets generated pages use
`<InterviewPrep/>` without imports [VERIFIED-REPO]; first-party Mermaid ≥11 [VERIFIED-REPO]; static output
self-hosts anywhere; MIT; active core (3.10.2, 2026-07) versus MkDocs/Material's maintenance cliff.
Full reasoning: `../02_comparison/decision_matrix.md`.

## 9. Runner-up

Raw score: Mintlify (85.0) — rejected on the provider-independence principle (vendor build/serve plane,
Enterprise-gated self-hosting/static export). Constraint-adjusted: MkDocs+Material (83.8) — viable fallback
only version-pinned with an exit date before Material's 2026-11-05 support cutoff. Re-evaluation candidate:
Zensical at 1.0 + plugin API + multi-language content (trigger in ADR-002).

## 10. Decision Boundary

The weighted model guides; constraints decide. Had Docusaurus not led the raw ranking, the constraint set
(static-first §9, self-hosting, canonical separation, component extensibility) would still have selected it;
no override was needed. Documented sensitivity analysis shows the decision robust to reasonable reweighting.

## 11. Information Architecture

Two planes, numbered canonical taxonomy, generated views mirroring audience needs — full tree, naming rules,
metadata schema and conventions in `content_architecture.md`. Summary:

```
docs/source/    00-overview … 15-ai-workflows   (canonical, human-owned)
docs/generated/ recruiter/ interview/ questions/ role-specific/ summaries/  (derived, bot-authored)
docs/diagrams/  c4/ sequence/ workflows/ deployment/  (.mmd sources, canonical)
```

## 12. GitHub Repository Architecture

Single repo: `docs/`, `src/components/` (InterviewPrep, EvidenceLink), `prompts/`, `contracts/`, `schemas/`,
`scripts/` (pipeline), `ai/` (adapters+router), `.github/workflows/`, `docusaurus.config.ts`, `sidebars/`.
CODEOWNERS: `docs/source/**` → engineer/architecture owners; `docs/generated/**` → docs-bot PRs but human
approval enforced by branch protection; `prompts/**`+`contracts/**` treated as code (they steer AI).

## 13. Canonical Knowledge Model

Canonical page = Markdown/MDX + frontmatter contract (`schemas/document.schema.json`): `id` (unique, stable),
`title`, `type: canonical`, `audience[]`, `sources[]` (repo paths this page describes), `owners[]`,
`related[]` (doc ids), `ai_generation: {allowed, derived_pages[]}`, `last_validated`. Canonical pages change
only via human PRs; CI validates schema, links, Mermaid on every PR.

## 14. Generated Knowledge Model

Generated page = MDX + provenance frontmatter: `type: generated`, `generated: true`, `generation:
{contract, contract_version, source_documents: [{id, path, content_hash}], provider, model, generated_at,
prompt_version, approval_status}`. Lifecycle: draft (bot branch) → in-review (PR) → approved (merged) →
stale (hash mismatch flagged by CI) → regenerated (new PR). Generated pages are deletable at any time
without touching canon — regeneration is always possible from sources.

## 15. AI Generation Architecture

Generation plane = Python scripts invoked by Actions or locally. Flow: contract load → context assembly
(Level-1 retrieval) → prompt render (versioned template) → router → provider adapter → output parse against
contract schema → deterministic gates (links, Mermaid, evidence citations present) → provenance stamp → PR.
No agent framework; no autonomous loops; one model call per artifact plus at most one repair retry.
Full detail + task contract catalog: `ai_architecture.md`.

## 16. Model Routing

`ai.config.yaml` maps task → provider chain with routing criteria (privacy class, context size, structured
output need, cost tier). `private_content → local` is enforced by the router, not convention. Fallback chain
on provider error; hard fail (no silent provider swap) for privacy-constrained tasks. Diagram:
`diagrams/model_routing.mmd`.

## 17. Context / Retrieval Architecture

Level 1 (adopted): deterministic file selection — contract-named files + frontmatter `sources`/`related`
closure + `git grep` keyword expansion; context budget enforced by priority truncation.
Level 2 (boundary: >~1,500 pages or measured grounding failure): build-time full-text index reused from the
search plugin. Level 3 (embeddings) and Level 4 (hybrid/rerank): only on documented retrieval-quality
failure; decision recorded in ADR-006. No vector database in MVP — the corpus is hundreds of pages, and
grep+metadata is auditable.

## 18. Recruiter View

`docs/generated/recruiter/` — three depths from one evidence base: 30-second summary, 2-minute hiring-manager
summary, technical deep dive; every claim carries an `<EvidenceLink>` to a canonical page or repo path.
`GenerateRecruiterPage` contract prohibits: unevidenced technologies, invented metrics, seniority claims.
CI evidence gate: every named technology must appear in the cited sources. Design detail in
`ai_architecture.md` §Recruiter; flow in `diagrams/flow_recruiter_generation.mmd`.

## 19. Interview Preparation

`<InterviewPrep>` MDX component renders a co-located generated data file (elevator pitch, technical
explanation, concepts, design decisions, trade-offs, likely questions, example answers, evidence links).
Canonical pages opt in via frontmatter `ai_generation.derived_pages: [interview]`; CI generates
`docs/generated/interview/<id>.interview.json` + a stub MDX page; the component also embeds at the bottom of
the canonical page's `/views` twin — the canonical file itself is never edited by the bot. Build-time only
(AD-11); hybrid rejected as unnecessary.

## 20. Special Question Workflow

Trigger: `workflow_dispatch` form or `question` label on an issue. Pipeline: classification (contract
selection) → retrieval → generation → validation → **preview PR** with rendered page. Lifecycle decision:
persist **only via approved PR** (safest + simplest); unapproved drafts expire with branch deletion (30
days); merged pages regenerate on source-hash drift like all generated content. Auto-persist and
temporary-page modes were rejected: they either bypass review or create a second content lifecycle.
Flow: `diagrams/flow_special_question.mmd`.

## 21. Mermaid Architecture

All diagrams are fenced ```mermaid blocks or `.mmd` files under `docs/diagrams/` imported by reference.
Rendered client-side by first-party theme (accepted trade-off: no-JS readers see code, which is itself
readable). CI compiles every diagram with mermaid-cli (headless Chromium, sandboxed) — a diagram that does
not compile blocks merge. AI may propose diagram updates only via `UpdateMermaidDiagram` contract.

## 22. GitHub Automation

Ingestion: push/PR → `detect_changes` (git diff + frontmatter dependency manifest) → classification
(canonical / code-with-doc-impact / generated) → hash comparison → stale set → targeted regeneration jobs →
validation → PR. Manifest (`.docs-manifest.json`, build artifact of frontmatter) maps source paths → dependent
docs → dependent generated pages, so `src/api/` change → architecture page flagged → recruiter+interview
derivatives flagged. Full pipeline + workflow specs: `automation_architecture.md`;
diagram: `diagrams/flow_git_change_to_docs.mmd`.

## 23. Drift Detection

Deterministic first: (a) generated-page source hashes vs current content; (b) canonical `sources[]` paths vs
git diff — code changed but no doc change ⇒ PR label `docs-drift-suspect` + checklist comment;
(c) `last_validated` age report (advisory). AI-assisted change classification is an optional advisory layer
(SummarizeRepositoryChange contract), never merge-blocking. Detail: `automation_architecture.md` §Drift.

## 24. Security Architecture

Six trust zones, thirteen modeled threats (prompt injection, MDX code execution, Mermaid XSS, pwn-request CI
patterns, supply chain, secret leakage, misinformation, cross-provider exposure), least-privilege token
blocks, provider data-handling policy, incident runbooks. Core stance: no runtime backend, human-gated
generation PRs, instruction/data separation, link allowlist, pinned actions + lockfiles.
Full document: `security_architecture.md`; boundary diagram: `diagrams/trust_boundaries.mmd`.

## 25. Deployment

Mode B (default): GitHub Actions build → GitHub Pages, cloud AI APIs in CI.
Mode A (minimal self-hosted): same artifact on any static server; generation via local CLI + local model.
Mode C (privacy-oriented): local model (Ollama/OpenAI-compatible) for all generation; self-hosted static
serving; no content leaves the machine. Shared: identical repo, build, artifact — modes differ only in
`ai.config.yaml` routing and hosting target. Diagram: `diagrams/deployment.mmd`.

## 26. Observability

Right-sized: CI job status + PR annotations are the primary signals; generation jobs emit a JSON run report
(tokens, provider, gates passed) attached to the PR; site availability via host status + a scheduled
link-check workflow; no metrics stack in MVP (Harden option: usage analytics, structured logs to a file).

## 27. CI/CD

PR: markdownlint → frontmatter schema → internal links → Mermaid compile → dependency/drift analysis →
security checks (secrets scan, pinned-action audit) → `docusaurus build` → preview deploy (PR artifact) →
human review → merge. Main: production build → Pages deploy → smoke test (HTTP 200 + search index present +
sampled pages). Generation workflows are separate, manually or drift-triggered, never in the read path.
Workflow specs: `automation_architecture.md`; diagram: `diagrams/flow_publishing.mmd`.

## 28. Cost Architecture

Software $0 (MIT). Hosting $0 (GitHub Pages) to ~$5-20/mo (small static host). CI: minutes within free tier
at this scale. AI: metered per generation event only — bounded by incremental regeneration (only stale pages)
and contract-limited context; local mode $0 marginal. Predictable-cost knob: `ai.config.yaml` cost tiers.

## 29. Risks

Top risks: MDX strictness breaking AI output (gate: build in CI, repair retry); prompt injection via repo
content (delimiting + human gate + allowlist); reviewer fatigue on generation PRs (batching, small diffs,
run reports); Docusaurus major upgrades (Node/React pinning, `future.v4` rehearsal); solo-operator bus factor
(everything is documented files; system degrades to a plain static site if pipeline is ignored); provider
API drift (thin adapters, contract tests); i18n divergence (EN-canonical rule, fallback). Full risk tables:
per-threat in `security_architecture.md`, delivery risks in `implementation_roadmap.csv`.

## 30. ADR Summary

ADR-001 GitHub as source of truth · ADR-002 Docusaurus as framework (runner-up + revisit triggers) ·
ADR-003 canonical/generated structural separation · ADR-004 thin provider abstraction, no framework ·
ADR-005 generated content persists only via PR · ADR-006 Level-1 retrieval with explicit escalation
boundary · ADR-007 Mermaid-as-code with CI compilation gate · ADR-008 build-time AI over runtime AI ·
ADR-009 GitHub Pages static deployment with mode variants. All in `ADRs/`.

## 31. MVP / Scale / Harden

Phase 1 MVP: repo + taxonomy + metadata schema + CI validation + one provider adapter (+local) +
GenerateRecruiterPage + GenerateInterviewPrep + PR approval + Pages publishing.
Phase 2 Scale: all four providers + routing policy, special-question workflow, automatic drift flagging,
role-specific views, HU locale rollout, search tuning.
Phase 3 Harden: audit trail on generation runs, provider failover drills, stricter policy gates, optional
analytics, Level-2 retrieval if boundary trips, private-site auth only if needed.
Milestones with objectives/deliverables/dependencies/complexity/exit criteria: `implementation_roadmap.csv`.

## 32. PoC Description

`../05_poc/` — runnable Docusaurus starter demonstrating: canonical architecture page with Mermaid;
recruiter + interview generated pages with full provenance frontmatter; `<InterviewPrep>` component;
provider abstraction (4 adapters + router, dry-run capable without keys); task contracts + prompts + JSON
schema; `detect_changes` / `generate_page` / `validate_docs` scripts; two GitHub workflows; `.env.example`.
Validation results (executed builds/tests): `../04_validation/validation_report.md`.

## 33. Migration Checklist

1. Create repo from PoC skeleton; 2. Move existing docs into taxonomy, add frontmatter (script-assisted);
3. Convert diagrams to Mermaid; 4. Enable CI validation (advisory → blocking after cleanup); 5. Configure
CODEOWNERS + branch protection; 6. Add provider key(s) as Actions secrets or configure local endpoint;
7. Run first recruiter/interview generation, review, merge; 8. Enable Pages; 9. Enable drift detection;
10. Document operator runbook; 11. (Optional) enable HU locale; 12. Retire legacy docs locations.

## 34. MEGOLDÁS

One repo. Two content planes. AI writes only via reviewed PRs, grounded in hashed canonical evidence, routed
through a thin provider layer that includes a local model. Docusaurus builds it all into one static,
searchable, bilingual-capable site that works even if every AI provider on Earth is down.

## 35. HU: MEGOLDÁS

Egy repository. Két tartalmi sík: kanonikus (ember által birtokolt) és generált (AI által származtatott,
strukturálisan elkülönítve). Az AI kizárólag ellenőrzött pull requesteken keresztül ír, hash-elt kanonikus
bizonyítékokra alapozva, vékony szolgáltató-absztrakción át — helyi modellel is működik. A Docusaurus
mindebből egyetlen statikus, kereshető, kétnyelvű oldalt épít, amely akkor is elérhető marad, ha minden
AI-szolgáltató elérhetetlen. A rendszer fájlokból és CI-feladatokból áll; egyetlen mérnök képes üzemeltetni,
hibát keresni benne és továbbfejleszteni.
