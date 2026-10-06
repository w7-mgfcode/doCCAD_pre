# 02 — Phase 2 plan: live AI generation behind the fixture default

Prepared 2026-10-06. Refines `docs/next-phase/03_NEXT_VERSION_PLAN.md` §6 (P2-01…P2-10) with the gaps in
`01_STATE_AND_GAPS.md`. Item IDs from the 2026-10-01 plan are kept, new items continue from P2-11, and new
requirements continue from NV-REQ-024. The run is executed from `03_ANTIGRAVITY_PROMPT.txt`.

## 0. Next-phase development, in bullets

**Before the run (owner)**
- Merge `close-open-items` (E8/App workflow, `TestWorkflowSecurityInvariants`, base-path fix) into `main`
  through its PR, so the run starts from a clean tree with 95 tests.
- Decide whether to rename the GitHub App decision from "E8" to E7 across the repository wording, or keep
  "E8" and treat KB E7 and repo E8 as the same decision (G9). Either way, the run must not recycle an ID.
- Optional, any time: create the DOCCAD GitHub App. This unblocks the first real approval and is
  independent of Phase 2.

**Baseline and hygiene**
- Re-verify the baseline: 40 pages, 38 hashes, 0 stale, 95 tests, typecheck and en + hu build.
- Install a test-wide network guard, so no test can reach anything except `127.0.0.1`.
- Correct the two stale statements (PROGRESS header, LIMITATIONS Tier 4 #3).

**Provider plumbing**
- One stdlib HTTP helper (`ai/http.py`). It retries 429/5xx/529 with backoff and jitter and honours
  `Retry-After`. It fails fast on 400/401/403 and on quota or spend-cap 429. It maps exhausted transport
  failures to `ProviderTransportError`, so live fallback finally works (G1).
- Explicit provider selection: `--provider <name>` on both generation scripts. It builds a one-provider
  chain (no fixture in front) and still obeys the private → local pin (G2).
- Provider-facing schemas derived from the repo schemas. Structured output is sent only where the
  contract says `structured_output: true` (today, interview prep). The repo schemas stay the gate.
- Native structured-output fields per adapter, each request shape in one function. Adapters return the
  model string the API reports (G3) and surface refusals as content errors.
- Sampling parameters and the token-limit field name become opt-in per provider in `ai.config.yaml`
  (G4, G5).

**Safety, cost and quality gates**
- Usage and `request-id` logging that never logs payloads, keys or auth headers.
- A per-run token and call budget. Repair retries count against it.
- A deterministic grounding gate (`scripts/check_grounding.py`). It runs before any generated page is
  written (alongside the MDX and link gates, G6) and in `npm run validate`, so CI enforces it.
- A golden set (contract → expected cited sources) and prompt-injection fixtures, each with failing cases.
- Fix `Router.chain_for` so it no longer swallows errors (G7).

**Workflow**
- `generate.yml` gets a `provider` input (default `fixture`). Only a non-fixture provider runs in the
  protected `generation` environment, with provider secrets scoped to the generation step (G8). All
  existing workflow invariant tests stay green.

**Owner-executed**
- One live smoke call per enabled provider, locally or through `generate.yml`, after keys, `AI_MODEL_*`
  values and spend caps exist. The result is recorded in `VALIDATION.md`.

**Exit**
- Local gate green with zero expected failures, `stale generated: 0`, VALIDATION / LIMITATIONS / README
  current, and PROGRESS evidence rows for every item.

**Not in this run**
- Phase 3 (external evidence, NV-SUP-2), Anthropic workload identity federation (P2-09), L2+ retrieval,
  provider SDKs, promptfoo/RAGAS, Playwright, mermaid-cli, and any runtime model call from the site.

## 1. Scope and roadmap mapping

| Roadmap milestone (`docs/primary-inputs/08_TASKS/future/implementation_roadmap.csv`) | Advanced by |
|---|---|
| M1.4 "live call works with one key" | P2-02, P2-11, P2-08 |
| M1.5 bot-PR generation flow | P2-12 (provider input; the App path is already built) |
| M2.1 provider matrix | P2-01…P2-04 |
| M3.1 / M3.2 cost and quality controls | P2-05, P2-06, P2-07 |

## 2. Run rules (deltas to `docs/next-phase/03_NEXT_VERSION_PLAN.md` §2, which still applies)

- **Branch:** `phase-2-live-ai`, created from an up-to-date `main` that contains `close-open-items`. Local
  commits only at the two checkpoints. No push, no PR. The guard hook denies them anyway.
- **No network in tests:** every Phase 2 test talks to a `http.server` stub bound to `127.0.0.1` on port 0.
  P2-00 installs a guard that turns any non-loopback connection into a test failure.
- **Cloud base URLs are not configurable from `ai.config.yaml`.** A `base_url` constructor argument exists
  for tests only, so no configuration can send a key to another host. The local provider keeps its
  `endpoint` setting.
- **Phase gate** at each checkpoint, from `prototype/`: `npm run typecheck && DOCCAD_REQUIRE_JSONSCHEMA=1
  npm run validate && npm run test && npm run build` exit 0, then `npm run detect` reports
  `stale generated: 0`.

## 3. Owner checklist for this run

| # | Action | Blocks |
|---|---|---|
| H2-1 | Merge the `close-open-items` PR into `main`, then `git checkout main && git pull` | Run start |
| H2-2 | Keep Antigravity command auto-execution for the `doCCAD_pre` project (set 2026-10-01). Confirm the guard self-test passes: `python3 .agents/hooks/test_doccad_guard.py` | Run start |
| H2-3 | Decision-ID wording (G9): **App decision** = KB E7 = repo "E8" (decided: GitHub App); **Phase 3 decision** = KB E8 = NV-SUP-2 (open). Tell the run if the repo wording should change | P2-00 wording only |
| H2-4 | E5: choose the first live provider, set its `AI_MODEL_*` value, create a key with an expiry and a hard spend cap | P2-08 |
| H2-5 | For CI live runs: create the `generation` environment (branch `main`, optional required reviewer) and store provider keys only as its secrets | P2-08 via `generate.yml` |
| H2-6 | Optional: create the DOCCAD GitHub App (`prototype/README.md` §Governance) | J3 end-to-end |

## 4. Work items

Order of execution: **Checkpoint 2A** = P2-00, P2-04, P2-11, P2-01, P2-02, P2-03.
**Checkpoint 2B** = P2-05, P2-06, P2-07, P2-12, P2-08 (preparation only), P2-10.

### P2-00 Baseline, network guard, truth sync
- **Rationale:** start from verified numbers; make "no network" a test, not a promise; remove the two
  stale claims (G10).
- **Files:** `tests/test_doccad.py` (a `setUpModule` network guard that patches socket connects to refuse
  non-loopback addresses, plus `TestNoExternalNetwork`); `planning/PROGRESS.md` (header);
  `LIMITATIONS.md` (Tier 4 #3).
- **Acceptance:** `npm ci && npm run typecheck && DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate && npm run
  test && npm run build && npm run detect`, with the result logged against the expected baseline (40
  pages, 38 hashes, 95 tests before this item, 0 stale). Then `python3 -m unittest
  tests.test_doccad.TestNoExternalNetwork -v`, which must include a case where connecting to a
  non-loopback address raises.
- **Traces:** NV-REQ-001, NV-REQ-025. **Human:** none.

### P2-04 HTTP helper: retry, error classification, usage logging (extended for G1)
- **Files:** `ai/http.py` (new). All four adapters send through it.
- **Behaviour:**
  - Retry 429 (with `Retry-After`), 500, 502, 503, 504 and 529 with exponential backoff and jitter. The
    sleep function is injectable so tests do not wait.
  - Terminal, no retry: 400, 401, 403, 404, and any 429 marked as quota or spend cap (Anthropic
    `enforced_spend_limit_reached` with no `retry-after`; OpenAI `insufficient_quota`).
  - Exhausted retries, timeouts and `URLError` raise `ProviderTransportError`. Terminal statuses raise
    `ProviderError`. Error text is truncated and redacts `authorization`, `x-api-key` and
    `x-goog-api-key`.
  - Log `request-id` (or the provider's equivalent header), status and token usage, including cache
    fields when present. Never log payloads.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestHttpRetryPolicy -v`. The stub serves each
  status in turn; tests assert the retry count, the terminal cases, the exception class, the redaction
  (a fake key-shaped header value never appears in the error or the log) and that live fallback works
  end to end (stub p1 → 503 ×N, stub p2 → 200).
- **Traces:** REQ-005; NV-REQ-007, NV-REQ-020; KB C5.1–C5.6. **Human:** none.

### P2-11 Explicit provider selection (new, G2)
- **Files:** `ai/router.py` (`select_chain_names(task_meta, provider=None)`), `scripts/generate_page.py`,
  `scripts/generate_question.py` (`--provider {fixture,anthropic,gemini,openai,local}`, default: chain
  from config).
- **Rules:** `--provider X` gives the chain `[X]`. A disabled provider is an error, not a silent fallback.
  `privacy: private` with any provider other than `local` raises `PrivacyRoutingError` before anything
  is instantiated. The routing config stays unchanged, so the default stays fixture-first.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestExplicitProviderSelection -v`. Cases:
  selected chain is exactly one provider; private + cloud raises; disabled provider raises; no
  `--provider` keeps today's chain. Also `python3 scripts/generate_page.py --contract
  GenerateRecruiterPage --target architecture-system-overview --provider anthropic --dry-run` exits 0,
  prints a provider chain consisting only of `anthropic`, and makes no call (no key needed).
- **Traces:** REQ-005; NV-REQ-024. **Human:** none.

### P2-01 Provider-facing schemas
- As specified in the 2026-10-01 plan (`ai/schema_adapt.py`), with one change: derivation applies only to
  contracts with `model_requirements.structured_output: true`. Today that is `GenerateInterviewPrep`
  (`contracts/GenerateInterviewPrep.yaml:35`). The MDX contracts stay free-text with local validation.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestProviderSchemaDerivation -v`. For each
  provider, the derived interview schema contains no keyword that provider rejects (KB C1.3, C1.6, C1.9,
  C1.11). OpenAI-strict objects carry `additionalProperties: false` and a full `required`. The repo
  schema file is byte-identical afterwards.
- **Traces:** REQ-005; NV-REQ-019.

### P2-02 Structured output in every adapter (extended for G3)
- As in the 2026-10-01 plan:
  - Anthropic: `output_config.format`.
  - OpenAI: `response_format` `json_schema`, strict.
  - Gemini: `generationConfig.responseMimeType` + `responseJsonSchema`.
  - Local: `response_format`, falling back to native `/api/chat` `format` with `stream: false`.
  Each request shape lives in one function.
- **Added:** the returned dict's `model` is the model string from the response body, falling back to the
  configured value only if the body has none. Refusals (Anthropic `stop_reason: "refusal"`, OpenAI
  `refusal`) raise `ProviderContentError`. `generate_page.py` re-validates every response locally, as
  today.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestAdapterRequestShapes -v`. The stub asserts
  URL, header *names* (never values) and body shape per provider; that the returned-model fallback works;
  and that a refusal does not fall back.
- **Traces:** REQ-005, REQ-009; NV-REQ-005, NV-REQ-019; KB C1.1–C1.12, C2.5.

### P2-03 Sampling parameters and token-limit field per provider (extended for G4, G5)
- **Files:** `ai.config.yaml` (optional `params:` per provider, for example `temperature`, and
  `token_param: max_tokens | max_completion_tokens` for OpenAI); adapters send sampling only when
  configured.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestSamplingOptIn -v`. With no `params`, no
  sampling key is in any body; a configured value is sent; `token_param` switches the OpenAI field.
  `TestPrivateChainConfig` stays green.
- **Traces:** KB C1.10, C2.2.
- **Checkpoint 2A:** phase gate; local commit `phase-2A: P2-00 P2-04 P2-11 P2-01 P2-02 P2-03`; stop with
  the resume line.

### P2-05 Per-run budget and cache-friendly prompt order
- As in the 2026-10-01 plan: `budget: {max_tokens_per_run, max_calls_per_run}` in `ai.config.yaml`. The
  run aborts with a budget error *before* the call that would exceed a limit, and repair retries count.
  Prompt templates put the static governance text and the evidence first.
- A template change bumps `prompt_version` and the contract `version`, then the run re-seeds until
  `npm run detect` reports 0 stale.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestRunBudget -v`.

### P2-06 Grounding gate and golden set (extended for G6)
- **Files:** `scripts/check_grounding.py`:
  - every citation resolves to allowed evidence with a matching hash;
  - quoted spans are contained in the cited source (whitespace-normalized);
  - recruiter technology tokens appear in the deterministic fact list or in cited canon.
  Also `tests/golden/` (contract → expected cited-source set).
- **Wiring:** `generate_page.py` and `generate_question.py` call the grounding gate, the MDX restriction
  gate and the link allowlist *before writing*. `validate_docs.py` runs the grounding gate on every
  generated page, so CI enforces it.
- **If seeded views fail the gate:** fix the cause through the scripts (fixture text or contract plus a
  re-seed), or record FAIL. Never loosen the gate.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestGroundingGate -v`, with at least one failing
  fixture per rule and one pre-write rejection that leaves no file on disk. Then `DOCCAD_REQUIRE_JSONSCHEMA=1
  npm run validate` exits 0.
- **Traces:** REQ-010, REQ-012; NV-REQ-021; KB C3.1, C3.3.

### P2-07 Prompt-injection fixtures
- As in the 2026-10-01 plan: canonical-looking evidence with injected instructions. A stub provider
  "obeys" the injection (new URL, invented technology, missing citation, an `import`), and the
  deterministic gates must reject every variant.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestPromptInjectionFixtures -v`.
- **Traces:** REQ-016; NV-REQ-021; T2; KB C4.1–C4.4.
- **Also:** G7. `Router.chain_for` re-raises `MissingKeyError` and `MissingModelError` instead of
  swallowing them; covered by a case in `TestExplicitProviderSelection`.

### P2-12 `generate.yml` provider input and `generation` environment (new, G8)
- **Files:** `.github/workflows/generate.yml`. Read `.claude/rules/github-workflows.md` first.
- **Changes:**
  - Add a `provider` choice input with default `fixture`, passed to the scripts through `env:`.
  - Run a separate job for non-fixture providers, with `environment: generation`, guarded by
    `if: inputs.provider != 'fixture'`. Provider secrets and `AI_MODEL_*` come from that environment and
    are exposed only to the generation step.
  - Keep `privacy: private` rejecting every provider except `local`.
  - Keep the existing App/branch-only logic unchanged.
- **Acceptance:** `python3 -m unittest tests.test_doccad.TestWorkflowSecurityInvariants
  tests.test_doccad.TestWorkflowScriptInvocations tests.test_doccad.TestGenerateWorkflowProviderInput
  -v`. The new class asserts:
  - the default is `fixture`;
  - a non-fixture path requires the `generation` environment;
  - no secret is referenced outside that job;
  - no `${{ inputs.* }}` appears inside `run:`.
  The GitHub-side dispatch stays NOT RUN until the owner reports it.
- **Traces:** REQ-012; NV-REQ-017, NV-REQ-026; KB C6.1–C6.3. **Human:** H2-5.

### P2-08 Live smoke (owner-executed) — the run prepares it and stops
- The run writes into `VALIDATION.md` the exact owner commands, one row per provider, each NOT RUN.
  Run from `prototype/`, with the key and `AI_MODEL_*` set in the shell:
  - `python3 scripts/generate_page.py --contract GenerateInterviewPrep --target architecture-system-overview --provider <name>`
  - `python3 scripts/generate_page.py --contract GenerateRecruiterPage --target architecture-system-overview --provider <name>`
  - then `DOCCAD_REQUIRE_JSONSCHEMA=1 npm run validate`
  - and `git restore docs/generated` if the output is not kept. Kept output goes through a docs-gen PR,
    never a direct commit.
- **Owner records:** provider, the returned model string, exit codes, validation result, and token usage
  from the log.
- **Traces:** NV-REQ-022. **Human:** H2-4 (and H2-5 for the workflow path).

### P2-09 Anthropic workload identity federation — out of scope for this run (owner-optional later)

### P2-10 Phase 2 exit gate
- Phase gate green; the full suite reports zero expected failures; `stale generated: 0`.
- `VALIDATION.md`, `LIMITATIONS.md` (live providers move from "unverified" to "implemented, stub-tested,
  live NOT RUN"), `prototype/README.md` and `PROGRESS.md` updated with evidence rows.
- **Checkpoint 2B:** local commit `phase-2B: P2-05 P2-06 P2-07 P2-12 P2-08-prep P2-10`; final report.

## 5. Acceptance matrix

| Item | Requirement | Test class / evidence | Journey |
|---|---|---|---|
| P2-00 | NV-REQ-001, **NV-REQ-025** (tests never reach a non-loopback address) | `TestNoExternalNetwork`; baseline evidence row | J7 |
| P2-04 | NV-REQ-007, NV-REQ-020 | `TestHttpRetryPolicy` | J6 |
| P2-11 | **NV-REQ-024** (explicit provider selection; the privacy pin survives it) | `TestExplicitProviderSelection`; dry-run output | J5, J6 |
| P2-01 | NV-REQ-019 | `TestProviderSchemaDerivation` | J6 |
| P2-02 | NV-REQ-005, NV-REQ-019 | `TestAdapterRequestShapes` | J6 |
| P2-03 | NV-REQ-020 | `TestSamplingOptIn` | J6 |
| P2-05 | NV-REQ-020 | `TestRunBudget` | J6 |
| P2-06 | NV-REQ-021 | `TestGroundingGate`; strict validate | J2, J5 |
| P2-07 | NV-REQ-021 | `TestPromptInjectionFixtures` | J5 |
| P2-12 | NV-REQ-017, **NV-REQ-026** (live CI generation only through the protected `generation` environment; fixture default) | `TestGenerateWorkflowProviderInput` + the two existing workflow classes; owner-observed dispatch | J3, J6 |
| P2-08 | NV-REQ-022 | `VALIDATION.md` owner row (NOT RUN until then) | J6 |
| P2-10 | REQ-015 | phase gate evidence rows | J7 |

The journeys (J1–J8) are those defined in `docs/next-phase/04_ACCEPTANCE.md` §3.

## 6. Risks

| Risk | Mitigation |
|---|---|
| The run claims tests it never wrote or ran (first-run pattern) | Named test classes, each with failing cases; evidence rows; `git diff --stat` after each edit |
| Seeded generated views fail the new grounding gate | Fix through scripts plus a contract bump and re-seed, or record FAIL; loosening the gate is banned |
| Request shapes drifted since 2026-10-01 | Shapes isolated in one function per adapter; the owner's live smoke is the real check; failures are recorded, not patched blind |
| A configurable cloud base URL leaks keys to another host | Base URL only as a constructor argument for tests (§2) |
| Retry tests are slow or flaky | Injectable sleep; port-0 stubs; no real timeouts above 2 s in tests |
| Workflow edit weakens hardening | Existing `TestWorkflowSecurityInvariants` plus the new workflow class; `github-workflows.md` read first |
| Compaction drops rules in a long phase | Two checkpoints with fresh conversations; the guard's PreInvocation reminder; Run rules in PROGRESS |
