# 02 — Phase 2 closeout plan: observable, fail-closed, hardened generation

Prepared 2026-10-07. Continues `docs/phase-2/02_PHASE2_PLAN.md` with the gaps in `01_STATE_AND_GAPS.md`. The
run is executed from `03_ANTIGRAVITY_PROMPT.txt`. IDs continue and are never recycled:
- work items: P2-13…P2-20;
- checkpoints: 2C, 2D;
- requirements: NV-REQ-027…029;
- owner actions: H3-n;
- new decisions: E11…E13.

## 0. Next-phase development, in bullets

**Unattended run (this pack)**
- Start offline from a clean, current `main`, then re-verify the baseline: 40 pages, 25 hashes, 0 stale, 155
  tests, typecheck, en + hu build. (P2-13)
- Every generation run prints one usage line and the truthful chain source. The usage line holds: provider,
  returned model, calls, input and output tokens, request IDs or `unavailable`. In CI the same facts go into the
  job's step summary as the run report. Never payloads or key values. (P2-14; G11–G13)
- Absent `visibility` means private everywhere: production filter, validator, generation output. Generation
  stamps `visibility` explicitly, and a page shaped like the live Gemini draft is proven held in production.
  (P2-15; G14)
- `Router.chain_for` stops swallowing errors (finishes G7). (P2-16; G18)
- `generate.yml`: one tested dispatch script instead of two drifted inline copies (P2-17; G17). A unique
  `docs-gen/*` branch per run (P2-18; G15). Read-only top-level permissions in `generate.yml` and `drift.yml`,
  enforced by a test (P2-19; G16).
- Truth sync of `prototype/README.md`, `LIMITATIONS.md`, `VALIDATION.md` and `PROGRESS.md`, then the exit gate.
  (P2-20; G19)

**Owner, before the run:**
- H3-1: clean `main` at or after `408b3cf`.
- H3-2: install dependencies.
- H3-3: guard protects this folder.

**Owner, any time (Blocked for the run, §5):**
- E5 and the remaining live provider rows.
- Create the GitHub App, then the first bot PR and the first real approval.
- E6 / P1-08 Mermaid gate. A matching `mermaid-cli` 11.17.0 exists.
- The environment branch-policy negative test.
- NV-SUP-2 / Phase 3.
- E9.
- G9 wording.
- E11 `q-002`.
- E12 model name in docs.
- E13 the evidence branch.
- Agent-layer upkeep: the guard, `.claude/rules/prototype-code.md` known debt, `AGENTS.md` line citations.

**Not in this run**
- Phase 3 (external evidence).
- Anthropic workload identity federation (P2-09).
- L2+ retrieval.
- Provider SDKs.
- promptfoo/RAGAS, Playwright, mermaid-cli.
- Any runtime model call.
- Any live provider call.
- Any GitHub-side action.

## 1. Scope, naming and roadmap mapping

This is not "Phase 3". In `docs/next-phase/03_NEXT_VERSION_PLAN.md:510-512`, Phase 3 is external repository
evidence, and it starts with NV-SUP-2 (KB E8), which is undecided (`prototype/planning/PROGRESS.md:157`).
Everything an unattended run can do now closes or hardens Phase 2.

| Roadmap milestone (`docs/primary-inputs/08_TASKS/future/implementation_roadmap.csv`) | Advanced by |
|---|---|
| M1.5 bot-PR generation flow (`:6`) | P2-17, P2-18, P2-19; the end-to-end part is the owner's App (H3-7) |
| M2.1 provider matrix (`:8`) | Owner live rows (H3-6); P2-14 makes their cost visible |
| M3.1 audit: run-report archive (`:13`) | P2-14 (step summary as run report) |
| M3.2 provider resilience: spend caps, budget alerts (`:14`) | P2-14 (usage line); caps are E5 |
| M3.3 security hardening (`:15`) | P2-15 (T12 fail-closed), P2-19 (least privilege), P2-16 |

## 2. Run rules (deltas to `docs/phase-2/02_PHASE2_PLAN.md` §2, which still applies)

- **Branch.** `phase-2-closeout`, created from `main`. Start check:
  - `git status --porcelain` prints nothing;
  - `git merge-base --is-ancestor 408b3cf HEAD` exits 0.

  Otherwise stop (H3-1). Local commits only at checkpoints 2C and 2D. No push, no PR.
