# DOCCAD Prototype Limitations & Architecture Disclosures

**Date**: 2026-10-01  
**Status**: Baseline Stabilized (Phase 0 Exit)  
**System Specification**: DOCCAD Prototype v0.2.0  

---

## 1. System Architecture

DOCCAD enforces a strict architectural boundary between human-owned canonical knowledge, build-time AI-assisted view derivation, and static site publication.

```mermaid
flowchart TD
    subgraph CanonicalPlane["Canonical Plane (Human-Owned)"]
        CS[docs/source/**<br/>Human-authored Markdown]
        CD[docs/diagrams/**<br/>Mermaid .mmd files]
    end

    subgraph AIGenerationPlane["AI Generation Plane (Build-Time / CI)"]
        TC[Task Contracts & Schemas<br/>contracts/*.yaml, schemas/*.json]
        PT[Prompt Templates<br/>prompts/*.md]
        AR[AI Router & Provider Protocol<br/>ai/router.py, ai/provider.py]
        FP[Default Fixture Provider<br/>Deterministic & Offline]
        SS[Secret Scanner & Privacy Pinning<br/>T6 & T12 Guards]
    end

    subgraph GovernancePlane["Governance & Validation Plane"]
        VD[validate_docs.py<br/>Schema, Plane, Provenance, MDX, Link Gates]
        DC[detect_changes.py<br/>Hash Drift & Target Mapping]
        RG[review_governance.py<br/>Review State Machine]
        BF[build_filter.py<br/>Production vs Demo Filter & Hold Stubs]
    end

    subgraph PresentationPlane["Presentation Plane (Static-First)"]
        DOCS["/docs<br/>Canonical Docs"]
        VIEWS["/views<br/>Governed Derived Views"]
        WORK["/workbench, /inspector, /explorer<br/>Interactive Client Tooling"]
        I18N["/hu/<br/>Hungarian Translated Locale"]
    end

    CS -->|Evidence & Hashes| AR
    TC & PT --> AR
    AR --> FP
    FP -->|Candidate MDX| VD
    VD -->|Verified Drafts| RG
    RG -->|Review Ledger| BF
    BF -->|Hold Stubs / Approved Views| VIEWS
    CS --> DOCS
    BF --> PresentationPlane
```

---

## 2. Four-Tier Capability Classification

To maintain absolute transparency and prevent unwarranted claims, DOCCAD categorizes every feature into one of four capability tiers:

### Tier 1: Implemented & Formally Verified Behavior
These capabilities are fully implemented in code and verified by automated tests in this repository:
1. **Two-Plane Separation**: Canonical pages (`docs/source/`) and generated views (`docs/generated/`) are strictly separated across Docusaurus docs plugin instances. Canonical content never imports or cites generated views (`TestPlaneSeparation`).
2. **Mechanical Drift Tracking**: Canonical source files are hashed using `sha256`. Provenance blocks in generated views record these hashes. `detect_changes.py` accurately identifies modified canonical sources and outputs a deduplicated regeneration plan (`TestHashDriftAndRegeneration`, `TestRegenerationPlanExecutable`).
3. **Strict Validation Pipeline**: `validate_docs.py` enforces JSON schemas via `jsonschema` with `referencing`, checks ID uniqueness, validates link allowlists (`contracts/link-allowlist.yaml`), and verifies provenance hashes.
4. **AST MDX Restriction Gate (T3)**: Generated MDX files are scanned and strictly prohibited from using `import`/`export`, `<iframe>`, `<object>`, event handlers, `data:` URLs, or arbitrary unallowlisted JSX (`TestMdxRestrictionGate`, `TestUnsafeMdxRejection`).
5. **Context Secret Sanitization (T6)**: `ai/router.py` automatically scans assembled prompts and evidence payloads for credential patterns (`sk-`, `AIza`, `ghp_`, PEM private keys) and aborts execution before any provider call (`TestContextSecretScan`).
6. **Hard-Pinned Privacy (T12)**: Tasks marked `privacy: private` route strictly to `local`. If local generation is disabled or fails, the router raises `PrivacyRoutingError` immediately with zero cloud fallback (`TestPrivateRoutingPolicy`, `TestRouterFallbackSemantics`, `TestPrivateChainConfig`).
7. **Production Publication Filter & Hold Stubs**: `build_filter.py` stashes unapproved and `approved-for-demo` files to `.work/stashed_unapproved/`, replacing them with valid, honest hold stubs (`type: stub`, `stub_version: 1`, explicit `hold_reason`, no fake approvals or mock generation blocks) (`TestProductionFilterValidity`, `TestBuildFilterExclusion`).
8. **Private Content Isolation**: Canonical and generated documents marked `visibility: private` are stashed prior to production static builds, preventing accidental data leaks (`TestPrivateContentExclusion`).
9. **Dual-Locale Static Publishing**: Docusaurus 3.10.2 builds static assets for both English (`/`) and Hungarian (`/hu/`) locales with `@easyops-cn/docusaurus-search-local` offline search indices for both languages (`npm run build`).
10. **Hungarian Fallback (D11)**: Untranslated canonical documents in secondary locales render localized navigation chrome and fall back gracefully to English source text without 404 errors.

