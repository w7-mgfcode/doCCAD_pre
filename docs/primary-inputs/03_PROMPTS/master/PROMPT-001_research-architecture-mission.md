# PROMPT-001 — Master Research & Architecture Mission (founding prompt)

**Provenance:** User-issued mission, Cowork session `docs-platform-architecture-2026-08-12`, received
2026-08-12. Preservation status: **near-verbatim transcription from the session conversation** — all 43
sections and their substantive rules are complete; whitespace/list formatting normalized during
transcription. Classification: ORIGINAL / EXPLICIT. Drove: TASK-001…TASK-011, RES-001…RES-007,
ARCH-001…ARCH-006, DEC-001…DEC-010.

---

MISSION: Act as Principal Solution Architect, AI Systems Architect, Documentation Platform Architect,
Developer Experience Architect, Security Architect, SRE-minded analyst. Two objectives:
**A — Comparative architecture research** of six documentation platforms: Mintlify (mintlify.com),
GitBook (gitbook.com), Docusaurus (docusaurus.io), MkDocs (mkdocs.org), Zensical (zensical.org),
Hyperbook (hyperbook.openpatch.org). **B — Design and prototype** a practical GitHub-native, AI-augmented
documentation ecosystem: canonical knowledge in Git, Mermaid-as-code diagrams, AI layer transforming
verified source material into multiple controlled documentation views. Not merely Markdown→static site but
a governed lifecycle: GitHub repo → canonical knowledge → structured documentation model → AI
context/retrieval → model router (Claude/Gemini/OpenAI/Local) → generated/transformed documentation →
validation + provenance + human review → Git PR / approved artifacts → documentation build → searchable
portal. Must remain simple, maintainable, operable by a small team. Do not overengineer.

**§1 Final system vision:** GitHub-stored docs knowledge system with optional AI generation layer; Git as
primary source of truth; version-controlled docs, architecture, operational knowledge, Mermaid, ADRs,
runbooks, workflows, metadata. Deep category list given (Overview, User Manual, Architecture Manual,
Development Manual, Development Process, AI/Agent Workflows, Getting Started, Onboarding, Operations,
Deployment, Security, Troubleshooting, Runbooks, ADRs, API Documentation, Integration Guides, Migration
Guides, Testing/Validation, Knowledge Base, Recruiter View, Interview Preparation, Generated Question
Pages) — to be refined during design, not blindly accepted.

**§2 Canonical vs AI-generated knowledge (fundamental):** canonical = human-authored/approved authoritative
material (architecture docs, dev process, source-derived facts, ADRs, procedures, API contracts, security
policies, domain knowledge). Derived AI knowledge = transformations of canonical evidence (recruiter
explanations, hiring-manager summaries, interview prep, beginner explanations, walkthroughs, role pages,
migration summaries, expanded docs). AI content must never silently become authoritative. Suggested
docs/source | docs/generated | docs/diagrams split as starting point — improve if research justifies.

**§3 AI-powered capabilities to investigate:** architecture generation (C4, explanations, components,
boundaries, Mermaid, deployment/integration views); developer documentation (setup, workflow, contribution,
testing, CI/CD, module docs); operational documentation (SOPs, troubleshooting, runbooks, incident,
deployment, recovery); career-oriented transformations of the same evidence (Recruiter View, Hiring Manager
View, Senior Engineer View, Portfolio Case Study, Interview Explanation, Skills/Competency Mapping).
Recruiter content must remain evidence-grounded; no fabricated achievements/metrics/technologies/impact.

**§4 Interview preparation as first-class feature:** optional "Interview Preparation" section per major
page: how to explain in interview, 30-second and 2-minute explanations, likely questions, key concepts,
trade-offs, competence demonstrated, follow-ups. Facts derived from the page's canonical docs + linked
evidence. Prefer build-time augmentation over runtime AI.

**§5 Special-question → dedicated page workflow:** question → classification → retrieval → evidence
selection → prompt/template selection → model routing → draft page → citation/factual validation → Mermaid
validation → preview → optional human approval → persist as versioned page. Decide lifecycle (temporary vs
auto-persist vs PR vs approval vs regeneration on change); recommend safest/simplest.

