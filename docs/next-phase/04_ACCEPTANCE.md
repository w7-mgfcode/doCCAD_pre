# 04 — Next-Version Acceptance Matrix & Journey Map

Status: target specification for the next Antigravity run (Phases 0–2) and the later Phase 3.
Shape follows `prototype/planning/ACCEPTANCE.md`. Plan items (`P0-…`, `P1-…`, `P2-…`) are defined in
`03_NEXT_VERSION_PLAN.md`; every "Verification evidence" cell names an executable command or test class,
or an owner-observed GitHub result. New requirements use the prefix **NV-REQ-** and never reuse an archive
ID (next free archive REQ is REQ-017; this pack allocates none).

A requirement is **accepted** only when its evidence was produced in the run and logged in
`prototype/planning/PROGRESS.md` §Evidence log (command, exit code, key output line, date). "Expected
failure" is not acceptance.

---

## 1. Archive requirements (REQ-001…016) — next-version acceptance

| ID | Title & scope | Next-version implementation path | User journey | Verification evidence |
|---|---|---|---|---|
| **REQ-001** | Six-platform research | Unchanged: `docs/source/architecture/platform-research.md` | J1 | `npm run validate` exit 0 |
| **REQ-002** | Weighted decision model | Unchanged: `adr-002-docusaurus-foundation.md`; Node aligned to ADR-002 (P0-03) | J1 | `npm run build` exit 0 on Node ≥24.14 |
| **REQ-003** | Git/GitHub source of truth | GitHub remote, all changes via PR (P1-01, P1-04) | J3, J4 | Owner-observed: ruleset active; CI check required on `main` |
| **REQ-004** | Structural canonical/generated separation | Plane checks + CI path guard for `docs-gen/*` branches (P1-01); production filter (P0-11) | J3 | `TestPlaneSeparation`; CI guard rejects a fixture PR touching `docs/source/` |
| **REQ-005** | Thin provider abstraction | Narrow fallback, one repair retry (P0-09); structured output per adapter (P2-02) | J6 | `TestRouterFallbackSemantics`, `TestRepairRetry`, `TestAdapterRequestShapes` |
| **REQ-006** | Static reads without AI | Pages deploy of the production build (P1-03) | J1 | `npm run build` with no keys; owner-observed Pages smoke step green |
| **REQ-007** | Level-1 deterministic retrieval | Unchanged design; question prompt fixed (P0-05) | J3 | `TestDeterministicRetrievalAndGeneration`, `TestQuestionPromptRendering` |
| **REQ-008** | Ingestion & incremental regeneration | Executable regeneration plan (P0-07); weekly drift job (P1-07) | J4 | `TestRegenerationPlanExecutable`; `npm run detect` → `stale generated: 0` |
| **REQ-009** | Provenance & hash drift | Honest `generation_mode` and model stamp (P0-06) | J4, J6 | `TestInvalidProvenance`, `TestGenerationModeStamp` |
| **REQ-010** | Evidence-grounded recruiter views | Live recruiter path valid (P0-04); grounding + named-entity gate (P2-06); truthful content (P0-13) | J2 | `TestLivePagePipeline`, `TestGroundingGate` |
| **REQ-011** | Interview prep component | Live interview path valid (P0-04); data loaded without MDX import (P0-12) | J2 | `TestLivePagePipeline`; `TestMdxRestrictionGate`; browser check of an interview page (P0-15) |
| **REQ-012** | Special-question workflow | Prompt carries question (P0-05); persistence as draft (P0-08); dispatch → bot PR → approval (P1-05, P1-06) | J3 | `TestQuestionPersistenceGovernance`, `TestApprovalRecord`; owner-observed bot PR |
| **REQ-013** | EN/HU bilingual | HU landing, navbar, footer, search (P0-14) | J1 | `build/hu/index.html` contains HU hero text; `build/hu/search-index.json` exists; HU fallback behaviour recorded |
| **REQ-014** | Anti-overengineering | No new services; new packages only with owner approval | all | `git diff` of `package.json` / `requirements.txt` matches approved list in PROGRESS.md |
| **REQ-015** | Runnable validated system | Evidence log, `VALIDATION.md`, `DEMO.md`, `LIMITATIONS.md` (P0-01, P0-15, P0-16) | J7 | Phase gate green; full suite with zero expected failures |
| **REQ-016** | Security architecture | T3, T4, T5, T6, T12 gates (P0-10, P0-12); CI hardening (P1-01); injection fixtures (P2-07) | J5 | `TestMdxRestrictionGate`, `TestExternalLinkAllowlist`, `TestContextSecretScan`, `TestPrivateChainConfig`, `TestPrivateContentExclusion`, `TestPromptInjectionFixtures` |

