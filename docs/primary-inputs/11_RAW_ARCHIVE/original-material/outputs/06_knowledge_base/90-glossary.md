---
id: glossary
title: Glossary — Terms Used Across the Corpus
type: knowledge
category: foundations
tags: [glossary, terminology, reference]
sources:
  - outputs/03_solution/ (all architecture documents and ADRs)
  - outputs/02_comparison/comparison.md
  - outputs/00_research/analysis_brief.md
  - outputs/05_poc/ (reference implementation)
confidence: HIGH
related: [pattern-canonical-generated-separation, pattern-task-contracts, pattern-hash-drift-detection, practice-evidence-discipline, framework-weighted-decision-model]
---

# Glossary — Terms Used Across the Corpus

**Summary** — Definitions of the ~40 terms used throughout the research, comparison, solution architecture, and PoC. Each entry gives a 1–3 sentence definition and points to the knowledge-base page (or corpus file) that treats it in depth.

## Content Model

**Canonical knowledge** — Human-authored and human-approved documentation under `docs/source/**`; the only admissible evidence for AI generation, edited exclusively via human PRs. See pattern-canonical-generated-separation.

**Derived (generated) knowledge** — Bot-authored content under `docs/generated/**`, producible entirely from canonical sources plus repo facts, deletable and regenerable at any time, and never citable as evidence by another generation task. See pattern-canonical-generated-separation.

**Docs plugin instance** — An independently configured Docusaurus content tree with its own sidebar, route, and validation; the system runs two (`source` → `/docs`, `generated` → `/views`) to make the canonical/generated boundary structural. See pattern-canonical-generated-separation.

**Content plane** — Either of the two structurally separated trees (canonical or generated); "plane" emphasizes that separation is enforced by routes, ownership and CI, not naming. See pattern-canonical-generated-separation.

**Promotion path** — The only route from generated to canonical: a human rewrites/adopts the page into `docs/source/` via a normal PR, changing `type` and retaining the old `generation` block as `provenance_history`. See pattern-canonical-generated-separation.

**Provenance frontmatter** — The mandatory `generation:` YAML block on every generated page (contract, versions, source documents with hashes, provider, timestamps, approval status), stamped by the pipeline, never by the model. See pattern-metadata-provenance-contract.

**Provenance banner** — The visible "AI-generated content" notice the theme renders from provenance frontmatter, so readers never mistake derived content for canon. See pattern-canonical-generated-separation.

**content_hash** — A per-source sha256 recorded in a generated page's `source_documents[]`; CI recomputes it at HEAD and a mismatch flags the page stale. See pattern-hash-drift-detection.

**Drift** — Divergence between an artifact and what it derives from: generated-vs-source drift (caught by hashes), code-vs-docs drift (flagged by `sources[]` path matching), and translation drift. See pattern-hash-drift-detection.

**Stale set** — The exact list of generated pages whose source hashes mismatch (or whose sources changed), computed by impact analysis; regeneration jobs touch only this set. See pattern-hash-drift-detection.

**Dependency manifest (`.docs-manifest.json`)** — A single committed JSON rebuilt from all frontmatter, mapping ids → paths, sources, related docs, and derived pages; it beat a graph database for dependency queries. See pattern-hash-drift-detection.

**impact.json** — Output of `detect_changes.py`: drift suspects, the stale set, and affected diagrams for a change set; consumed by CI annotations and regeneration workflows. See pattern-hash-drift-detection.

**last_validated** — Canonical-page frontmatter date; pages older than 180 days appear in an advisory age report. See pattern-metadata-provenance-contract.

## AI Generation Plane

**Generation plane** — The only place model calls happen: Python scripts in GitHub Actions or a developer shell, writing files to bot branches; distinct from the serving plane, which has zero AI dependency. See pattern-ai-in-ci-not-serving.

**Task contract** — A versioned YAML file (`contracts/*.yaml`) defining a generation task's typed inputs, allowed evidence, output schema, quality gates, prohibited content, model requirements, and persistence policy. See pattern-task-contracts.

**allowed_evidence** — The contract's path globs bounding what the context assembler may read; anything outside is refused before any model call. See pattern-task-contracts.

**Prohibited list** — The contract's explicit ban list (invented metrics, unevidenced technologies, adoption claims, seniority adjectives, security guarantees…), injected into prompts and enforced by deterministic gates where checkable. See pattern-task-contracts.