**§6 Automated GitHub ingestion (mandatory):** discover new/modified Markdown, architecture docs, ADRs,
Mermaid, READMEs, code architecture changes, API schemas, workflows, config, dev instructions. Candidate
flow: push/PR → change detection → classification → metadata extraction → link/dependency analysis →
validation → AI impact analysis → identify stale derived pages → regenerate only affected → validation →
preview/PR → merge → publish. Incremental updates; no full-corpus regeneration per commit; content
dependency mapping (source changed → affected pages/diagrams); prefer manifests over graph DB.

**§7 Metadata/provenance contract:** frontmatter with id/title/type/audience/sources/owners/related/
ai_generation/last_validated for canonical; generated:true + generation block (source_documents, provider,
model, generated_at, prompt_version, confidence, approval_status) for AI pages. Improve if appropriate.

**§8 Model provider abstraction:** Anthropic/Claude, Google/Gemini, OpenAI, local/open models,
OpenAI-compatible endpoints, Ollama. No deep coupling. Task classifier → model policy → provider adapter.
Routing by privacy, cost, availability, context, structured output, latency, offline, complexity. Pragmatic;
no autonomous multi-agent platform.

**§9 Critical principle:** approved documentation must remain available when every provider is down /
credentials expire / quotas exhausted. AI = generation/enrichment plane, not mandatory serving plane.
Isolate dynamic AI from ordinary site delivery.

**§10 Retrieval:** minimum sufficient architecture; evaluate Level 1 structured file selection + metadata +
repo search → L2 full-text index → L3 embeddings → L4 hybrid/rerank. No automatic vector DB; explain the
decision boundary.

**§11 Skills (mandatory):** apply bmad-architecture, architecture-diagram, agent-v3-security-architect;
reference getclaudeskills.com methodology pages (epic-architecture-specification-github,
architecture-diagram-nousresearch, v3-security-architect-ruvnet, bmad-architecture-bmad-code-org). If a
skill cannot be invoked, state the limitation.

**§12 Evidence rules:** classify as [VERIFIED-OFFICIAL] / [VERIFIED-REPO] / [OBSERVED] / [INFERRED] /
[UNKNOWN] / [HISTORICAL]. Never invent backend tech, internal services, security controls, compliance,
SLAs, pricing, benchmarks, performance, adoption, databases, customer counts.

**§13 GitBook safeguard:** current platform = proprietary SaaS unless proven otherwise; archived repos are
[HISTORICAL], never current architecture. Same discipline for Mintlify internals.

**§14 OSS repository deep dive:** inspect README, LICENSE, SECURITY, manifests, lockfiles, modules, source,
build system, config, plugins, themes, localization, search, CLI, tests, CI, dependency automation,
releases, contributor docs; derive authoring/config/parsing/build/rendering/plugin/theme/search/
localization/delivery layers; ground C4 L2/L3 in repo evidence.

**§15 Checkpoint/resume:** outputs/progress.json with p0_preflight, p1_<six platforms>, p2_comparison,
p3_target_architecture, p4_poc, p5_validation, p6_manifest; each with status/outputs/sources/timestamp/
evidence gaps/validation; resume completed work.

**§16 Per-product SAD** with ~35 mandated sections (Exec Summary + HU: Vezetői összefoglaló, business fit,
FR/NFR, C4 L1/L2/L3, author→build→publish sequence, search sequence, deployment, security, threat model,
operations, extensibility, DX, writer UX, localization, SEO, search, GitHub integration, Mermaid, AI
integration suitability, automated generation suitability, API surface, community, licensing, cost drivers,
top-8 risks+mitigations, migration plan, 6–10 recommendations, verdict); Mermaid mandatory; plus
ADRs_<product>/, runbook_<product>.md, roadmap_<product>.csv. Equal depth across all six.

**§17 Target-system-specific evaluation:** suitability as presentation/publishing foundation — GitHub-native
operation, Markdown fidelity, Mermaid, programmatic generation, generated-file handling,
metadata/frontmatter, build automation, incremental regeneration, custom components, AI integration, search,
bilingual, recruiter views, interview components, custom generated pages, self-hosting, hybrid, provider
independence.