- **Fully offline.** The run never runs `npm ci`, `npm install`, `npx` with a package download, `pip install`,
  or anything else that reaches a registry or a provider. It checks dependencies instead:
  - `npm ls --depth=0` exits 0 (from `prototype/`);
  - `python3 -c "import yaml, jsonschema, referencing"` exits 0.

  If either fails, that is a stop condition (H3-2). This replaces the `npm ci` step of the Phase 2 prompt
  (G20).
- **Do not edit** `AGENTS.md` or the root `README.md`. Proposed wording changes go to `PROGRESS.md` for the
  owner. Do not edit `.agents/`, `.claude/`, `docs/primary-inputs/`, `docs/next-phase/`, `docs/phase-2/`,
  `docs/phase-2-closeout/` or `docs/prototype-planning/`.
- **Phase gate** at each checkpoint, from `prototype/`: `npm run typecheck && DOCCAD_REQUIRE_JSONSCHEMA=1 npm
  run validate && npm run test && npm run build` exit 0, then `npm run detect` reports `stale generated: 0`.
- **Workflow edits.** Read `.claude/rules/github-workflows.md` first. `validate-and-build` is a ruleset
  contract: never rename a job in `ci.yml`. GitHub-side behaviour stays NOT RUN until the owner observes it.

## 3. Owner checklist

| # | Action | When | Blocks |
|---|---|---|---|
| H3-1 | Commit this pack (`docs/phase-2-closeout/`) to `main` through a PR, then `git checkout main && git pull`. Confirm that `git status --porcelain` prints nothing and that HEAD contains `408b3cf` (true locally at the end of the planning session, G21) | Before | Run start |
| H3-2 | From `prototype/`: `npm ci && pip install -r requirements.txt`. Confirm `npm ls --depth=0` and `python3 -c "import yaml, jsonschema, referencing"` exit 0 | Before | Run start |
| H3-3 | Guard: add `docs/phase-2-closeout` to `PROTECTED_DIRS` (`.agents/hooks/doccad_guard.py:31-35`) and to the PreInvocation text (`:124-125`), extend the self-test, run `python3 .agents/hooks/test_doccad_guard.py`. Record it in a dated `.claude/plans/` note (agent layer is git-ignored) | Before | Pack protection |
| H3-4 | Keep Antigravity command auto-execution for the `doCCAD_pre` project; use the 2.0 app | Before | Unattended run |
| H3-5 | After 2D: review branch `phase-2-closeout`, push, open the PR, CI green, merge. Then dispatch `generate.yml` once with `provider=fixture` and record what `PROGRESS.md` asks (step summary present, branch name carries the run id, job permissions) | After | GitHub-side observations of P2-14, P2-17…P2-19 |
| H3-6 | **E5**: choose providers, set `AI_MODEL_*` (environment variables for CI, shell for local), create keys with expiry and hard provider-side spend caps, and decide a per-month cap. Run the remaining `VALIDATION.md` §7 rows (scratch copy, hidden key prompt). Record the new usage line, and the name of the response field that carries Gemini's request ID | After P2-14 is merged | P2-08 rows, NV-REQ-022, M2.1 |
| H3-7 | **GitHub App** (KB E7 = repo E8): create and install it (`prototype/README.md` §Governance). Set the `DOCCAD_APP_CLIENT_ID` variable and the `DOCCAD_APP_PRIVATE_KEY` secret. Dispatch → bot PR → review → `review_governance.py approve` → code-owner approval → merge → `publish` verifies | Any time | J3, NV-REQ-016/017, first real approval |
| H3-8 | Environment policy negative test: push a throwaway branch from `main`, dispatch `generate.yml` from it with `provider=gemini`, and confirm GitHub refuses the `generate-live` job before secrets are released. Delete the branch. Record in `VALIDATION.md` §7 | Any time | Closes `VALIDATION.md:143-144` |
| H3-9 | **E6**: approve or reject `@mermaid-js/mermaid-cli` 11.17.x as a devDependency (browser download in CI) | Any time | P1-08, NV-REQ-018 |
| H3-10 | Decide **E11** (`q-002`), **E12** (model name in docs), **E13** (evidence branch), **G9 wording**, optional required reviewer on `generation` | Any time | Doc wording; G15 until P2-18 lands |
| H3-11 | **NV-SUP-2** (KB E8) and **E9** | Any time | Phase 3; archive task |
| H3-12 | Agent layer after the merge: update `.claude/rules/prototype-code.md:47-51` (known debt, after P2-16) and `AGENTS.md` line citations moved by the run; record in `.claude/plans/` | After | Rulebook truth |

