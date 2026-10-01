# DOCCAD next phase — handoff pack

Prepared 2026-10-01. Everything needed to start the next long Antigravity 2.0 + Gemini 3.8 Flash run that
turns the prototype (`prototype/`) into a usable, deployable, governed DOCCAD. This folder is a planning
deliverable outside the historical archive, like `docs/prototype-planning/`; it changes nothing else.

## Files

| File | What it is | Read it when |
|---|---|---|
| `01_CONTEXT_MAP.md` | Layered context: vision → requirements → decisions → target architecture → prototype → verified baseline (2026-10-01) → gaps; requirement trace; proven / designed / vision table | You need the current state, with evidence |
| `02_RESEARCH_KB.md` | Web research of 2026-10-01 (A Antigravity + Gemini 3.8 Flash, B docs-as-code delivery, C governed live AI), every finding cited and dated; D conflicts with proposed resolutions; E open questions | You need an external fact or a decision rationale |
| `03_NEXT_VERSION_PLAN.md` | HU executive summary; phases 0–3 with work items, acceptance commands, traces, risks and human actions; owner pre-run checklist | Planning or executing the run |
| `04_ACCEPTANCE.md` | REQ-001…016 and NV-REQ-001…023 mapped to journeys J1–J8 and verification evidence | Checking whether the run succeeded |
| `05_ANTIGRAVITY_PROMPT.txt` | The copy-ready prompt for the run (Phases 0–2) | Starting the run |
| `ANALYSIS.md` | How the prompt was derived; finding → instruction map; retained prohibitions; pre-mortem | Reviewing or changing the prompt |
| `concept.mmd` | Target architecture and phases (Mermaid) | Orientation |

## Starting the run

1. Work through the owner checklist in `03_NEXT_VERSION_PLAN.md` §3 — at minimum H-1 (commit pending
   changes), H-3 (Antigravity permissions), H-5 (use the 2.0 app); answer E1/E2 in `02_RESEARCH_KB.md` §E
   before Phase 1.
2. Open this repository as the Antigravity workspace, select Gemini 3.8 Flash, and paste the whole of
   `05_ANTIGRAVITY_PROMPT.txt`.
3. At each phase checkpoint the run stops; start a new conversation and paste the resume line it prints.

## Status of this pack

- Baseline checks were executed on a scratch copy (`01_CONTEXT_MAP.md` §6.1). The plan's acceptance
  commands were written, not executed — the run executes them.
- Research facts are dated 2026-10-01 and were read through a summarizing fetch tool; re-read the source
  before relying on an exact value.
- No archive ID was allocated. New identifiers use `NV-` prefixes (NV-REQ, NV-SUP) and plan item codes
  (P0-…, P1-…, P2-…, H-…).
