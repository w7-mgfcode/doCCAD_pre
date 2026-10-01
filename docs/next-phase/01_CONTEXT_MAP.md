# 01 — Context Map: from vision to verified prototype

Prepared 2026-10-01 for the next DOCCAD development phase. This is a planning deliverable outside the
historical archive (like `docs/prototype-planning/`); it changes nothing in `docs/primary-inputs/` or
`prototype/`.

Labels follow the archive convention (`docs/primary-inputs/01_PROJECT_KNOWLEDGE/OPEN_QUESTIONS.md`):
**EXPLICIT** = stated in the cited source; **INFERRED** = reasoning from cited sources, shown inline;
**UNKNOWN** = no evidence. Paths are repository-relative. `PI/` abbreviates `docs/primary-inputs/`.

Layers, in the order context was built: 1 Vision → 2 Requirements → 3 Decisions → 4 Target architecture →
5 Prototype implementation → 6 Verification evidence → 7 Gaps. Section 8 traces every requirement through
all layers; section 9 separates proven, designed-but-unproven, and vision-only.

---

## 1. Vision

- EXPLICIT: DOCCAD is a GitHub-based documentation ecosystem where documentation, architecture, Mermaid
  diagrams and processes live in a version-controlled repository, and AI models (Gemini, Claude, OpenAI,
  local) generate user manuals, architecture and development manuals, SOPs, security reviews, recruiter
  pages, interview preparation and special-question pages (`PI/01_PROJECT_KNOWLEDGE/VISION.md:7-12`).
- EXPLICIT: conceptual flows, verbatim from the mission: *Canonical GitHub Documentation → Project
  Knowledge → AI Processing → {User Docs | Technical Architecture | Recruiter View} → Interview Prep*, and
  *User Question → Retrieve → Analyze → Generate Dedicated Page → Optionally Persist*
  (`PI/01_PROJECT_KNOWLEDGE/VISION.md:14-20`).
- EXPLICIT: the vision explicitly lists what did **not** exist at archive time: production deployment, live
  AI generation with real keys, a real GitHub repository with CI running, HU content rollout
  (`PI/01_PROJECT_KNOWLEDGE/VISION.md:22-26`).
- EXPLICIT: nine architectural principles, P1 files over services … P9 one engineer can operate, debug and
  evolve the whole system (`PI/04_ARCHITECTURE/SAD/solution_architecture.md:59-64`).
- EXPLICIT non-goals: runtime AI chat, enterprise SSO, **multi-repo knowledge federation**, WYSIWYG
  editing, real-time collaboration (`PI/04_ARCHITECTURE/SAD/solution_architecture.md:53-57`).
  INFERRED: Phase 3 of the next-version plan (external repository ingestion) touches the "multi-repo
  federation" non-goal. It must be framed as *pinned external evidence* read into one canonical repo, not
  federation — or proposed as a superseding decision (see `02_RESEARCH_KB.md` §Conflicts).

## 2. Requirements

Sixteen requirements, all EXPLICIT from PROMPT-001 (`PI/01_PROJECT_KNOWLEDGE/REQUIREMENTS.md:7-22`):

| ID | Requirement (short) |
|---|---|
| REQ-001 | Six-platform research, equal depth |
| REQ-002 | Weighted 11-criterion decision model |
| REQ-003 | Git/GitHub single source of truth; files over databases |
| REQ-004 | Structural canonical/generated separation; no silent promotion |
| REQ-005 | Provider abstraction: Claude, Gemini, OpenAI, local; no deep coupling |
| REQ-006 | Docs readable with every AI provider unavailable |
| REQ-007 | Minimum sufficient retrieval; vector DB only past a decision boundary |
| REQ-008 | Automated GitHub ingestion, incremental regeneration |
| REQ-009 | Provenance contract on all documents; deterministic-first drift detection |
| REQ-010 | Evidence-grounded recruiter views (30s / 2min / deep); no fabrication |
| REQ-011 | Interview prep as reusable per-page component, build-time |
| REQ-012 | Special-question → governed dedicated-page workflow |
| REQ-013 | Bilingual EN/HU; HU executive summaries in key documents |
| REQ-014 | Anti-overengineering; one-engineer operability |
| REQ-015 | Runnable PoC, five scenarios, truthful executed-vs-not validation |
| REQ-016 | Security architecture for AI-specific threats and trust boundaries |