## 4. Work items

Order of execution:
- **Checkpoint 2C** = P2-13, P2-14, P2-15, P2-16.
- **Checkpoint 2D** = P2-17, P2-18, P2-19, P2-20.

All commands run from `prototype/`. Commands that write into `docs/` run on a scratch copy of `.github/` +
`prototype/` (AGENTS.md health-check block).

### P2-13 Start check, offline dependency check, baseline
- **Rationale:** start from verified numbers on the right commit without touching the network (G20, G21).
- **Steps:**
  1. Start check (§2).
  2. Dependency check (§2).
  3. Create the branch.
  4. Add "Run rules — Phase 2 closeout run" at the top of `PROGRESS.md` and mark the Phase 2 block superseded
     (do not delete it).
  5. Run the gate.
- **Acceptance:** `npm ls --depth=0 && python3 -c "import yaml, jsonschema, referencing" && npm run
  typecheck && DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate && npm run test && npm run build && npm run detect`.
  Expected results:
  - `Validated 40 pages, 4 interview datasets, 25 provenance hashes.`;
  - `Ran 155 tests` / `OK`;
  - `stale generated: 0`;
  - both locales built.

  Differences are recorded and investigated before any code change.
- **Traces:** NV-REQ-001, REQ-015. **Human:** H3-1, H3-2.

### P2-14 Run usage report (G11, G12, G13)
- **Rationale:** live cost and provenance must be visible where reviewers look: the terminal, the CI log and the
  run report. The usage line exists today but is never emitted.
- **Files:** `ai/router.py`, `ai/http.py` and the adapters (carry `request_id` and returned `model` into each
  result), `scripts/generate_page.py`, `scripts/generate_question.py`.