## 2. New requirements (NV-REQ)

| ID | Title & scope | Implementation path | User journey | Verification evidence |
|---|---|---|---|---|
| **NV-REQ-001** | Evidence-backed progress: no item is done without a logged command, exit code and date; no check is documented without an implementing script and test | `prototype/planning/PROGRESS.md` §Evidence log, §Tried-and-failed, §Blocked (P0-01) | J7 | Every ticked PROGRESS item has an evidence row; reviewer spot-reruns three rows |
| **NV-REQ-002** | Declared Python requirements; CI never runs degraded validation | `prototype/requirements.txt`; `DOCCAD_REQUIRE_JSONSCHEMA=1` (P0-02) | J7 | `TestValidatorDependencyMode` |
| **NV-REQ-003** | Supported runtime | `engines.node >=24.14`, `.nvmrc` 24 (P0-03) | J7 | engines check command in P0-03; CI runs Node 24 |
| **NV-REQ-004** | Live pipelines emit schema-valid output for recruiter, interview and question contracts | P0-04, P0-05 | J2, J3 | `TestLivePagePipeline`, `TestQuestionPromptRendering` |
| **NV-REQ-005** | Provenance states the real generation mode and returned model | P0-06 | J6 | `TestGenerationModeStamp` |
| **NV-REQ-006** | Regeneration plan is executable as written | P0-07 | J4 | `TestRegenerationPlanExecutable` |
| **NV-REQ-007** | Fallback only on transport errors; exactly one repair retry | P0-09 | J6 | `TestRouterFallbackSemantics`, `TestRepairRetry` |
| **NV-REQ-008** | Private content never reaches the production build or its search index; absent `visibility` means private | P0-10 (T12) | J5 | `TestPrivateContentExclusion`; marker text absent from `build/` incl. `search-index.json` |
| **NV-REQ-009** | Production filter output validates; no page claims approval it did not receive | P0-11 | J3 | `TestProductionFilterValidity`; `build_filter --mode production && validate_docs.py` exit 0 |
| **NV-REQ-010** | Archive security gates exist: MDX restriction, external-link allowlist, Mermaid strict, context secret scan, private-chain config check | P0-12 | J5 | the four test classes in P0-12; no `import`/`export` under `docs/generated/` |
| **NV-REQ-011** | Reader-facing content claims only implemented behaviour | P0-13 | J1, J2 | claim → file → test table in PROGRESS.md |
| **NV-REQ-012** | Hungarian landing, navigation and search | P0-14 | J1 | P0-14 acceptance |
| **NV-REQ-013** | Browser-verified journeys with recorded evidence | P0-15 (`/browser` in the Antigravity 2.0 app) | J1–J3 | `prototype/VALIDATION.md` rows with existing screenshot paths; NOT RUN when unavailable |
| **NV-REQ-014** | CI gate: least privilege, SHA-pinned actions, no `pull_request_target`, generation-path guard | P1-01 | J3, J4 | local YAML/pin/grep checks in P1-01; owner-observed green check |
| **NV-REQ-015** | Publication to GitHub Pages via OIDC with a smoke test | P1-02, P1-03 | J1 | owner-observed Pages URL; smoke step green |
| **NV-REQ-016** | Production approval is a recorded human act (`approval_record`), enforced by CI | P1-04, P1-05 (proposal D6, owner confirmation E3) | J3 | `TestApprovalRecord`; ruleset requires code-owner review |
| **NV-REQ-017** | Generation runs as `workflow_dispatch` → bot branch → PR with run report | P1-06 | J3, J4 | owner-observed PR touching only `prototype/docs/generated/**` |
| **NV-REQ-018** | Mermaid diagrams compile in CI | P1-08 (owner approval of dependency) | J4 | broken-diagram fixture fails the gate |
| **NV-REQ-019** | Structured output per provider, validated locally against repo schemas | P2-01, P2-02 | J6 | `TestProviderSchemaDerivation`, `TestAdapterRequestShapes` |
| **NV-REQ-020** | Resilient, budgeted provider calls; usage logged, payloads and keys never logged | P2-03, P2-04, P2-05 | J6 | `TestSamplingOptIn`, `TestHttpRetryPolicy`, `TestRunBudget` |
| **NV-REQ-021** | Grounding gate and prompt-injection fixtures | P2-06, P2-07 | J5, J6 | `TestGroundingGate`, `TestPromptInjectionFixtures` |
| **NV-REQ-022** | At least one live provider call validated end to end | P2-08 (owner-executed) | J6 | `VALIDATION.md` row by the owner; NOT RUN until then |
| **NV-REQ-023** | Pinned external repository evidence (Phase 3, conditional on NV-SUP-2) | `03_NEXT_VERSION_PLAN.md` §7 | J8 | Phase 3 acceptance list in §7 |

