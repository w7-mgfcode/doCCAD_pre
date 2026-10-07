# DOCCAD Prototype

A runnable, local prototype of **DOCCAD**: a GitHub-native documentation system in which canonical,
human-owned documentation lives in the repository and an AI layer derives governed views from it —
recruiter pages, interview preparation, and answers to specific questions.

It is two things:

- **A static Docusaurus 3.10.2 + React 19 site** with two separate content planes: canonical pages at
  `/docs` and AI-derived views at `/views`. The site makes no model calls at runtime.
- **An offline generation and governance toolchain** in Python: task contracts, evidence retrieval,
  sha256 provenance hashes, drift detection, a simulated review ledger and a publication filter. The
  default AI provider is `fixture`, which is deterministic and needs no keys or network.

Design intent: [`planning/CONCEPT.md`](planning/CONCEPT.md). Requirements mapping (REQ-001…016):
[`planning/ACCEPTANCE.md`](planning/ACCEPTANCE.md). Status and verification record:
[`planning/PROGRESS.md`](planning/PROGRESS.md). The research archive behind it is
[`../docs/primary-inputs/`](../docs/primary-inputs/README.md).

## Status

Verified on 2026-10-07 (Node 24.19, Python 3.14, branch `phase-2-closeout` after the review fixes):

| Area | Works today | Not yet |
| --- | --- | --- |
| Static site | Builds in `en` and `hu`; landing page, navbar, footer, and search index localized; all 29 canonical and 11 generated pages | Untranslated canonical docs fall back to English source (D11 verified) |
| Checks | `validate`, `detect`, 190 unit tests (0 expected failures), `typecheck`, `build` all pass | — |
| Run reporting | Every generation run prints one `Run usage:` line (provider, returned model, calls, tokens, request IDs or `unavailable`), also when it fails; in Actions the same facts go to the step summary. Generated pages and interview datasets carry an explicit `visibility`, and the production filter treats an absent one as private | Step summary and run-ID branch names not yet observed on GitHub (owner action H3-5) |
| Question pipeline | `generate_question.py`: retrieval, supported and unsupported questions, private-routing refusal, `--persist`, UI→CLI round-trip, forced draft, pre-write grounding gate | — |
| Page pipeline | `generate_page.py` live pipeline verified with date normalization, grounding gate, link allowlist, and strict schema adherence (`TestLivePagePipeline`, `TestGroundingGate`) | — |
| Regeneration | Targeted deduplicated regeneration through `generate_page.py` and `generate_question.py`; `seed_generated_views.py` | — |
| Review | Simulated review ledger with strict state machine; production check blocks simulated approval | Real approval via GitHub PRs and branch protection (P1-05 code verified; DOCCAD GitHub App pending owner creation) |
| Cloud / local models | Secret scanning (T6), transport vs content error fallback semantics, privacy hard-pinning (T12), HTTP retry backoff, provider JSON schema derivation, sampling opt-in, per-run budget, grounding gate, prompt injection rejection, workflow generation environment | Gemini passed an owner-run live smoke test (P2-08, `VALIDATION.md` §7); Anthropic, OpenAI and local live calls NOT RUN |

## Requirements

- Node.js >= 24.14 and npm (see `.nvmrc`)
- Python 3 with dependencies declared in `requirements.txt` (`pip install -r requirements.txt`: PyYAML, jsonschema, referencing).
- Full schema validation requires `jsonschema` (with `referencing`). Without it, `validate_docs.py` warns and falls back to a
  minimal frontmatter check, or exits with code 1 if `DOCCAD_REQUIRE_JSONSCHEMA=1` is set in CI/production.

No API keys, database or network access are needed.

## Quick start

```bash
cd prototype
npm ci
npm run validate      # → "Validated 40 pages, 4 interview datasets, 25 provenance hashes." + OK
npm run build         # → [SUCCESS] for en, then for build/hu
npm run serve         # → http://localhost:3000/doCCAD_pre/
```

`npm run start` serves a live-reloading dev server instead, one locale at a time
(`npm run start -- --locale hu` for Hungarian).

## Commands

All from `prototype/`.

