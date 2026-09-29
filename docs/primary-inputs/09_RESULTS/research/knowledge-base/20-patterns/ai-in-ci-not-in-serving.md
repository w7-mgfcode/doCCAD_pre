---
id: pattern-ai-in-ci-not-serving
title: AI in CI, Never in Serving
type: knowledge
category: patterns
tags: [build-time-ai, static-first, availability, degradation, runtime-ai]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-4, AD-11, AD-14)
  - outputs/03_solution/ADRs/adr-008-build-time-ai.md
  - outputs/03_solution/ai_architecture.md (§1, §9)
  - outputs/03_solution/security_architecture.md (intro — attack classes absent by construction)
  - outputs/04_validation/validation_report.md (Gate D, Gate F)
confidence: HIGH
related: [pattern-pr-gated-generation, pattern-canonical-generated-separation, pattern-thin-provider-abstraction, practice-github-actions-security]
---

# AI in CI, Never in Serving

**Summary** — All AI output is produced at build/CI time (or via a local CLI), committed through pull requests, and only then served as static files. The published site has zero AI dependency: readers never wait on a model, and the docs remain fully available when every provider is down. This is the availability-and-trust backbone of the architecture; the alternative (runtime AI) was rejected as a matter of principle, not cost.

## Core Logic

**Problem.** Derived views (recruiter pages, interview prep, question answers) could be produced at request time by a service calling model APIs, or at CI time as committed artifacts. Runtime generation couples read availability to provider availability, serves unreviewed output, and opens an injection surface at serve time.

**Solution structure.** AI is an *enrichment plane*, not a serving component:

- Python scripts run in GitHub Actions (`docs-generate.yml`, `workflow_dispatch`/schedule-triggered) or a developer shell.
- They read canonical files, call a model once per artifact (plus at most one repair retry), and write derived files to a `docs-gen/*` bot branch as a PR (see pattern-pr-gated-generation).
- The published site is a pure static build artifact (`docusaurus build` → GitHub Pages); no server, no runtime endpoint, no client-side model call exists in the read path.
- Even "special questions" — the most chat-like feature — are CI jobs producing preview PRs, not a chat endpoint. Interview/recruiter views render committed MDX/JSON at build time (AD-11).

**Degradation behavior** (the operational payoff): provider down → fallback chain (except privacy-pinned tasks) → generation job fails *visibly*; reads work, builds work, canonical authoring works — only new generation waits. Key expiry or quota exhaustion stops generation jobs and nothing else. VERIFIED BY EXECUTION in 05_poc: the full site (both locales) built and served with zero API keys present in the environment.

**Why runtime AI was rejected** (ADR-008): (a) availability coupling — the mission requires approved docs to remain readable when every provider is unavailable; (b) unreviewed output — runtime pages bypass the human gate that is the system's only non-deterministic-proof control; (c) injection surface at serve time; (d) cost/scaling — static caching is trivial, per-request inference is not. A hybrid (per-page runtime hydration) was rejected as "two lifecycles, worst of both."

## Best Practices

1. **Treat generation as batch, not interactive** — one model call per artifact plus one repair retry, because loops hide failures and inflate cost; failures should surface to a human.
2. **Prove the no-AI build in CI** — run the production build in a job that has no provider secrets, because the guarantee must be structural (the build job literally cannot call a model), not aspirational.
3. **Route "chat-like" requirements into the same pipeline** (structured request → contract → preview PR), because a second, runtime lifecycle for one content type doubles governance surface.
4. **Fail visibly, degrade silently** — generation failures alert the operator; readers never see them, because the serving plane is decoupled by construction.

## Pitfalls

- The explicit non-goal is real-time personalization and Q&A chat. If chat is ever needed, the spine defers it as an *isolated service* — bolting it onto the docs pipeline would reintroduce the coupling this pattern removes.
- Build-time AI means content freshness is bounded by regeneration cadence; the hash-based drift mechanism (pattern-hash-drift-detection) exists precisely to make regeneration targeted and timely rather than continuous.
- Do not let "advisory" AI CI checks become merge-blocking: AD-10 keeps AI-assisted checks as labels only, because AI judging AI is not a gate.

## Expert Notes

The security dividend is easy to underestimate: with no runtime backend, whole attack classes — server exploitation, session theft, API abuse of a serving endpoint, database injection — are *absent by construction, not by mitigation* (security_architecture.md). The comparison corpus reinforces the split: hosted platforms (Mintlify, GitBook) ship excellent AI *consumption* surfaces but put the build/serve/AI plane inside a vendor; the OSS SSGs ship zero AI features — "which is exactly what the target architecture wants, because AI belongs in the generation plane (CI), not the serving plane." Choosing where AI runs is therefore a platform-selection criterion, not an implementation detail.

## Evidence & Further Reading

- `outputs/03_solution/ADRs/adr-008-build-time-ai.md` — decision and rejected runtime/hybrid options.
- `outputs/03_solution/ai_architecture.md` §1 (position in system), §9 (failure modes and degradation).
- `outputs/03_solution/security_architecture.md` — "no runtime backend" as the central structural fact.
- `outputs/04_validation/validation_report.md` Gate D ("AI not required for static reads … VERIFIED BY EXECUTION") and Gate F; `outputs/05_poc/VALIDATION_NOTES.md` §b, §e.
