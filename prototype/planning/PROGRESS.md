# DOCCAD Prototype Implementation Progress Log

Status: In Progress — Milestones 1–5 complete; 6 and 7 partial; 8 started  
Timestamp: 2026-10-01 (previous: 2026-09-29, 2026-09-21)  
Lead: Product Engineer, Documentation Architect, UX Designer

Items are ticked only where the artifact exists on disk and, for checks, where the command was re-run
on 2026-09-29 (on a scratch copy of `prototype/`, so no state files were rewritten); the M7 test additions
were run on 2026-09-30 and again on 2026-10-01. Anything not re-run is marked NOT RUN, not assumed.

---

## 0. Owner decisions for the next-version run (recorded 2026-10-01)

Answers to `docs/next-phase/02_RESEARCH_KB.md` §E and the checklist in
`docs/next-phase/03_NEXT_VERSION_PLAN.md` §3. The run reads these before asking again.

| Decision | Answer |
|---|---|
| E1 — GitHub repository visibility | **Public** |
| E2 — repository owner/name or custom domain | **Not decided yet** — P1-02 stays Blocked until the owner names it; ask at the start of Phase 1 |
| E3 — approval-record semantics (D6) | Not yet confirmed — ask at the start of Phase 1 |
| E6 — dependencies | **Approved:** `jsonschema` + `referencing` as declared requirements (P0-02). **Not approved:** `@playwright/test`, `@mermaid-js/mermaid-cli`, `@docusaurus/faster`, lychee — P1-08 and any CI browser smoke stay Blocked |
| E5, E7, E8, E9 | Not decided — they gate Phase 2 live calls, the GitHub App, Phase 3 and the archive `ai-models/` folder |
| Antigravity setup | 2.0 app (not the CLI); command auto-execution enabled for the `doCCAD_pre` project only; workspace guard hook `.agents/hooks.json` active (blocks push, remote/`gh`, destructive git, protected-path writes, `.env`/keys) |
| Branch | Work on `next-version` (created 2026-10-01 with the baseline commits) |

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
  - [ ] Provide genuine Hungarian translations under `i18n/hu/` for landing page, navigation, overview, and onboarding. *(Partial: overview and onboarding are translated — 4 docs pages. The landing page (`src/pages/index.tsx`) uses no `<Translate>`, and there is no navbar/footer translation file; `i18n/hu/code.json` holds 9 theme strings.)*
  - [x] Implement UI components: `EvidenceLink`, `InterviewPrep`, `ProvenanceBanner`, `QuestionWorkbench`, `DriftInspector`, `KnowledgeExplorer`.
  - [x] Build responsive landing page `/`. *(Page exists and builds; responsiveness NOT verified in a browser.)*

- [ ] **Milestone 7: Automated Verification & Test Suite** — partial
  - [ ] Author comprehensive Python tests under `prototype/tests/`. *(36 tests in 12 test classes, 2026-10-01. 13 of the 14 required boundaries pass; private-content exclusion is an expected-failure test because the behaviour is not implemented — see §2.)*
  - [x] Execute `validate_docs.py` and `detect_changes.py`.
  - [ ] Run full test suite covering all 14 required failure boundaries and lifecycle transitions. *(Suite passes: 32 OK + 1 expected failure. Private-content exclusion remains open.)*
  - [x] Execute `npm run typecheck` and `npm run build` (both `en` and `hu` locales).
  - [x] Verify local search index generation. *(`build/search-index.json`, 361 KB.)*
  - [ ] Execute headless browser smoke tests and capture mobile/desktop screenshots. *(NOT RUN — no screenshots or browser evidence in the repository.)*
  - [ ] Compile `prototype/VALIDATION.md`. *(Missing.)*

- [ ] **Milestone 8: Delivery & Handoff** — started
  - [ ] Finalize `prototype/README.md`, `prototype/DEMO.md`, and `prototype/LIMITATIONS.md`. *(`README.md` written 2026-09-29, including known issues; `DEMO.md` and `LIMITATIONS.md` do not exist.)*
  - [ ] Generate final walkthrough artifact and summary.

---

## 2. Verification Snapshot — 2026-09-29

Run on a scratch copy of `prototype/` with `node_modules/` linked in; Node v24.19.0, Python 3.14.4
with `jsonschema` installed (so `validate` ran the full schema check, not its fallback).

| Check | Command | Result |
|---|---|---|
| Frontmatter, planes, provenance, security | `python3 scripts/validate_docs.py` | PASS — 40 pages, 4 interview datasets, 17 provenance hashes |
| Drift | `python3 scripts/detect_changes.py --all` | PASS — 0 stale generated pages (the command always exits 0; result read from output) |
| Unit tests | `python3 -m unittest discover tests` | PASS — 19/19 (re-run 2026-10-01 after M7 additions and review fixes: 36 tests, OK with 1 expected failure) |
| Types | `npx tsc` | PASS — exit 0 |
| Static build, both locales | `npx docusaurus build` | PASS — `en` and `hu` generated; only warning: no `blog/` directory |
| Local search index | build output | PASS — `build/search-index.json` |
| `build:production` / `build:demo` filter round-trip | — | NOT RUN directly (exercised by `TestBuildFilterExclusion`) |
| Mermaid rendering, browser journeys, screenshots, console errors | — | NOT RUN |
| Reading and generation with credentials unset and provider access blocked | — | NOT RUN as a dedicated check (the fixture provider needs neither) |

Required automated boundaries (from `docs/prototype-planning/ANTIGRAVITY_PROMPT.txt` §7) against
`tests/test_doccad.py`:

| Boundary | Covered by |
|---|---|
| Canonical/generated separation | `TestPlaneSeparation` |
| Supported-question generation | `TestDeterministicRetrievalAndGeneration` |
| Unsupported-question handling | `test_question_generation_cli_unsupported` |
| UI/CLI request round-trip | `TestUiCliJsonRoundtrip` |
| Invalid state transitions | `test_invalid_transitions_rejected`, `test_unknown_state_rejected`, `test_cli_rejects_invalid_transition` (enforcement added 2026-09-30: `ALLOWED_TRANSITIONS` in `review_governance.py`) |
| Draft and simulated-approval exclusion from publication | `TestBuildFilterExclusion`, `test_check_production_blocks_simulated_approval` |
| Drift and targeted regeneration | `TestHashDriftAndRegeneration` |
| Source deletion | `TestSourceDeletionDetection` |
| Private routing without cloud fallback | `TestPrivateRoutingPolicy` |
| Private-content exclusion | **Not implemented** — `test_private_content_excluded_from_production` is `expectedFailure`; pages have no privacy field and `build_filter.py` ignores privacy |
| Invalid provenance | `TestInvalidProvenance` (tampered, malformed, missing, traversal, incomplete block) |
| Blocked traversal | `TestPathTraversalSecurity` |
| Unsafe MDX | `TestUnsafeMdxRejection` |
| Broken citations | `TestBrokenCitations` (check 8 in `validate_docs.py` was documented but not implemented; added 2026-09-30) |

---

## 3. Current Activity

- Close Milestone 7: decide and implement private-content exclusion (then drop the `expectedFailure`),
  run browser smoke tests (or record the exact gap), and write `prototype/VALIDATION.md` from §2.
- Finish Milestone 6: translate the landing page and navigation into Hungarian.
- Then Milestone 8: `DEMO.md`, `LIMITATIONS.md`, and the walkthrough.