- **Behaviour:**
  - After every run, both scripts print exactly one line: `Run usage: provider=<name> model=<returned model>
    calls=<n> input_tokens=<i> output_tokens=<o> request_ids=<id,…|unavailable>`. Fixture runs print it
    too, with the fixture's own numbers.
  - The chain line names its true source: `Provider chain (--provider): gemini` or `Provider chain (from
    ai.config.yaml): fixture`.
  - When `GITHUB_STEP_SUMMARY` is set, the scripts append a Markdown run report. It contains: contract, target,
    privacy, provider, returned model, `generation_mode`, calls, tokens, request IDs, evidence ids, gate results,
    output path, `approval_status`. The run report never contains prompt text, evidence text, response text,
    header values or environment values.
  - Gemini's request-ID field is not guessed. If none of the known headers is present, the value is
    `unavailable` (G13; the owner records the real field at H3-6).
  - Proposed default, reversible: whether the `doccad.ai.http` INFO logger is also enabled. The usage line
    above is the contract either way.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestRunUsageReport -v`, with these cases:
  1. A loopback stub returns a body with usage and a `request-id` header; the printed line carries those exact
     numbers and that ID.
  2. A response without a request-ID header prints `request_ids=unavailable`.
  3. With `GITHUB_STEP_SUMMARY` pointed at a temp file, the report is written. It contains no sentinel string
     planted in the evidence and no fake key-shaped value set in the environment. This case fails if the report
     includes prompt text.
  4. `--provider` changes the chain label.

  Then `python3 scripts/generate_page.py --contract GenerateRecruiterPage --target
  architecture-system-overview --provider anthropic --dry-run` exits 0, prints `Provider chain (--provider):
  anthropic`, and makes no call.
- **Traces:** NV-REQ-020, **NV-REQ-027**; P1-06 run report; M3.1. **Human:** H3-5 (observe the summary in CI),
  H3-6.

### P2-15 Absent visibility fails closed (G14)
- **Rationale:** T12 and the schema say an unclassified page is private. The production filter treats it as
  public, and generation never classifies its output.
- **Files:** `scripts/build_filter.py`, `scripts/validate_docs.py`, `scripts/generate_page.py`,
  `scripts/generate_question.py`, and possibly `schemas/interview.schema.json`,
  `contracts/GenerateInterviewPrep.yaml` and `scripts/seed_generated_views.py` (see the trap below).
- **Behaviour:**
  - The production filter treats a missing `visibility` (and missing `privacy`) as private.
  - `validate_docs.py` rejects a generated `.md`/`.mdx` page without an explicit `visibility`.
  - Both generation scripts stamp `visibility`: `private` when the effective task privacy is private
    (including elevation from private evidence), else `public`.
- **Trap: the four interview JSON datasets carry no `visibility`.** A naive change stashes them in production.
  Choose one, record it as a proposed default, and never widen an exclusion to make it pass:
  - **(a)** a dataset takes the visibility of the generated page that loads it, where the mapping is
    deterministic (same id) and absent still means private; or
  - **(b)** stamp `visibility` in the datasets: bump the interview schema version and the
    `GenerateInterviewPrep` contract version, then re-seed until `npm run detect` reports `stale generated: 0`.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestVisibilityFailsClosed
  tests.test_doccad.TestPrivateContentExclusion tests.test_doccad.TestBuildFilterExclusion
  tests.test_doccad.TestProductionFilterValidity -v`. The new class covers these cases:
  1. A canonical page without `visibility` is excluded in production.
  2. A generated page without it is excluded.
  3. Validate rejects a generated page without it.
  4. `generate_page.py` output for a public task carries `visibility: public`, and for a private-evidence task
     carries `private`.
  5. A page shaped like the live draft is held in production: `provider: gemini`, `generation_mode:
     production`, `approval_status: draft`, no `visibility`. The test builds it in the temp tree; it does not
     depend on the remote branch.
  6. An expected-set check. Before changing the filter, run it on a scratch copy and record in `PROGRESS.md`
     the set of files it excludes. The test then asserts that set as a literal: on the real tree the filter
     excludes exactly those files, and the interview datasets follow their pages.

  Then the round trip on a scratch copy: `npm run build:production && npm run build:demo` exit 0.
- **Traces:** NV-REQ-008, **NV-REQ-028**; T12; REQ-016. **Human:** E13 (the evidence branch's page needs
  regenerating after this lands).

### P2-16 `chain_for` propagates errors (G18)
- **Files:** `ai/router.py` (`chain_for`). Keep `providers_from_config` working, or remove both only if `grep`
  shows no caller outside tests; record which.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestExplicitProviderSelection -v`, with a new case: an
  adapter whose constructor raises `ValueError` makes `chain_for` raise. That case fails before the change.
  `TestRouterFallbackSemantics` and `TestPrivateRoutingPolicy` stay green.
- **Traces:** REQ-005, NV-REQ-007; ADR-004. **Human:** H3-12 (agent-layer note).
- **Checkpoint 2C:**
  1. Phase gate.
  2. Local commit `phase-2C: P2-13 P2-14 P2-15 P2-16`.
  3. Stop with the resume line.

### P2-17 One tested dispatch script for `generate.yml` (G17)
- **Files:** new `scripts/dispatch_generation.py` with `build_parser()`; `.github/workflows/generate.yml`.
- **Behaviour:**
  - The script reads `INPUT_CONTRACT`, `INPUT_TARGET`, `INPUT_PRIVACY` and `INPUT_PROVIDER` from the environment.
  - It applies the union of today's checks: contract, privacy and provider allowlists; non-empty target;
    `private` only with `local`.
  - It runs `generate_page.py` or `generate_question.py` with an argument list (no shell). Target text with shell
    metacharacters stays one argument.
  - It also exposes the branch-name function used by P2-18.
  - Both jobs call `python3 scripts/dispatch_generation.py`. The inline validation copies disappear, and the
    header comment (`generate.yml:2`) describes both jobs.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestDispatchGeneration
  tests.test_doccad.TestWorkflowSecurityInvariants tests.test_doccad.TestWorkflowScriptInvocations
  tests.test_doccad.TestGenerateWorkflowProviderInput -v`. `TestDispatchGeneration` uses an injected runner:
  - invalid contract, privacy or provider, an empty target, and `private` + `gemini` each exit 1 with no
    subprocess started;
  - a valid input produces the exact argv;
  - a metacharacter target stays a single element.

  Then `grep -c "valid_contracts" ../.github/workflows/generate.yml` prints `0`.