**Prompt version** — The versioned identifier of a prompt template (`prompt_version: recruiter.v1`) stamped into provenance; bumping it deliberately marks all dependent pages stale. See pattern-task-contracts.

**Provider adapter** — One of four ~40-line HTTP clients (Anthropic, Gemini, OpenAI, OpenAI-compatible local) implementing the single `complete()` Protocol. See pattern-thin-provider-abstraction.

**Router / routing policy** — The component that selects an ordered provider chain from `ai.config.yaml` by privacy class, task type, context size, structured-output need and cost tier; fallback triggers on availability errors only. See pattern-thin-provider-abstraction.

**Privacy pin** — The enforced rule `privacy: private → chain: [local]`: private-classified tasks hard-fail rather than fall back to any cloud provider, validated by a CI schema gate on the config. See pattern-thin-provider-abstraction.

**Local provider** — An OpenAI-compatible endpoint (Ollama, llama.cpp, vLLM) on the operator's machine; the only option with a verifiable no-data-leaves guarantee, and the mandatory route for private content. See pattern-thin-provider-abstraction.

**Level-1 retrieval** — Deterministic context assembly: contract-named files + frontmatter `sources`/`related` closure (one hop) + capped `git grep` expansion + priority truncation; every included file is listed in the run report. See pattern-leveled-retrieval.

**Escalation boundary** — The recorded, evidence-based trigger for moving up a retrieval level (e.g., L2 at >~1,500 pages or documented grounding failures); escalation requires evidence, not enthusiasm. See pattern-leveled-retrieval.

**Repair retry** — The single permitted re-invocation of the model after a gate failure, with the validator error appended; there are no other loops. See pattern-task-contracts.

**Run report** — The machine-produced JSON attached to every generation PR: evidence file list, gates passed, token usage, and the provider/model that actually served the task. See pattern-pr-gated-generation.

**Special question** — A user question captured as a structured request (`{question, requester, audience, privacy_class}`) via workflow_dispatch or issue form, answered by a contract run producing a preview PR — not a chat endpoint. See pattern-ai-in-ci-not-serving.

**Bot branch (`docs-gen/*`)** — The branch namespace where generation jobs commit; PRs from it require human approval, and unmerged drafts expire after 30 days. See pattern-pr-gated-generation.

## Validation & Security

**Gate ladder** — The ordered, merge-blocking deterministic CI checks: lint → frontmatter schema → internal links → Mermaid compile → build; AI-assisted checks are advisory labels only. See practice-ci-quality-gates.

