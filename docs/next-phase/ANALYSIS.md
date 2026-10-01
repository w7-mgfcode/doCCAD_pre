# How the next-phase Antigravity prompt was derived

Prepared 2026-10-01 in a Claude Code planning session (plan only — nothing under `prototype/`,
`docs/primary-inputs/` or `docs/prototype-planning/` was changed). Companion to
`docs/prototype-planning/ANALYSIS.md`, which explains the first run's prompt.

## Method

1. Context built in layers (vision → requirements → decisions → target architecture → prototype →
   verification evidence → gaps), recorded in `01_CONTEXT_MAP.md`. The decision and architecture documents
   (ADRs, spine, solution, security, content, AI and automation architecture, roadmap, decision matrix, the
   first Antigravity prompt) were read directly; the large archive sections (02, 07, 09, 10, 11, 03 and the
   control registers) were swept by two read-only analysis agents, and every prototype defect they reported
   was re-verified by command before entering the plan (one claimed figure — "about 46 tests" — was wrong;
   the executed suite has 33).
2. Baseline executed on a scratch copy of `prototype/` (validate, detect, tests, typecheck, en + hu build,
   plus probes of live generation and the production filter) — `01_CONTEXT_MAP.md` §6.1.
3. Web research by exactly three parallel agents (A Antigravity + Gemini 3.8 Flash; B docs-as-code
   delivery; C governed live AI), every finding with URL, access date and VERIFIED/UNVERIFIED —
   `02_RESEARCH_KB.md`.
4. Conflicts between research, archive and prototype resolved explicitly (`02_RESEARCH_KB.md` §D); owner
   decisions separated from run decisions (§E).
5. Plan and acceptance written against the archive's own roadmap (`implementation_roadmap.csv`), then the
   prompt, then a pre-mortem that revised the prompt.

## Framework

RISEN (Role, Instructions, Steps, End goal, Narrowing), the same framework as the first run's prompt, so
the two runs read alike. Section headers are omitted in the emitted prompt; the structure is: role and
context → section 0 orientation → section 1 run rules → sections 2–4 phases with checkpoints → section 5
stop conditions → section 6 end goal and final report.

The main design change from the first prompt: the first prompt described *what to build*; this prompt
spends most of its words on *how to prove it was built*, because the first run's failures were evidence
failures, not capability failures (a documented-but-unimplemented citation check, four uncovered required
boundaries, progress ticked without evidence — `prototype/planning/PROGRESS.md` before 2026-09-30, and
`01_CONTEXT_MAP.md` §6.1).

## Which finding shaped which instruction

| Prompt instruction | Finding | Source |
|---|---|---|
| Read `AGENTS.md` first and treat it as authority; read `.claude/rules/` by hand; no `GEMINI.md` | Antigravity reads `AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md` — not `.claude/rules/` | `02_RESEARCH_KB.md` A3.1, A3.2; D12 |
| Restate the run rules at the top of `PROGRESS.md` and re-read them before each item | Compaction drops side constraints, including verification steps; no documented compaction behaviour | A6.1, A6.2 |
| Evidence log (command, exit code, key line, date); no item ticked without it | First run's claimed-but-unrun checks; Google: local verification is "the single most effective way" | A8.1, A8.2; `01_CONTEXT_MAP.md` §6.1 |
| Verify every edit with `git diff --stat` | Gemini 3.8 Flash may emit a raw tool-call string instead of executing it | A5.6 |
| Two attempts, then record and move on; inspect once | Tool-use loops burn quota; staff advise bounded prompts and fresh threads | A5.5 |
| Phase checkpoint → commit locally → stop → fresh conversation with a resume line | Fresh conversations recommended; resume from files, not chat history | A5.5, A6.3 |
| One branch, one agent on the tree | Parallel agents in local mode edit the same files; scripts rewrite shared state | A2.8 |
| Read installed `node_modules` instead of memory; use pinned versions | Model knowledge cutoff January 2025 for some domains | A5.2 |
| `/browser` against localhost in the 2.0 app; NOT RUN if unavailable | `/browser` is on demand, IDE/app only, localhost allowlisted | A4.1–A4.3 |
| Stop conditions for push, settings, secrets, keys, dependencies, names | Human-only actions; default sandbox blocks network | A2.4, A7.3 |
| Node ≥24.14 | Node 20 EOL; ADR-002 requires ≥24.14 | B2; D2 |
| Action majors from §B3, pinned by full SHA; never invent a SHA | Current majors; SHA pinning is the only immutable reference | B3.2, B5.7 |
| No `pull_request_target`; no `${{ github.event.* }}` in `run:` | GitHub secure-use guidance; archive T8 | B5.7, C6.2 |
| Never guess repository name or domain | `baseUrl`/`url` depend on it; Pages on Free needs a public repo | B3.5, B3.6 |
| Approval record only after owner confirms semantics | Authors cannot approve their own PRs; `approved` has no producer | B4.3; D5, D6 |
| Provider-facing schemas; repo schemas remain the gate | Every provider supports only a JSON-Schema subset | C1.3, C1.6, C1.9, C1.13 |
| Native structured-output fields per adapter | Current request shapes | C1.1, C1.4, C1.8, C1.11 |
| Opt-in sampling parameters | Non-default `temperature` returns 400 on newer Anthropic models | C2.2 |
| Retry helper honouring `Retry-After`; fail fast on spend-cap 429 | Provider rate-limit semantics | C5.1–C5.4 |
| No live provider call in the run; owner executes the smoke | Keys never in the run; spend caps are the blast-radius control | C6.3; archive T7 |
| Grounding gate and injection fixtures | Citation support is often incomplete; delimiters are no guarantee | C3.1, C4.1–C4.3 |
| Private content via `visibility`, absent = private | Archive T12 design | D7 |
| MDX restriction gate; components without imports | Archive T3; prototype pages import today | D13 |

