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

Verified on 2026-10-01 (Node 24.19, Python 3.14, branch `next-version`):

| Area | Works today | Not yet |
| --- | --- | --- |
| Static site | Builds in `en` and `hu`; landing page, navbar, footer, and search index localized; all 29 canonical and 11 generated pages | Untranslated canonical docs fall back to English source (D11 verified) |
| Checks | `validate`, `detect`, 75 unit tests (0 expected failures), `typecheck`, `build` all pass | — |
| Question pipeline | `generate_question.py`: retrieval, supported and unsupported questions, private-routing refusal, `--persist`, UI→CLI round-trip, forced draft | — |
| Page pipeline | `generate_page.py` live pipeline verified with date normalization and strict schema adherence (`TestLivePagePipeline`) | — |
| Regeneration | Targeted deduplicated regeneration through `generate_page.py` and `generate_question.py`; `seed_generated_views.py` | — |
| Review | Simulated review ledger with strict state machine; production check blocks simulated approval | Real approval via GitHub PRs and branch protection (Phase 1 P1-05) |
| Cloud / local models | Secret scanning (T6), transport vs content error fallback semantics, privacy hard-pinning (T12) | Real cloud provider calls deferred to Phase 2 with owner API keys |

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
npm run validate      # → "Validated 40 pages, 4 interview datasets, 37 provenance hashes." + OK
npm run build         # → [SUCCESS] for en, then for build/hu
npm run serve         # → http://localhost:3000
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

Several commands rewrite tracked files. To look without changing anything, copy the directory first:

```bash
rsync -a --exclude node_modules --exclude build --exclude .docusaurus prototype/ /tmp/doccad/
ln -s "$PWD/prototype/node_modules" /tmp/doccad/node_modules && cd /tmp/doccad
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
(`contracts/*.yaml`). Live runs currently fail; see Known issues.

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

For live generation (not yet exercised): copy `.env.example` to `.env`, which is git-ignored, and fill in
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
   > **Sole CODEOWNER and Bot-Authored PRs (Blocked on E8)**:
   > GitHub branch protection rules prohibit PR authors from approving their own pull requests. Because `@w7-mgfcode` is the sole CODEOWNER, any PR authored directly by `@w7-mgfcode` cannot receive a CODEOWNER approval from `@w7-mgfcode`.
   > While the generation workflow (`generate.yml`) pushes a `docs-gen/*` branch that the repository owner manually opens as a pull request, the owner is recorded as the PR author and cannot self-approve. Therefore, **real E3 production approval cannot pass while the owner opens docs-gen PRs**.
   > End-to-end automated E3 production approval remains **BLOCKED on decision E8** (configuring a GitHub App bot token so that pull requests are opened directly by the bot, allowing `@w7-mgfcode` to act independently as the approving CODEOWNER).

### GitHub Repository Ruleset Configuration

Repository rulesets on `main` must be applied by the repository owner (`@w7-mgfcode`) via GitHub repository settings (H-8):
- **Target branch**: `main`
- **Require a pull request before merging**: enabled
  - Require approvals: `1`
  - Require review from Code Owners: enabled
  - Dismiss stale pull request approvals when new commits are pushed: enabled
- **Require status checks to pass before merging**: enabled
  - Required check: `validate-and-build` (from workflow `ci.yml`)
  - Require branches to be up to date before merging: enabled
- **Block force pushes**: enabled
- **Bypass list**: Repository admin / owner bypass permitted for "Pull Requests only" to satisfy ruleset while unblocking bot PR merges.

## Rules

- Canonical pages never import or cite generated pages.
- Generated pages come only from `scripts/` and carry a `generation` block with source hashes.
- `approved-for-demo` is a simulation. Never present it as human approval.
- The site never calls a model at runtime.
- Python code uses the standard library and PyYAML only.
- No keys, tokens or `.env` values in the repository.

Contributor and agent conventions: [`../AGENTS.md`](../AGENTS.md).

## Known issues

- **`detect_changes.py --range`** needs git history; until the repository has remote commits, use `--all` for a full-workspace scan.
- **The test suite exercises the production filter.** An interrupted test run can leave unapproved views stashed in `.work/stashed_unapproved/`; `npm run build:demo` restores them.
- **Not verified in CI:** browser smoke tests and screenshots, mobile layout, Mermaid rendering in a live browser (interactive `/browser` available in Antigravity 2.0 app), and live cloud provider calls with real API keys (deferred to Phase 2).