**§18 Weighted decision model (mandatory):** score 1–5 × weights: GitHub/docs-as-code fit 15%, AI
integration & extensibility 15%, architecture simplicity 12%, structured content/IA 10%, security &
governance 10%, Mermaid 8%, localization/bilingual 8%, deployment/self-hosting 7%, dev+author UX 7%,
search+SEO 5%, cost 3%. Per score: rationale, evidence, confidence. weighted = Σ(score/5×weight). Math
guides but critical constraints may override with explicit justification.

**§19 Comparison:** comparison.md, scorecard.csv, decision_matrix.md; mandated table columns; include
ÖSSZEHASONLÍTÁS and concise HU: ÖSSZEHASONLÍTÁS.

**§20 Repository health:** stars, releases, commits, contributors, issues, maintenance assessment,
collection date; stars ≠ architecture quality; GitBook backend: N/A — proprietary SaaS.

**§21 Final architecture:** MEGOLDÁS — GitHub-Native AI Documentation System; best foundation + minimum
additional components; conceptual pipeline diagram (repo → knowledge/content pipeline → context/retrieval →
AI generation/model router → generated artifacts → validation+review → PR/merge → build → published hub);
improve rather than copy.

**§22 Anti-overengineering rules (mandatory):** GitHub system of record; static/build-time preferred; AI
not in read path; files over databases; manifests over graph DBs; built-in search first; built-in/plugin
over custom services; no Kubernetes without justification; no microservices without independent
lifecycle reason; no vector DB until justified; no multi-agent swarm; every component names the simpler
alternative it beat; MVP operable by one engineer.

**§23 Content architecture deliverable:** complete taxonomy (numbered dirs 00–15 + generated/); critique
and improve; define per-directory purpose, canonical vs generated, naming, metadata schema, link
conventions, diagram conventions, translation strategy, generated-content policy.

**§24 Recruiter view design:** answers what problem/design/competencies/decisions/technologies/practices/
talking points; depths: 30-second, 2-minute, deep dive, evidence links; never infer unsupported skills.

**§25 Interview prep component:** InterviewPrep schema (ElevatorPitch, TechnicalExplanation,
ConceptsToKnow, DesignDecisions, Tradeoffs, LikelyQuestions, ExampleAnswers, EvidenceLinks); choose
build-time vs stored vs dynamic vs hybrid — simplest robust option.

**§26 AI generation contracts:** GenerateArchitectureManual, GenerateDeveloperGuide, GenerateRecruiterPage,
GenerateInterviewPrep, GenerateTroubleshootingGuide, GenerateQuestionPage, UpdateMermaidDiagram,
DetectDocumentationDrift, SummarizeRepositoryChange — each defining inputs, allowed evidence, output
schema, quality gates, prohibited assumptions, model requirements, persistence policy.

**§27 Drift detection:** code-changed-docs-didn't + canonical-changed-generated-stale; git diff,
frontmatter dependencies, path mappings, content hashes, generated metadata, CI checks, AI-assisted
classification; deterministic before AI.

**§28 CI/CD:** PR → markdown lint → frontmatter validation → link validation → Mermaid validation →
dependency analysis → drift check → security checks → build → preview → human review → merge → production
build → publish → smoke tests; AI regeneration only where needed.

**§29 Security:** threat-model malicious repo content, prompt injection in docs, malicious generated
Markdown, AI external links, Mermaid injection, secret leakage to model APIs, compromised credentials,
malicious PRs, supply chain, untrusted plugins, generated misinformation, cross-provider exposure; trust
boundaries between repository/CI/AI context/cloud model/local model/generated files/build/published
site/user input; provider data handling without invented guarantees.

**§30 Modes:** A minimal self-hosted (GitHub + static + local model), B hybrid (GitHub + static + cloud AI),
C privacy-oriented (local model + self-hosted retrieval/generation); shared architecture, not three
platforms.

**§31 Architecture views (Mermaid, stored as .mmd):** C4 L1/L2/L3, deployment, git-change→doc-update,
special-question→page, recruiter generation, model routing, publishing, trust boundaries.

**§32 ADRs for final system:** GitHub as source of truth, chosen framework, canonical/generated separation,
provider abstraction, generated content via PR, retrieval strategy, Mermaid-as-code, build-time vs runtime
AI, deployment strategy — only where real decisions exist.

