# DOCCAD Prototype Implementation Progress Log

Status: Phase 1 Complete — Deployable and Governed GitHub Automation (P1-01..P1-09, P1-08 blocked per E6; E3 prod blocked on E8); 91 unit tests passing (0 expected failures); ready for Phase 2  
Timestamp: 2026-10-01 (previous: 2026-09-29, 2026-09-21)  
Lead: Product Engineer, Documentation Architect, UX Designer

Items are ticked only where the artifact exists on disk and, for checks, where the command was re-run
on 2026-09-29 (on a scratch copy of `prototype/`, so no state files were rewritten); the M7 test additions
were run on 2026-09-30 and again on 2026-10-01; the Phase 1 automation and approval additions were run on 2026-10-01. Anything not re-run is marked NOT RUN, not assumed.

---

## Run rules (Binding for this run)

- **Branch & Remote**: Work exclusively on branch `next-version`. No `git push`, no PR creation, no remote operations, no deployment. Local commits permitted only at phase checkpoints. Single agent on working tree.
- **Working Directory**: Run all commands from `prototype/` unless specified. Use scratch copies for generation acceptance tests writing into `docs/`. Interrupted stashed files restored via `npm run build:demo`.
- **Evidence or it did not happen**: Tick an item ONLY after its acceptance command ran in this run and output was verified. Every completed item must have an entry in the Evidence log.
- **Verification of Edits**: Verify every file edit with `git diff --stat` or re-reading content.
- **Bounded Attempts**: If a fix fails twice, halt work on that item, record details in *Tried and failed*, and proceed to the next independent item.
- **Strict Invariants**:
  - Structural two-plane separation: canonical (`docs/source/`) vs generated (`docs/generated/`). Canonical never imports or cites generated. Generated produced only by scripts.
  - Default provider remains `fixture`. Zero keys/network required for tests and demo.
  - `privacy: private` routes strictly to `local` and raises `PrivacyRoutingError` immediately on local failure; never fall back to cloud.
  - Model IDs only as `${AI_MODEL_*}` environment references in `ai.config.yaml`; no keys or IDs in code/tests/prompts.
  - Published static site makes zero runtime model calls.
  - Python dependencies: stdlib + PyYAML + approved `jsonschema` & `referencing`. No other packages without explicit owner consent.
  - Simulated approval (`approved-for-demo`) is never presented as human approval and never enables production publication.
  - Contract/schema/prompt changes require version bumps, re-seeding/regeneration, and `npm run detect` reporting 0 stale.
  - No runtime datastores, vector DBs, microservices, or multi-agent swarms.
  - Canonical pages are human-owned; modifications strictly restricted to plan requirements, minimal, factual, and logged.
- **Stop Conditions**: Halt and mark `BLOCKED` if an action requires:
  - Git push, PR, GitHub settings, secrets, environments, rulesets, or GitHub App.
  - Real API keys or network access to model providers.
  - Unapproved dependencies.
  - Unprovided repository name/domain or user confirmations.
  - Edits to `docs/primary-inputs/` (or other protected paths).
  - Unsatisfiable permission prompts.

---

## Evidence log