| Command | Does | Writes |
| --- | --- | --- |
| `npm run start` | Dev server with live reload | — |
| `npm run build` | Static build, `en` + `hu` | `build/` |
| `npm run serve` | Serve `build/` | — |
| `npm run typecheck` | `tsc` | — |
| `npm run validate` | Frontmatter schemas, plane separation, ID uniqueness, provenance hashes, links, MDX safety. Exits 1 on failure | — |
| `npm run detect` | Drift report: which generated pages are stale. **Always exits 0 — read the output** | `.docs-manifest.json`, `impact.json` |
| `npm run test` | `unittest` suite | Temporarily moves files out of `docs/generated/` and restores them |
| `npm run build:demo` | Restore stashed views, then build | `docs/generated/`, `build/` |
| `npm run build:production` | Remove drafts and demo-approved views, then build | **`docs/generated/`** — run `build:demo` afterwards |
| `npm run clear` | Clear Docusaurus caches | — |

Several commands rewrite tracked files. To look without changing anything, work on a copy. Run this
from the repository root, and copy `.github/` too, because one test checks the workflows' script calls:

```bash
mkdir -p /tmp/doccad && rsync -a .github /tmp/doccad/
rsync -a --exclude node_modules --exclude build --exclude .docusaurus prototype /tmp/doccad/
ln -s "$PWD/prototype/node_modules" /tmp/doccad/prototype/node_modules && cd /tmp/doccad/prototype
```

## Using the site

| Route | What to do there |
| --- | --- |
| `/` | Landing page: vision, tenets, navigation cards |
| `/docs/overview` | Canonical documentation: architecture, decisions (ADRs), security, operations, Mermaid diagrams |
| `/views/recruiter/project-overview` | Recruiter view: switch between 30-second, 2-minute and deep-dive modes; evidence links jump to the canonical source |
| `/views/interview/…` | Interview prep: concepts, design decisions, tradeoffs, likely questions, model answers |
| `/views/questions/…` | Question pages `q-001`…`q-005`; `q-006` shows the honest `insufficient_evidence` answer |
| `/workbench` | Question Workbench: choose a question, inspect evidence, generate a draft, step through simulated review, export `QuestionRequest.json` |
| `/inspector` | Drift Inspector: source hashes and staleness |
| `/explorer` | Knowledge Explorer |
| `/hu/` | Hungarian locale |

Search is local and offline (search box, or `/search`).

The workbench runs entirely in the browser. It uses built-in example scenarios, and for a custom question
it assembles a demo draft on the client. It does not call the Python pipeline. For real retrieval and
generation, export the request and run it through the CLI (below).

Every generated page carries a provenance banner: contract, provider, model, source hashes and approval
state. `approved-for-demo` is a simulated demo record, never a human approval.

## Using the toolchain

### Ask a question

```bash
python3 scripts/generate_question.py --question "How does DOCCAD detect drift?" --audience developer
```

It prints the evidence it retrieved (with hashes), the files it rejected and why, and the provider chain,
then writes a draft to `.work/drafts/<id>.mdx`. Useful options:

| Option | Effect |
| --- | --- |
| `--request QuestionRequest.json` | Run a request exported from `/workbench` (UI→CLI round-trip) |
| `--target <doc-id>` | Focus retrieval on one canonical page |
| `--privacy private` | Route only to the local provider; fails with `PrivacyRoutingError` rather than use a cloud provider |
| `--export-run run.json` | Save the GenerationRun record (evidence, provider, hashes) |
| `--persist` | Write to `docs/generated/questions/` instead of `.work/drafts/` |

An out-of-scope question (for example, *"What is the multi-cluster Kubernetes topology?"*) produces an
`insufficient_evidence` page instead of an invented answer.

### Review a generated artifact

```bash
python3 scripts/review_governance.py review --artifact q-002-drift-detection --decision in-review
python3 scripts/review_governance.py review --artifact q-002-drift-detection --decision approved-for-demo --notes "checked"
python3 scripts/review_governance.py list
python3 scripts/review_governance.py check-production --artifact q-002-drift-detection   # BLOCKED, exit 1
```

States: `draft` → `in-review` → `approved-for-demo` or `rejected`. Other moves are refused (exit 1):
a new artifact starts at `draft` or `in-review`, approval needs `in-review` first, `rejected` and
`approved-for-demo` go back through `draft`, and repeating the current state is refused. The ledger is
`.work/demo_reviews.json`. `check-production` always blocks simulated approval, since production
publication requires a real, human-approved pull request.

### Detect drift and regenerate

1. Edit a canonical page, for example `docs/source/architecture/content-planes.md`.
2. `npm run detect` lists the generated pages built from that page as stale, with a regeneration plan.
   Unrelated views stay clean.
3. `npm run validate` now fails on the provenance-hash mismatch.
4. Regenerate: `python3 scripts/seed_generated_views.py` rebuilds all derived views with current hashes.
   For a single question page, `generate_question.py --persist` also works.
