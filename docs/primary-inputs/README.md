# PRE-DOCCAD — Project Knowledge Archive

**What PRE-DOCCAD is.** The preparatory knowledge project for DOCCAD: a GitHub-native, AI-augmented
documentation ecosystem in which canonical project knowledge (documentation, architecture, Mermaid
diagrams, processes) lives in a version-controlled repository, and an AI layer (Claude / Gemini / OpenAI /
local models) transforms that canonical evidence into governed derived views — user docs, architecture
manuals, recruiter pages, interview preparation, special-question pages. See
`01_PROJECT_KNOWLEDGE/VISION.md` for the vision as vision, and what is actually proven today.

**What this repository contains.** The complete consolidated output of the PRE-DOCCAD research and design
phase (Cowork session, 2026-08-12/13): six repository-grounded platform analyses, a weighted platform
decision (Docusaurus), the full target architecture (spine, 6 architecture documents, 9 ADRs, 10 validated
Mermaid diagrams), a runnable and execution-validated proof of concept, a 33-file distilled knowledge base,
the founding prompts, and full provenance metadata.

**How the archive is organized.** Numbered sections 00–12; `PROJECT_STRUCTURE.md` defines each. Two layers:
`11_RAW_ARCHIVE/` holds byte-preserved originals; every other folder holds organized, classified copies
that remain traceable to their raw source (`00_PROJECT_CONTROL/SOURCE_REGISTER.md`).

**Where canonical knowledge lives.** Research: `02_RESEARCH/`. Architecture: `04_ARCHITECTURE/`. AI-layer
design: `06_AI_DOCUMENTATION/`. The distilled wiki: `09_RESULTS/research/knowledge-base/` (entry:
`INDEX.md` / `llms.txt`).

**How provenance works.** Stable IDs (REQ/TASK/DEC/DOC/ARCH/DIAG/RES/REF/PROMPT) with chains recorded in
`00_PROJECT_CONTROL/TRACEABILITY_MATRIX.md`; entity catalog in `ENTITY_REGISTER.md`; machine layer in
`PROJECT_KNOWLEDGE.json`; per-file hashes and sources in `PROJECT_MANIFEST.json`.

**Start here (human or agent):**
README.md → `00_PROJECT_CONTROL/PROJECT_INDEX.md` → `PROJECT_KNOWLEDGE.json` → `TRACEABILITY_MATRIX.md`.

**Raw historical vs maintained.** `11_RAW_ARCHIVE/` and `03_PROMPTS/` are historical — never edit.
Registers and control documents are maintained. New work: see `CONTRIBUTING.md`; improvements become FUTURE
tasks in `08_TASKS/`, not rewrites of history. This repo is Git-ready but intentionally not initialized,
committed, or pushed.
