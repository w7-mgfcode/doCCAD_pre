# 03 — Next-Version Plan: from prototype to usable DOCCAD

Prepared 2026-10-01. Inputs: `01_CONTEXT_MAP.md` (state and gaps, with evidence) and `02_RESEARCH_KB.md`
(web research A/B/C, conflicts D, open questions E). Executed by a long Antigravity 2.0 + Gemini 3.8 Flash
run from `05_ANTIGRAVITY_PROMPT.txt` (Phases 0–2); Phase 3 is specified only.

## Vezetői összefoglaló (HU)

A DOCCAD prototípus helyben működik és ellenőrzött: a validáció, a drift-észlelés, 33 teszt (egy tudatosan
„várt hibával"), a típusellenőrzés és a kétnyelvű (angol–magyar) build mind zöld (2026-10-01). Használható
termékké azonban még nem vált. Az élő AI-generálás hibára fut, több biztonsági kapu csak le van írva, de
nincs megvalósítva, nincs CI és nincs publikálás, a „jóváhagyott" állapotot pedig semmi sem állítja elő
hitelesen.

A terv négy fázisból áll:

- **0. fázis – stabilizálás.** Minden igazolt hiba javítása, a hiányzó biztonsági kapuk (MDX-import tiltás,
  link-allowlist, Mermaid `strict`, titokszkennelés, privát tartalom kizárása) beépítése, valamint az
  M6–M8 mérföldkövek lezárása: magyar nyitóoldal és navigáció, böngészős ellenőrzés, `VALIDATION.md`,
  `DEMO.md`, `LIMITATIONS.md`.
- **1. fázis – telepíthető és szabályozott.** GitHub remote, CI-kapu, GitHub Pages publikálás OIDC-vel, és
  valódi, PR-alapú emberi jóváhagyás a szimulált helyett.
- **2. fázis – élő AI-generálás.** Valódi szolgáltatói hívások a meglévő routeren át, a `fixture` marad az
  alapértelmezett. Strukturált kimenet és helyi sémavalidáció, újrapróbálás, költségplafon,
  forrás-hűségi kapu.
- **3. fázis – külső repók bevonása.** Csak specifikáció. Tulajdonosi döntést igényel, mert érinti a
  „multi-repo föderáció" nem-célt.

A futás előtt a tulajdonosnak kell elvégeznie a következőket: a függő változások commitja, döntés a
nyilvános repóról és a névről, az Antigravity jogosultságainak és archívum-védő hookjának beállítása,
később pedig a kulcsok, a költéskorlátok és a branch-szabályok beállítása. Ezek nélkül a futás az adott
lépésnél megáll, és nem talál ki megoldást.

## 1. Scope and mapping to the archive roadmap

The archive already defines the production roadmap — MVP M1.1–M1.6, SCALE M2.1–M2.5, HARDEN M3.1–M3.4
(`docs/primary-inputs/08_TASKS/future/implementation_roadmap.csv`). This plan does not replace it; it
sequences the next run against it.

| Plan phase | Roadmap milestones advanced | Outcome |
|---|---|---|
| Phase 0 — Stabilize | completes prototype M6–M8; closes defects blocking M1.4, M1.5, M2.3; security gates from M3.3 | A prototype whose every claim is true and every documented gate exists |
| Phase 1 — Deployable and governed | M1.1 (CODEOWNERS, protection), M1.2 (CI), M1.3 (Mermaid gate), M1.6 (publish), part of M1.5 (bot PR flow) | Site live on Pages; generation lands only via approved PRs |
| Phase 2 — Live generation | M1.4 ("live call works with one key"), M1.5, M2.1 (provider matrix), part of M3.1, M3.2 | Real providers behind the fixture default, gated by schema and grounding checks |
| Phase 3 — External evidence (spec only) | none (new scope, NV-SUP-2) | Owner decision + specification |

Not in scope: L2+ retrieval (ADR-006 boundary not tripped), runtime chat, SSO, the six missing task
contracts beyond what a phase needs, numbered-taxonomy re-foldering (`01_CONTEXT_MAP.md` §4, reversible
prototype choice).

## 2. Run rules that apply to every item

- **Work on one branch** (`next-version` or as the owner names it); no parallel agents on the same tree
  (`02_RESEARCH_KB.md` A2.8). No push, no PR creation, no remote operations by the run unless an item says
  the owner has enabled it.
- **Evidence or it did not happen.** An item is done only when its acceptance command has been run in this
  run, and `prototype/planning/PROGRESS.md` §Evidence log records: item ID, exact command, exit code, the
  key output line, date. No check may be described in docs, code comments or generated content unless the
  script that implements it exists and a test exercises it (`01_CONTEXT_MAP.md` §6.1, last probe row).
- **Verify edits by command, never by narration**: after each file edit, `git diff --stat` (or re-read the
  file) must show the change (`02_RESEARCH_KB.md` A5.6).
- **Bounded attempts**: if a fix fails twice, stop that item, record the failing command, the error and
  what was tried in PROGRESS.md §Tried-and-failed, and move to the next independent item
  (`02_RESEARCH_KB.md` A5.5).
- **Gate at every phase boundary**: from `prototype/`, `npm run typecheck && npm run validate && npm run test
  && npm run build` all exit 0, and `npm run detect` reports `stale generated: 0`. Then start a fresh
  conversation that resumes from PROGRESS.md (A6.2, A6.3).
- **Contract/schema/prompt changes** bump the version (`.claude/rules/prototype-code.md`), then
  `python3 scripts/seed_generated_views.py` (or targeted regeneration) and `npm run detect` → 0 stale.
- **Invariants** (never weakened): two planes; generated pages only via scripts; `fixture` default;
  `privacy: private` → `local` only, hard fail; model IDs only via `AI_MODEL_*`; no runtime AI; Python
  stdlib + PyYAML (+ owner-approved packages); simulated approval is never human approval.

## 3. Pre-run checklist (owner — human actions)

| # | Action | Why | Blocks |
|---|---|---|---|
| H-1 | Commit the four uncommitted files from 2026-09-30 (`git status`), or tell the run to treat them as its starting point | Clean, attributable baseline | Run start |
| H-2 | Answer E1 (public/private) and E2 (owner/repo name or domain) from `02_RESEARCH_KB.md` §E | `url`/`baseUrl`, Pages availability | P1-04, P1-03 |
| H-3 | Antigravity permissions: allow `npm ci`, `npm run *`, `npx tsc`, `npx docusaurus *`, `python3 scripts/*`, `python3 -m unittest *`, read-only `git status/diff/log`; deny `git push`, writes to `.env*`, and anything under `docs/primary-inputs/11_RAW_ARCHIVE/` and `docs/primary-inputs/03_PROMPTS/` | Default sandbox has no network; the run stalls on `npm ci` (A2.4) | Run start |
| H-4 | Optional but recommended: a PreToolUse hook in `.agents/hooks.json` denying edits to the two archive layers and `.env*` (A3.4); a trivial `always_on` canary rule in `.agents/rules/` to confirm git-ignored `.agents/` loads (A3.3) | Archive protection equivalent to `.claude/settings.json` | — |
| H-5 | Use the Antigravity 2.0 app (not the CLI) so `/browser` is available (A4.3); keep `localhost` in the browser allowlist | M7 browser evidence | P0-15 |
| H-6 | Decide E6 (dependencies). Assumed approved: `jsonschema` + `referencing` as declared requirements. Everything else needs an explicit yes | `AGENTS.md`: no packages without asking | P0-02, P1-09, P0-15 (CI smoke) |
| H-7 (Phase 1) | Create the GitHub repository and push `main`; enable Pages with source "GitHub Actions"; create environments `github-pages` (branch `main`) and `generation` (branch `main`, optional required reviewer) | Remote operations are human-only (A7.3) | P1-02…P1-08 |
| H-8 (Phase 1) | Apply the ruleset on `main` (P1-05) and, if E7 = yes, create the GitHub App and store its credentials as secrets | Approval gate; bot-PR checks (D5) | P1-05, P1-07 |
| H-9 (Phase 2) | Answer E5; create provider keys with expiry and hard spend caps; store them only as `generation` environment secrets or local `.env` (git-ignored); set `AI_MODEL_*` values | Live calls (T7) | P2-10 |

**Status 2026-10-01 (pre-run preparation session):**
- H-1 — done: the pending changes and this pack are committed on branch `next-version` (see `git log`).
- H-4 — done: `.agents/hooks.json` + `.agents/hooks/doccad_guard.py` installed and verified live
  (`02_RESEARCH_KB.md` A9); it denies pushes, remote/`gh` operations, destructive git, protected-path
  writes and `.env`/key access. Self-test: `python3 .agents/hooks/test_doccad_guard.py` (31/31).
- H-3 — partly done: the dangerous half (deny rules) is covered by the guard, so no global setting was
  changed. **Still open (owner):** commands in the 2.0 app need manual approval
  (`CASCADE_COMMANDS_AUTO_EXECUTION_OFF`); for an unattended run, set the `doCCAD_pre` project's command
  auto-execution to eager in the app's project settings, or approve commands as they come.
- H-2, H-5, H-6 (beyond `jsonschema` + `referencing`), H-7…H-9 — open.

The run must stop at any item whose human prerequisite is missing, record "BLOCKED: <prerequisite>" in
PROGRESS.md, and continue with independent items.

## 4. Phase 0 — Stabilize the baseline

Item format: **Rationale** · **Files** · **Traces** · **Acceptance** (exact command or observable) ·
**Risks** · **Human**. Commands run from `prototype/` unless stated. New test class names are part of
the acceptance contract so the check is executable.

### P0-01 Baseline re-verification and evidence log
- **Rationale**: start from measured state, not from this plan.
- **Files**: `prototype/planning/PROGRESS.md` (add §Evidence log, §Tried-and-failed, §Blocked).
- **Traces**: REQ-015; AD-10.
- **Acceptance**: `npm run typecheck && npm run validate && npm run test && npm run build` exit 0;
  `npm run detect` prints `stale generated: 0`; results logged with date.
- **Risks**: tests rewrite `docs/generated/` and restore it; an interrupted run leaves files stashed
  (`npm run build:demo` restores).
- **Human**: H-1.

### P0-02 Declare Python requirements; make degraded validation visible
- **Rationale**: `validate_docs.py` silently falls back to a 5-key check without `jsonschema`
  (`scripts/validate_docs.py:114-127`); CI must never run the degraded check.
- **Files**: new `prototype/requirements.txt` (`PyYAML`, `jsonschema`, `referencing`, pinned);
  `scripts/validate_docs.py` (print a `WARNING: jsonschema not installed — minimal fallback` line, and exit
  1 when `DOCCAD_REQUIRE_JSONSCHEMA=1` is set and the import fails); `AGENTS.md` Setup line; `README.md`.
- **Traces**: REQ-009, REQ-015; AD-10.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestValidatorDependencyMode -v` passes (simulates
  the missing import and asserts the warning and the strict-mode exit 1).
- **Risks**: none significant. `AGENTS.md` is canonical for all agents — keep the edit to the Setup line.
- **Human**: H-6 (assumed yes).

### P0-03 Node version alignment
- **Rationale**: Node 20 is EOL since 2026-04-30 (B2); ADR-002 requires Node ≥24.14 (D2).
- **Files**: `prototype/package.json` (`engines.node: ">=24.14"`), new `prototype/.nvmrc` (`24`), `README.md`.
- **Traces**: DEC-003 / ADR-002.
- **Acceptance**: `node -e "process.exit(require('./package.json').engines.node === '>=24.14' ? 0 : 1)"`;
  `npm ci` and `npm run build` exit 0 on the local Node 24.
- **Risks**: none (local Node is v24.19.0).
- **Human**: —

### P0-04 Live `generate_page.py` passes validation (recruiter and interview)
- **Rationale**: both live paths fail today (`01_CONTEXT_MAP.md` §6.1): YAML `last_validated` parses to a
  `date`; the fixture's interview JSON does not match `interview.schema.json`.
- **Files**: `scripts/generate_page.py` (normalize frontmatter before validation, reusing
  `validate_docs._normalize`); `ai/fixture_provider.py` (interview output in schema shape: concept objects
  `name/explanation`, `design_decisions[].evidence`, `tradeoffs[].choice/benefit/cost`,
  `example_answers` objects, `evidence_links[].to`).
- **Traces**: REQ-010, REQ-011; DEC-005; M1.5.
- **Acceptance** (on a scratch copy, because the commands write files):
  `python3 scripts/generate_page.py --contract GenerateRecruiterPage --target architecture-system-overview`
  and `… --contract GenerateInterviewPrep --target architecture-system-overview` both exit 0, then
  `python3 scripts/validate_docs.py` exits 0; `python3 -m unittest tests.test_doccad.TestLivePagePipeline -v`
  passes (runs both contracts through the fixture into a temp copy).
- **Risks**: changing fixture output changes seeded content → re-seed and `detect` 0 stale.
- **Human**: —

### P0-05 Question prompt carries the question
- **Rationale**: `prompts/question-page.md` has no `{{question}}`; `{{target_id}}` is never substituted
  (`scripts/generate_question.py:146-151`). A live model would never see the question.
- **Files**: `prompts/question-page.md` (add `{{question}}`, `{{audience}}`, `{{privacy}}`; bump to
  `question-page.v2`); `contracts/GenerateQuestionPage.yaml` (prompt version, contract version bump);
  `scripts/generate_question.py` (substitute every placeholder; raise if any `{{…}}` remains, as
  `generate_page.py` already does).
- **Traces**: REQ-012; AD-6.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestQuestionPromptRendering -v` (rendered prompt
  contains the question text; unresolved placeholder raises); re-seed; `npm run detect` 0 stale.
- **Risks**: prompt-version bump marks question views stale — expected, re-seed.
- **Human**: —

### P0-06 Generation honesty in provenance
- **Rationale**: live results default `generation_mode` to `demo` (`scripts/generate_page.py:212,228`).
- **Files**: `scripts/generate_page.py`, `scripts/generate_question.py` — set `generation_mode` from the
  provider actually used (`fixture` → `demo`; any live provider → `production`); record the model string
  the provider returns (C2.5).
- **Traces**: REQ-009; AD-8.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestGenerationModeStamp -v` (a stub non-fixture
  provider yields `production` and its returned model string).
- **Risks**: none.
- **Human**: —

### P0-07 Executable regeneration plan
- **Rationale**: `impact.json` `regenerate[].target` is a generated id; `generate_page.py` needs a
  canonical id (`scripts/detect_changes.py:123-125`; `scripts/generate_page.py:45-51`).
- **Files**: `scripts/detect_changes.py` (emit the canonical `source_documents[].id` as target, deduplicated
  per contract); question pages map to `generate_question.py` via their recorded request.
- **Traces**: REQ-008; AD-8; M2.2.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestRegenerationPlanExecutable -v` — for a
  simulated stale page, every `regenerate` entry runs through
  `generate_page.py --contract <c> --target <t> --dry-run` with exit 0.
- **Risks**: interview targets listed twice today (`prototype/README.md` Known issues) — dedupe.
- **Human**: —

### P0-08 Question persistence respects governance
- **Rationale**: `generate_question.py` only warns on schema errors and `--persist` writes directly into
  `docs/generated/questions/` (`scripts/generate_question.py:280-296`).
- **Files**: `scripts/generate_question.py` (schema errors exit 1; persisted files are always
  `approval_status: draft`).
- **Traces**: REQ-012; DEC-006 / ADR-005.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestQuestionPersistenceGovernance -v`.
- **Risks**: none.
- **Human**: —

### P0-09 Router and pipeline robustness (ADR-004 compliance)
- **Rationale**: bare `except Exception` (`ai/router.py:124,139`) makes fallback happen on any error,
  contradicting "fallback on 5xx/timeout only — never on content grounds"
  (`docs/primary-inputs/06_AI_DOCUMENTATION/model-strategy/ai_architecture.md:51-55`); `chain_for` drops
  failing providers silently; the PoC's single repair retry was lost.
- **Files**: `ai/provider.py` (distinguish `ProviderTransportError` from content/config errors),
  `ai/router.py`, `scripts/generate_page.py` (exactly one repair retry with validator errors appended).
- **Traces**: REQ-005; DEC-005 / ADR-004; AD-5.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestRouterFallbackSemantics tests.test_doccad.TestRepairRetry -v`
  (transport error → next provider; content error → no fallback; private task → `PrivacyRoutingError`
  on any local failure; second invalid output → `ContractViolation`, never a third call).
- **Risks**: must not weaken privacy pinning — `TestPrivateRoutingPolicy` stays green.
- **Human**: —

### P0-10 Private-content exclusion (T12)
- **Rationale**: required boundary with no implementation (`tests/test_doccad.py:385`); the archive
  specifies the design (`docs/primary-inputs/04_ARCHITECTURE/SAD/security_architecture.md:259-269`, D7).
- **Files**: `schemas/document.schema.json` (`visibility: public|private`; absent = private; version
  bump), every currently public page in `docs/source/` and `docs/generated/` (add `visibility: public` —
  a one-time metadata migration, listed in PROGRESS.md), `scripts/build_filter.py` (production build
  excludes private pages, so they are neither built nor indexed), generation scripts (a task whose
  evidence includes a private page is `privacy: private`), `tests/test_doccad.py` (remove the
  `expectedFailure` decorator).
- **Traces**: REQ-016; T12; ARCH-006.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestBuildFilterExclusion tests.test_doccad.TestPrivateContentExclusion -v`
  passes with **no expected failures** in the full suite; after `npm run build:production`, `grep -r` for a
  private fixture's marker text in `build/` (including `search-index.json`) finds nothing; `npm run build:demo`
  restores.
- **Risks**: forgetting `visibility: public` on a page silently removes it from production — the test
  must list the pages excluded by the production filter and compare against an expected set.
- **Human**: —

### P0-11 Production filter output is valid and honest
- **Rationale**: after `build_filter.py --mode production`, `validate_docs.py` fails on every hold stub
  (`source_documents: []`), and stubs claim `approval_status: approved` (`01_CONTEXT_MAP.md` §6.1).
- **Files**: `scripts/build_filter.py`, possibly `schemas/document.schema.json` (an explicit stub type,
  versioned) — the stub must not claim approval.
- **Traces**: REQ-004, REQ-015; DEC-006.
- **Acceptance**: `python3 scripts/build_filter.py --mode production && python3 scripts/validate_docs.py; echo $?`
  prints 0, `npx docusaurus build` exits 0, then `python3 scripts/build_filter.py --mode demo` restores
  (on a scratch copy); `python3 -m unittest tests.test_doccad.TestProductionFilterValidity -v`.
- **Risks**: `onBrokenLinks: 'throw'` if stubs are removed instead of replaced.
- **Human**: —

### P0-12 Security gates the archive specifies (T3, T4, T5, T6, T12-config)
- **Rationale**: specified in `security_architecture.md`, absent in the prototype (`01_CONTEXT_MAP.md` §4,
  §7 item 9).
- **Files**:
  - T3: `scripts/validate_docs.py` rejects `import`/`export` lines, JSX outside an allowlist
    (`EvidenceLink`, `InterviewPrep`, and the registered set), `<iframe>`, `<object>`, event-handler
    attributes and `data:` URLs in `docs/generated/**`. Generated pages stop importing: register
    components in `src/theme/MDXComponents.tsx`; load interview data by id without an MDX import.
  - T4: `contracts/link-allowlist.yaml` (path chosen per `security_architecture.md` T4; update
    `docs/source/security/prompt-injection-defense.md:45`, which says `config/`); validator rejects
    non-allowlisted external links in generated content.
  - T5: `docusaurus.config.ts` sets Mermaid `securityLevel: 'strict'` explicitly.
  - T6: a stdlib secret-pattern scan over the assembled prompt payload before any provider call
    (patterns such as `sk-`, `AIza`, `ghp_`, PEM headers); abort on match.
  - T12-config: a check that every routing chain matching `privacy: private` contains only `local`.
- **Traces**: REQ-016; AD-15; T3–T6, T12; M3.3.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestMdxRestrictionGate tests.test_doccad.TestExternalLinkAllowlist tests.test_doccad.TestContextSecretScan tests.test_doccad.TestPrivateChainConfig -v`
  — each class has at least one failing fixture that the gate rejects; `grep -rn "^import\|^export" docs/generated`
  prints nothing; `grep -n "securityLevel" docusaurus.config.ts` shows `'strict'`; full `npm run build` exit 0.
- **Risks**: removing MDX imports changes how interview data loads — browser-check the interview pages.
- **Human**: —

### P0-13 Content tells the truth
- **Rationale**: reader-facing content claims gates that do not exist (D15).
- **Files**: `docs/source/security/prompt-injection-defense.md`, `docs/source/decisions/adr-007-mermaid-as-code.md`,
  `ai/fixture_provider.py` text → re-seed `docs/generated/`. Each claim becomes either true (after P0-12/P1-09)
  or explicitly "planned".
- **Traces**: REQ-010 (no fabricated claims); constraints (`CONSTRAINTS.md:11-13`).
- **Acceptance**: a table in PROGRESS.md listing each claimed gate → implementing file → test class;
  `npm run validate` and `npm run detect` (0 stale).
- **Risks**: canonical pages are human-owned; keep edits factual and minimal, listed in PROGRESS.md.
- **Human**: —

### P0-14 Milestone 6 — Hungarian landing, navigation, search
- **Files**: `src/pages/index.tsx` (`<Translate>`/`translate()`), `npx docusaurus write-translations --locale hu`
  output (`i18n/hu/code.json`, `docusaurus-theme-classic/navbar.json`, `footer.json`) with real Hungarian;
  `docusaurus.config.ts` search `language: ['en', 'hu']` (B6.3); `markdown.hooks.onBrokenMarkdownLinks` and
  `onBrokenMarkdownImages: 'throw'`, `onBrokenAnchors: 'throw'`, explicit `trailingSlash` (B1.3, B5.1).
- **Traces**: REQ-013; AD-12; M2.4.
- **Acceptance**: `grep -c "<Translate\|translate(" src/pages/index.tsx` > 0; `npm run build` exit 0 for
  both locales; `build/hu/index.html` contains the Hungarian hero text; `build/hu/search-index.json` exists;
  the HU fallback test (D11) is run and its observed behaviour recorded in `VALIDATION.md`.
- **Risks**: `onBrokenAnchors: 'throw'` may expose existing anchor errors — fix them, do not relax.
- **Human**: —

### P0-15 Milestone 7 — browser verification and `VALIDATION.md`
- **Files**: new `prototype/VALIDATION.md`; screenshots under `prototype/planning/evidence/` (small PNGs).
- **Procedure**: `npm run build && npm run serve`, then `/browser` in the Antigravity 2.0 app against
  `http://localhost:3000` (A4.1–A4.3): home, a canonical page with Mermaid, the recruiter view and an
  evidence link, an interview page, the workbench question journey, the inspector, `/hu/`, theme switch,
  a 390 px and a 1440 px viewport. Record console errors per page.
- **Traces**: REQ-006, REQ-013, REQ-015; M7.
- **Acceptance**: `VALIDATION.md` lists every check as PASS / FAIL / NOT RUN with command or browser step,
  date and evidence path; every screenshot path it cites exists (`ls`). If `/browser` is unavailable, the
  check is NOT RUN with the reason — never PASS.
- **Risks**: browser tooling unavailable in the CLI; console errors from Mermaid.
- **Human**: H-5. Optional CI smoke (Playwright) needs H-6.

### P0-16 Milestone 8 — `DEMO.md`, `LIMITATIONS.md`, README
- **Files**: `prototype/DEMO.md` (ten-minute walkthrough: reader, recruiter, contributor, reviewer),
  `prototype/LIMITATIONS.md` (implemented / deterministic simulation / unverified integration / deferred),
  `prototype/README.md` (Known issues updated; remove fixed items).
- **Traces**: REQ-015; first-run prompt step 8 (`docs/prototype-planning/ANTIGRAVITY_PROMPT.txt:89-95`).
- **Acceptance**: files exist; every command in `DEMO.md` was executed in this run and logged in
  PROGRESS.md §Evidence log.
- **Human**: —

### P0-17 Phase 0 exit gate
- **Acceptance**: §2 phase gate; full suite with **zero expected failures**; `VALIDATION.md` current;
  PROGRESS.md marks Phase 0 complete with evidence lines; fresh conversation for Phase 1.

## 5. Phase 1 — Deployable and governed

Prerequisites: Phase 0 exit gate; H-2, H-7. Workflows live at the repository root `.github/workflows/`
(the site is in `prototype/`, so every job uses `working-directory: prototype`). Revive the PoC's
workflows as the starting point (`docs/primary-inputs/09_RESULTS/implementation/poc/.github/workflows/`),
updated to current action majors (B3.2).

### P1-01 CI gate workflow (`ci.yml`)
- **Rationale**: no CI exists; ADR-003, ADR-007 and AD-10 assume one.
- **Files**: `.github/workflows/ci.yml` — triggers `pull_request` and `push` to `main`; top-level
  `permissions: contents: read`; `concurrency`; steps: `actions/checkout` v7 (`persist-credentials: false`),
  `actions/setup-node` v7 (Node 24, npm cache), `actions/setup-python` v7 +
  `pip install -r prototype/requirements.txt`, `npm ci`, `npm run typecheck`,
  `DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate`, `npm run test`, `npm run detect` with a step that fails
  when `impact.json` lists any stale page, `npm run build`, then the production-filter check from P0-11,
  and `actions/upload-artifact` of `prototype/build` as the PR preview (archive preview strategy,
  `automation_architecture.md:64-68`). **Every action pinned by full commit SHA with a version comment**;
  no `pull_request_target`; no `${{ github.event.* }}` inside `run:` (T8, B5.7).
- **Generation-path guard** (ADR-003): when the head branch matches `docs-gen/*`, fail if any changed
  path is outside `prototype/docs/generated/**` and its i18n mirror.
- **Traces**: REQ-004, REQ-015; DEC-004, DEC-008; AD-10; T8; M1.2.
- **Acceptance (local, by the run)**: `python3 -c "import yaml,sys;[yaml.safe_load(open(f)) for f in sys.argv[1:]]" .github/workflows/*.yml`
  exits 0; `grep -nE "uses: [^@]+@[0-9a-f]{40}" .github/workflows/*.yml` matches every `uses:` line;
  `grep -n "pull_request_target" .github/workflows/*.yml` prints nothing.
  **Acceptance (on GitHub, observed by the owner)**: the first PR shows the CI check green.
- **Risks**: SHA lookup needs network — if unavailable, the run records the version tags and marks
  "pin SHAs" as BLOCKED rather than inventing hashes.
- **Human**: H-7 (push), observation of the first run.

### P1-02 Site configuration for Pages
- **Files**: `docusaurus.config.ts` (`url`, `baseUrl`, `trailingSlash` per E2).
- **Traces**: DEC-010 / ADR-009; B3.5.
- **Acceptance**: `npm run build` exit 0; `grep -o 'href="/<repo>/' build/index.html` matches when a
  project site is used. **Blocked until E2 is answered** — never guess the repository name.
- **Human**: H-2.

### P1-03 Publish workflow (`publish.yml`)
- **Files**: `.github/workflows/publish.yml` — on `push` to `main` after CI: build job runs
  `npm run build:production` (P0-10/P0-11 make this the publication build), `actions/configure-pages` v6,
  `actions/upload-pages-artifact` v5 (`path: prototype/build`); deploy job `needs: build`, environment
  `github-pages`, permissions `contents: read`, `pages: write`, `id-token: write`, `actions/deploy-pages`
  v5; smoke step: HTTP 200 for `/`, `/docs/…`, `/views/…`, `/hu/`, and the search index file (T13; B3.4;
  `automation_architecture.md:56-58`).
- **Traces**: REQ-006; DEC-010; T13; M1.6.
- **Acceptance (local)**: YAML parses; SHA pins as in P1-01; the production build passes locally.
  **Acceptance (GitHub, owner)**: the Pages URL serves the site; the smoke step is green.
- **Human**: H-7.

### P1-04 CODEOWNERS and ruleset
- **Files**: `.github/CODEOWNERS` (`/prototype/docs/generated/**`, `/prototype/contracts/**`,
  `/prototype/prompts/**`, `/prototype/ai.config.yaml`, `/.github/**`, `/.github/CODEOWNERS` → owner);
  the ruleset settings, which only the owner can apply, are documented in `prototype/README.md` (§Governance):
  require PR, required status check `ci`, require code-owner review, block force push, owner bypass "for
  pull requests only" (B4.1–B4.3, D5).
- **Traces**: DEC-006 / ADR-005; T1; M1.1.
- **Acceptance**: file exists with the listed patterns; README section exists. Ruleset applied: owner.
- **Human**: H-8.

### P1-05 Real approval replaces simulated approval for production (D6)
- **Rationale**: `approved` has no producer; `build_filter.py` trusts frontmatter.
- **Files**: `schemas/document.schema.json` (`approval_record: {pr, approved_by, approved_at}`, required
  when `approval_status: approved`; version bump); `scripts/review_governance.py` (`approve --artifact <id>
  --pr <n>` — run by the human reviewer on the PR branch; refuses unless the artifact is `in-review`);
  `scripts/build_filter.py` (production publishes only `approved` with a complete record);
  `scripts/validate_docs.py` (rejects `approved` without a record). The demo ledger and
  `approved-for-demo` remain for demo builds.
- **Traces**: REQ-004, REQ-012; DEC-006 / ADR-005; `content_architecture.md:100`.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestApprovalRecord -v`; production filter excludes
  `approved-for-demo` and record-less `approved` pages.
- **Risks**: the design is a proposal (E3) — if the owner rejects it, stop and record.
- **Human**: E3; the approval itself is always a human act.

### P1-06 Generation workflow (`generate.yml`)
- **Files**: `.github/workflows/generate.yml` — `workflow_dispatch` inputs `contract`, `target`,
  `privacy`; runs the fixture provider by default (no secrets needed); writes on branch
  `docs-gen/<contract>-<target>`; opens a PR with the run report (evidence files, gates, provider, model,
  usage). Permissions `contents: write`, `pull-requests: write` on that job only; environment
  `generation` only when a live provider is selected (Phase 2). Token: GitHub App installation token
  when E7 = yes; otherwise document the reopen-to-trigger workaround (D5).
- **Traces**: REQ-008, REQ-012; DEC-006; AD-9; M1.5.
- **Acceptance (local)**: YAML parses; SHA pins; no `pull_request_target`.
  **Acceptance (GitHub, owner)**: a dispatch with the fixture opens a PR whose CI runs and whose diff
  touches only `prototype/docs/generated/**`.
- **Human**: H-7, H-8.

### P1-07 Dependabot and drift schedule
- **Files**: `.github/dependabot.yml` (github-actions + npm, weekly, grouped); optional
  `.github/workflows/drift.yml` (weekly `npm run detect` → one "stale views" issue; `issues: write` only).
- **Traces**: AD-8; T9; M2.2.
- **Acceptance**: YAML parses; pins as P1-01.
- **Human**: H-7.

### P1-08 Mermaid compile gate (D4)
- **Files**: per owner choice: a mermaid-cli pinned to the site's Mermaid 11.x (verify availability
  first), or a headless-browser render check (NV-SUP-1).
- **Traces**: DEC-008 / ADR-007; M1.3.
- **Acceptance**: a deliberately broken `.mmd` fixture makes the gate exit non-zero; all real diagrams
  pass.
- **Human**: H-6 (new dependency). **Blocked without approval.**

### P1-09 Phase 1 exit gate
- Local §2 gate green; workflows parse and are pinned; PROGRESS.md lists which GitHub-side checks the owner
  observed and which remain NOT RUN.

## 6. Phase 2 — Live AI generation behind the fixture default

Prerequisites: Phase 1 exit (local parts at minimum). No item in this phase may read, print, or write an
API key. All tests use a local stub HTTP server (stdlib `http.server` on `127.0.0.1`) — never the network.

### P2-01 Provider-facing schemas
- **Rationale**: providers accept only JSON-Schema subsets (C1.3, C1.6, C1.9, C1.11); the repo schemas
  stay the gate (C1.13).
- **Files**: `ai/schema_adapt.py` (derive per-provider schema: drop unsupported keywords, add
  `additionalProperties: false` / full `required` where strict mode demands); local `jsonschema`
  validation remains mandatory after every response.
- **Traces**: REQ-005; AD-6.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestProviderSchemaDerivation -v` (for each
  provider, the derived interview and document schemas contain no keyword that provider rejects).

### P2-02 Structured output in every adapter
- **Files**: `ai/anthropic_provider.py` (`output_config.format`), `ai/openai_provider.py`
  (`response_format` `json_schema`, strict), `ai/gemini_provider.py` (`generationConfig.responseMimeType`
  + `responseJsonSchema`), `ai/local_provider.py` (`response_format` with fallback to native `/api/chat`
  `format`, `stream: false`). Each request shape isolated in one function (D10). Refusals surface as a
  content error, not a transport error.
- **Traces**: REQ-005; DEC-005.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestAdapterRequestShapes -v` (stub server
  asserts URL, headers without logging their values, and body shape per provider).

### P2-03 Sampling parameters and token limits per model
- **Files**: `ai.config.yaml` (optional per-provider `params`), adapters (send `temperature` only when
  configured).
- **Traces**: C2.2, C1.10.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestSamplingOptIn -v`.

### P2-04 Retry, error classification, usage logging
- **Files**: `ai/http.py` (stdlib retry: 429/500/502/503/504/529 with exponential backoff + jitter,
  honour `Retry-After`; fail fast on 400/401/403 and on quota or spend-cap 429; redact auth headers in any
  error text; log `request-id`, token usage and cache fields — never payloads).
- **Traces**: REQ-005; C5.1–C5.4, C5.6; T6.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestHttpRetryPolicy -v` (stub server returns each
  status; assert retries, terminal cases and redaction).

### P2-05 Per-run budget and cache-friendly prompts
- **Files**: `ai.config.yaml` (`budget: {max_tokens_per_run, max_calls_per_run}`), generation scripts
  (abort when exceeded); prompt templates order static governance + evidence first (C5.2).
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestRunBudget -v`.

### P2-06 Grounding gate and golden set
- **Rationale**: citation support must be checked (C3.1); `ai_architecture.md:107-114` requires a
  deterministic named-entity check for recruiter pages.
- **Files**: `scripts/check_grounding.py` (every citation resolves to allowed evidence with a matching
  hash; quoted spans are contained in the cited source; recruiter technology tokens appear in the
  deterministic fact list or cited canon); `tests/golden/` (contract → expected cited-source set).
- **Traces**: REQ-010, REQ-012; AD-10 (advisory AI checks stay non-gating).
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestGroundingGate -v` with at least one failing
  fixture per rule.

### P2-07 Injection fixtures
- **Files**: canonical-looking test fixtures containing injected instructions; tests assert the pipeline's
  deterministic gates reject the resulting output (schema, allowlist, grounding).
- **Traces**: T2; C4.1–C4.4.
- **Acceptance**: `python3 -m unittest tests.test_doccad.TestPromptInjectionFixtures -v`.

### P2-08 Live smoke — owner-executed
- **Rationale**: the run never holds keys. The owner runs one live call per enabled provider.
- **Procedure (owner)**: with keys and `AI_MODEL_*` in the environment and spend caps set,
  `python3 scripts/generate_page.py --contract GenerateInterviewPrep --target architecture-system-overview`
  with the provider chain set to the provider under test; then `npm run validate`. Or dispatch
  `generate.yml` with the `generation` environment.
- **Acceptance**: the owner records provider, returned model string, exit code and validation result in
  `VALIDATION.md`. Until then: NOT RUN.
- **Human**: H-9 — **the run stops here**.

### P2-09 Optional: Anthropic workload identity federation (D1)
- Owner-optional; replaces the static Anthropic key in CI (C6.5). Requires provider-side setup.

### P2-10 Phase 2 exit gate
- §2 gate green; zero expected failures; live smoke recorded or NOT RUN with reason.

## 7. Phase 3 — External repository evidence (specification only)

**Decision first**: NV-SUP-2 (`02_RESEARCH_KB.md` D8). If rejected, Phase 3 is dropped.

- **Source manifest** `prototype/external-sources.yaml`: `{name, repo, commit (full SHA), paths
  (sparse), license (SPDX), visibility}` per source; changing `commit` is a human PR.
- **Fetch**: CI `actions/checkout` with `repository`, `ref: <sha>`, `path: external/<name>`,
  `sparse-checkout`, `persist-credentials: false` (C7.1); local equivalent via the REST contents API with
  `ref=<sha>` using `urllib` (C7.3). Never fetched into `docs/`; never served.
- **Provenance**: `generation.source_documents[]` gains `{repo, commit, path, content_hash}` for external
  evidence (C7.8); schema and contract versions bump.
- **Gates**: license allowlist (block unlicensed — C7.6); secret scan over fetched content before it enters
  any prompt (C7.7); external text labelled untrusted in prompts (C4); evidence globs per contract cover
  `external/<name>/<path>` only.
- **Drift**: a `commit` bump marks dependent generated pages stale through the existing hash mechanism.
- **Acceptance (for the future run)**: a pinned public test repository yields a generated page whose
  provenance names repo, commit, path and hash; changing the commit marks it stale; an unlicensed source
  is refused; a planted fake secret aborts the job.
- **Risks**: private repositories need a PAT or GitHub App (C7.1); cross-repo triggers need a non-default
  token (C7.5); the multi-repo non-goal must be formally superseded first.

## 8. Risk register (top)

| Risk | Likelihood | Mitigation in this plan |
|---|---|---|
| The run claims checks it did not run (first-run pattern; tool-call bug A5.6) | High | Evidence log with command + exit code; named test classes; edits verified by `git diff` |
| The run stalls on permissions or network | High | H-3 pre-configured allow rules |
| Context compaction drops constraints in a long session | Medium | Rules in `AGENTS.md`; fresh conversation per phase; PROGRESS.md as state |
| Tool-use loops burn quota | Medium | Two-attempt bound; Tried-and-failed log; phase restarts |
| `visibility` default-private hides public pages | Medium | P0-10 expected-set test |
| Bot PRs never get required checks | Medium | GitHub App token (E7) or documented workaround |
| Live provider schema keyword mismatches | Medium | P2-01 derivation + local validation as the gate |
| Cost overrun in live runs | Low–Medium | Spend caps (owner), per-run budget (P2-05), live calls owner-executed |
| Mermaid 12 drift via fresh installs | Low | `npm ci` with committed lockfile; Mermaid upgrade only as its own PR |
