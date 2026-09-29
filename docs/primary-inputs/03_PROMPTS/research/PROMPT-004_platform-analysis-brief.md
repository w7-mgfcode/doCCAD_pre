# Shared Analysis Brief — Documentation Platform Deep Dive

You are one of six parallel Principal Solution Architect analysts. Each analyst covers ONE platform.
Today: 2026-08-12. Work directory root: /home/claude/outputs/01_products/<platform>/

## Purpose of the research
The findings feed the design of a **GitHub-native, AI-augmented documentation ecosystem**:
- Git/GitHub is the canonical source of truth (Markdown + Mermaid-as-code + frontmatter metadata).
- An AI layer (Claude / Gemini / OpenAI / local models behind a provider abstraction) transforms canonical
  docs into derived views: recruiter pages, interview-prep sections, special-question pages, role-specific docs.
- Derived AI content is separated from canonical content, goes through validation + PR review, and is
  regenerated incrementally when sources change.
- AI must NOT be required to serve/read the published documentation (static-first).
- The system must be operable by ONE capable engineer. Anti-overengineering is a hard rule.

So beyond generic platform quality, always evaluate: **"How well would this platform serve as the
presentation/publishing foundation for that ecosystem?"** — GitHub-native operation, Markdown fidelity,
Mermaid, programmatic content generation, generated-file handling, frontmatter/metadata, build automation,
incremental regeneration, custom components (e.g., a reusable InterviewPrep component), AI integration,
search, bilingual EN/HU support, self-hosting, provider independence.

## Evidence rules (MANDATORY)
Tag every factual capability claim with one of:
`[VERIFIED-OFFICIAL]` (current official docs/site), `[VERIFIED-REPO]` (inspected real repository files),
`[OBSERVED]` (observed behavior of public interfaces), `[INFERRED]` (reasoned, labeled as such),
`[UNKNOWN]`, `[HISTORICAL]` (archived/outdated material — never present as current architecture).

Never invent: backend technologies, internal services, security controls, compliance, SLAs, pricing numbers
you did not verify, benchmarks, adoption/customer counts. Proprietary SaaS internals (GitBook current
platform, Mintlify backend) must be treated as black boxes analyzed through public interfaces and docs;
archived GitBook OSS repos are [HISTORICAL] only.

## Required repository deep dive (OSS platforms)
Clone the real repo (shallow) into /tmp and inspect: README, LICENSE, SECURITY, package manifests, lockfiles,
module/package layout, source directories, build system, configuration model, plugin system, themes,
localization (i18n), search, CLI, tests, CI workflows, dependency automation, releases, contributor docs.
Derive the layer map from actual code: authoring / configuration / parsing / build / rendering / plugin /
theme / search / localization / delivery layers. Ground C4 L2/L3 in repo evidence and cite file paths.
Collect current repo health: stars, latest release + date, recent commit activity, contributor signal,
issue activity, maintenance assessment, collection date. (GitBook current backend: "N/A — proprietary SaaS".)

## Deliverables (write ALL of these into /home/claude/outputs/01_products/<platform>/)

1. `SAD_<platform>.md` — self-contained Solution Architecture Document with EXACTLY these sections:
   Executive Summary; HU: Vezetői összefoglaló (a faithful Hungarian executive summary, ~150-250 words);
   Business & Functional Fit; Functional Requirements; Non-functional Requirements;
   C4 L1 — System Context (Mermaid); C4 L2 — Containers (Mermaid); C4 L3 — Components (Mermaid);
   Author → Build → Publish sequence (Mermaid sequenceDiagram); Search/indexing sequence (Mermaid);
   Deployment & Infrastructure; Security Architecture; Threat Model; Operational Model;
   Extensibility / Plugin Architecture; Developer Experience; Writer / Content UX; Localization; SEO;
   Search; GitHub Integration; Mermaid Support; AI Integration Suitability;
   Automated Content Generation Suitability; API / Automation Surface; Community / Maintenance;
   Licensing; Cost Drivers; Top 8 Risks + Mitigations (table); Migration Plan;
   Prioritized Recommendations (6–10); Architectural Verdict;
   Target-System Fit Assessment (explicit paragraph-by-paragraph vs the ecosystem above).
   Mermaid diagrams are mandatory and must be syntactically valid (use `graph TB`/`flowchart`,
   `sequenceDiagram`; avoid experimental syntax; no C4 plugin syntax — model C4 levels with flowchart
   subgraphs; NEVER use round parentheses `(` `)` or `[` `]` inside node label text — they break parsing;
   keep labels short).

2. `ADRs/` — 3 to 5 ADRs a team ADOPTING this platform for the target ecosystem would need
   (format: Status/Context/Decision/Consequences/Alternatives). Name: `adr-001-<slug>.md` etc.

3. `runbook_<platform>.md` — operational runbook: install/setup, routine ops, upgrade, backup/restore
   (what Git covers vs not), common failures + recovery, monitoring signals, security ops.

4. `roadmap_<platform>.csv` — header:
   `phase,milestone,objective,deliverables,dependencies,complexity,exit_criterion`
   with rows for adopting the platform in the target ecosystem (MVP/Scale/Harden phasing).

5. `scores.json` — EXACTLY this shape (all 11 criteria):
```json
{
  "platform": "<name>",
  "criteria": {
    "github_docs_as_code_fit":        {"weight": 15, "score": 1-5, "rationale": "...", "evidence": "...", "confidence": "HIGH|MEDIUM|LOW"},
    "ai_integration_extensibility":   {"weight": 15, "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "architecture_simplicity":        {"weight": 12, "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "structured_content_ia":          {"weight": 10, "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "security_governance":            {"weight": 10, "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "mermaid_diagrams_as_code":       {"weight": 8,  "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "localization_bilingual":         {"weight": 8,  "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "deployment_self_hosting":        {"weight": 7,  "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "dev_author_ux":                  {"weight": 7,  "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "search_seo":                     {"weight": 5,  "score": 0, "rationale": "", "evidence": "", "confidence": ""},
    "cost_efficiency":                {"weight": 3,  "score": 0, "rationale": "", "evidence": "", "confidence": ""}
  },
  "weighted_score": 0.0,
  "critical_constraints": ["..."],
  "verdict_one_liner": "..."
}
```
Scoring anchors (apply consistently): 5 = best-in-class, native, no workarounds; 4 = strong, minor gaps;
3 = workable with documented workarounds/plugins; 2 = significant friction or partial lock-in;
1 = unsuitable/blocked. weighted_score = Σ(score/5 × weight), 0–100.
For SaaS platforms, score `github_docs_as_code_fit` against true Git-as-single-source operation and
`deployment_self_hosting` against actual self-host options — do not give credit for marketing claims.

6. `repo_health.json` — {stars, latest_release, release_date, recent_commit_activity, contributors_signal,
   issue_activity, maintenance_assessment, collected_at, notes} (nulls + note for proprietary SaaS).

7. `sources.md` — every URL/repo path consulted, with access date and what it evidenced.

## Style
English prose (plus the one Hungarian executive summary). Write in prose, use tables sparingly and only
where they add clarity (risks, scores). Equal analytical depth is required — this platform must be analyzed
as deeply as every other. Be honest about weaknesses; the comparison depends on calibrated honesty.
Your final chat reply should be SHORT (files are the deliverable): status, weighted score, top 3 findings,
evidence gaps.
