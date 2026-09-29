# PROMPT-002 — Archival & Consolidation Mission (this archive's founding prompt)

**Provenance:** User-issued mission, same Cowork session, received 2026-08-13 upon connecting the device
folder `W:\CC-COWORK_PROJECT-FOLDER\w7-PRE-DOCCAD_PROJECT`. Preservation status: **near-verbatim
transcription** — all 23 sections complete, formatting normalized. Classification: ORIGINAL / EXPLICIT.
Drove: the creation of this archive (TASK-014).

---

Act as Senior Project Archivist, Knowledge Architect, Documentation Engineer, Solution-Architecture Project
Coordinator, AI Knowledge-Base Engineer. Mission: recover, consolidate, structure, preserve, and make
traceable the existing PRE-DOCCAD project knowledge. **Archival and consolidation — NOT recreation.**
Destination: `w7-PRE-DOCCAD_PROJECT/`, the canonical project workspace after consolidation.

**§0 Absolute priority:** DISCOVER → COLLECT → CLASSIFY → PRESERVE → COPY/DOWNLOAD → ORGANIZE → TRACE →
INDEX → VERIFY. Do NOT: recreate the project, redesign architecture, rewrite existing documents, regenerate
research, replace imperfect documents, delete historical material, silently discard duplicates, invent
missing information, "improve" sources during collection. Imperfections: preserve and record; improvements:
future task, not replacement.

**§1 Primary objective:** consolidate ALL relevant material (files, documents, artifacts, prompts,
research, architecture analysis, decisions, requirements, vision, tasks, completed/intermediate/final
results, Mermaid diagrams, specs, external references, downloads, conversational knowledge, historical
versions, rejected alternatives, open questions, future ideas) into a complete, navigable, traceable
archive.

**§2 Preserve history:** distinguish ORIGINAL / CANONICAL / DERIVED / HISTORICAL / TRANSLATION /
EXPERIMENT / INTERMEDIATE / SUPERSEDED / DUPLICATE / REFERENCE; never delete historical evidence because a
newer version exists.

**§3 Full context recovery:** inspect the entire Cowork context and workspace before organizing; explicit
and implicit relationships; concept list includes PRE-DOCCAD, DOCCAD, documentation ecosystem, GitHub docs,
AI documentation, Mermaid, C4, manuals, recruiter docs, interview prep, AI-generated/special-question pages,
Claude/Gemini/OpenAI/local/Ollama, the six platforms, architecture-diagram/security/BMAD skills, SAD, ADR,
runbooks, roadmap, prompts, research, platform comparison. Context over keyword matching.

**§4 Preserve the project vision as vision (not as implemented fact):** GitHub-based documentation
ecosystem; docs/architecture/Mermaid/processes in a clean version-controlled repo; models: Gemini, Claude,
OpenAI, free/local; generates deeply structured user/architecture/development manuals, processes,
troubleshooting, SOPs, migration guides, security reviews, recruiter pages, interview prep, special
questions. Conceptual flow: Canonical GitHub Documentation → Project Knowledge → AI Processing → {User
Docs, Technical Architecture, Recruiter View} → Interview Prep; and User Question → Retrieve → Analyze →
Generate Dedicated Page → Optionally Persist. Do not claim capabilities exist unless artifacts prove it.

**§5 Full provenance and traceability:** stable IDs (REQ-, TASK-, DEC-, DOC-, ARCH-, DIAG-, RES-, REF-,
PROMPT-); relationship chains REQ→TASK→RES→DEC→ARCH→DOC; create 00_PROJECT_CONTROL/
{TRACEABILITY_MATRIX.md, ENTITY_REGISTER.md, SOURCE_REGISTER.md}; matrix answers origin/task/result/
decision/artifact questions; uncertain relationships marked UNKNOWN or INFERRED with explanation; do not
invent relationships.

**§6 Git-ready structure:** minimal supporting files (.gitignore, README.md, CONTRIBUTING.md,
PROJECT_STRUCTURE.md); README explains what PRE-DOCCAD is, contents, organization, canonical knowledge
location, provenance, contribution, raw vs maintained. No remote init, no commit, no push, no external repo
modification.

**§7 AI-ready knowledge layer:** 00_PROJECT_CONTROL/PROJECT_KNOWLEDGE.json — machine-readable
retrieval/navigation layer (not a replacement for documents); per-artifact: id, title, type, status, path,
source, source_reference, summary, topics, requirements, tasks, decisions, results, related_artifacts,
language, confidence. No fabricated summaries; concise metadata over duplication.

