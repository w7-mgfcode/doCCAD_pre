# How the Phase 2 closeout prompt was derived

Prepared 2026-10-07 in a Claude Code planning session. Companion to `docs/phase-2/ANALYSIS.md` (the Phase 2
prompt) and `docs/next-phase/ANALYSIS.md` (the Phase 0–2 prompt).

## Method

1. **Review.** Read both run packs in full:
   - `docs/next-phase/`: README, context map, research KB A–E, plan §0–8, acceptance, prompt, analysis;
   - `docs/phase-2/`: README, state and gaps, plan, prompt, analysis.
2. **Current state.** Read the following, and checked every claim against code or command output:
   - `prototype/planning/PROGRESS.md`, `prototype/VALIDATION.md`, `prototype/LIMITATIONS.md`,
     `prototype/README.md`;
   - the archive roadmap and backlog (`docs/primary-inputs/08_TASKS/`, `12_FUTURE/`);
   - the local `HANDOFF.md`.
3. **Read-only GitHub checks** (`gh api`, `gh run view --log`, `gh pr list`):
   - environments, and secret and variable *names*;
   - branches and the draft branch's diff;
   - the CI log of run 37541030510;
   - PR #12 on `origin/main`.
4. **Code read** of the paths the open items touch:
   - `ai/http.py`, `ai/router.py`;
   - `scripts/generate_page.py`, `scripts/build_filter.py`;
   - `schemas/document.schema.json`;
   - all four workflows.

   This read found G11–G18. The most consequential is G14: the schema says an unclassified page is private,
   and the production filter says it is public.
5. **Baseline.** Ran it on a scratch copy (`01_STATE_AND_GAPS.md` §1).
6. **Plan, then prompt, then pre-mortem.** The pre-mortem revised the prompt; the revisions are marked below.

No web research beyond one `npm view` of `@mermaid-js/mermaid-cli`, because E6 depends on whether a CLI
matching Mermaid 11.x exists. It does: 11.17.0, `mermaid ^11.14.0`.

## Design choices

| Choice | Why |
|---|---|
| Folder `docs/phase-2-closeout/`, IDs P2-13…P2-20, checkpoints 2C/2D | "Phase 3" in `docs/next-phase/03_NEXT_VERSION_PLAN.md:510-512` is external evidence, gated by NV-SUP-2, which is undecided. Calling this pack Phase 3 would make the next reader think NV-SUP-2 was accepted. Continuing the P2 numbering recycles nothing |
| New decision IDs from **E11** | KB §E uses E1–E10; G9 shows what happens when one ID means two things. Old decisions are named by meaning plus both IDs ("GitHub App (KB E7 = repo E8)") |
| Fully offline run; the owner installs dependencies (H3-2) | Fixes the Phase 2 prompt's contradiction (below). The 2.0 app's default sandbox has no network anyway (KB A2.4) |
| Usage report as a printed line plus the step summary, not "turn on logging" | The usage line exists but is dropped at INFO (G11). A printed, tested contract survives refactors; whether to also enable the logger is left as a proposed default |
| Never guess Gemini's request-ID field | KB §C does not record it, and the run is offline. `unavailable` is honest; the owner reads the real field at the next live call |
| P2-15 names the JSON-dataset trap and two allowed routes | The obvious fix (absent = private) silently hides four interview datasets in production. The prompt bans the tempting third route: exempting them from the filter |
| Branch name with the run id | Keeps the `docs-gen/` prefix that `ci.yml:77` keys on; every dispatch gets its own reviewable branch instead of failing on the second try |
| Extract the dispatch logic into a script | The two jobs' inline copies have already diverged (provider allowlist only in the live job). A script with `build_parser()` is covered by `TestWorkflowScriptInvocations` for free |
| The run must not edit `AGENTS.md` or the root `README.md` | `AGENTS.md` is the run's own rulebook and authority after compaction; a run rewriting it is the wrong direction. Another session was editing both files during this planning session (`git status`) |
| GitHub-side results always NOT RUN; one `fixture` dispatch after the merge (H3-5) | A fixture dispatch costs nothing and observes P2-14, P2-17, P2-18 and P2-19 at once |

## The Phase 2 prompt's contradiction, and the fix

`docs/phase-2/03_ANTIGRAVITY_PROMPT.txt` contradicts itself:
- `:43` tells the run "run npm ci";
- `:29` says no step "may contact a real provider or any non-loopback address";
- `:67` makes "any network access beyond 127.0.0.1" a stop condition.

A literal reader must either break a rule or stop at the first command. The Phase 2 run executed `npm ci`
anyway (`prototype/planning/PROGRESS.md:110`). This prompt removes the ambiguity in three ways:
- Installing is an owner step before the run (H3-2).
- The run proves the install offline: `npm ls --depth=0`, and an import probe for PyYAML, jsonschema and
  referencing.
- Any network access, package registries included, is a stop condition. The rule names `npm ci`,
  `npm install`, `npm update`, `pip install` and downloading `npx` explicitly.

## Every prohibition of the Phase 2 prompt, kept or deliberately changed

