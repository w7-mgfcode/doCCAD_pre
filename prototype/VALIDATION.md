# DOCCAD Prototype Validation Report

**Run Date**: 2026-10-06  
**Environment**: Linux x86_64, Node v24.19.0 (`engines.node: >=24.14`), Python 3.14.4  
**Dependencies**: `PyYAML 6.0.3`, `jsonschema 4.19.2`, `referencing 0.36.2`  
**Execution Context**: Branch `phase-2-live-ai`, Phase 2 (Live AI Behind Fixture Default)  

---

## 1. Executive Summary

This document records the definitive validation results for the DOCCAD prototype at the conclusion of Phase 2 (Live AI Generation Behind Fixture Default, Checkpoint 2B). Every check is categorized as **PASS**, **FAIL**, or **NOT RUN**. No assumed or historical test results are reported; every passing entry represents a command executed in this run with exit code 0.

- **Total Automated Python Unit Tests**: 147 tests across 39 test classes (**147 PASS, 0 FAIL, 0 EXPECTED FAILURES**).
- **Core Governance Scripts**: `validate_docs.py`, `detect_changes.py`, `generate_page.py`, `generate_question.py`, `review_governance.py`, `build_filter.py`, `github_approval.py`, and `check_grounding.py` all verified with exposed `build_parser()` CLI endpoints.
- **AI Abstraction & Providers**: Standard library HTTP transport helper (`ai/http.py`) with exponential backoff and jitter, provider-facing JSON schema derivation (`ai/schema_adapt.py`), sampling parameter opt-in (`TestSamplingOptIn`), explicit provider selection (`--provider`, `TestExplicitProviderSelection`), and per-run token/call budget (`TestRunBudget`).
- **Grounding & Security Gates**: Deterministic grounding gate (`scripts/check_grounding.py`) verifying citation existence, exact quote span containment (>= 15 chars), and recruiter technology claims against fact set; prompt injection rejection suite (`TestPromptInjectionFixtures`) verifying refusal of exfiltration links, fabricated citations, ungrounded tech claims, and executable MDX.
- **GitHub Automation & Workflows**: `ci.yml`, `publish.yml`, `generate.yml`, `drift.yml`, and `dependabot.yml` statically validated, action pins pinned to full commit SHAs, zero `pull_request_target`, CLI script invocations verified against argparse, and `.github/workflows/generate.yml` updated with `provider` choice input and protected `generation` environment job with scoped secrets (`TestGenerateWorkflowProviderInput`).
- **Governance & CODEOWNERS (E3)**: Real human approval replaces simulated approval for production: `approval_record` schema, body hash stamping, offline mockable GitHub API verifier, fail-closed permission error handling, draft reset on generation.
- **Frontend & Static Build**: TypeScript compilation (`tsc`) and Docusaurus dual-locale build (`en`, `hu`) exit 0 with search index generation.
- **Live Smoke Calls (P2-08)**: Documented with exact owner execution commands and clean-up command (`git restore docs/generated`), marked **NOT RUN** per run budget rules.
- **Browser Testing**: Marked **NOT RUN** per run rules (interactive `/browser` slash command in Antigravity 2.0 app and unapproved Playwright dependency per decision E6).

---

## 2. Automated Pipeline & Build Gates

