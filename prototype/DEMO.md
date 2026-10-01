# DOCCAD Prototype Walkthrough & Demonstration Guide

A reproducible, 10-minute guided demonstration of the **DOCCAD** prototype.

DOCCAD is a GitHub-native, docs-as-code documentation platform where canonical engineering knowledge is authored by humans in a Git repository, and an offline AI generation pipeline derives governed, evidence-backed views (recruiter profiles, interview preparation kits, question answers) with mechanical sha256 drift detection and zero runtime model dependencies.

---

## Prerequisites & Verification

All commands are executed from the `prototype/` directory.

Before starting, verify that the environment and test suite pass cleanly:

```bash
cd prototype
npm run validate
npm run detect
npm run test
```

Expected output:
- `validate`: `Validated 40 pages, 4 interview datasets, 37 provenance hashes. OK`
- `detect`: `stale generated: 0; nothing to regenerate`
- `test`: `Ran 75 tests ... OK (0 failures, 0 errors, 0 expected failures)`

Build and serve the static site locally:

```bash
npm run build
npm run serve
```

The site is served locally at `http://localhost:3000/doCCAD_pre/`.

---

## 1. Journey 1: The Reader (Architecture & Canonical Ground Truth)

**Goal**: Inspect the human-authored canonical knowledge base, system architecture spine, architecture decision records (ADRs), interactive Mermaid diagrams, offline search, and bilingual navigation.

1. **Visit the Landing Page**:
   - Navigate to `http://localhost:3000/doCCAD_pre/`.
   - Observe the system metrics: **29 Canonical Documents**, **11 Governed Derived Views**, **100% Offline Static Serving**, and **sha256 Mechanical Drift Tracking**.
   - Notice that the landing page is fully internationalized.

2. **Bilingual Hungarian Navigation**:
   - In the top-right navbar dropdown, select **Magyar (Hungarian)** or navigate to `http://localhost:3000/doCCAD_pre/hu/`.
   - Observe the fully translated landing page hero: *"DOCCAD Dokumentációs Ökoszisztéma"*, localized navbar items (*Dokumentáció (Kanonikus)*, *Toborzói Nézet*, *Tudásbázis Böngésző*, *Kérdés Munkapad*, *Eltérés Ellenőr*), and localized footer links.
   - Verify that untranslated canonical documents (such as `http://localhost:3000/doCCAD_pre/hu/docs/architecture/system-overview`) gracefully fall back to the English source text with Hungarian navigation chrome rather than returning a 404 error (Decision D11).

3. **Explore the Canonical Architecture Spine**:
   - Navigate to `http://localhost:3000/doCCAD_pre/docs/architecture/system-overview`.
   - Examine the system architecture tenets (AD-1 through AD-15).
   - Scroll down to the embedded Mermaid C4 architecture diagrams. Notice that Mermaid diagrams render with strict security mode enabled (`securityLevel: 'strict'`).
   - Read the Architecture Decision Records under `/docs/decisions/` (e.g., ADR-001 GitHub Source of Truth, ADR-003 Two Content Planes, ADR-004 Provider Abstraction).

4. **Local Offline Search**:
   - Press the search bar (`Ctrl+K` or `/`) and search for `"drift"` or `"provenance"`.
   - Results appear instantly from local pre-computed search indices (`build/search-index.json` and `build/hu/search-index.json`) without any network API calls.

---

## 2. Journey 2: The Recruiter (Governed Derived Views & Evidence Linking)

**Goal**: Evaluate how DOCCAD condenses complex engineering architectures into tailored views with verifiable citations.

1. **Open the Recruiter Briefing**:
   - Navigate to `http://localhost:3000/doCCAD_pre/views/recruiter/project-overview`.
   - Read the top Provenance Banner: contract `GenerateRecruiterPage v1`, provider `fixture`, generation mode `demo`, and source hashes.

2. **Toggle Depth Views**:
   - Use the interactive tabs at the top of the page:
     - **30-Second Elevator Pitch**: High-level problem statement, solution, and core metrics.
     - **2-Minute Walkthrough**: Architectural breakdown, content plane separation, and governance gates.
     - **Deep Dive**: Complete competency matrix linking claims directly to evidence.