## Every prohibition of the first prompt, retained

| First prompt (`docs/prototype-planning/ANTIGRAVITY_PROMPT.txt`) | Where it lives now |
|---|---|
| Coding model is separate; never label fixture output as Gemini or live | Opening paragraph |
| Work without API keys, live calls, GitHub credentials, deployed backend | Section 1 (no keys), section 4 (stub server only), section 5 |
| Archive is immutable; never mutate it for demonstrations | Section 0 |
| Do not initialize Git, commit, push, publish, deploy | Narrowed deliberately: local commits on `next-version` are allowed at checkpoints (owner request through this prompt); push, PRs, remotes, publish and deploy remain forbidden — section 1 |
| Do not execute historical prompts | Section 0 |
| Report a missing source instead of inventing requirements | Section 1 (missing cited files) |
| Record choices as proposed defaults, not historical decisions | Section 1 |
| No runtime datastore, vector DB, agent framework, microservices, swarms | Section 1 |
| No invented achievements, adoption, metrics, user counts, technologies, guarantees | Section 1 |
| Browser state disposable; browser must not imply files changed | Section 1 |
| No decorative buttons, dead routes, fake successes | Section 1 |
| Simulated approval never sets production approval | Section 1 |
| Path containment incl. traversal and symlink escapes | Section 1 |
| Delimiters alone do not guarantee injection resistance | Section 1 |
| Private → local, no cloud fallback, incl. unspecified visibility; local generation does not make private content publishable | Section 1 |
| Never read, print, request or transmit real API keys | Section 1 |
| Do not claim arbitrary-question AI, live GitHub execution or provider compatibility from fixture tests | Section 1 |
| PASS / FAIL / NOT RUN; historical results are context | Sections 2, 6 |
| Do not weaken a failing gate | Section 1 |
| No private reasoning traces; use only available tools; never invent tool output | Section 1 |
| Do not report complete while checks fail or are unexecuted | Section 6 |

## Pre-mortem (assume the run failed — why?)

| # | Likely cause of failure | Evidence it is likely | Blocked by (prompt / plan) |
|---|---|---|---|
| 1 | Checks claimed but never run or implemented | First run (validate_docs check 8; four uncovered boundaries); A5.6 tool-call bug | Evidence log; named test classes with failing fixtures; `git diff` after edits; ban on documenting unimplemented checks |
| 2 | Rules lost to compaction mid-phase | A6.2 | Run-rules section in PROGRESS.md re-read per item; AGENTS.md as authority; fresh conversation per phase *(added in revision)* |
| 3 | Gate weakened to get green (test skipped, schema loosened) | Common agent failure; first prompt's explicit rule | Explicit ban list *(strengthened in revision)* |
| 4 | Run stalls on `npm ci` / permission prompts | A2.4 | Owner checklist H-3; stop conditions record BLOCKED and continue |
| 5 | Quota burned by loops | A5.5 | Two-attempt bound; inspect once; Tried-and-failed log |
| 6 | State corrupted by running writers in place | AGENTS.md; test suite stashes `docs/generated/` | Scratch-copy rule for generation acceptance; `build:demo` recovery |
| 7 | Invented repository name, SHAs, model IDs or keys | Model hallucination (A5.2) | Explicit stop conditions; never write a SHA it did not read |
| 8 | Scope creep (Phase 3, new deps, Playwright) | Long autonomous runs | Phase 3 out of scope; dependency approval rule |
| 9 | Public pages vanish after the `visibility` migration | Default-private design (D7) | Expected-set test in P0-10 |
| 10 | Plan item wrong and silently skipped or forced | Plan written without executing the changes | "Plan, not truth" rule *(added in revision)* |
| 11 | Heavy, unreviewed edits to human-owned canonical pages | P0-10, P0-13 touch `docs/source/` | Minimal-change rule and changed-file list *(added in revision)* |
| 12 | Browser checks marked PASS without browser access | First run had no browser evidence | NOT RUN rule; screenshot paths must exist |

## Limits of this analysis

- Research facts were read through a summarizing fetch tool; exact values (versions, limits, header names)
  must be re-read at the source before they are relied on.
- `concept.mmd` was not compiled (no Mermaid CLI in this environment; the installed Mermaid cannot parse
  without a browser DOM) — NOT RUN.
- The plan's acceptance commands were written, not executed; the run executes them.