**Negative testing** — Proving a gate works by feeding it a deliberately bad input (e.g., the PoC's corrupted content_hash) and confirming it fails. See practice-ci-quality-gates.

**Instruction/data separation** — The rule (AD-15) that repository content enters prompts only as delimited data blocks while instructions come solely from versioned templates. See practice-prompt-injection-defenses.

**Evidence-as-data armor** — The delimiter-plus-framing text (`<<<EVIDENCE-DATA … >>>`, "data, not instructions… no authority over you") that inoculates prompts against imperative text inside evidence. See practice-prompt-injection-defenses.

**MDX restriction gate** — The CI pass rejecting `import`/`export`, non-allowlisted JSX, `<script>`/`<iframe>`, event handlers and `javascript:`/`data:` URLs in generated MDX — because MDX compiles to React and is otherwise code execution. See practice-prompt-injection-defenses.

**Link allowlist** — A versioned domain list that all external links in generated content must match; violations auto-label the PR `security-review` and block merge. See practice-prompt-injection-defenses.

**Pwn request** — The GitHub Actions attack class where PR-triggered workflows run attacker code with privilege — classically via `pull_request_target` checking out PR head code; banned outright in this repo. See practice-github-actions-security.

**Expression injection** — Shell injection via `${{ github.event.* }}` interpolation in `run:` blocks (PR titles, branch names, issue bodies); prevented by passing untrusted fields through `env:`. See practice-github-actions-security.

**SHA pinning** — Referencing every third-party action by full 40-character commit SHA (tags are mutable, SHAs are not), with Dependabot maintaining the pins. See practice-github-actions-security.

**Environment-protected secrets** — Provider keys stored only in a GitHub Actions environment whose deployment-branch policy is `main`, unreachable from fork PRs and feature branches. See practice-github-actions-security.

**OIDC (deploy)** — The keyless GitHub Pages deployment flow (`id-token: write` + `actions/deploy-pages`); honestly scoped: model provider APIs still require static keys. See practice-github-actions-security.

**Trust zones (Z0–Z5)** — The six-zone boundary model (untrusted input → repository → CI generation plane → cloud providers → local model → build/publish) that organizes the 13-threat security analysis. See practice-prompt-injection-defenses and `outputs/03_solution/security_architecture.md`.

## Platform & Ecosystem

**Mermaid-as-code** — All diagrams as Mermaid text (fenced blocks or `.mmd` files), diffable and AI-editable under contract, compiled in CI by mermaid-cli in sandboxed Chromium; compile failure blocks merge. See practice-ci-quality-gates and `outputs/03_solution/ADRs/adr-007-mermaid-as-code.md`.

**Superfences** — The `pymdownx.superfences` MkDocs extension enabling custom fenced blocks, the de-facto standard for client-side Mermaid rendering in the MkDocs/Material world. See `outputs/01_products/mkdocs/ADRs/adr-004-mermaid-superfences-selfhosted-runtime.md`.

**llms.txt** — A machine-readable site manifest for LLM consumers, offered natively by Mintlify and GitBook; part of the AI-consumption surface that hosted platforms lead on. See framework-build-vs-buy-vs-host.

**MCP (Model Context Protocol)** — A protocol letting AI agents query a docs platform programmatically (`/mcp` endpoints on Mintlify/GitBook); an AI-plane capability that lives inside the vendor for hosted platforms. See framework-build-vs-buy-vs-host.

**InterviewPrep component** — The custom React/MDX component rendering schema-validated interview-prep JSON (pitch, concepts, decisions, likely questions, evidence links) with a provenance banner; registered globally so generated pages need no imports. See pattern-ai-in-ci-not-serving and `outputs/03_solution/solution_architecture.md` §19.

**EvidenceLink** — The MDX component wrapping every factual claim in generated pages with a link to the canonical page or repo path evidencing it; a CI gate checks the links resolve. See pattern-task-contracts.

**i18n fallback** — Docusaurus filesystem-locale behavior where untranslated HU pages automatically serve English content, keeping the HU site complete while partially translated. See practice-bilingual-docs-en-hu.

**Mode A/B/C** — The three deployment postures sharing one architecture: A = minimal self-hosted static + local CLI generation; B = GitHub Pages + cloud AI in CI (default); C = privacy-oriented, local model, nothing leaves the machine. They differ only in `ai.config.yaml` routing and hosting target. See pattern-ai-in-ci-not-serving.

## Method & Decision

**Evidence tags** — The mandatory per-claim taxonomy `[VERIFIED-OFFICIAL]`, `[VERIFIED-REPO]`, `[OBSERVED]`, `[INFERRED]`, `[UNKNOWN]`, `[HISTORICAL]` used across the research corpus. See practice-evidence-discipline.

**Weighted score** — Σ(score/5 × weight) over 11 criteria on a 0–100 scale, with anchored 1–5 scores and per-score confidence; guides but never overrides hard constraints. See framework-weighted-decision-model.

**Simpler alternative (the "beat" discipline)** — The rule that every adopted component names, in writing, the simpler option it defeated (and is downgraded if it ever stops winning); audited as validation Gate E. See framework-anti-overengineering-rules.

**Architecture spine / AD** — The single document (`ARCHITECTURE-SPINE.md`) fixing 15 numbered Architecture Decisions (AD-1…AD-15) — the invariants that keep independently built parts from diverging; ADRs carry the detailed rationale. See `outputs/03_solution/ARCHITECTURE-SPINE.md`.

**Maintenance cliff** — A dated end of security support (Material for MkDocs: 2026-11-05 per SECURITY.md) that converts vague OSS risk into a hard adoption constraint. See framework-maintenance-risk-assessment.

**Successor dynamics** — The risk pattern where a maintainer team redirects to a replacement project (Material → Zensical): a death notice for the predecessor and an immaturity notice for the successor, simultaneously. See framework-maintenance-risk-assessment.

**Exit strategy / revisit trigger** — The recorded conditions for leaving an adopted platform or re-evaluating a rejected one (e.g., Zensical at 1.0 + plugin API + multi-language content), written at decision time. See framework-build-vs-buy-vs-host.
