# 01 — State and gaps before the Phase 2 run

Prepared 2026-10-06 in a Claude Code planning session (planning only: nothing under `prototype/`,
`docs/primary-inputs/`, `docs/next-phase/` or `docs/prototype-planning/` was changed). This file updates
`docs/next-phase/01_CONTEXT_MAP.md` (2026-10-01) for the parts that changed since; read that file for
vision, requirements, decisions and target architecture, which did not change.

Labels follow the archive convention: **EXPLICIT** (read in the cited file or command output),
**INFERRED** (reasoning shown), **UNKNOWN** (no evidence).

## 1. Baseline — executed 2026-10-06 on a scratch copy (`.github/` + `prototype/`)

| Check | Result | Key line |
|---|---|---|
| `DOCCAD_REQUIRE_JSONSCHEMA=1 python3 scripts/validate_docs.py` | PASS (exit 0) | `Validated 40 pages, 4 interview datasets, 38 provenance hashes.` |
| `python3 scripts/detect_changes.py --all` | PASS | `Manifest: .docs-manifest.json (44 entries)` / `stale generated: 0` |
| `python3 -m unittest discover tests` | PASS | `Ran 95 tests … OK` (91 committed + 4 in `TestWorkflowSecurityInvariants`, uncommitted on branch `close-open-items`) |
| `npm run typecheck`, `npm run build`, production-filter round-trip | NOT RUN in this session | last recorded PASS: `prototype/planning/PROGRESS.md` P1-09 (2026-10-01) |
| GitHub Actions (`gh run list --limit 5`) | PASS | `ci`, `publish`, Dependabot and the scheduled `drift` run (2026-10-05) all `success` |

## 2. What the previous run delivered (EXPLICIT, `prototype/planning/PROGRESS.md` Evidence log)

- **Phase 0 (P0-01…P0-17): complete.** Every item has an evidence row; zero expected failures.
- **Phase 1:** P1-01…P1-07 and P1-09 PASS. P1-08 (Mermaid compile gate) is **BLOCKED** because owner
  decision E6 does not approve `@mermaid-js/mermaid-cli`. Production approval end-to-end is **BLOCKED**
  until the owner creates the DOCCAD GitHub App. The workflow change that opens docs-gen PRs as the App is
  implemented but **uncommitted** on branch `close-open-items` (`git status`, 2026-10-06).
- **Phase 2 (P2-01…P2-10): not started.** None of the planned files exist (`ai/schema_adapt.py`,
  `ai/http.py`, `scripts/check_grounding.py`, `tests/golden/`), and none of the planned test classes are
  in `prototype/tests/test_doccad.py` (`TestProviderSchemaDerivation`, `TestAdapterRequestShapes`,
  `TestSamplingOptIn`, `TestHttpRetryPolicy`, `TestRunBudget`, `TestGroundingGate`,
  `TestPromptInjectionFixtures`).

## 3. New gaps that the 2026-10-01 plan does not cover

Found in this session by reading the code. Each one becomes a work item or an acceptance extension in
`02_PHASE2_PLAN.md`.

