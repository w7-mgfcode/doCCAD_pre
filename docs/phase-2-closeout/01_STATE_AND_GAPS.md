# 01 — State and gaps before the Phase 2 closeout run

Prepared 2026-10-07 in a Claude Code planning session (planning only: nothing outside
`docs/phase-2-closeout/` was changed). This file updates `docs/phase-2/01_STATE_AND_GAPS.md` (2026-10-06)
for what changed since then. Read that file for gaps G1–G10. Read `docs/next-phase/01_CONTEXT_MAP.md` for
vision, requirements, decisions and target architecture; none of these changed.

Labels follow the archive convention:
- **EXPLICIT**: read in the cited file or in command output.
- **INFERRED**: the reasoning is shown.
- **UNKNOWN**: no evidence.

## 1. Baseline — executed 2026-10-07 on a scratch copy (`.github/` + `prototype/`, `node_modules` symlinked)

The copy was taken from the working tree. That tree is local `main` `641b382` plus uncommitted edits to
`AGENTS.md` and `README.md` that match PR #12, so `prototype/` and `.github/` are identical to `origin/main`
`408b3cf` (§2).

| Check | Result | Key line |
|---|---|---|
| `DOCCAD_REQUIRE_JSONSCHEMA=1 python3 scripts/validate_docs.py` | PASS (exit 0) | `Validated 40 pages, 4 interview datasets, 25 provenance hashes.` |
| `python3 scripts/detect_changes.py --all` | PASS | `Manifest: .docs-manifest.json (44 entries)` / `stale generated: 0` |
| `python3 -m unittest discover tests` | PASS (exit 0) | `Ran 155 tests in 12.968s` / `OK` (41 `Test*` classes in `tests/test_doccad.py`) |
| `npx tsc --noEmit` | PASS (exit 0) | — |
| `npx docusaurus build` | PASS (exit 0) | `Generated static files in "build"` and `… "build/hu"` |
| `npm ls --depth=0` | PASS (exit 0) | installed `node_modules` matches the lockfile |
| `npm run build:production && npm run build:demo` | NOT RUN in this session | last PASS 2026-10-01 (`prototype/VALIDATION.md:35`) |

## 2. What happened since the Phase 2 pack (EXPLICIT)

- **Merged into `main`:**

  | PR | Content | Merge commit |
  |---|---|---|
  | #7 | Phase 2 run plus review fixes | `3b009a9` |
  | #8 | `AGENTS.md` and README after Phase 2 | `e1e4679` |
  | #9 | pipeline-owned `id`/`slug`, `TestLiveSmokeFindings` | `d841e4e` |
  | #10 | docs sync | `9c5de50` |
  | #11 | live CI run recorded | `641b382` |
  | #12 | the `generation` environment now exists | `408b3cf`, `origin/main` per `gh api …/commits?sha=main` |

  Local `main` reached `408b3cf` during this session (G21).
- **Live Gemini smoke test, owner-run, local** (`prototype/planning/PROGRESS.md:122`): both contracts passed;
  the interview contract needed one repair retry.
- **First live CI generation** (`prototype/planning/PROGRESS.md:124`; `prototype/VALIDATION.md:134-144`):
  run 37541030510 succeeded and pushed `docs-gen/generaterecruiterpage-architecture-system-overview`
  (`32a9cb7`). No PR was opened, because no App is configured.
- **`generation` environment.** It exists with deployment policy "protected branches only" and protection
  rule `branch_policy` only (no required reviewer). Its contents:
  - secret `GEMINI_API_KEY`;
  - variable `AI_MODEL_GEMINI`;
  - no repository-level Actions variables, so `DOCCAD_APP_CLIENT_ID` is not set.

  Source: `gh api repos/w7-mgfcode/doCCAD_pre/environments` and its `secrets` / `variables` listings (names
  only), 2026-10-07.
- **Open PRs:** none (`gh pr list`, 2026-10-07).

## 3. Status of the known open items (verified, not assumed)

