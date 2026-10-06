# DOCCAD Phase 2 — Antigravity handoff pack

Prepared 2026-10-06. Everything needed to start the next long Antigravity 2.0 + Gemini 3.8 Flash run. That
run adds governed live AI generation to the prototype behind its deterministic fixture default (Phase 2 of
`docs/next-phase/03_NEXT_VERSION_PLAN.md`). Phases 0 and 1 are complete (`prototype/planning/PROGRESS.md`).
`docs/next-phase/` stays the dated record of the previous run and is not modified.

## Files

| File | What it is | Read it when |
|---|---|---|
| `01_STATE_AND_GAPS.md` | Verified baseline (2026-10-06), what Phases 0–1 delivered, gaps G1–G10 with file:line, open owner decisions | You need the current state |
| `02_PHASE2_PLAN.md` | §0 development bullets; work items P2-00…P2-12 with acceptance commands; owner checklist H2-1…H2-6; acceptance matrix (NV-REQ-024…026 new); risks | Planning or executing the run |
| `03_ANTIGRAVITY_PROMPT.txt` | The copy-ready prompt (checkpoints 2A and 2B) | Starting the run |
| `ANALYSIS.md` | How the prompt was derived, design choices, retained prohibitions, pre-mortem | Reviewing or changing the prompt |

Background that still applies: `docs/next-phase/02_RESEARCH_KB.md` §C (provider request shapes and limits),
`docs/next-phase/04_ACCEPTANCE.md` (journeys J1–J8, NV-REQ-001…023).

## Starting the run

1. Owner checklist `02_PHASE2_PLAN.md` §3: at minimum H2-1 (merge `close-open-items`, check out an
   up-to-date `main`) and H2-2 (guard self-test passes).
2. Open this repository as the Antigravity workspace in the 2.0 app, select Gemini 3.8 Flash, and paste
   the whole of `03_ANTIGRAVITY_PROMPT.txt`.
3. At Checkpoint 2A the run commits and stops. Start a new conversation and paste the resume line it
   prints.
4. After 2B: review the branch `phase-2-live-ai`, push it, open the PR (CI must pass), then run the live
   smoke commands it wrote into `prototype/VALIDATION.md` (needs E5: key, `AI_MODEL_*`, spend cap).

## Status of this pack

- Baseline executed 2026-10-06 on a scratch copy: validate, detect, 95 tests. Typecheck and build NOT RUN.
- The acceptance commands were written, not executed. The run executes them.
- No new web research; provider facts are KB §C (2026-10-01).
