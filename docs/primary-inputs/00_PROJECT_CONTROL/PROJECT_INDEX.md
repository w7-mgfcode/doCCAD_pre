# PRE-DOCCAD — Project Index

Read this file to understand the whole project. Machine navigation: `PROJECT_KNOWLEDGE.json`. Provenance
chains: `TRACEABILITY_MATRIX.md`. Entities: `ENTITY_REGISTER.md`. Collection audit: `COLLECTION_REPORT.md`.

## Purpose

PRE-DOCCAD is the research-and-design phase for **DOCCAD**: a GitHub-native, AI-augmented documentation
ecosystem. Canonical knowledge lives in Git; an AI layer (Claude/Gemini/OpenAI/local behind a thin,
config-routed abstraction) transforms canonical evidence into governed derived views (recruiter pages,
interview prep, special-question pages); everything derived enters only via human-approved PRs with hashed
provenance; the published site is static and never depends on AI. Vision as vision — and the honest line
between designed vs proven — is in `../01_PROJECT_KNOWLEDGE/VISION.md`.

## Current state (2026-08-13)

Research, platform decision, target architecture, and an execution-validated PoC are COMPLETE. Nothing is
deployed to production; no live AI generation has run with real keys; the future implementation plan
(MVP → SCALE → HARDEN) is recorded, entirely FUTURE. This archive is the consolidated, provenance-aware
record of all of it.

## The headline facts

Platform decision: **Docusaurus 3.x, 88.6/100** on an 11-criterion weighted model over Mintlify (85.0),
MkDocs+Material (83.8), Zensical (76.4), Hyperbook (76.0), GitBook (72.2) — with constraint analysis
(`../04_ARCHITECTURE/architecture-decisions/decision_matrix.md`). Architecture: one repo, two structurally
separated content planes (canonical `/docs`, generated `/views`), AI only in CI, PR-gated persistence,
hash-based drift detection, Level-1 deterministic retrieval, static GitHub Pages deployment in three modes.
PoC: runnable Docusaurus starter, all five mandated scenarios VERIFIED BY EXECUTION
(`../09_RESULTS/validation/`).

## Archive map

| Where | What |
|---|---|
| `../01_PROJECT_KNOWLEDGE/` | Vision, 16 requirements, 10 decisions, constraints, rejected alternatives, open questions |
| `../02_RESEARCH/documentation-platforms/` | Six full platform analyses (SAD ~4.4-5.4k words each, 5 ADRs, runbook, roadmap, scores, repo health, sources) + `_comparison/` |
| `../03_PROMPTS/` | PROMPT-001/002 mission transcriptions (master/), analysis brief (research/), generation templates (documentation-generation/) |
| `../04_ARCHITECTURE/` | Architecture spine + solution SAD + security architecture (SAD/), 9 ADRs (ADR/), Mermaid sources (C4/, deployment/, data-flows/), decision matrix |
| `../05_DOCUMENTATION_DESIGN/` | Content architecture / taxonomy; automation architecture (ingestion, drift, CI/CD) |
| `../06_AI_DOCUMENTATION/` | AI architecture; provider adapters + router + config (code copies); 3 task contracts + 2 schemas; demo recruiter/interview artifacts |
| `../07_MERMAID/` | 10 standalone validated diagrams by type + 32 extracted embedded diagrams + `MERMAID_REGISTER.md` |
| `../08_TASKS/` | `TASK_REGISTER.md` (14 tasks, 13 DONE), final progress checkpoint, future roadmap CSV |
| `../09_RESULTS/` | `RESULT_REGISTER.md`; validation report (Gates A-F PASS) + execution logs; 33-file knowledge base wiki (`research/knowledge-base/INDEX.md`); runnable PoC (`implementation/poc/`); session manifest |
| `../10_EXTERNAL_ARTIFACTS/` | The three methodology skill documents applied during design |
| `../11_RAW_ARCHIVE/original-material/outputs/` | Byte-preserved original session workspace — never edit |
| `../12_FUTURE/` | Backlog incl. archival follow-ups |

## Key artifacts by question

*What was decided and why?* → `../01_PROJECT_KNOWLEDGE/DECISIONS.md` → ADRs + decision matrix.
*What does the target system look like?* → `../04_ARCHITECTURE/SAD/solution_architecture.md` (MEGOLDÁS, EN+HU).
*How does the AI layer work?* → `../06_AI_DOCUMENTATION/model-strategy/ai_architecture.md`.
*Is it secure?* → `../04_ARCHITECTURE/SAD/security_architecture.md` (13-threat model, trust zones).
*Was any of it proven?* → `../09_RESULTS/validation/validation_report.md` (+ PoC execution log).
*Where do I learn the field?* → `../09_RESULTS/research/knowledge-base/INDEX.md` (wiki: foundations,
platform profiles, 8 patterns, practices, decision frameworks, glossary, full SADs).
*What remains open?* → `../01_PROJECT_KNOWLEDGE/OPEN_QUESTIONS.md` and `../12_FUTURE/backlog/BACKLOG.md`.

## Unresolved issues (summary)

Evidence gaps on proprietary platform internals and some pricing (labeled [UNKNOWN] throughout); mission
prompts preserved as near-verbatim transcriptions, not byte-exact; sub-agent working prompts beyond the
analysis brief not persisted; external web evidence not snapshotted (URLs preserved). Details with labels:
`../01_PROJECT_KNOWLEDGE/OPEN_QUESTIONS.md`.