| Item | Status 2026-10-07 | Evidence |
|---|---|---|
| E5: which providers go live, `AI_MODEL_*` values, spend caps | **Open.** Only Gemini is live. The repo caps are per run only (50000 tokens / 10 calls); no per-month cap is recorded. Provider-side spend caps (T7) are not recorded anywhere | `prototype/planning/PROGRESS.md:157`, `:141`; `prototype/ai.config.yaml:7-9`; `HANDOFF.md:69` |
| E7 / E9 | **E9 open** (archive `ai-models/` folder). "E7" means two things, see G9 below | `prototype/planning/PROGRESS.md:157`; `docs/next-phase/02_RESEARCH_KB.md:373,375` |
| DOCCAD GitHub App (repo "E8") | **Decided (GitHub App), not created.** `generate.yml` mints a token only when `vars.DOCCAD_APP_CLIENT_ID` is set (`.github/workflows/generate.yml:62-70`); no repository variable exists. The first real approval (J3) has not happened | `prototype/planning/PROGRESS.md:140,156`; `prototype/LIMITATIONS.md:93-94` |
| P1-08 Mermaid compile gate (E6) | **Blocked on E6.** New fact: `@mermaid-js/mermaid-cli` 11.17.0 exists and depends on `mermaid ^11.14.0`, which the site's pinned `mermaid` 11.17.2 satisfies. So the "matching 11.x CLI" path of D4 is available, and the NV-SUP-1 fallback is not needed. It is still a new devDependency and needs a Puppeteer browser download | `npm view @mermaid-js/mermaid-cli versions` / `@11 dependencies.mermaid` (2026-10-07); `prototype/package-lock.json` (`node_modules/mermaid` 11.17.2); `docs/next-phase/02_RESEARCH_KB.md:346`; `prototype/planning/PROGRESS.md:139,155` |
| Phase 3 of `03_NEXT_VERSION_PLAN.md` | **Not startable.** "Decision first: NV-SUP-2 … If rejected, Phase 3 is dropped." NV-SUP-2 (KB E8) is undecided | `docs/next-phase/03_NEXT_VERSION_PLAN.md:510-512`; `docs/next-phase/02_RESEARCH_KB.md:350,374`; `prototype/planning/PROGRESS.md:157` |
| G9: E7/E8 ID drift | **Open.** In the KB, **E7** is the GitHub App and **E8** is NV-SUP-2. The repository calls the App "E8" in 22 places (`AGENTS.md`, `README.md`, the prototype docs, `PROGRESS.md`, `generate.yml`). This pack names both by meaning and allocates new IDs from E11 | `docs/phase-2/01_STATE_AND_GAPS.md:49`; `docs/next-phase/02_RESEARCH_KB.md:373-374`; `grep -rnE "\bE7\b\|\bE8\b"` (22 lines) |
| The CI log prints no token usage or request ID | **Confirmed; it is a code gap, G11.** The usage line is a `logger.info` call (`prototype/ai/http.py:144-150`) on logger `doccad.ai.http` (`:17`). No handler or level is configured anywhere under `ai/` or `scripts/` (`grep -rn "basicConfig\|setLevel\|addHandler"` finds nothing), so Python drops INFO records. The log of run 37541030510 has no usage line | `gh run view 37541030510 --log`; `prototype/VALIDATION.md:142-143` |
| Gemini request ID blank | **UNKNOWN which field Gemini returns.** The helper reads only the headers `x-request-id`, `request-id` and `x-goog-request-id` (`prototype/ai/http.py:137-142`). KB §C records no Gemini request-ID field | `HANDOFF.md:73` |
| The Phase 2 prompt's `npm ci` vs no-network rule | **Confirmed contradiction.** `docs/phase-2/03_ANTIGRAVITY_PROMPT.txt:43` says "run npm ci", while `:29` says "No test, script or step in this run may contact … any non-loopback address", and `:67` makes "any network access beyond 127.0.0.1" a stop condition. The Antigravity default sandbox has no network anyway (`docs/next-phase/02_RESEARCH_KB.md:41`, A2.4). Fixed in this pack (`ANALYSIS.md`) | `HANDOFF.md:74` |
| `q-002` re-seed question | **Open, needs an owner choice (E11).** Phase 1 regenerated `q-002` by script as a draft (`prototype/planning/PROGRESS.md:109`). The Phase 2 re-seed replaced it with a seeded page: `approval_status: approved-for-demo`, `provider: fixture`, `contract_version: 4`, `prompt_version: question-page.v4` (`prototype/docs/generated/questions/q-002-drift-detection.mdx`, frontmatter). README Known issues still tells readers to regenerate it from the original question | `HANDOFF.md:30,70`; `prototype/README.md:289` |
| The `generation` environment's branch policy is untested | **Open (owner).** The policy is set (§2), but no dispatch from an unprotected branch has been tried. `origin/next-version` (`228a225`) predates the `provider` input, so it cannot serve as the test branch. A throwaway branch from `main` is needed | `prototype/VALIDATION.md:143-144`; `HANDOFF.md:21` |
| Draft branch `docs-gen/generaterecruiterpage-architecture-system-overview` | **Exists on origin, no PR.** It is 1 commit ahead and 4 behind `main`, and adds one file: `prototype/docs/generated/recruiter/architecture-system-overview.mdx` (+70 lines). Frontmatter: `provider: gemini`, the returned model string, `generation_mode: production`, `approval_status: draft`, **no `visibility` field** (G14) | `gh api …/compare/main...docs-gen/…`; `git show origin/docs-gen/…:prototype/docs/generated/recruiter/architecture-system-overview.mdx` |

## 4. New gaps