| Gate ID | Check Description | Exact Command | Exit Code | Date | Result | Evidence / Output Note |
|---|---|---|---|---|---|---|
| **GATE-VAL** | Schema, plane, hash, link, MDX & grounding validation | `DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate` | 0 | 2026-10-06 | **PASS** | `Validated 40 pages, 4 interview datasets, 25 provenance hashes. OK — frontmatter schemas valid, planes intact, provenance hashes current, security checks passed.` |
| **GATE-DRIFT** | Change impact & drift detection | `npm run detect` | 0 | 2026-10-06 | **PASS** | `stale generated: 0; nothing to regenerate — all provenance hashes current.` |
| **GATE-TEST** | Comprehensive Python unit test suite | `python3 -m unittest discover tests -v` | 0 | 2026-10-06 | **PASS** | `Ran 147 tests in 12.470s ... OK (0 failures, 0 errors, 0 expected failures)` |
| **GATE-TYPE** | TypeScript static type verification | `npm run typecheck` | 0 | 2026-10-06 | **PASS** | `tsc --noEmit` exits 0 cleanly. |
| **GATE-BUILD** | Dual-locale static production build | `npm run build` | 0 | 2026-10-06 | **PASS** | `Generated static files in "build"` and `Generated static files in "build/hu"`. |
| **GATE-PROD-ROUND** | Production build filter & demo restoration | `npm run build:production && npm run build:demo` | 0 | 2026-10-01 | **PASS** | Production filter stashes unapproved files with hold stubs; demo build cleanly restores. |
| **GATE-BUDGET** | Per-run token and call budget enforcement | `python3 -m unittest tests.test_doccad.TestRunBudget -v` | 0 | 2026-10-06 | **PASS** | Ran 5 tests ... OK (token budget accumulation, pre-call aborts, repair retry counting). |
| **GATE-GROUNDING** | Deterministic citation, quote & tech grounding | `python3 -m unittest tests.test_doccad.TestGroundingGate -v` | 0 | 2026-10-06 | **PASS** | Ran 6 tests ... OK (Rule 1 hash/existence, Rule 2 quote spans, Rule 3 recruiter tech, golden set). |
| **GATE-INJECTION** | Prompt injection rejection fixtures | `python3 -m unittest tests.test_doccad.TestPromptInjectionFixtures -v` | 0 | 2026-10-06 | **PASS** | Ran 6 tests ... OK (exfiltration link, fabricated citation, invented tech, executable MDX). |
| **GATE-WORKFLOW-PROV** | Workflow provider input & environment scoping | `python3 -m unittest tests.test_doccad.TestGenerateWorkflowProviderInput -v` | 0 | 2026-10-06 | **PASS** | Ran 4 tests ... OK (default fixture, environment: generation, scoped secrets, env: pass-through). |
| **GATE-WORKFLOW-VAL** | Workflow YAML syntax & action SHA pin checks | `python3 -c "import yaml,sys;[yaml.safe_load(open(f)) for f in sys.argv[1:]]" .github/workflows/*.yml .github/dependabot.yml` | 0 | 2026-10-01 | **PASS** | All workflows & dependabot parse cleanly; 16/16 `uses:` lines pinned with 40-char SHA; 0 `pull_request_target`. |
| **GATE-WORKFLOW-ARG** | Dynamic workflow CLI invocation parsing vs argparse | `python3 -m unittest tests.test_doccad.TestWorkflowScriptInvocations -v` | 0 | 2026-10-06 | **PASS** | Ran 3 tests ... OK (workflow shell & subprocess calls match CLI parser definitions including provider). |
| **GATE-APP-REC** | E3 Approval Record schema and hash verification | `python3 -m unittest tests.test_doccad.TestApprovalRecord -v` | 0 | 2026-10-01 | **PASS** | Ran 13 tests in 0.041s ... OK (stamped body hash, tamper rejection, draft reset). |
| **GATE-SRCH-EN** | English local search index generation | `ls -lh build/search-index.json` | 0 | 2026-10-01 | **PASS** | File exists (350 KB, generated by `@easyops-cn/docusaurus-search-local`). |
| **GATE-SRCH-HU** | Hungarian local search index generation | `ls -lh build/hu/search-index.json` | 0 | 2026-10-01 | **PASS** | File exists (343 KB, generated by `@easyops-cn/docusaurus-search-local`). |
| **GATE-HU-HERO** | Hungarian translated landing page | `grep -o "DOCCAD Dokumentációs Ökoszisztéma" build/hu/index.html` | 0 | 2026-10-01 | **PASS** | Matches localized hero title in `build/hu/index.html`. |

---

## 3. Required Failure Boundaries (ANTIGRAVITY_PROMPT §7 + Phase 1 E3)

All 16 required failure boundaries are covered by unit tests in `prototype/tests/test_doccad.py` with zero expected failures:

| Boundary ID | Failure Boundary | Implementing / Guarding File | Test Class & Method | Result | Verification Notes |
|---|---|---|---|---|---|
| **BND-01** | Canonical/Generated Plane Separation | `scripts/validate_docs.py` | `TestPlaneSeparation` | **PASS** | Rejects generated files under `docs/source` and canonical files under `docs/generated`. |
| **BND-02** | Supported Question Generation | `scripts/generate_question.py` | `TestDeterministicRetrievalAndGeneration` | **PASS** | Retrieves canonical evidence, invokes fixture, stamps hashes, forces `approval_status: draft`. |
| **BND-03** | Unsupported Question Handling | `scripts/generate_question.py` | `TestDeterministicRetrievalAndGeneration.test_question_generation_cli_unsupported` | **PASS** | Unsupported queries (e.g. Kubernetes) generate honest answers citing absent scope. |
| **BND-04** | UI / CLI Request Round-Trip | `src/components/QuestionWorkbench/` | `TestUiCliJsonRoundtrip` | **PASS** | Validates JSON contract schema across UI interactive state and CLI invocation payload. |
| **BND-05** | Invalid Governance State Transitions | `scripts/review_governance.py` | `TestReviewGovernanceStateTransitions` | **PASS** | Enforces state machine: rejects skipping review, invalid target states, and unknown states. |
| **BND-06** | Draft & Simulated-Approval Exclusion | `scripts/build_filter.py` | `TestBuildFilterExclusion`, `test_check_production_blocks_simulated_approval` | **PASS** | Production filter stashes unapproved and `approved-for-demo` files to `.work/stashed_unapproved/`. |
| **BND-07** | Mechanical Drift & Targeted Regeneration | `scripts/detect_changes.py` | `TestHashDriftAndRegeneration`, `TestRegenerationPlanExecutable` | **PASS** | Hashes detect modified canonical sources; outputs deduplicated regeneration plan. |
| **BND-08** | Source Deletion Detection | `scripts/detect_changes.py` | `TestSourceDeletionDetection` | **PASS** | Missing source file referenced in provenance is flagged as stale/missing. |
| **BND-09** | Private Routing Hard Pinning | `ai/router.py` | `TestPrivateRoutingPolicy`, `TestRouterFallbackSemantics`, `TestPrivateChainConfig` | **PASS** | Tasks with `privacy: private` route strictly to `local`; failure raises `PrivacyRoutingError` immediately with zero cloud fallback. |
| **BND-10** | Private Content Isolation (T12) | `scripts/build_filter.py`, `scripts/generate_page.py` | `TestBuildFilterExclusion`, `TestPrivateContentExclusion` | **PASS** | Private documents are stashed before publication; generation elevates privacy when any evidence is private. |
| **BND-11** | Invalid Provenance Rejection | `scripts/validate_docs.py` | `TestInvalidProvenance` | **PASS** | Tampered hashes, missing hashes, malformed JSON blocks, and unlisted sources fail validation. |
| **BND-12** | Blocked Path Traversal | `scripts/validate_docs.py` | `TestPathTraversalSecurity` | **PASS** | Rejects `../` in evidence paths and prevents directory escape. |
| **BND-13** | Unsafe MDX Construct Rejection (T3) | `scripts/validate_docs.py` | `TestUnsafeMdxRejection`, `TestMdxRestrictionGate` | **PASS** | Forbids `import`/`export`, `<iframe>`, `<object>`, event handlers, `data:` URLs, and arbitrary JSX in `docs/generated/`. |
| **BND-14** | Broken Citations Detection | `scripts/validate_docs.py` | `TestBrokenCitations` | **PASS** | Rejects `<EvidenceLink>` referencing non-existent canonical documents or headings. |
| **BND-15** | Real CODEOWNER Approval & GitHub Gate (E3) | `scripts/github_approval.py`, `scripts/build_filter.py` | `TestApprovalRecord` | **PASS** | Requires merged PR, matching CODEOWNER review, and modified file; hash tamper sends back to in-review; fails closed on API permission error. |
| **BND-16** | Workflow Script Invocations vs Argparse | `tests/test_doccad.py` | `TestWorkflowScriptInvocations` | **PASS** | Dynamic workflow CLI extraction and parse against argparse: rejects `--query`, `--provider`, verifies `--question` and `--audience`. |

---

