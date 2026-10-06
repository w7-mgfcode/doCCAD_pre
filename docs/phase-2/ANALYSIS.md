# How the Phase 2 Antigravity prompt was derived

Prepared 2026-10-06 in a Claude Code planning session. Companion to `docs/next-phase/ANALYSIS.md`, which
explains the Phase 0–2 prompt that the previous run used for Phases 0 and 1.

## Method

1. **State.** Read `docs/next-phase/` in full where it touches Phase 2 (README, ANALYSIS, prompt,
   acceptance, plan §1–3 and §6–8, research KB §C–§E). Read `prototype/planning/PROGRESS.md` and
   `prototype/LIMITATIONS.md`.
2. **Baseline.** Ran validate, detect and the full test suite on a scratch copy of `.github/` +
   `prototype/`, and checked CI with `gh run list` (`01_STATE_AND_GAPS.md` §1).
3. **Code read.** Read the AI layer the phase changes: `ai/provider.py`, `ai/router.py`, all four live
   adapters, `ai.config.yaml`, the three contracts, the generation loop in `scripts/generate_page.py`,
   `.github/workflows/generate.yml` and `prototype/.env.example`. That read found G1–G8, which the
   2026-10-01 plan does not cover. The most important is G1: live fallback can never fire, because no
   adapter raises the exception class the router falls back on.
4. **No new web research.** The 2026-10-01 research (KB §C) is five days old and already covers every
   provider fact Phase 2 needs. The run is offline by design, and the owner's live smoke (P2-08) is the
   real check of the request shapes. That limit is stated in `01_STATE_AND_GAPS.md` §4.
5. **Plan, then prompt, then pre-mortem.** The pre-mortem revised the prompt (marked below).

## Design choices

| Choice | Why |
|---|---|
| A new folder `docs/phase-2/` instead of editing `docs/next-phase/` | `docs/next-phase/` is the dated record the previous run executed, and the guard protects it. A new pack keeps both runs traceable. |
| Keep the P2-0x IDs and add P2-11, P2-12, NV-REQ-024…026 | IDs are never recycled (`docs/primary-inputs/CONTRIBUTING.md` spirit). The old acceptance rows stay valid. |
| Two checkpoints (2A plumbing, 2B gates and workflow) instead of one phase | Compaction risk grows with run length (`docs/next-phase/02_RESEARCH_KB.md` A6.2). Each half ends in a green gate and a commit. |
| P2-00 network guard first | "No network" was a rule in the last prompt. It becomes a test, so a stub mistake cannot quietly hit a real endpoint. |
| `--provider` instead of reordering chains | Changing the default chains would change what every existing command does. An explicit flag keeps fixture as the default and gives the owner smoke a real mechanism (G2). |
| No cloud base URL in config | A config-settable URL plus an env key could send a key to any host. Tests need a URL override, so it is constructor-only. |
| Structured output only where the contract says so | `contracts/*.yaml` already declare `model_requirements.structured_output`. Only interview prep is JSON; the MDX contracts would need an envelope redesign that no requirement asks for. |
| Grounding gate both before writing and in `validate_docs.py` | Before writing: no invalid live file lands (G6). In validate: CI enforces it on every page, including seeded ones. |

## Every prohibition of the previous prompt, kept or deliberately narrowed

| Previous prompt (`docs/next-phase/05_ANTIGRAVITY_PROMPT.txt`) | This prompt |
|---|---|
| Never label fixture output as Gemini or live | Kept, extended to stub output (opening) |
| `AGENTS.md` is the authority; read rules by hand; no `GEMINI.md`, no Antigravity workflows | Kept, adds `github-workflows.md` (section 0) |
| Archive immutable; historical prompts not executed; plan folders read-only | Kept, adds `docs/phase-2/` (section 0) |
| Guard hook; record denials; never work around | Kept (section 0) |
| One branch, no push, PR, remote, deploy; local commits at checkpoints | Kept; branch `phase-2-live-ai` (section 1) |
| Scratch copies for state-rewriting commands | Kept, now `.github/` + `prototype/` as `AGENTS.md` requires (section 1) |
| Run rules in PROGRESS, re-read per item | Kept; the previous block is marked superseded, not deleted (section 1) |
| Evidence log; no undocumented checks; verify edits by `git diff`; two attempts | Kept (section 1) |
| New test classes need a failing case | Kept, generalized (section 1) |
| Invariants (planes, fixture default, privacy pin, env-only model IDs, static site, deps, simulated approval, version bumps, no datastore/agents) | Kept; adds the explicit-provider privacy case, no cloud base URL in config, and local re-validation (section 1) |
| Never touch keys or `.env` | Kept; adds the fake-key and log assertions (section 1) |
| Never weaken a gate | Kept; adds the seeded-view grounding case (section 1) |
| Canonical pages human-owned | Kept; this run should not need to touch them (section 1) |
| Plan, not truth; proposed defaults; no private reasoning; no invented tool output | Kept (section 1) |
| Live calls owner-executed; stub server only | Kept, now enforced by P2-00 (sections 1, 3, 4) |
| Stop conditions | Kept; adds model ID values (section 4) |
| Phase 3 out of scope; do not report complete while checks fail | Kept; adds P2-09 out of scope (section 5) |
| Browser verification (`/browser`) | Dropped on purpose: Phase 2 changes no page or component; the CI build and the Pages smoke cover the site |

## Pre-mortem (assume the Phase 2 run failed — why?)

| # | Likely cause | Blocked by |
|---|---|---|
| 1 | Tests written against mocks again, so G1 survives (the router test is green while live fallback stays dead) | P2-04 acceptance requires a stub-server end-to-end fallback case *(added in revision)* |
| 2 | A test accidentally reaches a real endpoint, or the model "verifies" a shape by calling out | P2-00 network guard first; network beyond 127.0.0.1 is a stop condition |
| 3 | The grounding gate rejects seeded views, and the run loosens the gate or hand-edits pages | Explicit ban plus the allowed fix path (scripts, version bump, re-seed) *(added in revision)* |
| 4 | Retry tests sleep for real and time out or flake | Injected sleep; port-0 stubs (prompt section 1, plan risk table) |
| 5 | Fake keys leak into logs or error text | Redaction tests with key-shaped fakes (P2-04) |
| 6 | Workflow edit weakens hardening (inline `${{ inputs }}`, secrets job-wide) | Existing workflow tests plus `TestGenerateWorkflowProviderInput`; `github-workflows.md` read first |
| 7 | The run starts on top of the unmerged `close-open-items` work, or on a dirty tree | Start check: clean tree and `TestWorkflowSecurityInvariants` present, else stop (H2-1) *(added in revision)* |
| 8 | The run invents model IDs to make the dry run look real | Model ID values are a stop condition; env-only invariant |
| 9 | Compaction mid-2B drops the "no live call" rule | Fresh conversation at 2A; PreInvocation reminder; Run rules in PROGRESS |
| 10 | Request shapes changed since 2026-10-01 and the run "fixes" them from memory | Shapes come from KB §C only; drift surfaces in the owner smoke and is recorded, not guessed |
| 11 | The previous run's Run rules are overwritten and lose history | New block on top, old block marked superseded *(added in revision)* |

## Limits

- Typecheck and build were not re-run in this planning session (last PASS 2026-10-01, P1-09).
- The provider facts are KB §C (2026-10-01, read through a summarizing fetch tool), not re-read today.
- The plan's acceptance commands were written, not executed. The run executes them.