### Tier 2: Deterministic Simulation
These capabilities are implemented as offline simulations for testing and demonstration:
1. **Fixture Provider (`fixture`)**: DOCCAD's default provider is `ai/fixture_provider.py`. It simulates AI generation using deterministic, pre-authored responses aligned with repo schemas. It requires zero API keys, no network access, and zero token spend. It is not an LLM.
2. **Simulated Approval (`approved-for-demo`)**: The CLI governance ledger (`.work/demo_reviews.json`) allows transitioning artifacts to `approved-for-demo`. This is explicitly a demo mechanism to demonstrate workbench workflows. It is never treated as human approval and is blocked from production publication by `check-production`.
3. **Browser Client Workbench**: The interactive Question Workbench at `/workbench` simulates retrieval, drafting, and review entirely in the user's browser client using client-side fixture state. It does not invoke the Python backend.

### Tier 3: Unverified Integrations
These components are implemented in code but have not been executed against external production infrastructure:
1. **Live Cloud AI Providers**: Adapters for Anthropic Claude (`ai/anthropic_provider.py`), OpenAI GPT (`ai/openai_provider.py`), and Google Gemini (`ai/gemini_provider.py`) are implemented. However, no live API requests were made during Phase 0 per run safety rules. Live execution is deferred to Phase 2 under owner credentials and spend caps.
2. **Local Model Provider**: The OpenAI-compatible adapter for local runtimes (`ai/local_provider.py`) is implemented but unverified against a live Ollama or vLLM daemon.
3. **GitHub Actions Workflows**: `ci.yml` and `publish.yml` run on GitHub (the site is live). `generate.yml` and the weekly `drift.yml` are written and tested offline but have not yet been dispatched or scheduled on GitHub.
4. **Interactive Browser Verification**: Visual verification using the Antigravity 2.0 `/browser` slash command is an interactive human procedure and is documented as NOT RUN in automated CI logs.

### Tier 4: Deferred Production Work
These features are intentional design decisions deferred to future phases or owner approval:
1. **Automated End-to-End Browser Testing**: Integration of `@playwright/test` was evaluated and deferred per owner decision E6 (dependency minimization).
2. **Mermaid-CLI Pre-Compilation Gate**: CI-level diagram compilation via `@mermaid-js/mermaid-cli` is planned for Phase 1 (P1-08) but currently blocked awaiting owner dependency approval (E6).
3. **Cryptographic Human Approval Records**: Replacing `approved-for-demo` with mandatory human pull request approval metadata (`approval_record: {pr, approved_by, approved_at}`) is scheduled for Phase 1 (P1-05).
4. **Bot-authored generation PRs (E8)**: `generate.yml` opens docs-gen PRs as the DOCCAD GitHub App when it is configured. The App itself is created by the owner, so the end-to-end path (bot PR → code-owner approval → verified publication) has not run yet.

---

## 3. Requirement-to-Evidence Matrix

Requirement IDs and titles follow `docs/primary-inputs/01_PROJECT_KNOWLEDGE/REQUIREMENTS.md` and
`planning/ACCEPTANCE.md`. Status vocabulary — kept deliberately narrow so no row claims more than was run:

- **VERIFIED** — an automated test or check covering the requirement ran and passed (2026-10-01).
- **BUILD-ONLY** — the code compiles into the static build; it was not exercised in a browser.
- **PARTIAL** — the local part is verified; the named remainder is planned and not yet built.
- **DOCUMENTED** — satisfied by a research or design artifact; there is nothing executable to test.