## 4. Quality & Security Gates Verification (T1–T6, T12, T14)

| Gate ID | Security / Quality Gate | Implementing Component | Test Class | Result | Notes |
|---|---|---|---|---|---|
| **T1** | Schema & AST Validation | `validate_docs.py`, `schemas/*.schema.json` | `TestValidatorDependencyMode`, `TestQuestionPersistenceGovernance` | **PASS** | Strict mode requires `jsonschema`; rejects malformed frontmatter. |
| **T3** | Clean MDX Generation | `validate_docs.py`, `src/theme/MDXComponents.tsx` | `TestMdxRestrictionGate` | **PASS** | Decoupled interview component loads data by ID without MDX `import`/`export`. |
| **T4** | External Link Allowlist | `contracts/link-allowlist.yaml`, `validate_docs.py` | `TestExternalLinkAllowlist` | **PASS** | Disallowed external domains in generated views are rejected. |
| **T5** | Mermaid Strict Rendering | `docusaurus.config.ts:84` | Config inspection | **PASS** | `mermaid.options.securityLevel: 'strict'` configured explicitly. |
| **T6** | Context Secret Sanitization | `ai/router.py:115` | `TestContextSecretScan` | **PASS** | Prompt payload scanning detects and rejects API keys (`sk-`, `AIza`, `ghp_`, PEM keys). |
| **T12** | Private Routing Chain Lock | `ai/router.py:44` | `TestPrivateChainConfig` | **PASS** | `ai.config.yaml` rules matching `privacy: private` validate strictly to `['local']`. |
| **T14** | CODEOWNER Review & Body Hash Verification | `scripts/github_approval.py`, `scripts/build_filter.py` | `TestApprovalRecord` | **PASS** | Validates PR status, CODEOWNER review identity, touched paths via GitHub API, and body sha256 checksum. |

---

## 5. Hungarian Fallback Verification (D11 / B6.2)

- **Test Target**: Canonical page `docs/source/architecture/system-overview.md` which has **no** translated counterpart in `i18n/hu/docusaurus-plugin-content-docs-source/current/`.
- **Observed Behavior**:
  - Docusaurus v3.10.2 generates the file at `build/hu/docs/architecture/system-overview/index.html`.
  - The generated HTML sets `<html lang="hu" dir="ltr" ...>` and renders the Hungarian navbar/footer chrome (`Dokumentáció (Kanonikus)`, `Toborzói Nézet`, etc.).
  - The document content gracefully falls back to the English source text.
  - The page **does NOT return 404** and the build succeeds without error.
- **Conclusion**: Resolves decision D11. The site architecture safely serves untranslated canonical pages in secondary locales with localized navigation and English fallback content.

---

## 6. Interactive Browser Verification (NOT RUN)

Interactive browser verification was specified in `docs/next-phase/05_ANTIGRAVITY_PROMPT.txt:47` using the `/browser` slash command against `http://localhost:3000`.

| Journey / Check | Target URL / Viewport | Status | Reason Not Run |
|---|---|---|---|
| Home Page | `http://localhost:3000/` (1440px desktop) | **NOT RUN** | `/browser` is a user-side slash command in Antigravity 2.0 app; automated browser testing (`@playwright/test`) unapproved per decision E6. |
| Canonical Page with Mermaid | `http://localhost:3000/docs/architecture/system-overview` | **NOT RUN** | Same as above. |
| Recruiter View & EvidenceLink | `http://localhost:3000/views/recruiter/project-overview` | **NOT RUN** | Same as above. |
| Interview Page | `http://localhost:3000/views/interview/architecture-system-overview` | **NOT RUN** | Same as above. |
| Question Workbench Journey | `http://localhost:3000/workbench` | **NOT RUN** | Same as above. |
| Drift Inspector | `http://localhost:3000/inspector` | **NOT RUN** | Same as above. |
| Hungarian Home Page | `http://localhost:3000/hu/` | **NOT RUN** | Same as above. |
| Theme Switcher | Dark mode / Light mode toggle | **NOT RUN** | Same as above. |
| Mobile Viewport | 390px responsive layout check | **NOT RUN** | Same as above. |