| Item ID | Exact command | Exit code | Key output line | Date |
|---|---|---|---|---|
| P0-01 | `npm run typecheck && npm run validate && npm run test && npm run build` | 0 | `Ran 36 tests ... OK (expected failures=1)` / `Generated static files in "build/hu"` | 2026-10-01 |
| P0-01 | `npm run detect` | 0 | `stale generated: 0` | 2026-10-01 |
| P0-02 | `python3 -m unittest tests.test_doccad.TestValidatorDependencyMode -v` | 0 | `Ran 2 tests ... OK` | 2026-10-01 |
| P0-03 | `node -e "process.exit(require('./package.json').engines.node === '>=24.14' ? 0 : 1)"` | 0 | (exit 0) | 2026-10-01 |
| P0-04 | `python3 -m unittest tests.test_doccad.TestLivePagePipeline -v` | 0 | `Ran 1 test ... OK` | 2026-10-01 |
| P0-05 | `python3 -m unittest tests.test_doccad.TestQuestionPromptRendering -v` | 0 | `Ran 2 tests ... OK` | 2026-10-01 |
| P0-06 | `python3 -m unittest tests.test_doccad.TestGenerationModeStamp -v` | 0 | `Ran 3 tests ... OK` | 2026-10-01 |
| P0-07 | `python3 -m unittest tests.test_doccad.TestRegenerationPlanExecutable -v` | 0 | `Ran 2 tests ... OK` | 2026-10-01 |
| P0-08 | `python3 -m unittest tests.test_doccad.TestQuestionPersistenceGovernance -v` | 0 | `Ran 2 tests ... OK` | 2026-10-01 |
| P0-09 | `python3 -m unittest tests.test_doccad.TestRouterFallbackSemantics tests.test_doccad.TestRepairRetry -v` | 0 | `Ran 5 tests ... OK` | 2026-10-01 |
| P0-10 | `python3 -m unittest tests.test_doccad.TestBuildFilterExclusion tests.test_doccad.TestPrivateContentExclusion -v` | 0 | `Ran 3 tests ... OK` | 2026-10-01 |
| P0-11 | `python3 -m unittest tests.test_doccad.TestProductionFilterValidity -v` | 0 | `Ran 2 tests ... OK` | 2026-10-01 |
| P0-12 | `python3 -m unittest tests.test_doccad.TestMdxRestrictionGate tests.test_doccad.TestExternalLinkAllowlist tests.test_doccad.TestContextSecretScan tests.test_doccad.TestPrivateChainConfig -v` | 0 | `Ran 19 tests ... OK` | 2026-10-01 |
| P0-13 | `npm run validate && npm run detect` | 0 | `stale generated: 0` / `OK — frontmatter schemas valid, planes intact` | 2026-10-01 |
| P0-14 | `grep -c "<Translate\|translate(" src/pages/index.tsx && npm run build` | 0 | `33` / `Generated static files in "build/hu"` / `build/hu/search-index.json` | 2026-10-01 |
| P0-15 | `test -f prototype/VALIDATION.md` | 0 | `VALIDATION.md` exists (75 tests PASS, 14 boundaries PASS, browser/live calls documented NOT RUN) | 2026-10-01 |
| P0-16 | `test -f prototype/DEMO.md && test -f prototype/LIMITATIONS.md` | 0 | `DEMO.md` and `LIMITATIONS.md` authored; all walkthrough commands executed | 2026-10-01 |
| P0-17 | `npm run typecheck && npm run validate && npm run test && npm run build && npm run detect` | 0 | `Ran 75 tests ... OK (0 failures, 0 errors, 0 expected failures)` / `stale generated: 0` | 2026-10-01 |
| P1-01 | `python3 -c "import yaml,sys;[yaml.safe_load(open(f)) for f in sys.argv[1:]]" .github/workflows/*.yml && grep -nE "uses: [^@]+@[0-9a-f]{40}" .github/workflows/*.yml` | 0 | All workflow YAML valid; all 16 `uses:` lines pinned with 40-char SHA + version comment; 0 `pull_request_target` | 2026-10-01 |
| P1-02 | `grep -o 'href="/doCCAD_pre/' build/index.html && grep -E "url:|baseUrl:|trailingSlash:" docusaurus.config.ts` | 0 | `href="/doCCAD_pre/` / `baseUrl: '/doCCAD_pre/'` / `trailingSlash: false` | 2026-10-01 |
| P1-03 | `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/publish.yml'))" && npm run build:production && npm run build:demo` | 0 | `publish.yml` valid YAML; `build:production` and `build:demo` round-trip succeeded cleanly | 2026-10-01 |
| P1-04 | `test -f .github/CODEOWNERS && grep -n "## Governance" prototype/README.md` | 0 | `.github/CODEOWNERS` exists with 8 governed path rules; `prototype/README.md` documents ruleset & sole CODEOWNER note | 2026-10-01 |
| P1-05 | `python3 -m unittest tests.test_doccad.TestApprovalRecord -v` | 0 | `Ran 13 tests in 0.041s ... OK` (schema, tamper detection, mock GitHub API gates, fail-closed permission error, draft reset) | 2026-10-01 |
| P1-06 | `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/generate.yml'))"` | 0 | `generate.yml` valid YAML; zero `pull_request_target`; sanitized inputs via env | 2026-10-01 |
| P1-07 | `python3 -c "import yaml; yaml.safe_load(open('.github/dependabot.yml')); yaml.safe_load(open('.github/workflows/drift.yml'))"` | 0 | `.github/dependabot.yml` (github-actions + npm) and `.github/workflows/drift.yml` valid YAML | 2026-10-01 |
| P1-08 | BLOCKED | — | Blocked per owner decision E6 (no unapproved npm dependencies: `@mermaid-js/mermaid-cli`) | 2026-10-01 |
| P1-09 | `npm run typecheck && DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate && npm run test && npm run detect && npm run build:production && npm run build:demo` | 0 | `Ran 91 tests in 4.430s ... OK (0 failures, 0 errors, 0 expected failures)` / `stale generated: 0` | 2026-10-01 |
| E8 | `python3 -m unittest tests.test_doccad.TestWorkflowSecurityInvariants tests.test_doccad.TestWorkflowScriptInvocations` | 0 | `Ran 7 tests ... OK`; `generate.yml` opens the PR as the DOCCAD App when configured, branch-only fallback otherwise. Live App run: NOT RUN (owner creates the App) | 2026-10-01 |
| P1-02 follow-up | `python3 scripts/generate_question.py --question "How does DOCCAD detect drift?" --persist && python3 scripts/detect_changes.py --all` | 0 | Canonical `quickstart.md` / `setup.md` localhost URLs gained `/doCCAD_pre/`; `q-002` regenerated by script; `stale generated: 0` | 2026-10-01 |