| Requirement | Title | Primary Implementing Files | Evidence | Status |
|---|---|---|---|---|
| **REQ-001** | Six-platform research | `docs/primary-inputs/02_RESEARCH/`, `docs/source/architecture/platform-research.md` | Archive research set; canonical summary page validates | **DOCUMENTED** |
| **REQ-002** | Weighted decision model | `docs/source/decisions/adr-002-docusaurus-foundation.md` | ADR with the 11-criterion scoring; page validates | **DOCUMENTED** |
| **REQ-003** | Git/GitHub source of truth | `docs/source/**`, `.docs-manifest.json` | Files only, no database; git repository with a GitHub remote. PR-based flows arrive in Phase 1 | **PARTIAL** |
| **REQ-004** | Structural canonical vs generated separation; no silent promotion | `scripts/validate_docs.py`, `scripts/build_filter.py`, `docusaurus.config.ts` | `TestPlaneSeparation`, `TestBuildFilterExclusion`, `TestProductionFilterValidity` | **VERIFIED** |
| **REQ-005** | Thin AI provider abstraction | `ai/provider.py`, `ai/router.py`, `ai.config.yaml` | `TestRouterFallbackSemantics`, `TestPrivateRoutingPolicy`, `TestRepairRetry`. Cloud and local adapters never ran live (Tier 3) | **PARTIAL** |
| **REQ-006** | Static reads without AI | `docusaurus.config.ts`, `src/**` | `npm run build` with no keys set; no runtime model calls in `src/`. Browser reading not run | **BUILD-ONLY** |
| **REQ-007** | Level-1 deterministic retrieval | `scripts/generate_question.py`, `scripts/generate_page.py` | `TestDeterministicRetrievalAndGeneration`, `TestPathTraversalSecurity` | **VERIFIED** |
| **REQ-008** | Ingestion & incremental regeneration | `scripts/detect_changes.py` | `TestHashDriftAndRegeneration`, `TestRegenerationPlanExecutable`, `TestSourceDeletionDetection`. Automated GitHub ingestion (P1-06) not built | **PARTIAL** |
| **REQ-009** | Provenance metadata & hash drift | `generation` frontmatter block, `scripts/validate_docs.py` | `TestInvalidProvenance`, `TestHashDriftAndRegeneration`, `TestGenerationModeStamp` | **VERIFIED** |
| **REQ-010** | Evidence-grounded recruiter views | `docs/generated/recruiter/project-overview.mdx`, `<EvidenceLink>` | `TestBrokenCitations`, `npm run validate`. Content is fixture output (Tier 2), not a live model | **VERIFIED** (fixture) |
| **REQ-011** | Interview prep component | `src/components/InterviewPrep/`, 4 `*.interview.json` datasets | Datasets pass `interview.schema.json`; component compiles. Rendering not checked in a browser | **BUILD-ONLY** |
| **REQ-012** | Special-question workflow | `scripts/generate_question.py`, `scripts/review_governance.py`, `/workbench` | `TestUiCliJsonRoundtrip`, `TestQuestionPersistenceGovernance`, `TestReviewGovernanceStateTransitions`. Approval is simulated; real approval is P1-05 | **PARTIAL** |
| **REQ-013** | EN/HU bilingual capability | `i18n/hu/**`, `src/pages/index.tsx` | Both locales build; landing, navigation and 4 canonical pages translated, the rest fall back to English (D11) | **PARTIAL** |
| **REQ-014** | Anti-overengineering | Whole prototype | By inspection: no database, service, vector store or agent swarm; Python is stdlib + PyYAML + jsonschema | **VERIFIED** (inspection) |
| **REQ-015** | Runnable validated prototype | `tests/test_doccad.py`, `VALIDATION.md`, `DEMO.md` | 75 unit tests pass; `VALIDATION.md` separates executed from NOT RUN checks | **VERIFIED** |
| **REQ-016** | Security architecture | `ai/router.py`, `scripts/validate_docs.py`, `contracts/link-allowlist.yaml` | `TestMdxRestrictionGate`, `TestContextSecretScan`, `TestExternalLinkAllowlist`, `TestPrivateChainConfig`. CI-side threats (T8) arrive with Phase 1 | **PARTIAL** |