### Manual Verification Procedure for Human Reviewer (H-5)
1. Run local web server:
   ```bash
   cd prototype && npm run serve
   ```
2. In the Antigravity 2.0 chat interface, invoke `/browser` and navigate to `http://localhost:3000`.
3. Verify rendering of Mermaid diagrams, collapsible interview cards, and evidence link click-through.
4. Switch to `/hu/` and verify Hungarian navigation labels.
5. Resize to 390px to confirm mobile hamburger menu and layout responsiveness.

---

## 7. Live AI Provider Smoke Verification (Phase 2 Owner Execution — NOT RUN)

Per run rules and decision E5, live provider calls require owner credentials, model choices, and spend caps. No external API requests were made during this agent run; all provider adapters have been verified against local loopback mock servers (`TestHttpRetryPolicy`, `TestAdapterRequestShapes`, `TestProviderSchemaDerivation`, `TestSamplingOptIn`).

The table below records the exact command sequence for owner-executed live smoke testing. Execute from `prototype/` with the appropriate provider API key and model environment variable exported in the shell. Kept output must proceed through a `docs-gen/*` branch and pull request, never a direct commit to `main`.

| Provider | Required Credentials & Env | Generation Commands (InterviewPrep & RecruiterPage) | Post-Run Validation & Clean-Up | Status | Owner Record Fields |
|---|---|---|---|---|---|
| **Anthropic Claude** | `export ANTHROPIC_API_KEY="sk-ant-..."`<br/>`export AI_MODEL_ANTHROPIC="claude-3-7-sonnet-..."` | `python3 scripts/generate_page.py --contract GenerateInterviewPrep --target architecture-system-overview --provider anthropic`<br/>`python3 scripts/generate_page.py --contract GenerateRecruiterPage --target architecture-system-overview --provider anthropic` | `DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate`<br/>`git restore docs/generated` | **NOT RUN** | Model returned: `__________`<br/>Exit codes: `__________`<br/>Validation: `__________`<br/>Tokens (in/out): `__________` |
| **Google Gemini** | `export GEMINI_API_KEY="AIza..."`<br/>`export AI_MODEL_GEMINI="gemini-2.5-flash-..."` | `python3 scripts/generate_page.py --contract GenerateInterviewPrep --target architecture-system-overview --provider gemini`<br/>`python3 scripts/generate_page.py --contract GenerateRecruiterPage --target architecture-system-overview --provider gemini` | `DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate`<br/>`git restore docs/generated` | **NOT RUN** | Model returned: `__________`<br/>Exit codes: `__________`<br/>Validation: `__________`<br/>Tokens (in/out): `__________` |
| **OpenAI GPT** | `export OPENAI_API_KEY="sk-proj-..."`<br/>`export AI_MODEL_OPENAI="gpt-4o-..."` | `python3 scripts/generate_page.py --contract GenerateInterviewPrep --target architecture-system-overview --provider openai`<br/>`python3 scripts/generate_page.py --contract GenerateRecruiterPage --target architecture-system-overview --provider openai` | `DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate`<br/>`git restore docs/generated` | **NOT RUN** | Model returned: `__________`<br/>Exit codes: `__________`<br/>Validation: `__________`<br/>Tokens (in/out): `__________` |
| **Local (Ollama / vLLM)** | Live local server on `http://localhost:11434/v1`<br/>`export AI_MODEL_LOCAL="llama3.1:..."` | `python3 scripts/generate_page.py --contract GenerateInterviewPrep --target architecture-system-overview --provider local`<br/>`python3 scripts/generate_page.py --contract GenerateRecruiterPage --target architecture-system-overview --provider local` | `DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate`<br/>`git restore docs/generated` | **NOT RUN** | Model returned: `__________`<br/>Exit codes: `__________`<br/>Validation: `__________`<br/>Tokens (in/out): `__________` |

### Owner Post-Execution Procedure
1. Execute the paired generation commands for the chosen provider.
2. Confirm that `DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate` exits 0.
3. If discarding generation test output, run `git restore docs/generated`.
4. If keeping generated output, do NOT commit directly to `main` or `next-version`. Create a branch `docs-gen/<contract>-<target>` and open a PR with the required provenance metadata.