## 3. User journeys

### J1 — Reader (EN and HU) on the published site
1. Opens the Pages URL; the landing page renders in English, and in Hungarian at `/hu/`.
2. Navigates canonical docs (`/docs/…`), sees Mermaid diagrams render.
3. Searches in either language and gets results from the local index.
4. Finds no private page and no unapproved generated page in navigation or search.

### J2 — Recruiter and interviewer
1. Opens `/views/recruiter/project-overview`; switches 30-second, 2-minute and deep-dive modes.
2. Follows `<EvidenceLink>` citations into canonical pages; every claim resolves.
3. Opens an interview page; concepts, decisions, trade-offs, questions and answers render from validated
   data, each decision citing evidence.

### J3 — Question to approved, published page
1. Contributor dispatches `generate.yml` with a question (or runs `generate_question.py` locally).
2. A `docs-gen/*` branch and PR appear with a run report (evidence, gates, provider, model, usage).
3. CI runs on the PR; the path guard confirms only generated content changed.
4. The owner reviews, records approval (`approval_record`), approves as code owner, and merges.
5. `publish.yml` builds the production site; the page is live; drafts and demo approvals are not.

### J4 — Contributor drift and targeted regeneration
1. A canonical page changes in a PR; `detect` lists exactly its dependents as stale.
2. The regeneration plan's entries run as written; a regeneration PR follows J3.
3. Unrelated generated pages are unchanged.

### J5 — Security and failure boundaries
1. A private page never appears in the production build or search index.
2. A private task with the local provider disabled hard-fails; no cloud call occurs.
3. Generated MDX with an `import`, a non-allowlisted link, or an unknown component is rejected before build.
4. A prompt payload containing a key-like string aborts before any provider call.
5. An injected instruction inside evidence cannot produce output that passes schema, allowlist and
   grounding gates.

### J6 — Operator runs live generation
1. Keys and `AI_MODEL_*` are set by the owner only; spend caps exist at the provider.
2. A live call returns structured output validated locally; the page records `generation_mode: production`
   and the returned model string.
3. A 429 with `Retry-After` is retried; a spend-cap 429 or a 401 stops immediately; usage is logged
   without payloads.
4. Exceeding the per-run budget aborts the run.

### J7 — Maintainer resumes an interrupted run
1. Opens `prototype/planning/PROGRESS.md`; sees the last completed item, its evidence row, blocked items and
   tried-and-failed attempts.
2. Runs `git status`, `npm run validate`, `npm run test`; state matches the log.
3. Continues with the next open item in a fresh conversation.

### J8 — External evidence (Phase 3, conditional)
1. Owner adds a source with repo, full commit SHA, sparse paths and license to `external-sources.yaml`.
2. Generation cites external evidence with `{repo, commit, path, content_hash}`.
3. Bumping the commit marks dependents stale; an unlicensed source or a planted secret is refused.