Constraints (EXPLICIT, `PI/01_PROJECT_KNOWLEDGE/CONSTRAINTS.md:3-13`): GitHub is system of record;
static/build-time generation; AI never in the read path; files over databases; manifests over graph DBs;
built-in search first; no Kubernetes, microservices, vector DB or multi-agent swarm without justification;
every component names the simpler alternative it beat; MVP operable by one engineer; never commit keys;
no fabrication in derived content; EN/HU on key deliverables.

## 3. Decisions

Ten recorded decisions (`PI/01_PROJECT_KNOWLEDGE/DECISIONS.md:7-16`), each backed by an ADR in
`PI/04_ARCHITECTURE/ADR/` (all "Accepted · 2026-08-12"):

| DEC | ADR | Decision | Binding rule for the next phase |
|---|---|---|---|
| DEC-001 | decision_matrix | Docusaurus 3.x (88.6/100); MkDocs fallback with dated exit | Stay on Docusaurus 3.x |
| DEC-002 | ADR-001 | One GitHub repo, no runtime datastore | Everything is a versioned file |
| DEC-003 | ADR-002 | Docusaurus with `future.faster`, multi-instance docs; **Node ≥24.14** + React 19 (`adr-002-docusaurus-framework.md:18`) | Prototype's `engines: node >=20` diverges (see §7) |
| DEC-004 | ADR-003 | Two plugin instances; **CI fails any generation PR touching paths outside `docs/generated/**`**; canonical never links to `/views` except one Views index (`adr-003…:10-14`) | Phase 1 CI gate |
| DEC-005 | ADR-004 | Thin provider Protocol, 4 adapters, router; privacy hard-fail; **one repair retry max; no agent loops** (`adr-004…:11-13`) | Phase 2 live generation |
| DEC-006 | ADR-005 | Generated content only via PRs on `docs-gen/*`; branch protection requires human approval; bot cannot self-approve; unmerged drafts expire after 30 days (`adr-005…:10-13`) | Phase 1 real approval |
| DEC-007 | ADR-006 | Level-1 retrieval; L2 only past ~1,500 pages or documented grounding failures | Keep L1 |
| DEC-008 | ADR-007 | Mermaid-as-code; **CI compiles every diagram with mermaid-cli**; compile failure blocks merge (`adr-007…:10-13`) | Phase 1 CI gate (needs a new dev dependency — owner approval) |
| DEC-009 | ADR-008 | AI only in CI/CLI; static site | Unchanged |
| DEC-010 | ADR-009 | GitHub Pages via Actions + **OIDC** (Mode B); Modes A/C on the same artifact (`adr-009…:10-13`) | Phase 1 deployment |

Fifteen architecture decisions AD-1…AD-15 bind the whole system
(`PI/04_ARCHITECTURE/SAD/ARCHITECTURE-SPINE.md:25-96`). The ones the next phase must not weaken:
AD-3 (two planes), AD-4 (AI only in CI/CLI), AD-5 (thin router, model names only in config),
AD-6 (task contracts), AD-8 (provenance frontmatter + hashes), AD-9 (PR-only persistence, no auto-merge),
AD-10 (deterministic-first validation: lint → schema → links → Mermaid compile → build; AI checks advisory
only), AD-15 (untrusted-content boundary; output parsed against schema; external-link allowlist; secrets
never in context). Spine seed: Python 3.11+, **stdlib + PyYAML + provider SDK-free HTTP**
(`ARCHITECTURE-SPINE.md:106-110`).

Rejected alternatives that the plan must not reintroduce (EXPLICIT,
`PI/01_PROJECT_KNOWLEDGE/REJECTED_ALTERNATIVES.md:10-17`): LangChain/LiteLLM-style frameworks, autonomous
multi-agent orchestration, auto-merge or direct commit of generated content, vector DB at MVP,
full-corpus-in-context, runtime AI, own server/Kubernetes, model self-reported confidence as provenance,
blocking merges on docs-drift suspicion.

## 4. Target architecture (designed, 2026-08-12)

The archive specifies the production system in far more detail than the prototype implements. The
next-phase plan should implement *these* specifications rather than invent new ones.