5. `npm run detect` reports `stale generated: 0`, and `npm run validate` passes.

Never hand-edit files under `docs/generated/`; they are produced by these scripts.

### Preview a page-generation contract

```bash
python3 scripts/generate_page.py --contract GenerateRecruiterPage --target architecture-system-overview --dry-run
```

This prints the filtered evidence and the assembled prompt without calling a model or writing anything.
The contracts are `GenerateRecruiterPage`, `GenerateInterviewPrep` and `GenerateQuestionPage`
(`contracts/*.yaml`).

### Production vs demo build

```bash
npm run build:production   # drafts and demo-approved views moved to .work/stashed_unapproved/, hold stubs left
npm run serve              # those views are gone
npm run build:demo         # REQUIRED afterwards: restores them
```

## AI providers

Routing is configured in `ai.config.yaml` and implemented in `ai/router.py`:

- `fixture` is the default and comes first in every public chain.
- `privacy: private` routes only to `local`. `local` is disabled by default, so private tasks fail on
  purpose; they never fall back to a cloud provider.
- Model IDs are never written in code or config, only referenced as `${AI_MODEL_*}` environment
  variables.
- The provider chain falls back only on transport or HTTP failures, never on content.

For live generation (exercised locally and in CI with Gemini; Anthropic, OpenAI and local NOT RUN): copy `.env.example` to `.env`, which is git-ignored, and fill in
the keys and `AI_MODEL_*` values. To use a local model, set `local.enabled: true` in `ai.config.yaml` and run
an OpenAI-compatible endpoint (for example Ollama) at `http://localhost:11434/v1`. Never commit `.env`.

## Layout

| Path | Contents |
| --- | --- |
| `docs/source/` | Canonical pages (`type: canonical`), served at `/docs` |
| `docs/generated/` | Derived views (`type: generated`), served at `/views` — script output only |
| `docs/diagrams/` | Mermaid sources |
| `i18n/hu/` | Hungarian translations |
| `src/` | Components (`EvidenceLink`, `InterviewPrep`, `ProvenanceBanner`, `QuestionWorkbench`, `DriftInspector`, `KnowledgeExplorer`) and pages |
| `ai/`, `ai.config.yaml` | Provider protocol, adapters, router, routing policy |
| `contracts/`, `prompts/`, `schemas/` | Task contracts, prompt templates, JSON schemas |
| `scripts/` | Validate, detect, generate, seed, review, build filter |
| `tests/` | `unittest` suite |
| `planning/` | Concept, acceptance matrix, progress |
| `.docs-manifest.json`, `impact.json` | Dependency manifest and last drift report (rewritten by `detect`) |
| `.work/` | Drafts, review ledger, stashed views (git-ignored) |

## Governance

DOCCAD enforces a strict two-step governance model to guarantee that AI-derived documentation cannot reach production without verified human code-owner review (AD-9, ADR-005, E3):

1. **Review Claim (`review_governance.py approve`)**:
   A human reviewer on a pull request branch runs:
   ```bash
   python3 scripts/review_governance.py approve --artifact <id> --pr <pr-number> --reviewer <github-login>
   ```
   This verifies the artifact is currently in `in-review`, computes `approved_hash` (sha256 of the markdown body), and stamps an `approval_record` into the document frontmatter. If the body is modified afterwards, the hash mismatch immediately invalidates the approval and returns the view to `in-review`.

2. **Publish Verification Gate (`build_filter.py --mode production` / `publish.yml`)**:
   The CLI stamp is a claim; the production publication gate is the GitHub API check during the `publish` workflow on `main`. For every page claiming `approval_status: approved`, the gate verifies via the GitHub REST API:
   - The pull request `pr` is merged into `main`.
   - The pull request was reviewed and approved by an authorized CODEOWNER (from `.github/CODEOWNERS`) matching `approved_by`.
   - The pull request touched the specific file.
   - Current content hash matches `approved_hash`.
   Any verification negative excludes the page from publication, replacing it with an audited production hold stub. Infrastructure/API/permission errors fail the build job immediately to prevent deploying unverified documentation.

   > [!IMPORTANT]
   > **Sole CODEOWNER, so generation PRs must be bot-authored (E8).** GitHub does not let a PR's author
   > approve it, and `@w7-mgfcode` is the only code owner. A generated view can therefore only reach
   > production through a PR opened by the **DOCCAD GitHub App**. `generate.yml` does this when the App is
   > configured; without it, the workflow only pushes the `docs-gen/*` branch and the E3 gate cannot pass.