- **Traces:** REQ-012, NV-REQ-017, **NV-REQ-029**; T8. **Human:** H3-5.

### P2-18 Unique docs-gen branch per dispatch (G15)
- **Files:** `scripts/dispatch_generation.py` (branch-name function), `.github/workflows/generate.yml` (both push
  steps).
- **Behaviour:** branch = `docs-gen/<contract-slug>-<target-slug>-<run id>`. The run id comes from
  `GITHUB_RUN_ID`, read through `env:`, never interpolated into `run:`. The `docs-gen/` prefix stays, because
  the `ci.yml` path guard keys on it (`.github/workflows/ci.yml:77`).
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestDispatchGeneration
  tests.test_doccad.TestWorkflowSecurityInvariants -v`, with cases:
  - same contract and target with two run ids give two names;
  - every name starts with `docs-gen/` and stays within a fixed length;
  - a missing run id is an error, not a silent fallback to the old name.

  GitHub-side: NOT RUN (H3-5).
- **Traces:** NV-REQ-017, **NV-REQ-029**. **Human:** H3-5, E13.

### P2-19 Read-only top-level permissions (G16)
- **Files:** `.github/workflows/generate.yml`: top level `contents: read`; jobs `generate` and `generate-live`
  get `contents: write` (the App token carries the PR permission). `.github/workflows/drift.yml`: top level
  `contents: read`; job `drift-check` gets `contents: read` and `issues: write`.
  `tests/test_doccad.py`: a new assertion in `TestWorkflowSecurityInvariants` that no workflow's top-level
  `permissions` grants `write`. This assertion fails on today's `generate.yml` and `drift.yml`, which is the
  required failing case.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestWorkflowSecurityInvariants
  tests.test_doccad.TestGenerateWorkflowProviderInput tests.test_doccad.TestWorkflowScriptInvocations -v`; YAML
  parses (`python3 -c "import yaml,sys;[yaml.safe_load(open(f)) for f in sys.argv[1:]]"
  ../.github/workflows/*.yml`). GitHub-side: NOT RUN (H3-5; next scheduled `drift` run).
- **Traces:** **NV-REQ-029**; T8; M3.3.

### P2-20 Truth sync and exit gate (G19)
- **Files:** `prototype/README.md`, `prototype/LIMITATIONS.md`, `prototype/VALIDATION.md`,
  `prototype/planning/PROGRESS.md`. The stale lines are listed in `01_STATE_AND_GAPS.md` §4 G19.
- **Rules:**
  - Re-verify each statement before rewriting it.
  - `detect_changes.py --range` is checked on a scratch copy of the **whole** repository including `.git/`
    (excluding `node_modules`, `build`, `.docusaurus`): `python3 scripts/detect_changes.py --range HEAD~1...HEAD`.
    Then the README Known issue is corrected or kept with the observed result.
  - `VALIDATION.md:153` gets `<model-id>`.
  - New `VALIDATION.md` rows for P2-14…P2-19, with GitHub-side columns NOT RUN.
  - `PROGRESS.md` gets this pack's Blocked rows (§5) and the proposed `AGENTS.md` / root `README.md` wording
    for the owner.
  - E11, E12 and E13 stay as written until the owner decides.
- **Acceptance:**
  1. The phase gate.
  2. On a scratch copy: `npm run build:production && npm run build:demo` exit 0.
  3. `npm run detect` reports `stale generated: 0`.
  4. `grep -n "Live runs currently fail\|not yet exercised" README.md` prints nothing.
- **Checkpoint 2D:**
  1. Local commit `phase-2D: P2-17 P2-18 P2-19 P2-20`.
  2. Final report.

## 5. Blocked / owner-only (never in the unattended run)