**Roadmap already exists.** `PI/08_TASKS/future/implementation_roadmap.csv` defines 16 milestones with
exit criteria — MVP M1.1–M1.6, SCALE M2.1–M2.5, HARDEN M3.1–M3.4 — all FUTURE
(`PI/08_TASKS/TASK_REGISTER.md:23-24`). INFERRED: the prototype covers the *demonstrable* part of
M1.1, M1.3, M1.4 (dry-run), M1.5 (fixture only), M2.2 (drift, locally) and M2.3 (workbench, simulated),
but none of their GitHub-hosted exit criteria (branch protection, CI, bot PRs, Pages).

**CI/CD** (`PI/05_DOCUMENTATION_DESIGN/documentation-process/automation_architecture.md:43-62`):
- `docs-validate.yml` on every PR, read-only token: markdownlint → frontmatter schema → internal links
  (via build) → Mermaid compile → manifest + impact annotations → gitleaks + pinned-action audit → build
  (both instances, both locales) → preview artifact.
- `docs-generate.yml` on `workflow_dispatch` / issue form / stale trigger, provider secrets only in a
  protected environment; never `pull_request_target`; never on fork code.
- `docs-publish.yml` on push to `main`: build → Pages (OIDC) → smoke test (HTTP 200 on `/`, `/docs`,
  `/views`, search index present).
- Weekly: hash sweep → single "stale views" issue; external link check (non-blocking).
- Full-corpus regeneration only via `workflow_dispatch` with `confirm: all` (`…:23-25`).

**Secrets and permissions** (`PI/04_ARCHITECTURE/SAD/security_architecture.md:283-341`): the complete
secret list is three provider keys in a `generation` environment restricted to `main`, plus the ephemeral
`GITHUB_TOKEN`. Exact `permissions:` blocks are specified per workflow. OIDC applies to Pages only —
the document states the model providers use static keys and that claiming otherwise "would be inventing
capability" (`…:296-303`). Note the archive names the Gemini secret `GOOGLE_API_KEY` (`…:290`) while the
prototype uses `GEMINI_API_KEY` (`prototype/.env.example`, `prototype/ai.config.yaml:15-17`).

**Security gates the prototype does not yet implement** (EXPLICIT specs, `security_architecture.md`):
- T3: an MDX restriction gate before build — reject any `import`/`export`, any JSX outside a component
  allowlist, `<script>`, `<iframe>`, event handlers, `javascript:`/`data:` URLs; generated pages use
  globally registered components instead of imports (`…:160-170`).
- T4: external links in generated content must match a versioned allowlist
  (`contracts/link-allowlist.yaml`), otherwise the PR is labeled `security-review` and blocked (`…:171-181`).
- T5: set Mermaid `securityLevel: 'strict'` explicitly in `docusaurus.config` (`…:182-192`).
- T6: secret-pattern scan over the assembled context payload before every provider call; abort on match
  (`…:193-203`).
- T7: hard spend limits set in every provider console (`…:204-214`).
- T8: `pull_request_target` banned; no `${{ github.event.* }}` in `run:`; top-level `contents: read`;
  actions pinned to SHAs (`…:215-225`).
- T12: content classification in frontmatter **`visibility: public|private`, defaulting to `private`
  when absent**; a cloud provider in a private chain is a config-validation error checked in CI
  (`…:259-269`). INFERRED: this is the design answer to the prototype's unimplemented private-content
  exclusion.
- T13: Pages deploy only via `actions/deploy-pages` from the `github-pages` environment restricted to
  `main`, with only `pages: write` + `id-token: write` (`…:270-282`).

**Generation pipeline** (`PI/06_AI_DOCUMENTATION/model-strategy/ai_architecture.md:97-105`): contract
load → evidence assembly (allowed globs only) → prompt render (instructions + delimited evidence) → router
→ **single model call** → parse against schema → deterministic gates (frontmatter, citations resolve,
external links allowlisted, Mermaid compiles, build passes) → on failure **one** repair retry with the
validator error → provenance stamp → commit to `docs-gen/<task>-<id>` → PR with run report. Fallback only
on 5xx/timeout, "never on content grounds" (`…:51-55`). Recruiter gate: every technology token in the
output must appear in a deterministically extracted fact list or cited canon (`…:107-114`).