### Setting up the DOCCAD GitHub App (E8, one-time, owner)

1. Create the App at <https://github.com/settings/apps/new>: any name (e.g. `doccad-generator`), homepage
   `https://github.com/w7-mgfcode/doCCAD_pre`, **Webhook: inactive**, repository permissions
   **Contents: Read and write** and **Pull requests: Read and write** (nothing else), "Only on this account".
2. On the App page, note the **Client ID**, then **Generate a private key** (a `.pem` file downloads).
3. **Install App** → only the `doCCAD_pre` repository.
4. Store the credentials (the key stays out of the repository and out of chat):
   ```bash
   gh variable set DOCCAD_APP_CLIENT_ID --repo w7-mgfcode/doCCAD_pre --body "<client id>"
   gh secret set DOCCAD_APP_PRIVATE_KEY --repo w7-mgfcode/doCCAD_pre < path/to/key.pem
   ```
   Then delete the local `.pem` or keep it in a password manager.

`generate.yml` mints a short-lived installation token with `actions/create-github-app-token`, narrowed to
contents and pull-requests write, pushes the branch and opens the PR as `<app>[bot]`. PRs opened with an
App token trigger `ci.yml`, unlike PRs opened with `GITHUB_TOKEN`.

### End-to-end approval of a generated view

1. **Actions → generate → Run workflow** (contract, target, privacy, provider). The workflow pushes
   `docs-gen/<contract>-<target>-<run-id>` (`-<attempt>` added on a re-run) and the App opens it as a PR;
   `validate-and-build` runs on it; the page is `draft`.
2. Check out the branch, review the page against its cited canonical sources, then from `prototype/`:
   ```bash
   python3 scripts/review_governance.py review --artifact <id> --decision in-review
   python3 scripts/review_governance.py approve --artifact <id> --pr <PR number> --reviewer w7-mgfcode
   ```
   Commit and push the stamped frontmatter to the PR branch (the docs-gen path guard allows it).
3. Approve the PR as code owner (after the stamp, so the review time is later than `approved_at`), and merge.
4. `publish` re-verifies the record against the GitHub API (merged, approved by `approved_by`, file in the
   PR, body hash unchanged) and only then publishes the page; otherwise it ships the hold stub.

### GitHub Repository Ruleset Configuration

Repository rulesets on `main` must be applied by the repository owner (`@w7-mgfcode`) via GitHub repository settings (H-8):
- **Target branch**: `main`
- **Require a pull request before merging**: enabled
  - Require approvals: `1`
  - Require review from Code Owners: enabled
  - Dismiss stale pull request approvals when new commits are pushed: enabled
- **Require status checks to pass before merging**: enabled
  - Required check: `validate-and-build` (from workflow `ci.yml`)
  - Require branches to be up to date before merging: disabled
- **Block force pushes** and **branch deletion**: enabled
- **Bypass list**: repository admins, "for pull requests only". The owner uses it to merge their own PRs (which they cannot approve); a bot-authored generation PR needs no bypass, because the owner approves it as code owner.
- Applied 2026-10-01 as ruleset `main-protection` (id 24289740).

## Rules

- Canonical pages never import or cite generated pages.
- Generated pages come only from `scripts/` and carry a `generation` block with source hashes.
- `approved-for-demo` is a simulation. Never present it as human approval.
- The site never calls a model at runtime.
- Python code uses the standard library, PyYAML, `jsonschema` and `referencing` only (`requirements.txt`).
- No keys, tokens or `.env` values in the repository.

Contributor and agent conventions: [`../AGENTS.md`](../AGENTS.md).

## Known issues

- **Question regeneration plans are not directly executable.** For a stale question page, `impact.json` lists only `--target <source id>`, not the original question, so running it literally creates a different page. Regenerate a question page with its original question: `python3 scripts/generate_question.py --question "<original question>" --persist` (for `q-002`: "How does DOCCAD detect drift?").
- **`detect_changes.py --range`** operates on git revision ranges (e.g. `HEAD~1...HEAD`); for a full-workspace scan without git range inspection, use `--all`.
- **The test suite exercises the production filter.** An interrupted test run can leave unapproved views stashed in `.work/stashed_unapproved/`; `npm run build:demo` restores them.
- **Not verified in CI:** browser smoke tests and screenshots, mobile layout, Mermaid rendering in a live browser (interactive `/browser` available in Antigravity 2.0 app), and live provider calls with real API keys (owner-executed under spend caps, P2-08: Gemini PASS, others NOT RUN).