| Phase 2 prompt (`docs/phase-2/03_ANTIGRAVITY_PROMPT.txt`) | This prompt |
|---|---|
| Never label fixture or stub output as Gemini or live (opening) | Kept |
| `AGENTS.md` is the authority; read rules by hand; no `GEMINI.md`, no Antigravity workflows (§0) | Kept |
| Archive immutable; historical prompts not executed; plan folders read-only (§0) | Kept. Adds `docs/phase-2-closeout/` and the Phase 2 prompt to the not-executed list. **New:** no edits to `AGENTS.md` or the root `README.md` |
| Guard hook; record denials; never work around it; `.agents/skills` not used (§0) | Kept; the guard covering this pack is owner action H3-3 |
| Memory may be stale; installed `node_modules`; KB §C for request shapes; no provider network (§0) | Kept; widened to no network of any kind |
| Start on clean `main` with the prerequisite merged, else stop (§1) | Kept; the probe is now `git merge-base --is-ancestor 408b3cf HEAD` |
| One branch, no push/PR/remote/deploy, one agent, commits at checkpoints (§1) | Kept; branch `phase-2-closeout` |
| Scratch copies of `.github/` + `prototype/` for state-rewriting commands (§1) | Kept, plus a whole-repository copy (with `.git/`) for the one `--range` check |
| Run rules restated in `PROGRESS.md`, previous block superseded, re-read per item (§1) | Kept |
| Evidence log; no undocumented checks; verify edits by `git diff`; two attempts (§1) | Kept; GitHub-side observations explicitly NOT RUN |
| New test classes need a failing case; stub servers on 127.0.0.1:0; injected sleeps; network guard (§1) | Kept; the existing `TestNoExternalNetwork` must stay green |
| Invariants: planes, fixture default, no keys or network, privacy pin incl. explicit provider, env-only model IDs, no cloud base URL in config, schemas as gate with local re-validation, static site, dependency rule, simulated approval, version bumps, no SDK, datastore or agents (§1) | Kept verbatim in substance. Adds: no npm package added or upgraded; workflow invariants named in place (SHA pins, no `pull_request_target`, no inline expressions, `validate-and-build` never renamed, no PAT instead of the App token); privacy pin also in `generate.yml` |
| Never touch keys or `.env`; fake keys asserted absent from logs (§1) | Kept. Widened to GitHub variable values and run reports; the usage output allow-list is spelled out |
| Never weaken a gate; seeded-view grounding case (§1) | Kept; adds the P2-15 dataset case and "never exempt files from the filter" *(added in revision)* |
| Canonical pages human-owned (§1) | Kept |
| Plan, not truth; proposed defaults; no private reasoning; no invented tool output (§1) | Kept; adds the explicit list of owner decisions the run must not make |
| Stop conditions (§4) | Kept. Adds: any GitHub-side action including a dispatch; variables; missing or out-of-sync dependencies; owner decisions; `AGENTS.md` / root `README.md` |
| Out of scope: Phase 3, P2-09 (§5) | Kept; adds live calls, the App and the Mermaid gate |
| **`npm ci` at the start of P2-00 (§2)** | **Removed**: the contradiction above |

## Pre-mortem (assume the closeout run failed — why?)

| # | Likely cause | Blocked by |
|---|---|---|
| 1 | The run stalls on its first command or "fixes" a missing package by installing it | Owner install (H3-2); offline probes; installs named as forbidden; missing dependency = stop *(added in revision)* |
| 2 | P2-15 makes interview pages lose their data in production, and the run "fixes" it by exempting the datasets | Trap and two allowed routes in the plan; exemption explicitly banned; expected-set recorded before the change *(added in revision)* |
| 3 | The usage report leaks evidence or prompt text into a public CI log | Sentinel-string and fake-key assertions; output allow-list in the prompt |
| 4 | The run invents Gemini's request-ID header to make the line look complete | `unavailable` required; owner verifies (H3-6) |
| 5 | A workflow refactor drops a hardening property or renames the required check | Existing workflow test classes; new top-level-permissions assertion; `validate-and-build` named as untouchable |
| 6 | The branch-name change escapes the `ci.yml` path guard | Prefix kept and asserted (P2-18) |
| 7 | The run reports GitHub-side behaviour as PASS from YAML inspection | NOT RUN rule; dispatch is a stop condition; H3-5 lists the observations |
| 8 | The run edits `AGENTS.md` or `.claude/rules/` to match its changes | Both forbidden; proposed wording goes to `PROGRESS.md` (H3-12) |
| 9 | The run settles an owner question (`q-002`, model name, evidence branch) on its own | Decisions listed by ID in the prompt as not the run's *(added in revision)* |
| 10 | The run starts on the stale local `main` (`641b382`) or on the dirty tree | Ancestor check on `408b3cf` plus clean-tree check (H3-1) |
| 11 | Compaction mid-2D drops the no-network rule | Fresh conversation at 2C; the resume repeats the dependency and status checks; Run rules in `PROGRESS.md` |

## Limits

- The production-filter round trip was not re-run in this session (last PASS 2026-10-01).
- G15 (push collision on re-dispatch) is inferred from the workflow text, not executed.
- The provider facts are still KB §C (2026-10-01). No live provider behaviour was observed in this session.
- The plan's acceptance commands were written, not executed. The run executes them.
- `HANDOFF.md` is git-ignored and local. Its claims were cross-checked against tracked files and `gh` output
  where possible (environment, branches, run log). The way the owner obtained the local smoke test's token
  counts is not recorded anywhere and stays UNKNOWN.