**Content model** (`PI/05_DOCUMENTATION_DESIGN/information-architecture/content_architecture.md`):
numbered canonical taxonomy `00-overview … 14-knowledge-base` (`:17-47`); generated
`approval_status: draft|in-review|approved`, with `approved` "set by merge automation" (`:100`); the bot may
write only under `docs/generated/**` and its i18n mirror (`:133-137`); deleting a canonical page flags all
dependents for removal in the same PR (`:137`). INFERRED: the prototype uses a flatter taxonomy
(`prototype/docs/source/{overview,getting-started,architecture,…}`); this is a reversible prototype choice,
not a decision, and the plan does not require re-foldering.

## 5. Prototype implementation (as on disk, 2026-10-01)

Built 2026-09-21 by Antigravity 2.0 + Gemini 3.8 Flash from `docs/prototype-planning/ANTIGRAVITY_PROMPT.txt`
(`docs/prototype-planning/ANALYSIS.md:3-7`). Git: branch `main`, commits `36eac97`, `1a02d68`, no remote.
**Four files carry uncommitted changes from the 2026-09-30 M7 test work** (`git status`:
`prototype/planning/PROGRESS.md`, `scripts/review_governance.py`, `scripts/validate_docs.py`,
`tests/test_doccad.py`).

| Area | Implementation | Notes |
|---|---|---|
| Site | Docusaurus 3.10.2, React 19; `source` → `/docs`, `generated` → `/views` (`prototype/docusaurus.config.ts:33-50`); `markdown.mermaid: true` (`:27-28`); `onBrokenLinks: 'throw'` (`:12`); locales `en`, `hu` (`:16`) | No `future` flags; no explicit Mermaid `securityLevel`; `engines.node >=20.0` (`prototype/package.json:38`) |
| Pages & components | `src/pages/{index,explorer,inspector,workbench}.tsx`; components `EvidenceLink`, `InterviewPrep`, `ProvenanceBanner`, `QuestionWorkbench`, `DriftInspector`, `KnowledgeExplorer`; `src/theme/MDXComponents.tsx` exists | Generated MDX still uses `import` statements (e.g. `prototype/docs/generated/recruiter/project-overview.mdx:37`) |
| Content | 29 canonical pages, 7 `.mmd` diagrams, 11 generated pages (1 recruiter, 4 interview + 4 JSON datasets, 6 questions) | All seeded as `approval_status: approved-for-demo` by `scripts/seed_generated_views.py` |
| i18n | HU: 4 docs pages (`overview/index`, `overview/vision-and-goals`, `getting-started/installation`, `getting-started/quickstart`); `i18n/hu/code.json` 9 strings | Landing page has no `<Translate>` (0 occurrences in `src/pages/index.tsx`); no navbar/footer translation files |
| AI layer | `ai/provider.py` Protocol; adapters anthropic, gemini, openai, local, fixture; `ai/router.py`; `ai.config.yaml` with `default_provider: fixture` (`:4`), private → `[local]`, `local.enabled: false` | Adapters never run against a real provider; bare `except Exception` at `ai/router.py:124,139` |
| Contracts/schemas/prompts | 3 contracts, 3 schemas (`document`, `governance`, `interview`), 3 prompt templates | `generation_mode` + `fixture` provider added as explicit schema extensions |
| Scripts | `validate_docs.py` (schema, planes, ids, interview JSON, hashes, containment, unsafe MDX, citations), `detect_changes.py`, `generate_page.py`, `generate_question.py`, `review_governance.py`, `build_filter.py`, `seed_generated_views.py` | Citation check (check 8) and review transition table were added 2026-09-30 |
| Tests | `tests/test_doccad.py`: 36 tests in 12 test classes (33 at the baseline run; 3 citation-edge tests added 2026-10-01) | `test_private_content_excluded_from_production` is `@unittest.expectedFailure` (`tests/test_doccad.py:385`) |
| Planning | `prototype/planning/{CONCEPT,ACCEPTANCE,PROGRESS}.md`, `prototype/README.md` (Known issues) | No `VALIDATION.md`, `DEMO.md`, `LIMITATIONS.md` |
| CI / hosting | none — no `.github/`, no remote | |

## 6. Verification evidence

### 6.1 Prototype baseline — executed 2026-10-01 on a scratch copy

Scratch copy of `prototype/` (without `node_modules/`, `build/`, `.docusaurus/`; `node_modules` symlinked
back). Node v24.19.0, Python 3.14.4, `jsonschema` 4.19.2 installed (so `validate` ran the full schema
check, not its fallback).