| Item | Decision / prerequisite | Evidence | Smallest unblocking action |
|---|---|---|---|
| P2-08 rows Anthropic, OpenAI, local | E5; keys and spend caps | `prototype/planning/PROGRESS.md:141`; `prototype/VALIDATION.md:150-153` | H3-6 |
| First bot PR and real approval (J3) | GitHub App (KB E7 = repo E8), decided, not created | `prototype/planning/PROGRESS.md:140,156` | H3-7 |
| P1-08 Mermaid gate | E6 | `prototype/planning/PROGRESS.md:139,155`; `mermaid-cli` 11.17.0 (`01_STATE_AND_GAPS.md` §3) | H3-9 |
| Environment branch-policy negative test | GitHub dispatch | `prototype/VALIDATION.md:143-144` | H3-8 |
| Phase 3 (NV-REQ-023) | NV-SUP-2 (KB E8) | `docs/next-phase/03_NEXT_VERSION_PLAN.md:510-512` | H3-11 |
| Archive `ai-models/` | E9 | `docs/next-phase/02_RESEARCH_KB.md:375` | H3-11 |
| `q-002` content; model name in docs; evidence branch; G9 wording | E11, E12, E13, G9 | `01_STATE_AND_GAPS.md` §5 | H3-10 |
| Guard protects this pack | `.agents/` is owner-only | `.agents/hooks/doccad_guard.py:31-35` | H3-3 |
| Agent-layer truth (`prototype-code.md` known debt, `AGENTS.md` citations) | `.claude/`, `AGENTS.md` are outside the run | `.claude/rules/prototype-code.md:47-51`; `AGENTS.md:123` | H3-12 |
| Browser verification (M7) | Interactive `/browser`; Playwright not approved (E6) | `prototype/VALIDATION.md:100-124` | Owner session with `/browser`, or E6 |

## 6. Acceptance matrix

| Item | Requirement | Test class / evidence | Journey |
|---|---|---|---|
| P2-13 | NV-REQ-001, REQ-015 | baseline evidence rows | J7 |
| P2-14 | NV-REQ-020, **NV-REQ-027** (every generation run reports provider, returned model, calls, tokens and request IDs on stdout and in the CI step summary; never payloads, headers or key values) | `TestRunUsageReport`; dry-run output; owner-observed step summary | J3, J6 |
| P2-15 | NV-REQ-008, **NV-REQ-028** (absent `visibility` is private in the schema, the validator and the production filter; generation stamps it explicitly) | `TestVisibilityFailsClosed` + three existing filter classes; production round trip | J5 |
| P2-16 | NV-REQ-007 | `TestExplicitProviderSelection` new case | J6 |
| P2-17 | NV-REQ-017, **NV-REQ-029** (`generate.yml` validates inputs in one tested script, pushes a unique branch per run, and grants write only at job level) | `TestDispatchGeneration`, workflow classes | J3 |
| P2-18 | NV-REQ-029 | `TestDispatchGeneration`; owner-observed branch name | J3 |
| P2-19 | NV-REQ-029 | `TestWorkflowSecurityInvariants` new assertion | J3 |
| P2-20 | REQ-015, NV-REQ-011 | phase gate evidence rows; doc greps | J7 |

Journeys J1–J8 are defined in `docs/next-phase/04_ACCEPTANCE.md` §3.

## 7. Risks

| Risk | Mitigation |
|---|---|
| The run stalls or improvises on a missing dependency (the Phase 2 `npm ci` contradiction) | Owner installs first (H3-2); `npm ls` / import probe; a missing dependency is a stop condition |
| P2-15 silently hides the interview datasets in production | Trap written into the item; expected-set test; round trip on a scratch copy |
| The usage report leaks prompt or evidence text into CI logs | Sentinel and fake-key assertions in `TestRunUsageReport` |
| A workflow refactor weakens hardening or breaks the required check | Existing workflow classes, the new top-level assertion, `github-workflows.md` read first; `ci.yml` job names untouched |
| The branch-name change breaks the `ci.yml` docs-gen path guard | `docs-gen/` prefix kept and asserted |
| The run claims GitHub-side results | They stay NOT RUN; the owner observes them (H3-5) |
| The run edits `AGENTS.md` to match its own changes | Forbidden; it proposes wording in `PROGRESS.md` |
| Compaction drops rules | Two checkpoints with fresh conversations; Run rules in `PROGRESS.md`; guard reminder once H3-3 is done |
