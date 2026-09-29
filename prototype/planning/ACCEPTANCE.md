# DOCCAD Prototype Acceptance Matrix & Journey Map

Status: Prototype Target Specification  
Inherited Baseline: PRE-DOCCAD Research Archive (`docs/primary-inputs/`)  
Execution Target: Local Prototype (`prototype/`)

This document maps all applicable requirements (REQ-001 through REQ-016) to tangible user journeys, implementation components, and deterministic verification criteria.

---

## 1. Requirements to Implementation & Verification Traceability

| ID | Title & Scope | Prototype Implementation Path | User Journey / Feature | Verification Evidence |
|---|---|---|---|---|
| **REQ-001** | Six-platform research | `docs/source/architecture/platform-research.md` (distilled canonical summary) | Reader explores platform comparison findings in canonical plane | Page exists, valid frontmatter, links resolve |
| **REQ-002** | Weighted decision model | `docs/source/decisions/adr-002-docusaurus-foundation.md` | Reader/Architect reviews Docusaurus 88.6/100 weighted decision | ADR page rendered, links to criteria |
| **REQ-003** | Git/GitHub source of truth | Filesystem repo layout under `prototype/`, `.docs-manifest.json` | Contributor audits repository files; no database required | Pure static build, JSON manifest generated |
| **REQ-004** | Structural canonical vs generated separation | `docusaurus.config.ts` dual `plugin-content-docs` (`/docs` vs `/views`) | Reader navigates `/docs` (human canon) vs `/views` (AI views) | `scripts/validate_docs.py` plane check |
| **REQ-005** | Thin AI provider abstraction | `ai/provider.py`, `ai/router.py`, `ai/fixture_provider.py` | CLI & UI execute generation without provider lock-in | Unit tests verify routing and fixture fallback |
| **REQ-006** | Static reads without AI | Docusaurus static build (`npm run build`) with zero runtime API | Reader browses complete site offline with no keys/network | Build & serve succeed with model keys unset |
| **REQ-007** | Level-1 deterministic retrieval | `scripts/generate_question.py`, `scripts/generate_page.py` | Question pipeline assembles only allowed canonical files | Retrieval logs report included/rejected files |
| **REQ-008** | Ingestion & incremental regeneration | `scripts/detect_changes.py` | Source edit triggers targeted staleness for dependent views only | Targeted drift test verifies only affected view regens |
| **REQ-009** | Provenance metadata & hash drift | `generation` frontmatter block, `sha256` content hashes | Inspector displays source hashes; drift flagged on mismatch | Negative hash tampering test exits with code 1 |
| **REQ-010** | Evidence-grounded recruiter views | `docs/generated/recruiter/project-overview.mdx`, `<EvidenceLink>` | Recruiter switches 30s/2m/deep modes and clicks evidence | Recruiter page renders with verifiable citations |
| **REQ-011** | Interview prep component | `<InterviewPrep>`, 4 `*.interview.json` datasets | Interviewer/Candidate unfolds concepts, tradeoffs, Q&A | Schema validation passes; component renders |
| **REQ-012** | Special-question workflow | Question Workbench (`/workbench`), `scripts/generate_question.py` | User enters question, inspects evidence, generates draft | 5 supported + 1 unsupported question tested |
| **REQ-013** | EN/HU bilingual capability | Docusaurus i18n (`en`, `hu`), `i18n/hu/` translations | User switches language toggle; views HU landing & core docs | Both locales build clean; fallback indicator visible |
| **REQ-014** | Anti-overengineering | Zero databases, zero microservices, zero agent swarms | Single engineer operates all scripts and runs prototype locally | Complete codebase operable via stdlib & npm |
| **REQ-015** | Runnable validated prototype | Complete `prototype/` application with test suite | End-to-end user journeys executed and verified | `scripts/validate_docs.py`, build, test suite pass |
| **REQ-016** | Security architecture | `scripts/validate_docs.py` (link allowlist, traversal check), private routing | User submits private question; pipeline refuses cloud | Traversal attempts blocked; private routing enforced |

---

## 2. Core User Journeys

### Journey 1: The Canonical Reader & Architect
1. **Landing & Exploration**: The reader lands on `/`, views the project vision, core tenets, and navigation cards.
2. **Canonical Reading**: The reader navigates to `/docs/overview`, explores system architecture (`/docs/architecture/system-overview`), and reads Architectural Decision Records (`/docs/decisions/adr-003-canonical-generated-separation`).
3. **Diagram Inspection**: The reader views embedded Mermaid diagrams rendering system spines and trust boundaries.
4. **Offline Search**: The reader searches for "drift detection" or "trust zones" via local offline search, receiving instant highlighted results from both `/docs` and `/views`.

### Journey 2: The Recruiter & Interviewer
1. **Recruiter Fast Scan (30s)**: The recruiter opens `/views/recruiter/project-overview`, reads the 30-second elevator pitch highlighting verifiable engineering achievements.
2. **Technical Review (2m & Deep Dive)**: The recruiter switches to the 2-minute summary and deep-dive architecture view, clicking `<EvidenceLink>` citations that jump directly into the supporting canonical files.
3. **Interview Preparation**: The interviewer/candidate visits `/views/interview/architecture-system-overview`, exploring collapsible tabs for concepts, design decisions, architectural tradeoffs, likely interview questions, and model answers.

### Journey 3: The Question-to-Governed-Preview Workflow
1. **Question Submission**: In the Question Workbench (`/workbench`), the user selects a preset question scenario (e.g. "How does DOCCAD detect drift when canonical architecture changes?") or enters a custom query.
2. **Retrieval Audit**: The user inspects retrieved canonical evidence, verifying context budgets and seeing excluded files.
3. **Deterministic Generation**: The user triggers draft generation via the fixture provider. A candidate page is produced with full provenance metadata (`sha256` source hashes, contract version, provider ID).
4. **Real-time Validation**: The draft is validated against `schemas/document.schema.json`, verifying frontmatter integrity and citation targets.
5. **Simulated Review**: The reviewer simulates approval (`draft` -> `in-review` -> `approved-for-demo`), which records a demo review record.
6. **UI/CLI Round-Trip**: The user exports the request/result JSON from the browser workbench and re-runs `scripts/generate_question.py --request request.json` via CLI, verifying exact parity.

### Journey 4: The Contributor Drift & Targeted Regeneration
1. **Canonical Source Edit**: A contributor modifies a canonical architecture document (`docs/source/architecture/content-planes.md`).
2. **Drift Detection**: Running `scripts/detect_changes.py` detects the hash mismatch and flags dependent derived pages as `STALE`. Unrelated derived views remain clean.
3. **Targeted Regeneration**: The contributor runs targeted regeneration for the stale views.
4. **Revalidation & Review**: `scripts/validate_docs.py` validates updated hashes, and the review record is refreshed.

### Journey 5: Security & Failure Boundary Enforcement
1. **Unsupported Question Handling**: A user asks an out-of-domain question ("What is DOCCAD's multi-cluster Kubernetes topology?"). The system returns an honest `insufficient_evidence` state with citations to what actually exists.
2. **Private Routing Enforcement**: A user sets `privacy: private`. The router routes strictly to local/fixture. A test simulating an unavailable local provider verifies that the system hard-fails and never leaks data to cloud providers.
3. **Path Traversal Defense**: Malicious retrieval attempts (`../../etc/passwd`) are caught and blocked by path containment checks.