| Check | Command | Result |
|---|---|---|
| Frontmatter, planes, ids, hashes, security, citations | `python3 scripts/validate_docs.py` | **PASS** — 40 pages, 4 interview datasets, 17 provenance hashes, exit 0 |
| Drift | `python3 scripts/detect_changes.py --all` | **PASS** — 44 manifest entries, 0 stale (always exits 0; read from output) |
| Unit tests | `python3 -m unittest discover tests` | **PASS** — 33 run, OK with 1 expected failure (re-run after the 2026-10-01 test fixes: 36 run, OK with 1 expected failure) |
| Types | `npx tsc` | **PASS** — exit 0 |
| Static build, both locales | `npx docusaurus build` | **PASS** — `en` and `hu` built; `build/search-index.json` 360,924 B and `build/hu/search-index.json` 357,220 B; only warning: no `blog/` |
| Live page generation | `python3 scripts/generate_page.py --contract GenerateRecruiterPage --target architecture-system-overview` | **FAIL** — `ContractViolation: last_validated: datetime.date(2026, 9, 21) is not of type 'string'` |
| Live interview generation | `python3 scripts/generate_page.py --contract GenerateInterviewPrep --target architecture-system-overview` | **FAIL** — 21 interview-schema errors (`concepts`/`example_answers` are strings not objects; missing `evidence`, `choice`/`benefit`/`cost`, `to`) |
| Dry-run generation | same with `--dry-run` | PASS — renders prompt, no provider call |
| Browser journeys, screenshots, console errors | — | NOT RUN |
| Mermaid compile (mermaid-cli) | — | NOT RUN (no tool in repo) |
| `build:production` → `build:demo` round trip | — | NOT RUN directly (exercised by `TestBuildFilterExclusion`) |

Additional probes, same scratch method:

| Probe | Result |
|---|---|
| `python3 scripts/build_filter.py --mode production` then `python3 scripts/validate_docs.py` | **FAIL** (exit 1) — every hold stub the filter writes has `generation.source_documents: []`, which `schemas/document.schema.json` rejects (`minItems: 1`); stubs are also stamped `approval_status: approved` (`scripts/build_filter.py` tombstone block). Restored with `--mode demo` |
| `grep -rn "{{" prompts/question-page.md` vs `scripts/generate_question.py:146-151` | Template has no `{{question}}` placeholder; `{{target_id}}` is never substituted → **the user's question never reaches a live model** (fixture works only because the question travels in `task_meta`) |
| `scripts/generate_page.py:212,228` | Live results default `generation_mode` to `"demo"` — only `ai/fixture_provider.py` returns the field → live output would be stamped demo |
| `scripts/detect_changes.py:123-125` vs `scripts/generate_page.py:45-51` | `regenerate[].target` is the *generated* page id; `generate_page.py` expects a *canonical* id → the regeneration plan cannot be executed as written |
| `scripts/generate_question.py:280-296` | Schema errors are only warnings; `--persist` writes straight into `docs/generated/questions/` |
| `scripts/build_filter.py:85-88` | A page whose frontmatter says `approved` is published without any ledger record; `scripts/review_governance.py:31` has no `approved` state and nothing produces one |
| `grep -n -i "retry\|repair" scripts/generate_page.py` | No repair retry (the PoC had one; ADR-004 and `ai_architecture.md:103-105` require exactly one) |
| `ai/fixture_provider.py:384-389`; `docs/source/security/prompt-injection-defense.md:45`; `docs/source/decisions/adr-007-mermaid-as-code.md:30` | Content describes a context secret scan, `config/link-allowlist.yaml` and a mermaid-cli CI gate **that do not exist** — the first run's "documented but not implemented" pattern, now inside reader-facing content |

### 6.2 Historical evidence (PoC, executed 2026-08-12)

From the archive sweep of `PI/09_RESULTS/` (paths relative to that folder):

- EXPLICIT: validation gates A–F all PASS (`validation/validation_report.md:99-102`). Executed on Node 22,
  Python 3.11, `jsonschema` present (`implementation/poc/VALIDATION_NOTES.md:1-6`): full en + hu build
  (`onBrokenLinks: throw` genuinely failed on two wrong slugs), `tsc`, `validate_docs.py` including a
  corrupted-hash negative test (exit 1), `detect_changes.py` one-byte drift demo, zero-key dry-run that
  refused out-of-allowlist evidence and raised `PrivacyRoutingError`, **mermaid-cli compiled both
  diagrams**, serve smoke test HTTP 200 on six routes including `/hu/` (`VALIDATION_NOTES.md:15-137`).