3. **Verify Competency Evidence Links**:
   - In the Competencies section, click on an `<EvidenceLink>` chip (e.g. `[architecture/system-overview.md#core-architecture-tenets]`).
   - Notice the link navigates directly to the exact canonical source page and section anchor, proving that the generated summary is grounded in repository ground truth.

4. **Explore Interview Preparation**:
   - Navigate to `http://localhost:3000/doCCAD_pre/views/interview/architecture-system-overview`.
   - Expand the collapsible accordion cards to review system concepts, design trade-offs, and sample technical interview questions with evidence citations.

---

## 3. Journey 3: The Contributor (Contract Generation & Drift Detection)

**Goal**: Generate an evidence-backed answer to an engineering question using the CLI pipeline, observe honest handling of unsupported queries, and verify mechanical drift detection.

1. **Ask a Supported Question via CLI**:
   ```bash
   python3 scripts/generate_question.py --question "How does DOCCAD detect drift?" --audience developer --persist
   ```
   - Observe the pipeline execution:
     - Retrieves canonical evidence from `docs/source/`.
     - Rejects non-markdown files and diagrams outside the contract's `allowed_evidence` filter.
     - Scans prompts for secrets (T6).
     - Renders prompt template `prompts/question-page.md` v2.
     - Invokes deterministic fixture provider.
     - Computes and stamps sha256 hashes of all evidence files into frontmatter.
     - Forces `approval_status: draft`.
     - Writes `docs/generated/questions/q-002-drift-detection.mdx`.

2. **Ask an Unsupported (Out-of-Scope) Question**:
   ```bash
   python3 scripts/generate_question.py --question "What is the multi-cluster Kubernetes topology?" --audience engineer
   ```
   - Notice that the pipeline does **not** hallucinate or invent an answer.
   - It outputs an honest `insufficient_evidence` candidate draft citing that Kubernetes deployment is outside the documented repository scope.

3. **Verify Mechanical Drift Detection**:
   ```bash
   npm run detect
   ```
   - `detect_changes.py` scans all 44 manifest entries, verifies the sha256 hash of each evidence document, and reports `stale generated: 0`.

---

## 4. Journey 4: The Reviewer (Governance State Machine & Publication Filter)

**Goal**: Step through the human governance lifecycle, verify that simulated demo approval is blocked from production release, and demonstrate the production hold-stub filter.

1. **Simulate Governance Review Transitions**:
   - Advance artifact from `draft` to `in-review`:
     ```bash
     python3 scripts/review_governance.py review --artifact q-002-drift-detection --decision in-review
     ```
   - Advance artifact from `in-review` to `approved-for-demo`:
     ```bash
     python3 scripts/review_governance.py review --artifact q-002-drift-detection --decision approved-for-demo --notes "Reviewed against canonical ADR-003"
     ```
   - List review ledger entries:
     ```bash
     python3 scripts/review_governance.py list
     ```

2. **Verify That Simulated Approval Cannot Publish to Production**:
   - Execute production readiness check:
     ```bash
     python3 scripts/review_governance.py check-production --artifact q-002-drift-detection
     ```
   - Command exits with code 1 and outputs:
     `BLOCKED: q-002-drift-detection only has simulated demo approval (approved-for-demo). It is NOT eligible for production publication build!`

3. **Demonstrate Production Build Filter & Hold Stubs**:
   - Run the production build filter:
     ```bash
     npm run build:production
     ```
     - `build_filter.py` stashes unapproved and demo-approved generated files to `.work/stashed_unapproved/`.
     - It writes honest hold stubs (`type: stub`, `stub_version: 1`, explicit `hold_reason: pending-human-approval`).
     - Builds the production static site without publishing unapproved content.
   - Restore the demo environment:
     ```bash
     npm run build:demo
     ```
     - Restores all stashed views from `.work/stashed_unapproved/` back to `docs/generated/`.
     - Rebuilds the demo site with all views active.

4. **Final System Health Check**:
   ```bash
   npm run validate && npm run detect
   ```
   - Confirms that all pages, datasets, and provenance hashes are valid and in sync.