| # | Gap | Evidence | Consequence |
|---|---|---|---|
| G1 | No adapter ever raises `ProviderTransportError`. Every HTTP and network failure becomes the base `ProviderError`. | `ai/anthropic_provider.py:56-61`, `ai/openai_provider.py:48-53`, `ai/gemini_provider.py:58-63`, `ai/local_provider.py:57-62`; the router only falls back on `ProviderTransportError` (`ai/router.py:190`) | EXPLICIT. In live mode a 503 or a timeout aborts the chain instead of falling back. `TestRouterFallbackSemantics` passes only because it uses mocks that raise the right class. |
| G2 | Live providers cannot be reached. Every non-private chain starts with `fixture`, which always succeeds, and no CLI or workflow input selects a provider. | `ai.config.yaml:33,35,37`; `scripts/generate_page.py:152-157` (flags: `--contract`, `--target`, `--privacy`, `--dry-run`) | EXPLICIT. The owner smoke procedure in `docs/next-phase/03_NEXT_VERSION_PLAN.md` P2-08 ("with the provider chain set to the provider under test") has no mechanism except editing the config. |
| G3 | Adapters return the *configured* model string, not the model the API returns. | `ai/anthropic_provider.py:71`, `ai/openai_provider.py:65`, `ai/gemini_provider.py:76`, `ai/local_provider.py:77` | EXPLICIT. Provenance would record an alias, not the served snapshot (`docs/next-phase/02_RESEARCH_KB.md` C2.4, C2.5). |
| G4 | `temperature` is forwarded whenever it is in `opts`. | `ai/anthropic_provider.py:40-41` and the same pattern in the other three adapters | EXPLICIT. Newer Anthropic models return 400 on non-default sampling (KB C2.2). |
| G5 | The OpenAI adapter sends `max_tokens`. | `ai/openai_provider.py:33` | UNVERIFIED risk: newer models may require `max_completion_tokens` (KB C1.10). |
| G6 | Before writing a page, generation checks only the frontmatter schema. The MDX restriction gate (T3) and the link allowlist (T4) run later, in `npm run validate`. | `scripts/generate_page.py:279-284` | EXPLICIT. Live output that breaks T3 or T4 is written to disk first, then rejected. The grounding gate (P2-06) is the natural place to run all of them before writing. |
| G7 | `Router.chain_for` still swallows every instantiation error. | `ai/router.py:159-167` | EXPLICIT. Low impact (`run_with_fallback` does not use it), but it contradicts ADR-004. |
| G8 | `generate.yml` has no `provider` input and no `generation` environment. | `.github/workflows/generate.yml` (`on.workflow_dispatch.inputs`: contract, target, privacy) | EXPLICIT. Live CI generation is impossible. That is correct until E5 is decided; Phase 2 adds the switch and keeps fixture as the default. |
| G9 | Decision-ID drift. In `docs/next-phase/02_RESEARCH_KB.md` §E and `03_NEXT_VERSION_PLAN.md` H-8, **E7** is the GitHub App and **E8** is NV-SUP-2 (Phase 3). The repository uses "**E8**" for the GitHub App. | `AGENTS.md`, `README.md`, `prototype/README.md`, `prototype/LIMITATIONS.md`, `prototype/VALIDATION.md`, `prototype/planning/PROGRESS.md`, `.github/workflows/generate.yml` | EXPLICIT. A reader following the pack would mix up the App and Phase 3. Resolution: `02_PHASE2_PLAN.md` §3 names both by meaning and recycles neither ID. Fixing the repository wording is an owner choice (bullet in §0 of the plan). |
| G10 | Stale statements. | `prototype/planning/PROGRESS.md:3` says "91 unit tests passing" (95 with `close-open-items`). `prototype/LIMITATIONS.md` Tier 4 #3 says the approval record is "scheduled for Phase 1 (P1-05)" (P1-05 is PASS) and omits `approved_hash`. `.claude/plans/2026-10-01-close-open-items.md` names `vars.DOCCAD_APP_ID`, but the code uses `DOCCAD_APP_CLIENT_ID`. | EXPLICIT. Small; P2-00 fixes the two tracked files. |

## 4. Owner decisions still open (EXPLICIT, `prototype/planning/PROGRESS.md` §0)

| Decision | Blocks |
|---|---|
| E5: first live provider, `AI_MODEL_*` values, spend cap per run and per month | P2-08 live smoke; live dispatch of `generate.yml` |
| Create the DOCCAD GitHub App and set `DOCCAD_APP_CLIENT_ID` + `DOCCAD_APP_PRIVATE_KEY` | First real approval end-to-end (J3) |
| E6: further dependencies | P1-08 stays BLOCKED. Phase 2 needs **no** new dependency (stdlib `http.server` for stubs) |
| NV-SUP-2 (KB E8): pinned external evidence | Phase 3 |
| E9: `docs/primary-inputs/02_RESEARCH/ai-models/` | Archive task, outside this run |

Research facts from 2026-10-01 (`docs/next-phase/02_RESEARCH_KB.md` §C) are five days old. Each request
shape must be re-read at the provider's documentation before an adapter changes (§C was read through a
summarizing fetch tool). The run cannot do that offline, so the plan makes the request-shape tests
assert the shapes recorded in §C, and the owner's live smoke (P2-08) is the real check.
