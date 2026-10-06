# DOCCAD Phase 2 closeout — Antigravity handoff pack

Prepared 2026-10-07. Everything needed to start the next unattended Antigravity 2.0 + Gemini 3.8 Flash run.
That run closes the gaps the first live provider calls exposed (Gemini, locally and in CI, 2026-10-06) and
hardens the generation workflow. It does **not** start Phase 3: in `docs/next-phase/03_NEXT_VERSION_PLAN.md`
§7, Phase 3 means external repository evidence. That phase starts with the owner decision NV-SUP-2, and the
owner has not made it. So this pack continues the Phase 2 numbering: work items P2-13…P2-20, checkpoints 2C and
2D, requirements NV-REQ-027…029, gaps G11…G22.

`docs/next-phase/` and `docs/phase-2/` stay the dated records of the previous runs and are not modified.

## Files

| File | What it is | Read it when |
|---|---|---|
| `01_STATE_AND_GAPS.md` | Baseline executed 2026-10-07; status of every known open item, with file:line; new gaps G11–G22; open owner decisions | You need the current state |
| `02_CLOSEOUT_PLAN.md` | §0 development bullets; run rules; owner checklist H3-1…H3-12; work items P2-13…P2-20 with acceptance commands; Blocked / owner-only table; acceptance matrix; risks | Planning or executing the run |
| `03_ANTIGRAVITY_PROMPT.txt` | The copy-ready prompt (checkpoints 2C and 2D) | Starting the run |
| `ANALYSIS.md` | How the prompt was derived; the fix for the Phase 2 prompt's `npm ci` contradiction; retained prohibitions; pre-mortem | Reviewing or changing the prompt |

Background that still applies: `docs/phase-2/01_STATE_AND_GAPS.md` (G1–G10), `docs/next-phase/02_RESEARCH_KB.md`
§C (provider request shapes) and §E (decision IDs), `docs/next-phase/04_ACCEPTANCE.md` (journeys J1–J8,
NV-REQ-001…023).

## Starting the run

1. Work through the owner checklist in `02_CLOSEOUT_PLAN.md` §3. At minimum:
   - H3-1: clean `main` that contains `408b3cf` (PR #12);
   - H3-2: `npm ci` and `pip install -r requirements.txt` already run, because the run is offline;
   - H3-3: guard protects `docs/phase-2-closeout/`.
2. Open this repository as the Antigravity workspace in the 2.0 app, select Gemini 3.8 Flash, and paste the
   whole of `03_ANTIGRAVITY_PROMPT.txt`.
3. At Checkpoint 2C the run commits and stops. Start a new conversation and paste the resume line it prints.
4. After 2D:
   - review the branch `phase-2-closeout`, push it and open the PR (CI must pass);
   - after the merge, run one `fixture` dispatch of `generate.yml` and record the GitHub-side observations
     listed in `PROGRESS.md`.

## Status of this pack

- Baseline executed 2026-10-07 on a scratch copy of `.github/` + `prototype/`: strict validate, detect, 155
  tests, `tsc` and the en + hu build all PASS (`01_STATE_AND_GAPS.md` §1). The production-filter round trip was
  not re-run.
- The plan's acceptance commands were written, not executed. The run executes them.
- No new web research, with one exception: an `npm view` of `@mermaid-js/mermaid-cli` for the E6 decision
  (`01_STATE_AND_GAPS.md` §3).
- The Antigravity guard (`.agents/hooks/doccad_guard.py:31-35`) does not yet protect this folder. That is
  owner action H3-3 (`.agents/` is outside this pack).