- EXPLICIT not executed: `actionlint` (workflows only YAML-parsed), live model calls, any GitHub workflow
  run, a real Pages deployment; `future.faster` and the search plugin deliberately omitted
  (`VALIDATION_NOTES.md:140-146`; `validation_report.md:83-88`).
- EXPLICIT PoC limitations (`implementation/poc/README.md:51-66`): generated pages hand-authored to match
  pipeline output; HU was English fallback only; PR push/create lines commented out in
  `docs-generate.yml:83-87`; named-entity evidence gate and link allowlist declared but not implemented.
- EXPLICIT contradiction inside the archive: `validation_report.md:43-47` ticks the link allowlist, while
  `implementation/poc/README.md:62-64` says it is not implemented; `validation_report.md:60` speaks of
  "four CI workflows", two shipped.
- PoC → prototype (INFERRED from file comparison by the sweep): carried forward unchanged —
  `detect_changes.py`, the three contracts (version 1), the three prompts, `interview.schema.json`, the
  adapters and `provider.py`. Added — fixture provider, question pipeline, review ledger, build filter,
  seed script, governance schema, tests, citation and unsafe-MDX checks. **Dropped** — both GitHub
  workflows (`docs-validate.yml`, `docs-generate.yml`, available at
  `PI/09_RESULTS/implementation/poc/.github/workflows/`), the Mermaid compile step, the single repair
  retry, the strict router exception handling (`PI/09_RESULTS/implementation/poc/ai/router.py:129` caught only `ProviderError`), and
  the ~70-line jsonschema-free fallback validator (`PI/09_RESULTS/implementation/poc/scripts/validate_docs.py:100-173`; the prototype's
  fallback checks five keys, `prototype/scripts/validate_docs.py:114-127`).

Knowledge-base pages that already answer next-phase questions (`PI/09_RESULTS/research/knowledge-base/`):
`30-best-practices/ci-quality-gates.md` (seven-rung deterministic ladder, a failing fixture per gate),
`20-patterns/pr-gated-generation.md` (`approved` set by merge automation; drafts expire after 30 days),
`30-best-practices/github-actions-security.md`, `20-patterns/hash-based-drift-detection.md`,
`20-patterns/leveled-retrieval.md`, `30-best-practices/prompt-injection-defenses.md` (five layers; the
human gate is the only one injection cannot defeat), `20-patterns/thin-provider-abstraction.md` (CI gate
so a private chain cannot contain a cloud adapter). EXPLICIT gaps: no KB page on evaluating generation
quality and none on ingesting external repositories.

### 6.3 Archive integrity notes (from the sweeps)

