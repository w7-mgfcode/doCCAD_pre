# AGENTS.md — doCCAD_pre

<!-- BEGIN maintaining-agent-docs (generated) -->

## Project

PRE-DOCCAD: the preparatory knowledge project for **DOCCAD**, a GitHub-native, AI-augmented
documentation system in which canonical, human-owned documentation lives in a repository and an AI
layer derives governed views from it (recruiter pages, interview prep, question answers). This
repository holds two things:

- `docs/primary-inputs/` — the provenance-aware research and design archive (sections 00–12).
- `prototype/` — a runnable local DOCCAD prototype: Docusaurus 3.10.2 + React 19 static site, Python
  governance scripts, a provider-agnostic AI router, task contracts and JSON schemas.

The repository is a git repository (initialized 2026-09-29; branch `main`, first commit 2026-09-29,
no remote yet — `docs/primary-inputs/README.md` still says it is uninitialized, which predates this).
Git history starts at that initial import, so `git log` explains nothing from before it. `.claude/`,
`.agents/`, `.kb/` and local session notes are git-ignored, so git does not track the agent layer. Read-only git commands (`status`, `diff`, `log`) are fine; do not commit, push, or create
branches unless asked.

## Project structure

| Path | What it is |
| --- | --- |
| `docs/primary-inputs/` | Archive. Map: `PROJECT_STRUCTURE.md`. Entry: `README.md` → `00_PROJECT_CONTROL/PROJECT_INDEX.md` |
| `docs/prototype-planning/` | How the prototype prompt was derived (`ANALYSIS.md`, `ANTIGRAVITY_PROMPT.txt`) |
| `prototype/docs/source/` | Canonical pages (`type: canonical`), served at `/docs` |
| `prototype/docs/generated/` | AI-derived views (`type: generated`), served at `/views` |
| `prototype/ai/`, `prototype/ai.config.yaml` | Provider router and adapters; `fixture` is the default provider |
| `prototype/scripts/` | validate, detect drift, generate page/question, seed generated views, review governance, build filter |
| `prototype/contracts/`, `prototype/schemas/`, `prototype/prompts/` | Generation contracts, JSON schemas, prompt templates |
| `prototype/src/` | Site components and pages (workbench, inspector, explorer) |
| `prototype/tests/` | `unittest` suite |
| `prototype/planning/` | `CONCEPT.md`, `ACCEPTANCE.md` (REQ-001…016), `PROGRESS.md` |

## Setup

- Node >= 24.14 (`prototype/package.json:38`, `prototype/.nvmrc`) and Python 3 with dependencies declared in `prototype/requirements.txt` (`pip install -r prototype/requirements.txt`: PyYAML, jsonschema, referencing). From `prototype/`: `npm ci`.
- Full schema validation requires `jsonschema` (with `referencing`). Without it,
  `validate_docs.py` warns and falls back to a minimal frontmatter check (`scripts/validate_docs.py`), or exits with code 1 if `DOCCAD_REQUIRE_JSONSCHEMA=1` is set.
- No API keys are needed. `prototype/.env.example` lists optional provider keys and `AI_MODEL_*`
  variables for live generation only; never create or commit a real `.env`.

## Build and run

All commands run from `prototype/` (`prototype/package.json:7-16`):

| Command | Does |
| --- | --- |
| `npm run start` / `npm run serve` | Dev server / serve the built site |
| `npm run build` | Static build, both locales (`en`, `hu`) |
| `npm run build:demo` | Restores stashed demo views, then builds |
| `npm run build:production` | **Rewrites `docs/generated/`**: moves unapproved and demo-approved files to `.work/stashed_unapproved/` and leaves hold stubs in their place, then builds. Run `npm run build:demo` afterwards to restore them |
| `npm run typecheck` | `tsc` |
| `npm run clear` | Clear Docusaurus caches |

## Test and verification (definition of done)

From `prototype/`:

1. `npm run validate` — frontmatter schemas, plane separation, ID uniqueness, provenance hashes, link and security checks. Must exit 0 (and is only a full schema check when `jsonschema` is installed).
2. `npm run detect` — drift report; rewrites `.docs-manifest.json` and `impact.json`. Always exits 0, so read its output: any stale generated page must be regenerated.
3. `npm run test` — `python3 -m unittest discover tests -v`.
4. For site changes: `npm run typecheck` and `npm run build`.

Several commands rewrite state: `detect` (`.docs-manifest.json`, `impact.json`), review and
generation scripts (`.work/`), `build:production` (`docs/generated/`), and the test suite, which
exercises the production filter on the live `docs/generated/` tree and restores it in `tearDown` —
an interrupted run can leave it stashed; `npm run build:demo` restores. For a read-only health check, copy `prototype/` (without `node_modules/`, `build/`, `.docusaurus/`) to a
scratch directory and run them there.

## Safety rules and conventions

- **Never edit** `docs/primary-inputs/11_RAW_ARCHIVE/` or `docs/primary-inputs/03_PROMPTS/`
  (`docs/primary-inputs/README.md`). Organized copies stay traceable to their raw sources; improve
  them through new artifacts or FUTURE tasks, and never recycle a stable ID
  (`docs/primary-inputs/CONTRIBUTING.md`). `docs/primary-inputs/_to_delete/` is outside the archive
  structure (not in `PROJECT_STRUCTURE.md`); do not use it as a source.
- **Two planes.** Canonical pages never import generated pages or cite them as evidence (a
  convention — `validate_docs.py` checks plane location and type, not citations). Generated pages are
  produced by `prototype/scripts/`, never hand-edited, and carry a `generation` block with source hashes.
- **Simulated approval is not approval.** `approved-for-demo` is a demo record; never claim human
  approval.
- **AI layer.** `fixture` stays the deterministic default; `privacy: private` routes only to the
  local provider and must fail rather than fall back to cloud; model IDs only via `${AI_MODEL_*}`.
- **Static site.** No runtime model calls from the site.
- **Dependencies.** Python: standard library + PyYAML only. Do not add packages without asking.
- **Secrets.** Never write keys, tokens or `.env` values anywhere.
- Never edit generated output: `prototype/build/`, `prototype/.docusaurus/`, `node_modules/`.

## Path-scoped rules

Detailed conventions live in `.claude/rules/` (local-only; the directory is git-ignored). The index
`.claude/rules/README.md` maps each rule to the paths it governs. Agents without path-glob loading
should read the matching rule before editing: `primary-inputs.md` (archive), `prototype-content.md`
(pages and translations), `prototype-code.md` (scripts, AI layer, contracts, tests),
`prototype-site.md` (Docusaurus config and components).

<!-- END maintaining-agent-docs -->