**§33 Roadmap:** Phase 1 MVP (repo, framework, taxonomy, Mermaid, metadata, CI validation, one adapter,
GenerateRecruiterPage, GenerateInterviewPrep, generated folder, PR approval, static publication); Phase 2
SCALE (multi-provider, richer retrieval, stale detection, special questions, role content, search,
analytics); Phase 3 HARDEN (identity, policy, hardening, audit, observability, failover, privacy, advanced
retrieval); milestones with objective/deliverables/dependencies/complexity/exit criterion.

**§34–36 PoC (mandatory):** runnable starter under outputs/05_poc/ with docs source/generated/diagrams,
prompts/, schemas/document.schema.json, scripts (detect_changes, generate_page, validate_docs), ai/
(provider + anthropic + gemini + openai + local), .github/workflows (docs-validate, docs-generate),
platform config; no meaningless placeholders; no real API keys (.env.example); provider-independent config
example given (improve schema; no unverifiable hard-coded model names).

**§35 PoC scenarios:** 1 canonical Markdown renders with Mermaid; 2 AI transforms architecture doc into
recruiter page; 3 AI creates interview-prep from canonical evidence; 4 user question as structured
generation request; 5 git change detection identifies stale generated content.

**§37 PoC validation:** actually test dependency install, build, Mermaid, schema, links, dry-run, CI syntax
where feasible; report actual results; distinguish VERIFIED BY EXECUTION from NOT EXECUTED; never claim
untested success.

**§38 Deliverable structure:** outputs/{progress.json, manifest.json, 00_research, 01_products/<six>,
02_comparison/{comparison.md, decision_matrix.md, scorecard.csv}, 03_solution/{solution_architecture.md,
content_architecture.md, ai_architecture.md, security_architecture.md, automation_architecture.md, ADRs/,
diagrams/, implementation_roadmap.csv}, 04_validation/validation_report.md, 05_poc/}.

**§39 solution_architecture.md contents:** Exec Summary; HU: Vezetői összefoglaló; Problem; Goals;
Non-goals; Principles; Chosen Foundation; Why It Won; Runner-up; Decision Boundary; Information
Architecture; Repo Architecture; Canonical Model; Generated Model; AI Generation Architecture; Model
Routing; Retrieval; Recruiter View; Interview Prep; Special Question Workflow; Mermaid Architecture; GitHub
Automation; Drift Detection; Security; Deployment; Observability; CI/CD; Cost; Risks; ADR Summary;
MVP/Scale/Harden; PoC Description; Migration Checklist; MEGOLDÁS; HU: MEGOLDÁS.

**§40 Validation gates:** A evidence; B product parity (product 6 as deep as product 1); C decision
traceability; D AI architecture (separation, independence, grounding, provenance, injection protection, no
AI for static reads, regeneration lifecycle); E simplicity (can this be removed / can the framework do it /
can Actions do it / can a file do it); F PoC demonstrates key architecture.

**§41 Manifest:** manifest.json — path, purpose, status, validation, language, canonical/generated class.

**§42 Final response format:** STATUS / PLATFORM WINNER / RUNNER-UP / WEIGHTED SCORE / CORE ARCHITECTURE /
AI MODEL STRATEGY / GITHUB AUTOMATION / RECRUITER VIEW / INTERVIEW PREP / SPECIAL QUESTION WORKFLOW / POC
STATUS / VALIDATION / OPEN EVIDENCE GAPS / OUTPUT ROOT — concise; no mass-pasting.

**§43 Definition of done:** 30-item checklist (all six researched; repo-grounded OSS; labeled proprietary
assumptions; GitBook historical handling; full SADs; C4 L1–L3; security; runbooks; ADRs; roadmaps; weighted
scorecard; AI suitability; GitHub-native architecture; canonical/generated separation; Mermaid architecture;
provider abstraction; cloud+local; ingestion; incremental regeneration; recruiter; interview; special
questions; drift; AI-doc security threats; no overengineering; runnable PoC; truthful validation; EN/HU;
validation report; manifest; complete checkpoint). Record uncertainty; continue past failures; don't stop
for permission. "Research → understand → compare → architect → simplify → prototype → validate. Produce a
system a real developer could maintain and evolve."