**§8 Archive structure (baseline, adapt only if objectively better):** 00_PROJECT_CONTROL, 01_PROJECT_
KNOWLEDGE (incl. DECISIONS.md, OPEN_QUESTIONS.md), 02_RESEARCH (documentation-platforms/<six>, ai-models,
architecture, security, deployment, references), 03_PROMPTS (master, architecture, research,
documentation-generation, claude, fable, prompt-generator), 04_ARCHITECTURE (SAD, ADR, C4, deployment,
data-flows, architecture-decisions), 05_DOCUMENTATION_DESIGN (information-architecture, content-model,
user/architecture/development-manual, operations, documentation-process), 06_AI_DOCUMENTATION
(model-strategy, provider-abstraction, retrieval, generation, recruiter, interview,
special-question-pages), 07_MERMAID (c4, sequence, workflows, deployment, misc), 08_TASKS (completed,
in-progress, pending, blocked, future), 09_RESULTS (completed, research, architecture, implementation,
validation, experiments), 10_EXTERNAL_ARTIFACTS (downloaded, repositories, reference-documents, snapshots),
11_RAW_ARCHIVE (original-material), 12_FUTURE (backlog, ideas, improvements). No empty directories unless
structurally required.

**§9 Raw vs organized:** 11_RAW_ARCHIVE preserves originals; other folders hold classified copies/
references; RAW SOURCE → ORGANIZED ARTIFACT → KNOWLEDGE INDEX; every organized artifact traceable to
source.

**§10 Duplicates:** never auto-delete; classify IDENTICAL / NEAR-DUPLICATE / DIFFERENT VERSION / DERIVED /
TRANSLATION / HISTORICAL / UNKNOWN; 00_PROJECT_CONTROL/DUPLICATES.md with source, candidate, relationship,
hash, version clues, canonical recommendation, reason.

**§11 Task/result traceability:** 08_TASKS/TASK_REGISTER.md (DONE / IN PROGRESS / PENDING / BLOCKED /
FUTURE / SUPERSEDED / UNKNOWN; no inferred completion without evidence); 09_RESULTS/RESULT_REGISTER.md;
chain TASK→WORK→RESULT→ARTIFACT→DECISION.

**§12 Mermaid preservation:** find all diagrams incl. embedded in Markdown; preserve; index in 07_MERMAID/
with diagram ID, source, type, related document/decision, source path; do not redraw.

**§13 Prompt preservation:** prompts are first-class artifacts (original, refined, generator, Claude,
Fable, architecture, research, documentation prompts); no collapsing versions; record version
relationships.

**§14 External artifacts:** download relevant accessible artifacts with URL, date, source type,
authority status into 10_EXTERNAL_ARTIFACTS/; no massive irrelevant downloads.

**§15 Conversational knowledge:** preserve project-level knowledge (vision, requirements, preferences,
rejected alternatives, decisions, constraints, goals, future concepts) in 01_PROJECT_KNOWLEDGE/; no
fabricated history; distinguish EXPLICIT / INFERRED / UNKNOWN.

**§16 Git-ready rules:** .gitignore excludes generated/cache/secrets; never include API keys, passwords,
credentials, tokens, .env secrets, cookies; discovered credentials are not copied — record "SECRET DETECTED
— NOT ARCHIVED".

**§17 AI-ready design:** PROJECT_KNOWLEDGE.json answers what/requirements/decisions/research/architecture/
tasks-complete/remaining/which-document/which-result/which-source; stable IDs and relationships; NO vector
DB, NO RAG infrastructure, NO model APIs — this creates the knowledge foundation only.

**§18 Project index:** 00_PROJECT_CONTROL/PROJECT_INDEX.md — a new agent reads this single file and
understands purpose, vision, archive map, major artifacts, architecture, research, prompts, Mermaid, tasks,
results, decisions, external references, future work, unresolved issues.

**§19 Workflow phases 0–15:** inspect destination → inventory destination → inspect context → discover →
classify → assign IDs → preserve originals → copy/download → provenance → task/result registers →
PROJECT_KNOWLEDGE.json → index → duplicates → Git metadata → verify coverage → collection report. No
skipping discovery or verification.

**§20 Verification gates:** 31-item checklist (destination inspected/preserved; context inspected;
discovery; documents/prompts/research/architecture/Mermaid/tasks/results/decisions/references/downloads
collected; conversational knowledge; historical versions; duplicates; IDs; provenance; traceability;
PROJECT_MANIFEST.json; PROJECT_KNOWLEDGE.json; PROJECT_INDEX.md; registers; README; CONTRIBUTING;
PROJECT_STRUCTURE; secrets excluded; manifest paths verified; no destructive overwrite; no unnecessary
recreation).

**§21 Collection report:** 00_PROJECT_CONTROL/COLLECTION_REPORT.md — statistics (discovered, preserved,
copied, downloaded, documents, prompts, research, architecture, Mermaid, tasks, results, decisions,
references, duplicates, historical versions, unresolved), coverage, inaccessible information, potential
future work (recorded, not executed).

**§22 Do not implement:** the eventual system (GitHub + Markdown + Mermaid + AI APIs + RAG + generation +
recruiter/interview/special-question) is to be archived as requirements/concepts, not built now.

**§23 Success condition:** structured, Git-ready, provenance-aware, AI-ready knowledge repository; a
future agent navigates README.md → PROJECT_INDEX.md → PROJECT_KNOWLEDGE.json → TRACEABILITY_MATRIX.md to
every significant artifact. Final principle: **Preserve first. Structure second. Improve later.** Do not
recreate the project; recover the project that already exists.
