# DOCCAD prototype prompt analysis

Prepared 2026-09-21 using the explicitly requested prompt-architect skill. This folder is a new planning deliverable outside the historical archive. No prototype implementation was requested in this turn or performed.

## Confirmed intent

The user confirmed DOCCAD as the subject, complete local workflows with deterministic demo data as the implementation depth, and balanced attention to documentation UX, AI workflows, and governance. The execution target is Google Antigravity 2.0 using Gemini 3.8 Flash.

## Assessment of the original prompt

These scores assess the original wording before repository research and clarification.

| Dimension | Score | Reason |
|---|---:|---|
| Clarity | 5/10 | Requests a build prompt and graph, but does not name the prototype subject. |
| Specificity | 4/10 | Names the target environment and model; "massive" has no measurable scope. |
| Context | 2/10 | Product, users, existing assets, and constraints are unstated in the message. |
| Completeness | 3/10 | Omits implementation boundaries, acceptance checks, and failure behavior. |
| Structure | 5/10 | Gives analysis → graph → prompt ordering, but combines requirements in a run-on instruction. |
| Overall | 3.8/10 | Arithmetic mean of the five scores. |

## Framework and changes

Selected RISEN: Role, Instructions, Steps, End goal, Narrowing. One framework is sufficient because the deliverable is an ordered implementation procedure with explicit boundaries and success criteria. Tool execution and verification are requirements inside that procedure, not a second framework requiring invented tool signatures or simulated observations.

Role: lead product engineer with documentation architecture and UX responsibilities.

Instructions: build the confirmed local DOCCAD prototype, grounded in the supplied archive and existing PoC.

Steps: evidence inspection → concept and contracts → complete first journey → content and UX → deterministic workflows → governance → verification → handoff.

End goal: a runnable application with substantial content, complete question/review/preview and drift/regeneration journeys, and current verification evidence.

Narrowing: immutable archive; static delivery; no runtime database; no real provider calls or GitHub publication; no fabricated claims, tool results, or human approval.

The skill influenced the result by converting the ambiguous scale requirement into concrete coverage and acceptance criteria, retaining explicit prohibitions, and resolving missing product context through repository evidence and user answers. No placeholders remain: the prompt locates its source material relative to the supplied workspace. Missing source files cause a specific blocker rather than guessed requirements.

Worked few-shot examples were not added. The task needs implementation contracts and acceptance journeys, and the workspace already supplies real schemas, task contracts, components, and sample content. There is no need to invent an example of a completed build.

The proposed coverage defaults are at least 20 canonical pages, one recruiter view at three depths, four interview topics, five supported question scenarios plus one insufficient-evidence scenario, and a ten-minute demonstration. These are new prototype targets, not historical user requirements or claims about existing assets.

## Concept and evidence

DOCCAD has a human-maintained knowledge plane and a derived-content plane. The generation workflow uses canonical evidence, a task contract, validation, provenance, and review. The reading workflow consumes static artifacts and does not depend on generation availability. A basic graph is in [concept.mmd](concept.mmd).

The implementation prompt preserves those boundaries while adding a static browser workbench. Browser interaction uses disposable state and file exchange; the CLI performs actual candidate-file generation. A simulated review affects only a demo record and preview, never production approval. This makes a full local demonstration possible without adding an application server or disguising fixture behavior as live AI.

| Evidence inspected | Consequence for the prompt |
|---|---|
| [Vision](../primary-inputs/01_PROJECT_KNOWLEDGE/VISION.md) and [requirements](../primary-inputs/01_PROJECT_KNOWLEDGE/REQUIREMENTS.md) | Focus on documentation, evidence-backed audience views, question pages, EN/HU, and one-engineer operation. |
| [Decisions](../primary-inputs/01_PROJECT_KNOWLEDGE/DECISIONS.md) and [architecture spine](../primary-inputs/04_ARCHITECTURE/SAD/ARCHITECTURE-SPINE.md) | Retain Docusaurus, two content planes, files, deterministic retrieval, hashes, and static delivery. |
| [Archive contribution policy](../primary-inputs/CONTRIBUTING.md) | Build in a new prototype directory; preserve historical sources. |
| [Content architecture](../primary-inputs/05_DOCUMENTATION_DESIGN/information-architecture/content_architecture.md) | Preserve IDs, source mappings, generated-to-canonical citations, locale strategy, and canonical independence. |
| [AI architecture](../primary-inputs/06_AI_DOCUMENTATION/model-strategy/ai_architecture.md) and existing contracts | Route generation through contracts and evidence restrictions; keep model identities configurable and distinguish fixture mode. |
| [PoC README](../primary-inputs/09_RESULTS/implementation/poc/README.md) and [historical validation](../primary-inputs/09_RESULTS/implementation/poc/VALIDATION_NOTES.md) | Reuse demonstrated foundations but require fresh execution; explicitly close search, translation, question-flow, and validation gaps. |
| [Generation script](../primary-inputs/09_RESULTS/implementation/poc/scripts/generate_page.py) | Existing CLI is target-page-driven; the question contract alone does not implement a question-to-page journey. |
| [Security architecture](../primary-inputs/04_ARCHITECTURE/SAD/security_architecture.md) | Enforce safe generated-content handling, private routing, evidence allowlists, and review boundaries; do not treat delimiters as a security guarantee. |

The current workspace does not expose a usable Git repository. The prompt does not rely on Git initialization or a remote to complete its local demonstration. Historical statements about installed dependencies and successful builds have not been revalidated during this prompt-authoring task.

## Target environment verification and use

Google's [Antigravity overview](https://www.antigravity.google/docs/overview) describes the agent environment. Its [model documentation](https://antigravity.google/docs/models) lists Gemini 3.8 Flash and describes selecting models in the conversation UI. Google's [model reference](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) documents the requested model. Verified on 2026-09-21; no speculative model tuning settings are required by this prompt.

Open this workspace in Antigravity 2.0, select Gemini 3.8 Flash in the model selector, and paste [ANTIGRAVITY_PROMPT.txt](ANTIGRAVITY_PROMPT.txt). The prompt cannot change the selected model itself. For browser verification, enable the application's browser capability; the [Antigravity 2.0 announcement](https://www.antigravity.google/blog/introducing-google-antigravity-2) documents the /browser command. The prompt also provides an honest fallback if browser tooling is unavailable.

This deliverable contains a prompt, analysis, and diagram source. It does not claim that the future prototype, browser journeys, provider adapters, or CI workflows have been executed here.