- `PI/02_RESEARCH/ai-models/` (22 files, "verified against official documentation 2026-08-14") is not
  registered anywhere in `PI/00_PROJECT_CONTROL/` (0 matches in SOURCE_REGISTER, ENTITY_REGISTER,
  PROJECT_MANIFEST, copy_map, PROJECT_KNOWLEDGE.json, COLLECTION_REPORT), has no original in
  `PI/11_RAW_ARCHIVE/`, contains the empty directory `ai_model_docs/` (confirmed with
  `find -type d -empty`), and contradicts `PI/PROJECT_STRUCTURE.md:22-23` ("ai-models … were not
  created") and the "no empty directories" rule. Its price and retirement data are already partly
  expired (e.g. a Sonnet intro price "through 2026-08-31").
- `PI/11_RAW_ARCHIVE/`: every raw original has at least one organized copy (copy_map.json 533 entries;
  248 raw files). 57 organized files are `created-during-archiving` (registers, prompt transcriptions,
  extracted diagrams).
- Stable-ID next free values: REQ-017, TASK-015, DEC-011, ARCH-007, DOC-004, DIAG-011 (canonical) /
  DIAG-133 (extracted), RES-008, REF-009, PROMPT-009 (`PI/00_PROJECT_CONTROL/ENTITY_REGISTER.md`;
  `PI/01_PROJECT_KNOWLEDGE/REQUIREMENTS.md`; `PI/08_TASKS/TASK_REGISTER.md`). This handoff pack uses its
  own `NV-` prefixes and allocates no archive ID.
- Smaller inconsistencies (none blocking): manifest 590 files vs COLLECTION_REPORT 588; `DUPLICATES.md`
  says three classes, lists five; DIAG-001…010 live in both `04_ARCHITECTURE/` and `07_MERMAID/`;
  TASK-014 still "IN PROGRESS"; `PI/README.md` and `BACKLOG.md` still say git is not initialized.

## 7. Gaps (confirmed 2026-10-01)

Each gap is a work item in `03_NEXT_VERSION_PLAN.md`. Status of the known issues the session was asked to
re-check:

| Known issue | Still holds? | Evidence |
|---|---|---|
| Live `generate_page.py` fails validation for recruiter and interview | **Yes** | §6.1 (date type; 21 interview-schema errors) |
| Private-content exclusion not implemented | **Yes** | `tests/test_doccad.py:385` `expectedFailure`; no `visibility` field anywhere (`grep -rln visibility scripts schemas src docs` → none) |
| Router catches bare `Exception` | **Yes** | `ai/router.py:124` (`chain_for` swallows instantiation errors), `:139` (`except (ProviderError, Exception)`) |
| `jsonschema` undeclared; validate silently degrades | **Yes** | no requirements file in `prototype/`; fallback at `scripts/validate_docs.py:114-127` |
| `PI/02_RESEARCH/ai-models/` unregistered | **Yes** | §6.3 |
| M6 open (HU landing, navigation) | **Yes** | 0 `<Translate>` in `src/pages/index.tsx`; no `navbar.json`/`footer.json` under `i18n/hu/` |
| M7 open (browser smoke, `VALIDATION.md`) | **Yes** | no `prototype/VALIDATION.md`; no browser evidence |
| M8 open (`DEMO.md`, `LIMITATIONS.md`) | **Yes** | files absent |

Further gaps found this session (all EXPLICIT from cited files or the §6.1 probes):

1. Production filter output fails validation (hold stubs with empty `source_documents`, stamped `approved`).
2. `approved` has no producer; `build_filter.py` trusts frontmatter `approved` with no evidence.
3. Question prompt never receives the question; `{{target_id}}` left unresolved.
4. Live output would be stamped `generation_mode: demo`.
5. Regeneration plan targets generated ids that `generate_page.py` cannot consume.
6. `generate_question.py --persist` bypasses validation and review.
7. No repair retry; no per-call retry/backoff in adapters; adapters forward `temperature` unconditionally
   (Anthropic rejects non-default sampling on newer models — `02_RESEARCH_KB.md` C2.2).
8. No structured-output fields in any adapter; repo schemas use keywords providers reject
   (`02_RESEARCH_KB.md` C1.13).
9. Security gates specified but absent: MDX import/export + component allowlist (T3 — generated pages use
   `import` today), external-link allowlist (T4), Mermaid `securityLevel: 'strict'` (T5), context secret
   scan (T6), CI check that a private chain has no cloud adapter (T12).
10. Content claims features that do not exist (secret scan, link allowlist, mermaid-cli gate).
11. Site not deployable as configured: `url: 'https://doccad.local'`, `baseUrl: '/'`, no `trailingSlash`;
    `engines.node >=20.0` while Node 20 is EOL since 2026-04-30 (`02_RESEARCH_KB.md` B2).
12. Search indexes English only (`language: ['en']`) although the site has a HU locale.
13. No CI, no `.github/`, no remote; the PoC's two workflows were not carried over.
14. Uncommitted working-tree changes from 2026-09-30 (four files) must be committed before a new run.
15. Antigravity does not read `.claude/rules/` (`02_RESEARCH_KB.md` A3.2): every rule the next run must
    follow has to live in `AGENTS.md` or flat `.agents/rules/*.md`.

## 8. Requirement trace (REQ → DEC → prototype → evidence → status)

Status: **P** = proven by an executed check (2026-10-01 or historical, as cited); **D** = designed, not
proven; **V** = vision only; **G** = implemented with a confirmed defect.

| REQ | DEC / ADR | Prototype implementation | Evidence | Status |
|---|---|---|---|---|
| REQ-001 | — (RES-001…006) | `docs/source/architecture/platform-research.md` (distilled) | archive research corpus; page validates | P (research) |
| REQ-002 | DEC-001 | `docs/source/decisions/adr-002-docusaurus-foundation.md` | `PI/04_ARCHITECTURE/architecture-decisions/decision_matrix.md:21-23` | P |
| REQ-003 | DEC-002 / ADR-001 | files only, `.docs-manifest.json` | build + validate PASS (§6.1); git repo exists, no remote | P locally; D on GitHub |
| REQ-004 | DEC-004 / ADR-003 | dual docs plugins; `validate_docs.py` plane checks; `TestPlaneSeparation` | §6.1 validate + tests PASS | P locally; CI path guard D |
| REQ-005 | DEC-005 / ADR-004 | `ai/` Protocol, router, 5 adapters | `TestPrivateRoutingPolicy` PASS; no live call ever | G (bare `except`, no retry, no structured output) |
| REQ-006 | DEC-009 / ADR-008 | static build, no runtime model calls | build PASS with no keys (§6.1) | P (credentials unset); "outbound access blocked" NOT RUN |
| REQ-007 | DEC-007 / ADR-006 | `generate_question.py` deterministic retrieval; `generate_page.py` closure | `TestDeterministicRetrievalAndGeneration` PASS | P (L1); keyword expansion only in question path |
| REQ-008 | DEC-006 / ADR-005 | `detect_changes.py` (`--all`, `--range`) | `TestHashDriftAndRegeneration`, `TestSourceDeletionDetection` PASS | G (regeneration targets wrong id); CI ingestion D |
| REQ-009 | DEC-004/006 | `generation` frontmatter, sha256 hashes | `TestInvalidProvenance` PASS (5 cases) | P |
| REQ-010 | DEC-006 | `docs/generated/recruiter/project-overview.mdx`, `<EvidenceLink>` | page validates; citations resolve (`TestBrokenCitations`) | G (live generation FAIL; named-entity gate absent) |
| REQ-011 | DEC-009 | `<InterviewPrep>`, 4 `*.interview.json` | schema validation PASS on seeded data | G (live generation FAIL) |
| REQ-012 | DEC-006 | `/workbench`, `generate_question.py`, review ledger | 5 supported + 1 unsupported scenario tests PASS | G (question never reaches a live model; `--persist` bypasses review); preview PR D |
| REQ-013 | — | `en` + `hu` locales; 4 HU pages | hu build PASS (§6.1) | G (landing/nav untranslated; search EN only) |
| REQ-014 | all | stdlib + PyYAML scripts, no DB/services | inspection | P |
| REQ-015 | — | `prototype/` + 36 tests | §6.1 | P (with 1 expected failure); `VALIDATION.md` missing |
| REQ-016 | — (ARCH-006) | traversal check, unsafe-MDX regexes, private routing | `TestPathTraversalSecurity`, `TestUnsafeMdxRejection`, `TestPrivateRoutingPolicy` PASS | G (T3/T4/T5/T6/T12 gates absent; private-content exclusion expected-failure) |

## 9. Proven vs designed vs vision

| Proven (executed evidence) | Designed but unproven | Vision only |
|---|---|---|
| Two-plane structural separation, locally (§6.1) | CI gates, Pages deployment via OIDC, smoke test (`automation_architecture.md:43-62`) | Generation of user/architecture/development manuals, SOPs, migration guides, security reviews (`VISION.md:7-12`) |
| Static en + hu build with no provider keys (§6.1; PoC `VALIDATION_NOTES.md`) | PR-gated persistence with real human approval (ADR-005) | Role-specific views, `summaries/` (`content_architecture.md:38-43`) |
| Hash provenance, drift and source-deletion detection (tests) | Live generation through four providers with one repair retry (ADR-004) | Automatic HU translation of generated pages (deferred, `ARCHITECTURE-SPINE.md:104`) |
| Privacy pinning hard-fails without local provider (tests; PoC dry-run) | Security gates T3–T6, T12 (`security_architecture.md`) | L2+ retrieval (deferred until boundary trips) |
| Deterministic question pipeline with insufficient-evidence handling (tests) | Weekly stale-views issue, docs-drift-suspect comments (`automation_architecture.md:27-41`) | Runtime Q&A chat (non-goal) |
| Citation resolution, provenance tampering, traversal and unsafe-MDX rejection (tests) | Mermaid compile gate in CI (proven once in the PoC, absent now) | Multi-repo federation (non-goal) |
| Review state machine with enforced transitions (tests) | Private-content exclusion via `visibility` (T12; expected-failure test) | |
| Local search index for both locales (§6.1) | Remaining six task contracts (`ai_architecture.md:77-87`) | |