Found in this session by reading code and command output. Each gap becomes a work item in `02_CLOSEOUT_PLAN.md`
or a Blocked row.

| # | Gap | Evidence | Consequence |
|---|---|---|---|
| G11 | Live runs never show usage or request IDs, and CI writes no run report | `prototype/ai/http.py:17,144-150` (INFO, no handler configured); no `GITHUB_STEP_SUMMARY` in any workflow (`grep`); P1-06 specified a run report with "evidence files, gates, provider, model, usage" (`docs/next-phase/03_NEXT_VERSION_PLAN.md:405-406`); J3 step 2 (`docs/next-phase/04_ACCEPTANCE.md:80`); roadmap M3.1 "run-report archive" (`docs/primary-inputs/08_TASKS/future/implementation_roadmap.csv:13`) | EXPLICIT. Live cost is not observable in CI (`prototype/planning/PROGRESS.md:124`, "token usage not logged in CI"). How the owner obtained the token counts in the local smoke row (`PROGRESS.md:122`) is UNKNOWN |
| G12 | The provider-chain label lies when `--provider` is used | `prototype/scripts/generate_page.py:206` always prints `Provider chain (from ai.config.yaml): …`. The CI log shows `Provider chain (from ai.config.yaml): gemini`, although the chain came from `--provider gemini` | EXPLICIT. A misleading audit line in the one place a reviewer reads |
| G13 | Request ID is blank for Gemini | `prototype/ai/http.py:137-142` | UNKNOWN which header or body field Gemini uses. The run must not guess: it prints `unavailable` and the owner reads the field name at the next live call (H3-6) |
| G14 | **Absent `visibility` means private in the schema but public in the code** | `prototype/schemas/document.schema.json:25-29` (`"default": "private"`, "Default private when omitted"); `prototype/scripts/build_filter.py:87-88,117-118` (`is_private = (visibility == "private")`, so absent counts as public); `scripts/generate_page.py` and `scripts/generate_question.py` read evidence visibility (`:198`, `:249`) but never stamp it on output; `scripts/seed_generated_views.py:45,207,280` stamps `public`. The live draft page on the docs-gen branch has no `visibility`. The four `docs/generated/interview/*.interview.json` datasets have no `visibility` either | EXPLICIT. T12 says absent means private (`docs/next-phase/01_CONTEXT_MAP.md:141-144`; NV-REQ-008, `docs/next-phase/04_ACCEPTANCE.md:47`). No leak today: every `.md`/`.mdx` under `docs/` declares `visibility` (`grep -L` empty), and nothing is `private`. But the first live page that is approved would publish by accident of code, not by classification. **Trap:** a naive fix stashes the four JSON datasets in production |
| G15 | A second dispatch with the same contract and target cannot push | `generate.yml:165-167,368-370` derive the branch only from contract and target; `:183,193` and `:386,396` run `git checkout -b` and `git push origin <branch>`; that branch already exists on origin (`32a9cb7`) | INFERRED (not executed): the push is rejected as non-fast-forward, so the same dispatch fails until the branch is deleted |
| G16 | `generate.yml` grants write at the top level | `generate.yml:46-47` `permissions: contents: write`; `.github/workflows/drift.yml:10` top level includes `issues: write`. `ci.yml` and `publish.yml` are `contents: read`. The rule "Top level stays read-only; a job raises only what it needs" is in `.claude/rules/github-workflows.md:26`; archive T8 "top-level `contents: read`" in `docs/next-phase/01_CONTEXT_MAP.md:139-140` | EXPLICIT. `TestWorkflowSecurityInvariants` checks only that a top-level block exists, so this is not caught |
| G17 | `generate.yml` duplicates its inline Python, and the copies have drifted | input validation and dispatch `:95-145` vs `:286-348`; push `:150-202` vs `:353-405`; PR `:204-242` vs `:407-445`. The provider allowlist check exists only in the live job (`:325-328`). The header comment still says "Generates views with the deterministic fixture provider" (`:2`) | EXPLICIT. A security fix applied to one job can miss the other |
| G18 | G7 is only half closed | `prototype/ai/router.py:211-221`: `chain_for` re-raises `MissingKeyError` / `MissingModelError` but still swallows every other instantiation error (`except Exception: pass`). Its caller is `providers_from_config` (`:284`). `run_with_fallback` is correct now (`:261-275`, only `ProviderTransportError` falls through) | EXPLICIT. The agent-layer note `.claude/rules/prototype-code.md:47-51` ("Known debt") is half stale. That file is the owner's to update; it is outside this pack and the run |
| G19 | Stale statements in tracked docs | see the list below | EXPLICIT. Small; P2-20 fixes the prototype files |
| G20 | The Phase 2 prompt contradicts itself on network use (`npm ci`) | §3 above | EXPLICIT. Fixed by moving installs to the owner (H3-2) |
| G21 | The run must start from a clean, current `main` | At the start of this session: `git status` showed ` M AGENTS.md`, ` M README.md` (edits made outside this session, matching PR #12), and local `main` `641b382` was behind `origin/main` `408b3cf`. **By the end of the session the tree was clean and local `main` was `408b3cf`**, changed by another session. Only `docs/phase-2-closeout/` is untracked | EXPLICIT. Resolved for now, but the state moves under concurrent sessions, so the run's start check stays: clean tree, `408b3cf` an ancestor of HEAD (H3-1). The new pack itself must be committed first, or the tree is not clean |
| G22 | The guard does not protect this pack | `.agents/hooks/doccad_guard.py:31-35` (`PROTECTED_DIRS` lists `docs/primary-inputs`, `docs/next-phase`, `docs/phase-2`, `docs/prototype-planning`); the PreInvocation text at `:124-125` names the same set | EXPLICIT. Owner action H3-3 (`.agents/` is outside this pack) |

**G19 — stale statements:**

`prototype/README.md`
- `:31` lists "Real approval via GitHub PRs … (Phase 1 P1-05)" as not yet done. The code is done (P1-05 PASS); only the App is missing.
- `:48` says the quick start prints "37 provenance hashes". It prints 25.
- `:162` says "Live runs currently fail; see Known issues".
- `:183` says live generation is "not yet exercised".
- `:290` says `--range` needs git history "until the repository has remote commits". The repository has remote commits now.

`prototype/LIMITATIONS.md`
- `:3` is dated 2026-10-06.
- `:86` says "live dispatch on GitHub is NOT RUN". It ran 2026-10-06.
- `:112` (REQ-003) says "PR-based flows arrive in Phase 1".
- `:117` (REQ-008) says "Automated GitHub ingestion (P1-06) not built".

`prototype/VALIDATION.md`
- `:6` names branch `phase-2-live-ai` as the execution context.
- `:153` shows a model-like value `llama3.1:...` where the convention is `<model-id>`.

`prototype/planning/PROGRESS.md`
- `:237` says "88/88" for P1-09; the evidence row `:107` says 91.
- §2 (`:255-270`) is a 2026-10-01 snapshot (37 hashes, 91 tests) and is not marked historical.

Outside the run's scope:
- `AGENTS.md:123` cites `scripts/generate_page.py:158` for `--provider`. The flag is at `:165` today, and P2-14 will move it again. The owner updates `AGENTS.md`.

## 5. Owner decisions still open

| Decision (by meaning; IDs as used where) | Blocks |
|---|---|
| **E5**: next live providers, their `AI_MODEL_*` values, per-run and per-month spend caps, provider-side caps (T7) | Remaining P2-08 rows (Anthropic, OpenAI, local) |
| **GitHub App**: KB **E7** = repo "**E8**". Decided 2026-10-01; the owner creates it | The first bot PR and the first real approval (J3, NV-REQ-016/017) |
| **E6**: approve `@mermaid-js/mermaid-cli` 11.17.x as a devDependency (plus its browser download in CI)? | P1-08, NV-REQ-018 |
| **NV-SUP-2** (KB **E8**): allow pinned external evidence? Which licenses? | Phase 3 (§7 of the 2026-10-01 plan) |
| **E9**: archive `docs/primary-inputs/02_RESEARCH/ai-models/` | Archive task, never this run |
| **G9 wording**: rename the repository's App "E8" to KB E7, or keep it and record the alias | Wording only; until then this pack writes "GitHub App (KB E7 = repo E8)" |
| **E11 (new)**: `q-002`. Keep the seeded `approved-for-demo` page, or restore a script-generated draft (`generate_question.py --question "How does DOCCAD detect drift?" --persist`)? | README Known issues wording; demo content |
| **E12 (new)**: keep `gemini-3.1-flash-lite` named in `README.md` / `PROGRESS.md` as a recorded result, or write `AI_MODEL_GEMINI` | Doc wording (`HANDOFF.md:71`) |
| **E13 (new)**: the evidence branch `docs-gen/generaterecruiterpage-architecture-system-overview`. Keep it, delete it, or open its PR by hand (admin bypass). Its page lacks `visibility` (G14) and would need regenerating after P2-15 | G15 (a re-dispatch with the same inputs fails while it exists, until P2-18 lands) |
| Optional: add a required reviewer to the `generation` environment | Defence in depth for live CI spend |
| Record only: the MkDocs fallback's dated exit decision is due before **2026-11-05** (`docs/next-phase/02_RESEARCH_KB.md:356`, D14; `docs/primary-inputs/12_FUTURE/backlog/BACKLOG.md:10-11`). No action unless DEC-001 is revisited | — |

KB §E (`docs/next-phase/02_RESEARCH_KB.md:365-376`) uses E1–E10. New decisions start at E11, so no ID is
recycled.