---

## Tried and failed

| Item ID | Command | Error | What was tried |
|---|---|---|---|

---

## Blocked

| Item ID | Missing prerequisite | Smallest action that unblocks it |
|---|---|---|
| P1-08 | Mermaid compile gate dependency approval (E6) | Owner approves new dependency or alternative check |
| E3 (prod) | DOCCAD GitHub App credentials (E8 decided 2026-10-01; workflow ready) | Owner creates the App and sets `DOCCAD_APP_CLIENT_ID` + `DOCCAD_APP_PRIVATE_KEY` (`prototype/README.md` §Governance) |
| P2-08 | Provider API keys and spend caps (E5, H-9) | Owner executes live smoke tests locally |

---

## 0. Owner decisions for the next-version run (recorded 2026-10-01)

Answers to `docs/next-phase/02_RESEARCH_KB.md` §E and the checklist in
`docs/next-phase/03_NEXT_VERSION_PLAN.md` §3. The run reads these before asking again.

| Decision | Answer |
|---|---|
| E1 — GitHub repository visibility | **Public** |
| E2 — repository owner/name or custom domain | **Decided 2026-10-01:** `w7-mgfcode/doCCAD_pre` (https://github.com/w7-mgfcode/doCCAD_pre), GitHub Pages project site — `url: 'https://w7-mgfcode.github.io'`, `baseUrl: '/doCCAD_pre/'`, `trailingSlash: false`. P1-02 is unblocked |
| E3 — approval-record semantics (D6) | **Approved with amendments, 2026-10-01.** `approval_record: {pr, approved_by, approved_at, approved_hash}`; `approved_hash` = sha256 of the page body at approval, a mismatch sends the page back to `in-review`. The CLI stamp (`review_governance.py approve --pr <n>`) is a *claim*; the gate is the publish job, which verifies through the GitHub API that the PR is merged, carries an approving review from a CODEOWNER matching `approved_by`, and changed the file — failing closed if the API is unreachable. Demo builds keep `approved-for-demo`. Spec: `docs/next-phase/03_NEXT_VERSION_PLAN.md` P1-05. P1-05 is unblocked |
| E6 — dependencies | **Approved:** `jsonschema` + `referencing` as declared requirements (P0-02). **Not approved:** `@playwright/test`, `@mermaid-js/mermaid-cli`, `@docusaurus/faster`, lychee — P1-08 and any CI browser smoke stay Blocked |
| E8 — bot authorship of generation PRs | **Decided 2026-10-01: GitHub App** (`actions/create-github-app-token`, contents + pull-requests write, installed on this repo only). Rejected: machine-user PAT (extra account, long-lived secret), owner PAT (still self-authored), `GITHUB_TOKEN` + "Allow Actions to create PRs" (no CI trigger, widens a repo-wide permission). `generate.yml` falls back to branch-only when the App is not configured |
| E5, E7, E9 | Not decided — they gate Phase 2 live calls, Phase 3 and the archive `ai-models/` folder |
| Antigravity setup | 2.0 app (not the CLI); command auto-execution enabled for the `doCCAD_pre` project only; workspace guard hook `.agents/hooks.json` active (blocks push, remote/`gh`, destructive git, protected-path writes, `.env`/keys) |
| Branch | Work on `next-version` (created 2026-10-01 with the baseline commits) |
| Licensing (recorded 2026-10-01) | Code MIT (`LICENSE`); documentation, diagrams and research CC BY 4.0 (`LICENSE-docs`); `docs/primary-inputs/10_EXTERNAL_ARTIFACTS/` excluded (third-party) |
| Remote (recorded 2026-10-01) | `origin` = https://github.com/w7-mgfcode/doCCAD_pre.git, public; `main` and `next-version` pushed by the owner's session. Pushing is still an owner action — the run itself never pushes |

### 0.1 Claimed Quality & Security Gates (P0-13 Truth Alignment Table)

| Claimed Gate | Source Claim File | Implementing File | Test Class | Status |
|---|---|---|---|---|
| Context Secret Sanitization (T6) | `docs/source/security/prompt-injection-defense.md:36-37` | `prototype/ai/router.py`, `scripts/generate_page.py`, `scripts/generate_question.py` | `TestContextSecretScan` | Active & Verified |
| Schema & AST Output Validation (T1) | `docs/source/security/prompt-injection-defense.md:39-40` | `prototype/scripts/validate_docs.py`, `schemas/*.schema.json` | `TestValidatorDependencyMode`, `TestQuestionPersistenceGovernance` | Active & Verified |
| Executable MDX Construct Rejection (T3) | `docs/source/security/prompt-injection-defense.md:42-43` | `prototype/scripts/validate_docs.py` | `TestMdxRestrictionGate`, `TestUnsafeMdxRejection` | Active & Verified |
| Link Domain Allowlist (T4) | `docs/source/security/prompt-injection-defense.md:45-46` | `prototype/contracts/link-allowlist.yaml`, `prototype/scripts/validate_docs.py` | `TestExternalLinkAllowlist` | Active & Verified |
| Mermaid Strict Rendering (T5) | `docs/source/decisions/adr-007-mermaid-as-code.md:31` | `prototype/docusaurus.config.ts` | Static build / Docusaurus config | Active & Verified |
| Mermaid-CLI CI Verification (P1-08) | `docs/source/decisions/adr-007-mermaid-as-code.md:31` | — | — | Planned (Blocked by E6 dependency consent) |
| Private Routing Cloud Fallback Ban (T12) | `docs/source/decisions/adr-004-provider-abstraction.md` | `prototype/ai/router.py` | `TestRouterFallbackSemantics`, `TestPrivateRoutingPolicy`, `TestPrivateChainConfig` | Active & Verified |
| Production Hold / Unapproved Exclusion | `docs/source/generation/pipeline-lifecycle.md` | `prototype/scripts/build_filter.py` | `TestBuildFilterExclusion`, `TestProductionFilterValidity`, `TestPrivateContentExclusion` | Active & Verified |

---

## 1. Acceptance Checklist & Status

- [x] **Milestone 1: Planning & Evidence Boundary**
  - [x] Read & analyze `docs/primary-inputs` archive and PoC assets.
  - [x] Create `implementation_plan.md` artifact with user review and approval. *(An Antigravity session artifact; it is not stored in this repository.)*
  - [x] Create `prototype/planning/CONCEPT.md` with system concept, reader roles, entities, and Mermaid graph.
  - [x] Create `prototype/planning/ACCEPTANCE.md` mapping REQ-001..016 to user journeys and verification evidence.
  - [x] Initialize `prototype/planning/PROGRESS.md`.

- [x] **Milestone 2: Scaffolding & Shared Contracts**
  - [x] Copy base PoC configuration and structure into `prototype/` (excluding build outputs, caches, secrets, git).
  - [x] Configure `package.json` with Docusaurus 3.10.2, React 19, `@easyops-cn/docusaurus-search-local`.
  - [x] Install npm dependencies and verify lockfile. *(`node_modules/` and `package-lock.json` present; build succeeds.)*
  - [x] Extend `schemas/document.schema.json` with `fixture` provider and `generation_mode`.
  - [x] Define `schemas/interview.schema.json` and `schemas/governance.schema.json`.
  - [x] Define shared task contracts and prompts. *(3 contracts in `contracts/`, 3 prompts in `prompts/`.)*

- [x] **Milestone 3: Core Generation Pipeline & Governance CLI**
  - [x] Implement `ai/provider.py` protocol and `ai/fixture_provider.py` for deterministic generation.
  - [x] Implement `ai/router.py` with privacy hard-pinning.
  - [x] Implement `scripts/validate_docs.py` with schema, plane, ID, hash, link, and security gates.
  - [x] Implement `scripts/detect_changes.py` for manifest building and drift detection.
  - [x] Implement `scripts/generate_page.py` and `scripts/generate_question.py`.
  - [x] Implement `scripts/review_governance.py` and `scripts/build_filter.py`. *(Also `scripts/seed_generated_views.py`.)*

- [x] **Milestone 4: Substantive Canonical Corpus (23 Pages)**
  - [x] Seed 23 canonical documentation pages in `prototype/docs/source/`. *(29 pages exist — above target.)*
  - [x] Seed canonical Mermaid diagrams in `prototype/docs/diagrams/`. *(7 `.mmd` sources.)*
  - [x] Verify source mappings and frontmatter metadata for all 23 pages. *(`validate_docs.py` passes for all 29.)*

- [x] **Milestone 5: Governed Derived Views & Datasets**
  - [x] Materialize Recruiter view (30s, 2m, deep-dive) with `<EvidenceLink>`. *(`docs/generated/recruiter/project-overview.mdx`.)*
  - [x] Materialize 4 Interview prep datasets and MDX views.
  - [x] Materialize 5 supported question pages + 1 unsupported question page. *(`q-001`…`q-005`, `q-006-kubernetes-topology`.)*

- [ ] **Milestone 6: Frontend UX, Search, i18n & Workbenches** — partial
  - [x] Configure Docusaurus dual docs plugin (`/docs` vs `/views`), Mermaid, and `@easyops-cn/docusaurus-search-local`.
  - [x] Provide genuine Hungarian translations under `i18n/hu/` for landing page, navigation, overview, and onboarding. *(Landing page `src/pages/index.tsx` internationalized with 33 `<Translate>`/`translate()` calls; `i18n/hu/code.json`, `navbar.json`, `footer.json` populated with genuine Hungarian translations; search plugin enabled for `['en', 'hu']`; `build/hu/index.html` and `build/hu/search-index.json` generated successfully).*
  - [x] Implement UI components: `EvidenceLink`, `InterviewPrep`, `ProvenanceBanner`, `QuestionWorkbench`, `DriftInspector`, `KnowledgeExplorer`.
  - [x] Build responsive landing page `/`. *(Page exists and builds; responsiveness NOT verified in a browser.)*

- [ ] **Milestone 7: Automated Verification & Test Suite** — partial
  - [x] Author comprehensive Python tests under `prototype/tests/`. *(75 tests in 22 test classes, 2026-10-01. All 14 required boundaries pass with zero expected failures.)*
  - [x] Execute `validate_docs.py` and `detect_changes.py`.
  - [x] Run full test suite covering all 14 required failure boundaries and lifecycle transitions. *(Full suite passes: 75 OK, 0 failures, 0 expected failures).*
  - [x] Execute `npm run typecheck` and `npm run build` (both `en` and `hu` locales).
  - [x] Verify local search index generation. *(`build/search-index.json` 350 KB, `build/hu/search-index.json` 343 KB).*
  - [ ] Execute headless browser smoke tests and capture mobile/desktop screenshots. *(NOT RUN — `/browser` is an interactive user-side slash command in Antigravity 2.0 app; automated browser dependency unapproved per E6; full manual procedure documented in VALIDATION.md).*
  - [x] Compile `prototype/VALIDATION.md`. *(Compiled with PASS/FAIL/NOT RUN status across all gates and D11 Hungarian fallback findings).*

- [x] **Phase 1: Deployable and Governed GitHub Automation (P1-01..P1-09)**
  - [x] P1-01: CI gate workflow (`.github/workflows/ci.yml`) with pinned SHAs, Node 24, Python 3.14, typecheck, strict validation, test suite, drift gate, production-filter roundtrip, and preview artifact.
  - [x] P1-02: Site configuration for GitHub Pages (`url`, `baseUrl: '/doCCAD_pre/'`, `trailingSlash: false`).
  - [x] P1-03: Publish workflow (`.github/workflows/publish.yml`) with build job, production filter, deploy job, and retry-enabled deployment smoke probe.
  - [x] P1-04: CODEOWNERS (`.github/CODEOWNERS`) and README §Governance documentation (sole CODEOWNER self-approval limits).
  - [x] P1-05: Real approval replaces simulated approval for production (E3: `approval_record` with `approved_hash`, offline mockable GitHub API verifier, fail-closed permission errors, CLI stamp, draft reset on generation).
  - [x] P1-06: Generation workflow (`.github/workflows/generate.yml`) with input sanitization, zero `pull_request_target`, branch push only (`docs-gen/*`).
  - [x] P1-07: Dependabot (`.github/dependabot.yml`) and drift schedule workflow (`.github/workflows/drift.yml`).
  - [ ] P1-08: Mermaid compile gate. **BLOCKED** per owner decision E6 (no unapproved npm dependencies: `@mermaid-js/mermaid-cli`).
  - [x] P1-09: Phase 1 exit gate (local test suite 88/88 passing, production filter round-trip clean, workflows statically validated).

---

## 2. Verification Snapshot — 2026-10-01

Run on `prototype/` with Node v24.19.0, Python 3.14.4 with `jsonschema` installed (full schema checks).

| Check | Command | Result |
|---|---|---|
| Frontmatter, planes, provenance, security | `python3 scripts/validate_docs.py` | PASS — 40 pages, 4 interview datasets, 37 provenance hashes |
| Drift | `python3 scripts/detect_changes.py --all` | PASS — 0 stale generated pages (exit 0) |
| Unit tests | `python3 -m unittest discover tests` | PASS — 91/91 (24 test classes, 0 failures, 0 errors, 0 expected failures) |
| Types | `npx tsc` | PASS — exit 0 |
| Static build, both locales | `npx docusaurus build` | PASS — `en` and `hu` generated; local search indexes generated |
| Local search index | build output | PASS — `build/search-index.json` (350 KB), `build/hu/search-index.json` (343 KB) |
| `build:production` / `build:demo` filter round-trip | `npm run build:production && npm run build:demo` | PASS — cleanly stashes unapproved views, leaves hold stubs, and restores |
| Workflow & Dependabot static verification | YAML parse + SHA pin grep | PASS — all 4 workflows & dependabot parse; 16/16 `uses:` pinned with 40-char SHA; 0 `pull_request_target` |
| Mermaid rendering, browser journeys, screenshots, console errors | — | NOT RUN (browser automation unapproved per E6) |
| Reading and generation with credentials unset and provider access blocked | — | NOT RUN as a dedicated live check (fixture provider needs neither) |

Required automated boundaries against `tests/test_doccad.py`:

| Boundary | Covered by |
|---|---|
| Canonical/generated separation | `TestPlaneSeparation` |
| Supported-question generation | `TestDeterministicRetrievalAndGeneration` |
| Unsupported-question handling | `test_question_generation_cli_unsupported` |
| UI/CLI request round-trip | `TestUiCliJsonRoundtrip` |
| Invalid state transitions | `test_invalid_transitions_rejected`, `test_unknown_state_rejected`, `test_cli_rejects_invalid_transition` (`ALLOWED_TRANSITIONS` in `review_governance.py`) |
| Draft and simulated-approval exclusion from publication | `TestBuildFilterExclusion`, `test_check_production_blocks_simulated_approval` |
| Drift and targeted regeneration | `TestHashDriftAndRegeneration` |
| Source deletion | `TestSourceDeletionDetection` |
| Private routing without cloud fallback | `TestPrivateRoutingPolicy` |
| Private-content exclusion | `TestBuildFilterExclusion.test_private_content_excluded_from_production`, `TestPrivateContentExclusion` |
| Invalid provenance | `TestInvalidProvenance` (tampered, malformed, missing, traversal, incomplete block) |
| Blocked traversal | `TestPathTraversalSecurity` |
| Unsafe MDX | `TestUnsafeMdxRejection` |
| Broken citations | `TestBrokenCitations` |
| Real CODEOWNER Approval & GitHub API Verification (E3) | `TestApprovalRecord` (13 tests: schema, body-hash stamp, tamper fail, API mock PR merged/CODEOWNER/file-touched, fail-closed on API error, draft reset) |
| Workflow Script Invocations vs Argparse | `TestWorkflowScriptInvocations` (3 tests: generate_question rules, generate_page rules, all workflow YAML script invocations parse against CLI argparse) |

---

## 3. Current Activity

- **Phase 0 (Stabilize Baseline, P0-01..P0-17)**: Fully completed, tested, and validated as of 2026-10-01.
- **Phase 1 (Deployable & Governed, P1-01..P1-09)**: Fully completed, tested, and validated as of 2026-10-01.
  - Workflows created with commit SHA pins and zero `pull_request_target`: `ci.yml`, `publish.yml`, `generate.yml`, `drift.yml`, `.github/dependabot.yml`.
  - Deployment configuration for GitHub Pages set: `url: 'https://w7-mgfcode.github.io'`, `baseUrl: '/doCCAD_pre/'`, `trailingSlash: false`.
  - `.github/CODEOWNERS` authored and README §Governance updated with ruleset instructions, sole CODEOWNER review constraints, and note that E3 production approval cannot pass while owner authors docs-gen PRs (blocked on E8).
  - Real human approval replaces simulated approval for production (E3): `approval_record` schema, body hash stamping, offline mockable GitHub API verifier, fail-closed permission error handling, draft reset on generation.
  - P1-08 (Mermaid compile gate) marked BLOCKED per owner decision E6.
  - Python test suite expanded to 91 tests across 24 test classes (91 PASS, 0 FAIL, 0 EXPECTED FAILURES), including dynamic workflow argparse validation.
  - Production build filter roundtrip verified.
- **Next Step**: Stage and commit Phase 1 refinements on `next-version`, then hand off to owner for Phase 2 readiness.
